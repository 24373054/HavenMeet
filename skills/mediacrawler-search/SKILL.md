# MediaCrawler 社交媒体爬虫与分析 Skill

使用 MediaCrawler 项目进行多平台社交媒体数据爬取、分析和报告生成。

## 🎯 核心能力

### 支持平台
- ✅ **小红书 (xhs)** - 图文/视频笔记、评论、用户信息
- ✅ **知乎 (zhihu)** - 问题、回答、文章、评论
- ✅ 抖音 (dy)、快手 (ks)、B 站 (bili)、微博 (wb)、贴吧 (tieba)

### 主要功能
1. **数据爬取** - 关键词搜索、笔记/问题详情、评论数据
2. **数据分析** - 互动量统计、内容分类、趋势分析
3. **报告生成** - 可视化图表、Markdown 报告、飞书文档
4. **内容创作** - 基于数据分析创作社交媒体推文

## 🚦 何时使用此 Skill

**当用户需要以下能力时触发此 Skill：**

### 1. 舆情监控与资讯收集
- "帮我看看网上对 XX 产品的评价"
- "爬取一下小红书/知乎上关于 XX 的讨论"
- "了解 XX 话题的舆论情况"
- "收集竞品在社交媒体上的反馈"

### 2. 市场调研与竞品分析
- "分析竞品在社交媒体上的表现"
- "看看用户最关心什么功能"
- "了解目标用户群体的偏好"
- "收集行业趋势数据"

### 3. 内容创作与优化
- "帮我写一篇小红书推文"
- "基于数据分析创作内容"
- "看看什么类型的内容更受欢迎"
- "生成配图和文案"

### 4. 学术研究
- "爬取学术讨论数据"
- "分析某领域的研究热点"
- "收集论文/技术讨论"

## 📚 快速开始

### 前置条件
```bash
# 进入项目目录
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

# 安装依赖（首次）
pip3 install playwright
playwright install

# 检查浏览器
playwright install chromium
```

### 配置参数
编辑 `config/base_config.py`:
```python
KEYWORDS = "OpenClaw"           # 搜索关键词
PLATFORM = "xhs"                # 平台：xhs/zhihu
CRAWLER_TYPE = "search"         # 类型：search/detail/comment
SEARCH_NOTE_NUM = 30           # 爬取笔记数量
GET_COMMENTS = "yes"            # 是否获取评论：yes/no
COMMENTS_NUMBER = 50            # 每篇笔记获取评论数
```

## 🚀 常用场景

### 场景 1: 爬取小红书笔记和评论（扫码登录）

**方式 A: 使用配置文件**
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
python3 main.py --platform xhs --lt qrcode --type search
```

**方式 B: 命令行参数（推荐）**
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

python3 main.py \
  --platform xhs \
  --type search \
  --keywords "OpenClaw" \
  --start 1 \
  --get_comment yes \
  --save_data_option jsonl \
  --save_data_path data/xhs/jsonl \
  --headless yes
```

**输出文件**:
- `search_contents_YYYY-MM-DD.jsonl` - 笔记数据
- `search_comments_YYYY-MM-DD.jsonl` - 评论数据

### 场景 2: 爬取知乎回答和评论（扫码登录）

```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

python3 main.py \
  --platform zhihu \
  --type search \
  --keywords "OpenClaw" \
  --start 1 \
  --get_comment yes \
  --save_data_option jsonl \
  --save_data_path data/zhihu/jsonl \
  --headless yes
```

### 场景 3: 批量爬取（多次运行）

```bash
# 第一次爬取 30 篇
python3 main.py --platform xhs --type search --keywords "OpenClaw" --note-num 30

# 第二次继续爬取（避免重复）
python3 main.py --platform xhs --type search --keywords "OpenClaw" --start 31 --note-num 30
```

## 📊 数据分析与报告

### 使用分析脚本

项目自带 `generate_openclaw_report.py` 可生成分析报告：

