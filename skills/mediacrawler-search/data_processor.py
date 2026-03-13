#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理器 - 用于清洗、分类和导入知识库
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import re

class DataProcessor:
    def __init__(self, data_dir="/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/zhihu/jsonl"):
        self.data_dir = data_dir
        self.categories = {
            "AI 技术": ["大模型", "机器学习", "深度学习", "神经网络", "算法", "Transformer"],
            "AI 应用": ["AI 应用", "生成式 AI", "AIGC", "AI 工具", "ChatGPT"],
            "AI 产业": ["AI 投资", "AI 公司", "AI 市场", "AI 泡沫", "AI 经济"],
            "AI 伦理": ["AI 安全", "AI 风险", "AI 伦理", "AI 监管", "AI 法律"],
            "学习资源": ["AI 学习", "AI 教程", "AI 课程", "AI 书籍", "AI 入门"],
            "行业分析": ["AI 趋势", "AI 发展", "AI 未来", "AI 预测", "AI 展望"]
        }
        
    def load_data(self, filename):
        """加载 JSONL 文件"""
        filepath = os.path.join(self.data_dir, filename)
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        return data
    
    def classify_content(self, text):
        """根据关键词分类内容"""
        text_lower = text.lower()
        for category, keywords in self.categories.items():
            if any(kw in text_lower for kw in keywords):
                return category
        return "其他"
    
    def extract_insights(self, data):
        """提取关键洞察"""
        insights = {
            "total_count": len(data),
            "categories": defaultdict(int),
            "top_users": defaultdict(int),
            "avg_likes": 0,
            "avg_comments": 0,
            "hot_topics": defaultdict(int)
        }
        
        total_likes = 0
        total_comments = 0
        
        for item in data:
            # 分类统计
            content = item.get('content_text', '') + item.get('title', '')
            category = self.classify_content(content)
            insights["categories"][category] += 1
            
            # 用户统计
            user = item.get('user_nickname', 'Unknown')
            insights["top_users"][user] += 1
            
            # 点赞和评论
            likes = item.get('voteup_count', 0)
            comments = item.get('comment_count', 0)
            total_likes += likes
            total_comments += comments
            
            # 热门话题（从标题提取）
            title = item.get('title', '')
            if title:
                # 提取关键词
                words = re.findall(r'[\u4e00-\u9fa5]{2,6}', title)
                for word in words[:5]:  # 只取前 5 个词
                    insights["hot_topics"][word] += 1
        
        insights["avg_likes"] = total_likes / len(data) if data else 0
        insights["avg_comments"] = total_comments / len(data) if data else 0
        
        # 转换 default dict 为普通 dict
        insights["categories"] = dict(insights["categories"])
        insights["top_users"] = dict(insights["top_users"])
        insights["hot_topics"] = dict(insights["hot_topics"])
        
        return insights
    
    def generate_summary(self, insights):
        """生成总结报告"""
        summary = f"""# 数据分析报告

## 📊 数据概览
- **总记录数**: {insights['total_count']}
- **平均点赞数**: {insights['avg_likes']:.1f}
- **平均评论数**: {insights['avg_comments']:.1f}

## 📁 内容分类
"""
        for category, count in sorted(insights["categories"].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / insights["total_count"]) * 100
            summary += f"- **{category}**: {count} ({percentage:.1f}%)\n"
        
        summary += "\n## 👥 活跃用户 TOP 10\n"
        top_users = sorted(insights["top_users"].items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (user, count) in enumerate(top_users, 1):
            summary += f"{i}. **{user}**: {count} 条内容\n"
        
        summary += "\n## 🔥 热门话题 TOP 15\n"
        hot_topics = sorted(insights["hot_topics"].items(), key=lambda x: x[1], reverse=True)[:15]
        for i, (topic, count) in enumerate(hot_topics, 1):
            summary += f"{i}. **{topic}**: {count} 次出现\n"
        
        summary += f"\n---\n*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return summary
    
    def export_to_markdown(self, data, output_file="analysis_report.md"):
        """导出为 Markdown 报告"""
        insights = self.extract_insights(data)
        summary = self.generate_summary(insights)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ 报告已保存到：{output_file}")
        return output_file

if __name__ == "__main__":
    processor = DataProcessor()
    
    # 加载所有数据
    print("📥 正在加载数据...")
    contents = processor.load_data("search_contents_2026-03-13.jsonl")
    comments = processor.load_data("search_comments_2026-03-13.jsonl")
    
    print(f"📄 内容数据：{len(contents)} 条")
    print(f"💬 评论数据：{len(comments)} 条")
    
    # 生成报告
    print("\n📊 正在分析数据...")
    processor.export_to_markdown(contents, "/home/Matrix/.openclaw/workspace/skills/mediacrawler-search/知乎数据分析报告.md")
    
    print("\n✨ 分析完成！")
