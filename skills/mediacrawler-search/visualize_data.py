#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据可视化脚本 - 生成图表
"""

import json
import os
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from wordcloud import WordCloud
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class DataVisualizer:
    def __init__(self, data_dir="/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/zhihu/jsonl"):
        self.data_dir = data_dir
        self.output_dir = "/home/Matrix/.openclaw/workspace/skills/mediacrawler-search/charts"
        os.makedirs(self.output_dir, exist_ok=True)
    
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
    
    def create_category_pie(self, data):
        """创建分类饼图"""
        categories = defaultdict(int)
        
        for item in data:
            content = item.get('content_text', '') + item.get('title', '')
            if any(kw in content.lower() for kw in ['大模型', '机器学习', '深度学习', '神经网络', '算法']):
                categories['AI 技术'] += 1
            else:
                categories['其他'] += 1
        
        plt.figure(figsize=(10, 8))
        labels = list(categories.keys())
        sizes = list(categories.values())
        colors = ['#3498db', '#e74c3c']
        
        wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                           startangle=90, shadow=True)
        plt.title('Content Category Distribution', fontsize=16, fontweight='bold')
        plt.savefig(os.path.join(self.output_dir, 'category_pie.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ 饼图已保存：{self.output_dir}/category_pie.png")
    
    def create_bar_chart(self, data):
        """创建点赞数分布柱状图"""
        likes = [item.get('voteup_count', 0) for item in data]
        
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(likes)), sorted(likes, reverse=True), color='#3498db')
        plt.xlabel('Content Index', fontsize=12)
        plt.ylabel('Likes', fontsize=12)
        plt.title('Likes Distribution (Top to Bottom)', fontsize=16, fontweight='bold')
        plt.xticks(range(0, len(likes), 5))
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(os.path.join(self.output_dir, 'likes_distribution.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ 柱状图已保存：{self.output_dir}/likes_distribution.png")
    
    def create_scatter_plot(self, data):
        """创建点赞 vs 评论散点图"""
        likes = [item.get('voteup_count', 0) for item in data]
        comments = [item.get('comment_count', 0) for item in data]
        
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(likes, comments, c=range(len(data)), cmap='viridis', s=100, alpha=0.6)
        plt.xlabel('Likes', fontsize=12)
        plt.ylabel('Comments', fontsize=12)
        plt.title('Likes vs Comments Correlation', fontsize=16, fontweight='bold')
        plt.grid(alpha=0.3)
        plt.colorbar(scatter, label='Content Index')
        plt.savefig(os.path.join(self.output_dir, 'likes_comments_scatter.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ 散点图已保存：{self.output_dir}/likes_comments_scatter.png")
    
    def create_wordcloud(self, data):
        """创建词云"""
        # 提取所有文本
        text = ''
        for item in data:
            title = item.get('title', '')
            content = item.get('content_text', '')[:500]  # 只取前 500 字
            text += f" {title} {content}"
        
        # 创建词云（使用英文，因为中文支持有限）
        wordcloud = WordCloud(width=1600, height=900, background_color='white',
                             max_words=200, contour_width=1, contour_color='steelblue').generate(text)
        
        plt.figure(figsize=(16, 9))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud - AI Topics', fontsize=20, fontweight='bold', pad=20)
        plt.savefig(os.path.join(self.output_dir, 'wordcloud.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ 词云已保存：{self.output_dir}/wordcloud.png")
    
    def create_user_activity_chart(self, data):
        """创建用户活跃度图表"""
        users = defaultdict(int)
        for item in data:
            user = item.get('user_nickname', 'Unknown')
            users[user] += 1
        
        # 取前 10 个用户
        top_users = sorted(users.items(), key=lambda x: x[1], reverse=True)[:10]
        user_names = [u[0][:10] for u in top_users]  # 截断长名字
        user_counts = [u[1] for u in top_users]
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(range(len(user_names)), user_counts, color='#9b59b6')
        plt.yticks(range(len(user_names)), user_names)
        plt.xlabel('Number of Contents', fontsize=12)
        plt.title('Top 10 Active Users', fontsize=16, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # 添加数值标签
        for i, (bar, count) in enumerate(zip(bars, user_counts)):
            plt.text(count + 0.1, i, str(count), va='center', fontsize=10)
        
        plt.savefig(os.path.join(self.output_dir, 'user_activity.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ 用户活跃度图已保存：{self.output_dir}/user_activity.png")
    
    def generate_all_charts(self):
        """生成所有图表"""
        print("📥 正在加载数据...")
        contents = self.load_data("search_contents_2026-03-13.jsonl")
        print(f"📄 加载了 {len(contents)} 条数据")
        
        print("\n📊 正在生成图表...")
        self.create_category_pie(contents)
        self.create_bar_chart(contents)
        self.create_scatter_plot(contents)
        self.create_wordcloud(contents)
        self.create_user_activity_chart(contents)
        
        print(f"\n✨ 所有图表已保存到：{self.output_dir}")

if __name__ == "__main__":
    visualizer = DataVisualizer()
    visualizer.generate_all_charts()
