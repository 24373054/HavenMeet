# 🌐 上网技能配置指南

> **最后更新**: 2026-03-14  
> **状态**: ✅ 所有测试通过

---

## 📊 技能概览

| 技能名称 | 类型 | 需要 API Key | 状态 | 适用场景 |
|---------|------|------------|------|---------|
| **web_fetch** | 轻量级提取 | ❌ | ✅ | 快速获取网页内容 |
| **browser-automation-ultra** | 浏览器自动化 | ❌ | ✅ | 复杂交互、登录、表单填写 |
| **mediacrawler-search** | 社交媒体爬虫 | ❌ | ✅ | 知乎/小红书/抖音/B 站数据爬取 |
| web_search (Brave) | API 搜索 | ✅ | ❌ | 通用网页搜索（需配置） |

---

## 1️⃣ web_fetch - 轻量级网页内容提取

### 🎯 使用场景
- 快速获取网页文本内容
- 提取文章、文档、新闻
- 不需要 JavaScript 渲染的页面

### ✅ 测试验证
```bash
# 已测试：成功访问百度
✅ URL: https://www.baidu.com
✅ 响应时间：372ms
✅ 内容提取：正常
```

### 📝 使用示例
```javascript
// 在 OpenClaw 中直接调用
web_fetch:
  url: "https://example.com"
  extractMode: "markdown"  # 或 "text"
  maxChars: 5000  # 最大字符数
```

### ⚙️ 参数说明
- `url`: 目标网页 URL（必填）
- `extractMode`: `"markdown"` 或 `"text"`
- `maxChars`: 最大返回字符数（默认 5000）

### ⚠️ 限制
- 无法处理需要 JavaScript 渲染的页面
- 无法处理需要登录的网站
- 不适合复杂交互场景

---

## 2️⃣ browser-automation-ultra - 浏览器自动化

### 🎯 使用场景
- 需要 JavaScript 渲染的页面
- 登录、表单填写、点击操作
- 反爬虫网站（模拟人类行为）
- 复杂的多步骤流程

### ✅ 测试验证
```bash
# 已测试：成功访问知乎
✅ 浏览器路径：/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome
✅ 浏览器大小：385MB
✅ 访问知乎：成功
✅ 截图功能：正常
```

### 📝 使用示例

#### 方式 A: 使用 Playwright Python 脚本
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
    
    # 执行操作
    page.click('#some-element')
    page.type('#input', '搜索内容')
    
    # 截图
    page.screenshot(path='/tmp/openclaw/screenshot.png')
    
    browser.close()
```

#### 方式 B: 使用 OpenClaw browser 工具
```javascript
browser:
  action: "open"
  url: "https://example.com"
  profile: "openclaw"
  
browser:
  action: "click"
  selector: "#button"
  
browser:
  action: "screenshot"
  fullPage: true
```

### ⚙️ 环境配置

**Chrome 浏览器路径**:
```bash
/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome
```

**验证浏览器**:
```bash
ls -lh /home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome
# 输出：-rwxr-xr-x 1 Matrix Matrix 385M ...
```

**Playwright 版本**:
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
pip list | grep playwright
# 输出：playwright  1.45.0
```

### 📚 技能文档位置
```
/home/Matrix/.openclaw/workspace/skills/browser-automation-ultra/SKILL.md
```

### ⚠️ 注意事项
- 需要 `headless=True` 在无显示环境下运行
- 添加 `--no-sandbox` 参数避免权限问题
- 复杂操作建议使用 Python 脚本而非 browser 工具

---

## 3️⃣ mediacrawler-search - 社交媒体爬虫

### 🎯 使用场景
- 爬取知乎、小红书、抖音、B 站内容
- 舆情监控、市场调研
- 竞品分析、数据收集
- 学术研究

