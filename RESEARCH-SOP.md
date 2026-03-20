# 🎯 多工具综合调研流程 (Standard Operating Procedure)

**版本**: v1.0  
**创建时间**: 2026-03-14  
**最后更新**: 2026-03-14  
**适用场景**: 需要深度调研、多源数据验证、综合分析报告的任务

---

## 📋 一、流程概述

### 1.1 核心思想

**四步递进法**:
```
快速概览 → 深度访问 → 精准爬取 → 综合分析
```

**设计理念**:
- ⚡ **速度优先**: 先用最快的工具获取概览
- 🔍 **深度验证**: 用浏览器访问需要 JS 渲染的页面
- 🎯 **精准获取**: 用专业爬虫获取结构化数据
- 📊 **综合输出**: 整合多源数据生成完整报告

### 1.2 工具矩阵

| 工具 | 速度 | 深度 | 适用场景 | 是否需要登录 |
|------|------|------|----------|-------------|
| **web_fetch** | ⚡⚡⚡ (秒级) | 📊 浅 | 快速搜索、静态页面 | ❌ |
| **browser-automation** | ⚡⚡ (数十秒) | 📊📊 中 | 需要 JS 渲染、交互 | ⚠️ 可选 |
| **mediacrawler** | ⚡ (分钟级) | 📊📊📊 深 | 社交媒体数据爬取 | ✅ 需要 |

---

## 🚀 二、完整流程 (四步法)

### Step 1: web_fetch 快速调研

**目标**: 快速获取信息概览，验证调研方向

**执行命令**:
```javascript
web_fetch:
  url: "https://www.baidu.com/s?wd=你的搜索关键词"
  extractMode: "markdown"
  maxChars: 15000
```

**关键参数**:
- `extractMode`: "markdown" (推荐) 或 "text"
- `maxChars`: 10000-20000 (根据内容量调整)

**成功标志**:
- ✅ 返回时间在 1-3 秒内
- ✅ 获取到 2000+ 字的搜索结果
- ✅ 能够看到主要信息点

**失败处理**:
- ❌ 返回空内容 → 检查 URL 是否正确
- ❌ 返回时间过长 → 改用 browser-automation
- ❌ 需要登录 → 跳过此步，直接进入 Step 2

**示例**:
```javascript
web_fetch:
  url: "https://www.baidu.com/s?wd=北航 软件工程 小组项目"
  extractMode: "markdown"
  maxChars: 15000
```

---

### Step 2: browser-automation 深度访问

**目标**: 访问需要 JavaScript 渲染的页面，获取更详细内容

**前置检查**:
```bash
# 检查 Chrome 是否安装
ls -lh /home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome
```

**执行脚本**:
```python
# /tmp/browser-deep-search.py
from playwright.sync_api import sync_playwright
import time
import json

chrome_path = '/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome'

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=chrome_path,
        headless=True,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    )
    
    page = browser.new_page()
    
    # 访问目标页面
    page.goto('https://目标 URL', wait_until='networkidle', timeout=30000)
    time.sleep(3)  # 等待内容加载
    
    # 提取内容 (根据页面结构调整选择器)
    contents = page.query_selector_all('.目标选择器')
    
    # 保存结果
    results = []
    for item in contents:
        # 提取具体字段
        results.append({...})
    
    # 截图
    page.screenshot(path='/tmp/page-screenshot.png')
    
    browser.close()
    
    # 保存 JSON
    with open('/tmp/browser-results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
```

**常见错误及修复**:

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `No supported browser found` | 缺少启动参数 | 添加 `--no-sandbox` 等参数 |
| `ERR_SSL_PROTOCOL_ERROR` | SSL 证书问题 | 添加 `--ignore-certificate-errors` |
| 超时 (timeout) | 网络慢或页面复杂 | 增加 `timeout` 值，或改用 web_fetch |
| 提取不到内容 | 选择器错误 | 检查页面结构，调整 CSS 选择器 |

**成功标志**:
- ✅ 浏览器成功启动
- ✅ 页面加载完成
- ✅ 生成截图 (验证访问成功)
- ✅ 提取到结构化数据

---

### Step 3: mediacrawler 精准爬取

**目标**: 从社交媒体平台获取大量结构化数据

**适用平台**: 知乎、小红书、抖音、B 站、微博、贴吧

