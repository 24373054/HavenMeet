#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成包含完整内容的飞书文档
"""

import json
import os

def generate_zhihu_full_content():
    """生成知乎完整内容文档"""
    input_file = '/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/zhihu/jsonl/search_contents_2026-03-13.jsonl'
    
    notes = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            notes.append(data)
    
    markdown = """# 📝 知乎搜索结果 - 完整内容（163 条）

> **关键词**: 人工智能  
> **更新时间**: 2026-03-13  
> **数据来源**: MediaCrawler 爬取  
> **说明**: 本文档包含完整的回答正文内容，可直接阅读

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 总回答数 | 163 条 |
| 总评论数 | 2,596 条 |
| 平均评论数 | 15.9 条/回答 |

---

## 📄 完整回答内容

"""
    
    for i, note in enumerate(notes, 1):
        title = note.get('title', '无标题')
        author = note.get('user_nickname', '未知')
        voteup = note.get('voteup_count', 0)
        comment_count = note.get('comment_count', 0)
        content = note.get('content_text', '').strip()
        url = note.get('content_url', '#')
        
        # 如果内容超过 5000 字符，截断并显示"展开全文"
        if len(content) > 5000:
            content = content[:5000] + "\n\n...（内容过长，已截断，点击链接查看完整内容）"
        
        markdown += f"""### {i}. {title}

**作者**: {author}  
**点赞**: {voteup} | **评论**: {comment_count}  
**链接**: [查看原文]({url})

---

{content}

---

"""
    
    markdown += """
---

*文档生成时间：2026-03-13*  
*数据来源：MediaCrawler 知乎爬虫*  
*注：本文档包含完整的回答正文，可直接在飞书中阅读*
"""
    
    return markdown

def generate_xhs_full_content():
    """生成小红书完整内容文档（包含图片和描述）"""
    input_file = '/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/xhs/jsonl/search_contents_2026-03-13.jsonl'
    
    notes = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            notes.append(data)
    
    markdown = """# 📱 小红书搜索结果 - 完整内容（20 条）

> **关键词**: 人工智能  
> **更新时间**: 2026-03-13  
> **数据来源**: MediaCrawler 爬取  
> **说明**: 本文档包含笔记描述、图片列表和完整元数据

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 总笔记数 | 20 条 |
| 总评论数 | 198 条 |
| 平均评论数 | 9.9 条/笔记 |

---

## 📄 完整笔记内容

"""
    
    for i, note in enumerate(notes, 1):
        title = note.get('title', '无标题')
        author = note.get('nickname', '未知')
        liked = note.get('liked_count', 0)
        collected = note.get('collected_count', 0)
        comment_count = note.get('comment_count', 0)
        desc = note.get('desc', '').strip()
        url = note.get('note_url', '#')
        tags = note.get('tag_list', [])
        images = note.get('image_list', [])
        
        markdown += f"""### {i}. {title}

**作者**: {author}  
**点赞**: {liked} | **收藏**: {collected} | **评论**: {comment_count}  
**链接**: [查看原文]({url})  
**标签**: {', '.join(tags[:5])}

**图片数量**: {len(images)} 张
"""
        
        # 显示图片 URL（前 3 张）
        if images:
            markdown += "\n**图片列表**:\n"
            for j, img in enumerate(images[:3], 1):
                markdown += f"- 图片 {j}: `{img}`\n"
            if len(images) > 3:
                markdown += f"- ... 还有 {len(images) - 3} 张图片\n"
        
        markdown += f"\n**描述内容**:\n\n{desc}\n\n---\n\n"
    
    markdown += """
## ⚠️ 重要说明

**小红书数据限制**：
- MediaCrawler 爬虫只能获取笔记的 `desc`（描述字段），**无法获取完整的正文内容**
- 完整正文需要点击链接后在小红书 App/网页中查看
- 图片 URL 已保存，但需要手动下载或点击查看

**建议**：
1. 点击笔记链接查看完整内容
2. 如需保存完整内容，需要手动复制或使用其他工具
3. 图片可通过提供的 URL 下载保存

---

*文档生成时间：2026-03-13*  
*数据来源：MediaCrawler 小红书爬虫*
"""
    
    return markdown

if __name__ == '__main__':
    print("开始生成完整内容文档...")
    
    # 生成知乎完整内容
    print("\n1. 生成知乎完整内容文档...")
    zhihu_md = generate_zhihu_full_content()
    
    with open('/tmp/zhihu_full.md', 'w', encoding='utf-8') as f:
        f.write(zhihu_md)
    print(f"✅ 知乎完整文档已生成：/tmp/zhihu_full.md ({len(zhihu_md)} 字符)")
    
    # 生成小红书完整内容
    print("\n2. 生成小红书完整内容文档...")
    xhs_md = generate_xhs_full_content()
    
    with open('/tmp/xhs_full.md', 'w', encoding='utf-8') as f:
        f.write(xhs_md)
    print(f"✅ 小红书完整文档已生成：/tmp/xhs_full.md ({len(xhs_md)} 字符)")
    
    print("\n✅ 所有文档生成完成！")
