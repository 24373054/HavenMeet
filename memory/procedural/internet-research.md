# 上网调研流程 (Internet Research)

**更新时间**: 2026-03-14  
**版本**: 1.0

---

## 🎯 调研任务流程

### 步骤 1: 确定调研目标

**输入**: 用户调研需求  
**输出**: 明确的调研关键词和目标平台

**示例**:
```
用户："帮我调研北航软件工程课程设计项目"
→ 关键词："北航 软件工程基础 课程设计"
→ 目标平台：知乎（学术讨论多）
```

---

### 步骤 2: 选择调研工具

**决策树**:

```
需要快速获取网页内容？
  ↓ 是
  使用 web_fetch
  ↓ 否
需要登录/交互/动态页面？
  ↓ 是
  使用 browser-automation
  ↓ 否
需要社交媒体数据？
  ↓ 是
  使用 mediacrawler
  ↓ 否
使用 browser-automation 访问搜索引擎
```

**工具选择表**:

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
| 静态网页内容 | web_fetch | 最快（~372ms） |
| 需要登录/交互 | browser-automation | 完整浏览器功能 |
| 知乎/小红书数据 | mediacrawler | 专为社交媒体优化 |
| 通用搜索 | browser-automation | 无需 API Key |

---

### 步骤 3: 执行调研

#### 场景 A: 使用 web_fetch

```javascript
web_fetch:
  url: "https://example.com/page"
  extractMode: "markdown"
  maxChars: 10000
```

**适用**: 快速获取文章、文档、新闻

#### 场景 B: 使用 browser-automation

**方式 1: Python 脚本**
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
    
    # 执行搜索
    page.type('input[name="q"]', '搜索关键词')
    page.press('input[name="q"]', 'Enter')
    page.wait_for_timeout(3000)
    
    # 提取内容
    content = page.content()
    
    browser.close()
```

**方式 2: OpenClaw browser 工具**
```javascript
browser:
  action: "open"
  url: "https://www.baidu.com/s?wd=关键词"
  
browser:
  action: "screenshot"
  fullPage: true
```

#### 场景 C: 使用 mediacrawler（推荐用于社交媒体）

**知乎爬虫**:
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

python3 main.py \
  --platform zhihu \
  --lt qrcode \
  --type search \
  --keywords "搜索关键词" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes
```

**小红书爬虫**:
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

**扫码登录流程**:
1. 运行程序 → 自动生成二维码图片
2. 上传二维码 → 到飞书云盘获取链接
3. 发送链接 → 到群聊
4. 用户扫码 → 用手机 APP 扫码
5. 自动爬取 → 扫码后程序自动开始

**生成报告**:
```bash
# 知乎报告
python3 generate_openclaw_report.py \
  --platform zhihu \
  --contents-file data/zhihu/jsonl/search_contents_YYYY-MM-DD.jsonl \
  --comments-file data/zhihu/jsonl/search_comments_YYYY-MM-DD.jsonl \
  --output report.md

# 小红书报告
python3 generate_openclaw_report.py \
  --platform xhs \
  --contents-file data/xhs/jsonl/search_contents_YYYY-MM-DD.jsonl \
  --comments-file data/xhs/jsonl/search_comments_YYYY-MM-DD.jsonl \
  --output report.md
```

---

### 步骤 4: 数据分析

**数据位置**:
```
/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/
├── zhihu/jsonl/search_contents_YYYY-MM-DD.jsonl
└── zhihu/jsonl/search_comments_YYYY-MM-DD.jsonl
```

**读取数据**:
```bash
# 查看内容
cat data/zhihu/jsonl/search_contents_YYYY-MM-DD.jsonl | jq .

# 统计数量
wc -l data/zhihu/jsonl/search_contents_YYYY-MM-DD.jsonl
```

**分析要点**:
1. 提取关键信息（项目案例、技术栈、功能模块）
2. 识别趋势和模式
3. 总结创新点
4. 生成建议

---

### 步骤 5: 生成报告

**报告结构**:
```markdown
# 调研报告

## 📊 调研总结
- 数据来源
- 样本数量
- 调研时间

## 🎯 发现
- 主要趋势
- 典型案例
- 技术栈分析

## 💡 建议
- 创新方向
- 实施建议
- 注意事项

## 📁 数据文件
- 原始数据位置
- 报告生成时间
```

**上传到飞书**（可选）:
```bash
# 使用 feishu_create_doc 工具
feishu_create_doc:
  title: "调研报告：xxx"
  markdown: "# 调研报告\n\n内容..."
```

---

## 🔧 故障排查

### 问题 1: web_fetch 返回空内容

**原因**: 页面需要 JavaScript 渲染  
**解决**: 改用 browser-automation

### 问题 2: browser-automation 无法启动

**检查**:
```bash
# 验证浏览器是否存在
ls -lh /home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome

# 测试浏览器
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
python3 << 'EOF'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    print("✅ 浏览器正常")
    browser.close()
EOF
```

### 问题 3: MediaCrawler 扫码失败

**解决**:
```bash
# 检查二维码图片
ls -lh data/qrcode/

# 重新生成二维码
python3 main.py --platform zhihu --lt qrcode ...
```

### 问题 4: 爬取速度慢

**优化**:
- 减少 `--get_comment`（不获取评论）
- 使用 `--headless yes`
- 控制并发数量

---

## 📝 最佳实践

### ✅ 推荐做法

1. **优先使用 web_fetch** - 最快、最简单
2. **社交媒体用 mediacrawler** - 专为社交平台优化
3. **保存原始数据** - JSONL 格式便于后续分析
4. **控制爬取频率** - 避免对网站造成压力
5. **定期测试** - 使用 `scripts/test-internet-skills.sh`

### ❌ 避免做法

1. **不要频繁爬取** - 遵守 robots.txt
2. **不要爬取隐私数据** - 尊重用户隐私
3. **不要用于商业用途** - 仅供学习研究
4. **不要忘记保存数据** - 原始数据很重要

---

## 🚀 快速参考

**一键测试所有技能**:
```bash
cd /home/Matrix/.openclaw/workspace
./scripts/test-internet-skills.sh
```

**查看完整文档**:
```
/home/Matrix/.openclaw/workspace/INTERNET_SKILLS.md
```

**查看测试报告**:
```
/home/Matrix/.openclaw/workspace/INTERNET_SKILLS_TEST_REPORT.md
```

---

*流程更新时间：2026-03-14 01:24*