**前置检查**:
```bash
# 检查是否有已保存的登录态
ls -la /home/Matrix/.openclaw/workspace/MediaCrawler-main/browser_data/
# 应该看到 zhihu_user_data_dir, xhs_user_data_dir 等目录

# 检查 Cookie 是否有效
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
python3 -c "
import sqlite3
conn = sqlite3.connect('browser_data/zhihu_user_data_dir/Default/Cookies')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM cookies')
count = cursor.fetchone()[0]
print(f'Cookie 数量：{count}')
conn.close()
"
```

**执行命令 (Cookie 登录 - 推荐)**:
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
python3 main.py \
  --platform zhihu \
  --lt cookie \
  --type search \
  --keywords "你的搜索关键词" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes
```

**执行命令 (扫码登录 - 首次使用)**:
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
python3 main.py \
  --platform zhihu \
  --lt qrcode \
  --type search \
  --keywords "你的搜索关键词" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes

# 然后:
# 1. 程序会生成二维码图片
# 2. 上传到飞书云盘获取链接
# 3. 发送链接到群聊
# 4. 用手机 App 扫码
# 5. 程序自动开始爬取
```

**关键参数说明**:

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `--platform` | 平台 | zhihu / xhs / douyin / bilibili |
| `--lt` | 登录方式 | cookie (推荐) / qrcode |
| `--type` | 爬取类型 | search (搜索) / detail (指定 ID) |
| `--keywords` | 搜索关键词 | 用空格分隔多个关键词 |
| `--get_comment` | 是否爬取评论 | yes / no |
| `--save_data_option` | 保存格式 | jsonl (推荐) / json / csv |
| `--headless` | 无头模式 | yes (后台运行) |

**成功标志**:
- ✅ 显示 "Zhihu Crawler finished"
- ✅ 生成 `search_contents_YYYY-MM-DD.jsonl`
- ✅ 生成 `search_comments_YYYY-MM-DD.jsonl`
- ✅ 数据行数 > 0

**失败处理**:
- ❌ Cookie 过期 → 改用 `--lt qrcode` 重新扫码
- ❌ 需要扫码但无法扫码 → 等待人工协助
- ❌ 爬取失败 → 检查网络，重试

**数据位置**:
```
MediaCrawler-main/data/{平台}/jsonl/
├── search_contents_YYYY-MM-DD.jsonl  # 内容数据
└── search_comments_YYYY-MM-DD.jsonl  # 评论数据
```

---

### Step 4: 综合分析生成报告

**目标**: 整合所有数据源，生成完整调研报告

**数据整合**:
```python
# 读取所有数据源
import json

# 1. web_fetch 结果 (已保存为 markdown)
with open('/path/to/web_fetch_result.md', 'r', encoding='utf-8') as f:
    web_data = f.read()

# 2. browser-automation 结果
with open('/tmp/browser-results.json', 'r', encoding='utf-8') as f:
    browser_data = json.load(f)

# 3. mediacrawler 结果
contents = []
comments = []
with open('/path/to/search_contents.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        contents.append(json.loads(line))
with open('/path/to/search_comments.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        comments.append(json.loads(line))

# 综合分析
analysis = {
    'web_search': web_data,
    'browser_deep': browser_data,
    'social_media': {
        'contents': contents,
        'comments': comments
    }
}
```

**报告结构模板**:
```markdown
# 🎯 调研报告标题

**调研时间**: YYYY-MM-DD HH:MM  
**调研方式**: 四步完整流程  
**数据规模**: X 条 web 结果 + Y 条浏览器数据 + Z 条社交媒体数据

## 📊 一、调研方法论
### 1.1 使用的工具和技术
### 1.2 调研流程执行记录

## 📈 二、调研发现
### 2.1 核心发现
### 2.2 数据统计
### 2.3 用户反馈

## 💡 三、建议/推荐
### 3.1 推荐方案 1
### 3.2 推荐方案 2
### 3.3 推荐方案 3

## 🎯 四、实施建议
### 4.1 避坑指南
### 4.2 最佳实践
### 4.3 成功关键

## 📚 五、参考资料

## 🎬 六、总结

---
*报告生成时间：YYYY-MM-DD HH:MM*  
*数据来源：web_fetch + browser-automation + mediacrawler*  
*版本：vX.X*
```

**成功标志**:
- ✅ 报告包含所有数据源的分析
- ✅ 有明确的数据统计
- ✅ 有可操作的建议
- ✅ 有参考资料链接

---

## 🛠️ 三、常见问题与解决方案

### 3.1 浏览器相关问题

**Q: `No supported browser found`**  
A: 添加启动参数 `--no-sandbox`, `--disable-setuid-sandbox`