```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

# 生成小红书报告
python3 generate_openclaw_report.py \
  --platform xhs \
  --contents-file data/xhs/jsonl/search_contents_2026-03-13.jsonl \
  --comments-file data/xhs/jsonl/search_comments_2026-03-13.jsonl \
  --output openclaw_xhs_report.md

# 生成知乎报告
python3 generate_openclaw_report.py \
  --platform zhihu \
  --contents-file data/zhihu/jsonl/search_contents_2026-03-13.jsonl \
  --comments-file data/zhihu/jsonl/search_comments_2026-03-13.jsonl \
  --output openclaw_zhihu_report.md
```

**报告包含**:
- 📈 互动量统计（点赞、评论、收藏、分享）
- 🎯 内容分类（教程、体验、测评等）
- 📊 可视化图表（分布图、饼图、散点图）
- 🔥 关键词热度分析
- 💬 评论情感分析

### 上传到飞书文档

```bash
# 使用 OpenClaw 工具上传
feishu_create_doc:
  title: "📱 小红书数据分析报告（2026-03-13）"
  markdown: |
    （读取报告内容）
```

## 🎨 内容创作

### 基于数据创作推文

1. **分析数据** - 了解用户关注点、热门话题
2. **创作文案** - 结合数据洞察撰写内容
3. **生成配图** - 使用 Flux.2 生成高质量图片
4. **发布内容** - 手动或 API 发布到平台

**示例流程**:
```bash
# 1. 爬取数据
python3 main.py --platform xhs --type search --keywords "OpenClaw"

# 2. 生成报告
python3 generate_openclaw_report.py --platform xhs ...

# 3. 生成配图（6 张）
python3 generate_xhs_images.py

# 4. 创建飞书文档预览
feishu_create_doc ...

# 5. 手动发布到小红书
```

## 📁 数据管理

### 文件结构
```
MediaCrawler-main/
├── data/
│   ├── xhs/
│   │   └── jsonl/
│   │       ├── search_contents_YYYY-MM-DD.jsonl
│   │       └── search_comments_YYYY-MM-DD.jsonl
│   └── zhihu/
│       └── jsonl/
│           ├── search_contents_YYYY-MM-DD.jsonl
│           └── search_comments_YYYY-MM-DD.jsonl
├── config/
│   ├── base_config.py
│   └── xhs_config.py
├── reports/
│   └── openclaw_xhs_report.md
└── main.py
```

### 数据格式（JSONL）

**笔记数据字段**:
```json
{
  "note_id": "69821980000000000e03c95f",
  "title": "OpenClaw 教程",
  "desc": "内容描述",
  "liked_count": 1234,
  "comment_count": 56,
  "collect_count": 789,
  "share_count": 45,
  "create_time": "2026-03-13 10:00:00",
  "user_id": "5c5b792f0000000018014882",
  "user_nickname": "用户名"
}
```

**评论数据字段**:
```json
{
  "comment_id": "xxx",
  "note_id": "69821980000000000e03c95f",
  "content": "评论内容",
  "liked_count": 10,
  "create_time": "2026-03-13 11:00:00",
  "user_nickname": "评论者"
}
```

## ⚙️ 高级技巧

### 1. 无头模式运行（服务器环境）
```bash
python3 main.py --platform xhs --headless yes
```

### 2. 指定输出路径
```bash
python3 main.py --save_data_path /custom/path/data
```

### 3. 只爬取不获取评论（加快速度）
```bash
python3 main.py --get_comment no
```

### 4. 爬取指定 URL 的笔记
编辑 `config/xhs_config.py`:
```python
XHS_SPECIFIED_NOTE_URL_LIST = [
    "https://www.xiaohongshu.com/explore/699f0139000000000e00fd1e"
]
```

### 5. 数据去重
```python
# 读取现有数据
existing_ids = set()
with open('existing.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        existing_ids.add(data['note_id'])

# 爬取时跳过已存在的 ID
```

## 📱 知乎/小红书登录方式

### 方式 1: Cookie 登录（推荐，稳定）
```python
# 在浏览器中获取 Cookie，填入 config/xhs_config.py
COOKIES = {
    "web_rid": "...",
    "other_cookies": "..."
}
```