### ✅ 测试验证
```bash
# 已测试：成功爬取知乎数据
✅ 平台：知乎
✅ 关键词："北航 软件工程基础 课程设计"
✅ 抓取内容：12 条
✅ 抓取评论：163 条
✅ 数据保存：JSONL 格式
✅ 报告生成：正常
```

### 📝 使用示例

#### 爬取知乎数据
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

# 扫码登录方式（推荐）
python3 main.py \
  --platform zhihu \
  --lt qrcode \
  --type search \
  --keywords "搜索关键词" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes
```

#### 爬取小红书数据
```bash
python3 main.py \
  --platform xhs \
  --lt qrcode \
  --type search \
  --keywords "搜索关键词" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes
```

#### 生成分析报告
```bash
# 知乎报告
python3 generate_openclaw_report.py \
  --platform zhihu \
  --contents-file data/zhihu/jsonl/search_contents_2026-03-14.jsonl \
  --comments-file data/zhihu/jsonl/search_comments_2026-03-14.jsonl \
  --output zhihu_report.md

# 小红书报告
python3 generate_openclaw_report.py \
  --platform xhs \
  --contents-file data/xhs/jsonl/search_contents_2026-03-14.jsonl \
  --comments-file data/xhs/jsonl/search_comments_2026-03-14.jsonl \
  --output xhs_report.md
```

### ⚙️ 参数说明

**主要参数**:
- `--platform`: 平台选择（`zhihu` / `xhs` / `douyin` / `bilibili`）
- `--lt`: 登录方式（`qrcode` 扫码 / `cookie` Cookie）
- `--type`: 操作类型（`search` 搜索 / `detail` 详情）
- `--keywords`: 搜索关键词
- `--get_comment`: 是否获取评论（`yes` / `no`）
- `--save_data_option`: 保存格式（`jsonl` / `csv` / `xlsx`）
- `--headless`: 无头模式（`yes` / `no`）

**输出文件位置**:
```
/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/
├── zhihu/
│   └── jsonl/
│       ├── search_contents_YYYY-MM-DD.jsonl
│       └── search_comments_YYYY-MM-DD.jsonl
├── xhs/
│   └── jsonl/
│       ├── search_contents_YYYY-MM-DD.jsonl
│       └── search_comments_YYYY-MM-DD.jsonl
```

### 📱 扫码登录流程

1. **运行程序** → 自动生成二维码图片
2. **上传二维码** → 到飞书云盘获取链接
3. **发送链接** → 到群聊
4. **用户扫码** → 用手机 APP 扫码
5. **自动爬取** → 扫码后程序自动开始

**⚠️ 注意事项**:
- 二维码有效期约 120 秒
- 需要手机 APP 扫码
- 扫码失败需重新生成

### 📚 完整文档
```
/home/Matrix/.openclaw/workspace/skills/mediacrawler-search/SKILL.md
/home/Matrix/.openclaw/workspace/TOOLS.md (社交媒体爬虫与分析章节)
```

---

## 4️⃣ web_search (Brave API) - 需要配置

### ❌ 当前状态
```
❌ 缺少 BRAVE_API_KEY
❌ 无法使用
```

### 🔧 配置方法（可选）

如果需要启用：
```bash
# 方法 1: 设置环境变量
export BRAVE_API_KEY="your_api_key_here"

# 方法 2: 配置 OpenClaw
openclaw configure --section web
```

### 🔄 替代方案
**推荐使用**: `web_fetch` + `browser-automation-ultra` 组合

---

## 🚀 快速使用指南

### 场景 1: 快速查看网页内容
```
✅ 使用：web_fetch
示例：web_fetch(url="https://example.com")
```

### 场景 2: 需要登录/交互的网站
```
✅ 使用：browser-automation-ultra
示例：编写 Playwright 脚本或使用 browser 工具
```

### 场景 3: 社交媒体数据爬取
```
✅ 使用：mediacrawler-search
示例：python3 main.py --platform zhihu --keywords "xxx"
```

### 场景 4: 通用网页搜索
```
❌ web_search (需 API Key)
✅ 替代：使用浏览器访问 baidu.com / google.com
```

---

## 📋 测试脚本

### 运行完整测试
```bash
cd /home/Matrix/.openclaw/workspace
./scripts/test-internet-skills.sh
```

### 测试浏览器
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
python3 << 'EOF'
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page()
    page.goto('https://www.baidu.com')
    print(f"✅ 测试成功：{page.title()}")
    browser.close()
EOF
```