**Q: 浏览器启动超时**  
A: 检查 Chrome 路径是否正确，或增加 timeout 值

**Q: 提取不到内容**  
A: 检查页面是否加载完成，调整 CSS 选择器

### 3.2 MediaCrawler 相关问题

**Q: 每次都要扫码**  
A: 改用 `--lt cookie` 模式，使用已保存的登录态

**Q: Cookie 过期**  
A: 重新扫码登录，或检查 Cookie 有效期

**Q: 爬取速度慢**  
A: 减少爬取数量，或增加延时

### 3.3 数据整合问题

**Q: 数据格式不统一**  
A: 在分析前进行数据清洗和标准化

**Q: 数据量太大**  
A: 抽样分析，或分批处理

---

## 📊 四、性能指标

### 4.1 时间预算

| 步骤 | 正常耗时 | 超时阈值 | 说明 |
|------|----------|----------|------|
| web_fetch | 1-3 秒 | 10 秒 | 最快 |
| browser-automation | 30-60 秒 | 120 秒 | 中等 |
| mediacrawler | 60-180 秒 | 300 秒 | 最慢 |
| 综合分析 | 1-5 分钟 | 10 分钟 | 取决于数据量 |

**总耗时**: 3-10 分钟 (正常情况)

### 4.2 数据质量

| 指标 | web_fetch | browser-automation | mediacrawler |
|------|-----------|-------------------|--------------|
| 数据量 | 低 (~2KB) | 中 (~100KB) | 高 (~1MB+) |
| 结构化 | 低 | 中 | 高 |
| 真实性 | 中 | 高 | 高 |
| 时效性 | 高 | 高 | 高 |

---

## 🎯 五、最佳实践

### 5.1 何时使用此流程

**推荐使用**:
- ✅ 需要深度调研的课题
- ✅ 需要多源数据验证
- ✅ 需要生成正式报告
- ✅ 涉及社交媒体数据

**不推荐使用**:
- ❌ 简单信息查询 (直接用 web_fetch)
- ❌ 实时性要求极高 (流程太长)
- ❌ 数据量很小 (不值得)

### 5.2 优化建议

**提高效率**:
1. 先检查是否有现成的 Cookie，避免扫码
2. 合理设置爬取数量，避免超时
3. 使用 headless 模式后台运行
4. 提前准备好 CSS 选择器

**保证质量**:
1. 每一步都要验证结果
2. 保留原始数据文件
3. 生成截图作为证据
4. 记录所有参数和配置

**降低成本**:
1. 优先使用免费工具 (web_fetch, browser)
2. 只在必要时使用 mediacrawler
3. 控制数据量，避免浪费
4. 复用已有登录态

---

## 📝 六、案例参考

### 6.1 北航软件工程课程项目调研 (2026-03-14)

**背景**: 需要为北航《软件工程基础》课程推荐小组项目

**执行过程**:
1. **web_fetch**: 百度搜索 "北航 软件工程 小组项目" (1.36 秒)
   - 获取 2640 字搜索结果
   - 发现传统项目类型

2. **browser-automation**: 访问知乎获取详细内容 (~60 秒)
   - 修复浏览器启动问题
   - 生成 168KB 截图
   - 验证浏览器功能正常

3. **mediacrawler**: 爬取知乎数据 (~90 秒)
   - 使用 Cookie 登录 (避免扫码)
   - 获取 69 条内容 + 248 条评论
   - 总计 317 条数据

4. **综合分析**: 生成终极报告
   - 整合所有数据源
   - 推荐 AI 辅助代码审查平台
   - 提供避坑指南

**成果**:
- 📄 终极调研报告 (8.6 KB)
- 📊 原始数据 (362 KB + 146 KB)
- 🎯 明确的项目推荐
- ⚠️ 详细的避坑指南

**关键突破**:
- 🔧 修复了浏览器启动问题
- 🔑 发现了 Cookie 登录方式
- 📊 成功获取真实用户反馈

---

## 🔄 七、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-03-14 | 初始版本，基于北航调研案例 |

---

## 📞 八、联系方式

**问题反馈**: 通过飞书私聊 HavenMeet  
**文档维护**: 更新到 `/home/Matrix/.openclaw/workspace/`  
**技能位置**: `/home/Matrix/.openclaw/workspace/skills/`

---

**记住**: 这个流程是经过实战验证的，遇到问题先查文档，再尝试修复，最后才考虑放弃某一步。灵活调整，但保持完整性！🦾
