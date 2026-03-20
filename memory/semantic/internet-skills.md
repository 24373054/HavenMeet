# 上网技能知识 (Internet Skills)

**更新时间**: 2026-03-14  
**状态**: ✅ 全部测试通过

---

## 📊 技能概览

| 技能名称 | 类型 | API Key | 状态 | 用途 |
|---------|------|---------|------|------|
| web_fetch | 轻量级提取 | ❌ | ✅ | 快速获取网页内容 |
| browser-automation-ultra | 浏览器自动化 | ❌ | ✅ | 复杂交互、登录 |
| mediacrawler-search | 社交媒体爬虫 | ❌ | ✅ | 知乎/小红书数据 |
| web_search (Brave) | API 搜索 | ✅ | ❌ | 通用搜索（需配置） |

---

## 1️⃣ web_fetch - 轻量级网页提取

**核心知识**:
- **用途**: 快速获取静态网页文本内容
- **优势**: 速度快（~372ms）、无需浏览器、Token 消耗低
- **限制**: 无法处理 JavaScript 渲染、需要登录的网站

**使用方式**:
```javascript
web_fetch:
  url: "https://example.com"
  extractMode: "markdown"  # 或 "text"
  maxChars: 5000  # 最大字符数
```

**适用场景**:
- ✅ 提取文章、文档、新闻
- ✅ 快速获取网页文本
- ❌ 需要 JavaScript 渲染的页面
- ❌ 需要登录的网站

---

## 2️⃣ browser-automation-ultra - 浏览器自动化

**核心知识**:
- **用途**: 需要 JavaScript 渲染、登录、表单填写、点击操作
- **技术栈**: Playwright + Chrome (Chromium)
- **优势**: 支持完整浏览器功能、可模拟人类行为、零 Token 消耗

**环境配置**:
```
Chrome 路径：/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome
Chrome 大小：385MB
Playwright 版本：1.45.0
运行模式：Headless (无头模式)
```

**使用方式**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page()
    page.goto('https://www.zhihu.com')
    # 执行操作...
    browser.close()
```

**适用场景**:
- ✅ 动态网页（需要 JavaScript）
- ✅ 需要登录的网站
- ✅ 复杂交互（点击、输入、滚动）
- ✅ 反爬虫网站（模拟人类行为）

---

## 3️⃣ mediacrawler-search - 社交媒体爬虫

**核心知识**:
- **用途**: 爬取知乎、小红书、抖音、B 站内容
- **优势**: 专为社交媒体优化、支持批量爬取、自动生成报告
- **登录方式**: 扫码登录（推荐）或 Cookie 登录

**平台支持**:
- ✅ 知乎 (zhihu)
- ✅ 小红书 (xhs)
- ✅ 抖音 (douyin)
- ✅ B 站 (bilibili)

**使用方式**:
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

# 知乎爬虫
python3 main.py \
  --platform zhihu \
  --lt qrcode \
  --type search \
  --keywords "搜索关键词" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes

# 生成报告
python3 generate_openclaw_report.py \
  --platform zhihu \
  --contents-file data/zhihu/jsonl/search_contents_YYYY-MM-DD.jsonl \
  --comments-file data/zhihu/jsonl/search_comments_YYYY-MM-DD.jsonl \
  --output report.md
```

**输出文件**:
```
data/
├── zhihu/
│   └── jsonl/
│       ├── search_contents_YYYY-MM-DD.jsonl
│       └── search_comments_YYYY-MM-DD.jsonl
├── xhs/
│   └── jsonl/
│       └── ...
```

**适用场景**:
- ✅ 舆情监控
- ✅ 市场调研
- ✅ 竞品分析
- ✅ 学术研究
- ✅ 数据收集

---

## 4️⃣ web_search (Brave API) - 未配置

**状态**: ❌ 缺少 `BRAVE_API_KEY`

**配置方法**（可选）:
```bash
# 方法 1: 设置环境变量
export BRAVE_API_KEY="your_api_key_here"

# 方法 2: 配置 OpenClaw
openclaw configure --section web
```

**替代方案**: 使用 browser-automation 访问 baidu.com / google.com

---

## 🎯 使用优先级

**推荐工作流**:
```
1. 简单网页内容 → web_fetch (最快)
   ↓ 失败或需要交互
2. 动态网页/登录 → browser-automation
   ↓ 社交媒体数据
3. 社交媒体爬取 → mediacrawler
```

---

## 📊 性能对比

| 技能 | 速度 | 复杂度 | Token 消耗 | 适用场景 |
|------|------|--------|----------|---------|
| web_fetch | ⚡⚡⚡ 372ms | 🟢 简单 | 低 | 静态页面 |
| browser-automation | ⚡⚡ 2-5s | 🟡 中等 | 零 | 动态页面 |
| mediacrawler | ⚡ 1-5 分钟 | 🔴 复杂 | 零 | 社交媒体 |

---

## ⚠️ 注意事项

1. **控制爬取频率** - 避免对目标网站造成压力
2. **遵守 robots.txt** - 尊重网站爬虫协议
3. **数据隐私** - 不爬取个人隐私信息
4. **仅供学习研究** - 不用于商业用途
5. **保存原始数据** - JSONL 格式便于后续分析

---

## 📚 相关文档

- **完整配置**: `/home/Matrix/.openclaw/workspace/INTERNET_SKILLS.md`
- **测试报告**: `/home/Matrix/.openclaw/workspace/INTERNET_SKILLS_TEST_REPORT.md`
- **测试脚本**: `/home/Matrix/.openclaw/workspace/scripts/test-internet-skills.sh`
- **TOOLS.md**: `/home/Matrix/.openclaw/workspace/TOOLS.md` (上网技能章节)

---

*知识更新时间：2026-03-14 01:24*