---

## 📊 性能对比

| 技能 | 速度 | 复杂度 | 适用场景 | Token 消耗 |
|------|------|--------|---------|----------|
| web_fetch | ⚡⚡⚡ 快 | 🟢 简单 | 静态页面 | 低 |
| browser-automation | ⚡⚡ 中等 | 🟡 中等 | 动态页面 | 零 |
| mediacrawler | ⚡ 慢 | 🔴 复杂 | 社交媒体 | 零 |
| web_search | ⚡⚡⚡ 快 | 🟢 简单 | 通用搜索 | 中 |

---

## 🔍 故障排查

### 问题 1: 浏览器无法启动
```bash
# 检查浏览器是否存在
ls -lh /home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome

# 重新安装浏览器
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
playwright install chromium
```

### 问题 2: MediaCrawler 扫码失败
```bash
# 检查二维码图片是否生成
ls -lh /home/Matrix/.openclaw/workspace/MediaCrawler-main/data/qrcode/

# 重新生成二维码
python3 main.py --platform zhihu --lt qrcode ...
```

### 问题 3: web_fetch 返回空内容
```
可能原因：
1. 页面需要 JavaScript 渲染 → 改用 browser-automation
2. 需要登录 → 使用 browser-automation 先登录
3. 反爬虫机制 → 使用 browser-automation 模拟人类行为
```

---

## 📝 最佳实践

### ✅ 推荐工作流

**简单网页内容获取**:
```
web_fetch → 提取文本 → 分析
```

**复杂网站交互**:
```
browser-automation → 登录/操作 → 截图/提取 → 分析
```

**社交媒体研究**:
```
mediacrawler → 爬取数据 → 生成报告 → 飞书文档
```

### ⚠️ 注意事项

1. **控制爬取频率** - 避免对目标网站造成压力
2. **遵守 robots.txt** - 尊重网站爬虫协议
3. **数据隐私** - 不爬取个人隐私信息
4. **仅供学习研究** - 不用于商业用途
5. **保存原始数据** - JSONL 格式便于后续分析

---

## 📚 相关文档

- **browser-automation-ultra**: `/home/Matrix/.openclaw/workspace/skills/browser-automation-ultra/SKILL.md`
- **mediacrawler-search**: `/home/Matrix/.openclaw/workspace/skills/mediacrawler-search/SKILL.md`
- **TOOLS.md**: `/home/Matrix/.openclaw/workspace/TOOLS.md` (社交媒体爬虫与分析章节)
- **测试脚本**: `/home/Matrix/.openclaw/workspace/scripts/test-internet-skills.sh`

---

## 🎯 总结

**✅ 已配置并测试通过的技能**:
1. **web_fetch** - 轻量级网页内容提取
2. **browser-automation-ultra** - Playwright 浏览器自动化
3. **mediacrawler-search** - 社交媒体爬虫（知乎/小红书/抖音/B 站）

**📊 能力覆盖**:
- ✅ 静态网页内容获取
- ✅ 动态网页交互操作
- ✅ 社交媒体数据爬取
- ✅ 自动化报告生成

**🚀 推荐使用顺序**:
1. 优先使用 `web_fetch`（最快）
2. 需要交互时使用 `browser-automation`
3. 社交媒体数据使用 `mediacrawler`

---

*文档生成时间：2026-03-14 01:18*  
*下次更新：技能添加或配置变更时*