### 方式 2: 二维码扫码登录（灵活，需人工介入）

**小红书扫码流程**:
1. 运行程序，自动生成二维码图片
2. 上传二维码到飞书云盘
3. 发送二维码链接到群聊
4. 用户用手机小红书 App 扫码
5. 扫码成功后自动开始爬取

**知乎扫码流程**:
1. 运行程序，生成二维码
2. 上传到云盘并发送链接
3. 用户用知乎 App 扫码
4. 扫码后自动爬取

**示例代码**:
```bash
# 小红书扫码
python3 main.py --platform xhs --lt qrcode --type search

# 知乎扫码
python3 main.py --platform zhihu --lt qrcode --type search
```

**注意事项**:
- ⏱️ 二维码有效期约 120 秒
- 📱 需要手机 App 扫码（小红书 App / 知乎 App）
- 🔄 扫码失败需重新生成二维码
- ⚡ 扫码后程序会自动开始爬取

## ⚠️ 注意事项

### 法律合规
- ✅ **仅供学习研究**，请勿用于商业用途
- ✅ **遵守平台条款**，尊重 robots.txt
- ✅ **控制爬取频率**，避免对平台造成干扰
- ✅ **保护用户隐私**，不爬取敏感信息

### 技术限制
- ⚠️ **需要扫码登录**，首次运行需手机扫码
- ⚠️ **依赖浏览器**，服务器环境需安装 Chromium
- ⚠️ **数据可能不完整**，部分字段可能被平台限制
- ⚠️ **XHS 图片截断**，图片 URL 可能被截断为 `htt`
- ⚠️ **小红书只能获取 desc 字段**，完整正文需点击链接查看

### 常见问题

**Q: 扫码后仍然提示未登录**
A: 等待 5-10 秒，或重新扫码

**Q: 爬取速度慢**
A: 减少 `COMMENTS_NUMBER` 或使用 `--get_comment no`

**Q: 数据路径错误**
A: 检查 `save_data_path` 配置，确保目录存在

**Q: 脚本报错 AttributeError**
A: 更新 `generate_openclaw_report.py`，处理 `tag_list` 类型

**Q: 图片无法保存**
A: 小红书图片 URL 被截断，只能保存描述文本

## 📊 实际应用案例

### 案例 1: OpenClaw 热度分析
- **目标**: 了解 OpenClaw 在社交媒体的热度
- **平台**: 小红书 + 知乎
- **数据量**: 40 篇笔记 + 163 个回答，2794 条评论
- **发现**: 总互动 152 万次，视频教程最受欢迎
- **产出**: 数据分析报告 + 小红书推文

### 案例 2: 竞品分析
- **目标**: 分析竞品在社交媒体的表现
- **方法**: 爬取竞品关键词，对比互动数据
- **产出**: 竞品分析报告，指导产品优化

### 案例 3: 舆情监控
- **目标**: 监控品牌相关讨论
- **方法**: 定期爬取品牌关键词，分析情感倾向
- **产出**: 舆情周报，及时发现负面信息

### 案例 4: 知识库构建
- **目标**: 建立内部知识库，存储多源数据
- **方法**: 
  1. 爬取知乎/小红书数据
  2. 数据清洗和分类
  3. 导入飞书知识空间
  4. 生成可视化报告
- **产出**: 结构化知识库，包含原始数据、分析报告、可视化图表

## 🔧 维护与更新

### 更新依赖
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
pip3 install -U -r requirements.txt
```

### 更新浏览器
```bash
playwright install chromium
```

### 备份数据
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz data/
```

## 📞 技术支持

- **GitHub**: https://github.com/AnyaLife/MediaCrawler
- **本地路径**: `/home/Matrix/.openclaw/workspace/MediaCrawler-main`
- **相关脚本**: 
  - `generate_openclaw_report.py` - 报告生成
  - `generate_xhs_images.py` - 配图生成
  - `generate_full_docs.py` - 完整文档生成

---

**最后更新**: 2026-03-14  
**版本**: v2.1  
**维护者**: OpenClaw Assistant
