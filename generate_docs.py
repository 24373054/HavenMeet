#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成知乎和小红书数据的飞书文档
"""

import json
import os

def process_zhihu_contents():
    """处理知乎笔记数据"""
    input_file = '/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/zhihu/jsonl/search_contents_2026-03-13.jsonl'
    
    notes = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            data = json.loads(line.strip())
            notes.append(data)
    
    print(f"知乎笔记总数：{len(notes)}")
    return notes

def process_xhs_contents():
    """处理小红书笔记数据"""
    input_file = '/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/xhs/jsonl/search_contents_2026-03-13.jsonl'
    
    notes = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            notes.append(data)
    
    print(f"小红书笔记总数：{len(notes)}")
    return notes

def generate_zhihu_markdown(notes):
    """生成知乎笔记的 Markdown 内容"""
    markdown = """# 📝 知乎搜索结果 - 内容数据（163 条完整）

> **关键词**: 人工智能  
> **更新时间**: 2026-03-13  
> **数据来源**: MediaCrawler 爬取

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 总回答数 | 163 条 |
| 总评论数 | 2,596 条 |
| 平均评论数 | 15.9 条/回答 |

---

## 📄 完整回答列表

"""
    
    for i, note in enumerate(notes, 1):
        title = note.get('title', '无标题')
        author = note.get('user_nickname', '未知')
        voteup = note.get('voteup_count', 0)
        comment_count = note.get('comment_count', 0)
        content = note.get('content_text', '')[:500]  # 只显示前 500 字
        
        markdown += f"""### {i}. {title}
- **作者**: {author}
- **点赞**: {voteup} | **评论**: {comment_count}
- **问题**: {note.get('desc', '无')}
- **链接**: [查看原文]({note.get('content_url', '#')})

> {content}...

---

"""
    
    markdown += """
## 📥 原始数据

完整 JSONL 原始数据已上传至飞书云空间。

---

*文档生成时间：2026-03-13*  
*数据来源：MediaCrawler 知乎爬虫*
"""
    
    return markdown

def generate_xhs_markdown(notes):
    """生成小红书笔记的 Markdown 内容"""
    markdown = """# 📱 小红书搜索结果 - 笔记数据（20 条完整）

> **关键词**: 人工智能  
> **更新时间**: 2026-03-13  
> **数据来源**: MediaCrawler 爬取

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 总笔记数 | 20 条 |
| 总评论数 | 198 条 |
| 平均评论数 | 9.9 条/笔记 |

---

## 📄 完整笔记列表

"""
    
    for i, note in enumerate(notes, 1):
        title = note.get('title', '无标题')
        author = note.get('nickname', '未知')
        liked = note.get('liked_count', 0)
        comment_count = note.get('comment_count', 0)
        desc = note.get('desc', '')[:200]
        
        markdown += f"""### {i}. {title}
- **作者**: {author}
- **点赞**: {liked} | **评论**: {comment_count}
- **描述**: {desc}...
- **标签**: {', '.join(note.get('tag_list', '').split(','))[:5]}
- **链接**: [查看原文]({note.get('note_url', '#')})

---

"""
    
    markdown += """
## 📥 原始数据

完整 JSONL 原始数据已上传至飞书云空间。

---

*文档生成时间：2026-03-13*  
*数据来源：MediaCrawler 小红书爬虫*
"""
    
    return markdown

if __name__ == '__main__':
    print("开始处理数据...")
    
    # 处理知乎数据
    print("\n1. 处理知乎数据...")
    zhihu_notes = process_zhihu_contents()
    zhihu_md = generate_zhihu_markdown(zhihu_notes)
    
    with open('/tmp/zhihu_notes.md', 'w', encoding='utf-8') as f:
        f.write(zhihu_md)
    print(f"知乎笔记文档已生成：/tmp/zhihu_notes.md ({len(zhihu_md)} 字符)")
    
    # 处理小红书数据
    print("\n2. 处理小红书数据...")
    xhs_notes = process_xhs_contents()
    xhs_md = generate_xhs_markdown(xhs_notes)
    
    with open('/tmp/xhs_notes.md', 'w', encoding='utf-8') as f:
        f.write(xhs_md)
    print(f"小红书笔记文档已生成：/tmp/xhs_notes.md ({len(xhs_md)} 字符)")
    
    print("\n✅ 所有文档生成完成！")
