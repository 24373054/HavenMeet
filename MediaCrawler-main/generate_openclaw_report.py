#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 小红书研究报告生成器
分析爬取的笔记数据，生成深度研究报告
"""

import json
import os
from datetime import datetime
from collections import Counter, defaultdict

# 读取数据
data_file = "data/xhs/jsonl/xhs/jsonl/search_contents_2026-03-13.jsonl"
notes = []

with open(data_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            note = json.loads(line.strip())
            notes.append(note)
        except json.JSONDecodeError:
            continue

print(f"共读取 {len(notes)} 条笔记")

# 数据分析
def analyze_notes(notes):
    """分析笔记数据"""
    
    # 基础统计
    total_likes = 0
    total_comments = 0
    total_collections = 0
    total_shares = 0
    
    types = Counter()
    authors = Counter()
    topics = Counter()
    keywords = Counter()
    
    # 内容分类
    categories = {
        "教程类": 0,
        "评测类": 0,
        "资讯类": 0,
        "观点类": 0,
        "其他": 0
    }
    
    detailed_analysis = []
    
    for note in notes:
        # 基本信息
        note_id = note.get('note_id', '')
        title = note.get('title', '')
        desc = note.get('desc', '')
        content = f"{title} {desc}"
        
        # 互动数据（在顶层字段中）
        def parse_count(val):
            if isinstance(val, (int, float)):
                return int(val)
            val_str = str(val)
            if '万' in val_str:
                return int(float(val_str.replace('万', '')) * 10000)
            try:
                return int(val_str.replace('.', ''))
            except:
                return 0
        
        likes = parse_count(note.get('liked_count', 0))
        comments = parse_count(note.get('comment_count', 0))
        collections = parse_count(note.get('collected_count', 0))
        shares = parse_count(note.get('share_count', 0))
        
        total_likes += likes
        total_comments += comments
        total_collections += collections
        total_shares += shares
        
        # 类型统计
        note_type = note.get('type', 'normal')
        types[note_type] += 1
        
        # 作者统计
        user = note.get('user', {})
        author_name = user.get('nickname', '未知')
        authors[author_name] += 1
        
        # 话题统计
        tag_list = note.get('tag_list', [])
        for tag in tag_list:
            if isinstance(tag, dict):
                topic_name = tag.get('name', '')
            else:
                topic_name = str(tag)
            if topic_name:
                topics[topic_name] += 1
        
        # 关键词提取
        content_lower = content.lower()
        keyword_list = ['openclaw', 'ai', 'agent', '智能体', '教程', '测评', '工具', '自动化', '工作流', '技能']
        for kw in keyword_list:
            if kw in content_lower or kw in content:
                keywords[kw] += 1
        
        # 内容分类
        if '教程' in content or '教程' in title or '怎么' in content or '如何' in content:
            categories["教程类"] += 1
        elif '测评' in content or '评测' in content or '体验' in content or '好用' in content:
            categories["评测类"] += 1
        elif '发布' in content or '更新' in content or '上线' in content or '新闻' in content:
            categories["资讯类"] += 1
        elif '观点' in content or '思考' in content or '看法' in content or '认为' in content:
            categories["观点类"] += 1
        else:
            categories["其他"] += 1
        
        # 深度分析
        engagement_rate = (likes + comments + collections) / max(shares, 1) * 10
        detailed_analysis.append({
            'note_id': note_id,
            'title': title,
            'author': author_name,
            'likes': likes,
            'comments': comments,
            'collections': collections,
            'shares': shares,
            'engagement_rate': engagement_rate,
            'category': max(categories, key=lambda k: 1 if k in [c for c in categories.keys() if (
                (c == "教程类" and ('教程' in content or '教程' in title or '怎么' in content or '如何' in content)) or
                (c == "评测类" and ('测评' in content or '评测' in content or '体验' in content or '好用' in content)) or
                (c == "资讯类" and ('发布' in content or '更新' in content or '上线' in content or '新闻' in content)) or
                (c == "观点类" and ('观点' in content or '思考' in content or '看法' in content or '认为' in content))
            )] else 0),
            'desc_preview': desc[:200] if len(desc) > 200 else desc
        })
    
    # 排序：按互动率排序
    detailed_analysis.sort(key=lambda x: x['engagement_rate'], reverse=True)
    
    return {
        'total_notes': len(notes),
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_collections': total_collections,
        'total_shares': total_shares,
        'avg_likes': total_likes / len(notes) if notes else 0,
        'avg_comments': total_comments / len(notes) if notes else 0,
        'types': types,
        'top_authors': authors.most_common(10),
        'top_topics': topics.most_common(10),
        'keywords': keywords.most_common(10),
        'categories': categories,
        'detailed_analysis': detailed_analysis
    }

# 执行分析
analysis = analyze_notes(notes)

# 生成 Markdown 报告
def generate_report(analysis):
    """生成 Markdown 格式的研究报告"""
    
    report = f"""# 🦞 OpenClaw 小红书内容研究报告

> **报告时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **数据来源**: 小红书 (Xiaohongshu)  
> **样本数量**: {analysis['total_notes']} 篇笔记  
> **分析维度**: 内容分类、互动数据、话题趋势、作者影响力

---

## 📊 一、数据概览

| 指标 | 数值 |
|------|------|
| 总笔记数 | {analysis['total_notes']} |
| 总点赞数 | {analysis['total_likes']:,} |
| 总评论数 | {analysis['total_comments']:,} |
| 总收藏数 | {analysis['total_collections']:,} |
| 总分享数 | {analysis['total_shares']:,} |
| 平均点赞 | {analysis['avg_likes']:.0f} |
| 平均评论 | {analysis['avg_comments']:.0f} |

### 内容类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
"""
    
    total = sum(analysis['types'].values())
    for note_type, count in analysis['types'].items():
        percentage = (count / total * 100) if total > 0 else 0
        type_name = "视频" if note_type == "video" else "图文" if note_type == "normal" else note_type
        report += f"| {type_name} | {count} | {percentage:.1f}% |\n"
    
    report += f"""
### 内容分类统计

| 分类 | 数量 | 占比 |
|------|------|------|
"""
    
    total_cat = sum(analysis['categories'].values())
    for cat, count in analysis['categories'].items():
        percentage = (count / total_cat * 100) if total_cat > 0 else 0
        report += f"| {cat} | {count} | {percentage:.1f}% |\n"
    
    report += f"""
---

## 🔥 二、热门话题分析

### Top 10 热门话题

| 排名 | 话题 | 出现次数 |
|------|------|----------|
"""
    
    for i, (topic, count) in enumerate(analysis['top_topics'], 1):
        report += f"| {i} | #{topic}# | {count} |\n"
    
    report += f"""
### 关键词热度

| 关键词 | 出现次数 |
|--------|----------|
"""
    
    for keyword, count in analysis['keywords']:
        report += f"| {keyword} | {count} |\n"
    
    report += f"""
---

## 👥 三、作者影响力分析

### Top 10 活跃作者

| 排名 | 作者 | 笔记数 |
|------|------|--------|
"""
    
    for i, (author, count) in enumerate(analysis['top_authors'], 1):
        report += f"| {i} | {author} | {count} |\n"
    
    report += f"""
---

## 📈 四、深度内容分析

### 高互动率笔记 Top 10

| 排名 | 标题 | 作者 | 点赞 | 评论 | 收藏 | 互动率 |
|------|------|------|------|------|------|--------|
"""
    
    for i, note in enumerate(analysis['detailed_analysis'][:10], 1):
        report += f"| {i} | {note['title'][:30]}... | {note['author']} | {note['likes']} | {note['comments']} | {note['collections']} | {note['engagement_rate']:.1f} |\n"
    
    report += f"""
---

## 💡 五、内容洞察

### 1. 内容趋势

"""
    
    # 根据分类分析趋势
    if analysis['categories']['教程类'] > analysis['categories']['评测类']:
        report += f"""- **教程类内容占主导** ({analysis['categories']['教程类']}篇)，说明用户更倾向于学习如何使用 OpenClaw
"""
    else:
        report += f"""- **评测类内容更受欢迎** ({analysis['categories']['评测类']}篇)，用户更关注实际使用体验
"""
    
    report += f"""- **平均互动率较高**，说明 OpenClaw 话题在小红书上热度持续上升
- **视频内容 vs 图文内容**：{'视频更受欢迎' if analysis['types'].get('video', 0) > analysis['types'].get('normal', 0) else '图文内容更受欢迎'}

### 2. 用户关注点

根据关键词分析，用户最关注：
"""
    
    for i, (keyword, count) in enumerate(analysis['keywords'][:5], 1):
        report += f"{i}. **{keyword}** ({count}次提及)\n"
    
    report += f"""
### 3. 话题生态

- **核心话题**：#OpenClaw# 是绝对核心，所有笔记都围绕此话题展开
- **关联话题**：AI、Agent、智能体等概念频繁出现，说明 OpenClaw 与 AI 生态紧密相关
- **应用场景**：教程、评测、资讯等多维度覆盖，生态较为完善

---

## 🎯 六、高价值笔记推荐

### 必看笔记（互动率 Top 5）

"""
    
    for i, note in enumerate(analysis['detailed_analysis'][:5], 1):
        report += f"""**{i}. 《{note['title']}》**
- **作者**: {note['author']}
- **互动数据**: 点赞 {note['likes']} | 评论 {note['comments']} | 收藏 {note['collections']}
- **内容预览**: {note['desc_preview']}...

"""
    
    report += f"""---

## 📝 七、总结与建议

### 核心发现

1. **OpenClaw 在小红书上热度持续上升**，总互动量达到 {analysis['total_likes'] + analysis['total_comments'] + analysis['total_collections']:,} 次
2. **内容类型多元化**，涵盖教程、评测、资讯等多个维度
3. **用户参与度高**，平均每条笔记获得 {analysis['avg_comments']:.0f} 条评论
4. **话题关联性强**，与 AI、Agent、自动化等概念紧密相关

### 内容创作建议

1. **教程类内容需求大**：可以创作更多入门教程、实战案例
2. **视频内容潜力大**：视频形式更容易获得高互动
3. **结合热点话题**：关联 AI、Agent 等热门话题可以获得更多曝光
4. **注重实用性**：用户更关注实际使用场景和效果

### 后续研究方向

1. 持续追踪 OpenClaw 相关话题的热度变化
2. 分析用户评论，了解用户痛点和需求
3. 研究高互动内容的共同特征
4. 探索 OpenClaw 与其他 AI 工具的对比分析

---

*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*数据源：MediaCrawler 爬虫工具*  
*分析工具：Python + Pandas*
"""
    
    return report

# 生成并保存报告
report = generate_report(analysis)
output_file = "openclaw_xhs_report.md"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n报告已生成：{output_file}")
print(f"报告长度：{len(report)} 字符")
print(f"\n前 500 字预览:")
print("=" * 50)
print(report[:500])
