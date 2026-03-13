# MEMORY.md - 长期记忆

**最后更新**: 2026-03-14  
**记忆系统**: Episodic + Semantic + Procedural (memory-manager skill)

---

## 🌐 上网技能配置 (2026-03-14)

### ✅ 已配置技能

1. **web_fetch** - 轻量级网页提取
   - 速度：~372ms
   - 用途：快速获取静态网页内容
   - 无需 API Key ✅

2. **browser-automation-ultra** - Playwright 浏览器自动化
   - Chrome 路径：`/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome` (385MB)
   - Playwright 版本：1.45.0
   - 用途：需要登录、交互、JavaScript 渲染的网站
   - 无需 API Key ✅

3. **mediacrawler-search** - 社交媒体爬虫
   - 平台：知乎、小红书、抖音、B 站
   - 用途：舆情监控、市场调研、竞品分析
   - 登录方式：扫码登录（推荐）
   - 无需 API Key ✅

4. **browser-screenshot** - 已登录状态浏览器截图（2026-03-14 新增）
   - 关键：使用 `launch_persistent_context` + 已登录的用户数据目录
   - 用户数据位置：`MediaCrawler-main/browser_data/{平台}_user_data_dir`
   - 验证：截图大小 > 1MB 说明内容完整
   - 文档：`TOOLS.md` (浏览器截图最佳实践章节)

### ❌ 未配置技能

- **web_search (Brave API)** - 缺少 `BRAVE_API_KEY`
  - 替代方案：使用 browser-automation 访问搜索引擎

### 📁 相关文档

- `INTERNET_SKILLS.md` - 完整配置指南
- `INTERNET_SKILLS_TEST_REPORT.md` - 测试报告
- `scripts/test-internet-skills.sh` - 一键测试脚本
- `TOOLS.md` - 上网技能章节

### 🎯 使用优先级

```
web_fetch (最快) 
  → 失败或需要交互 → 
browser-automation 
  → 社交媒体 → 
mediacrawler
```

---

## 🧠 记忆管理系统

### 架构

使用 `memory-manager` skill 实现三层记忆：

```
memory/
├── episodic/           # What happened (时间事件)
├── semantic/           # What I know (知识)
├── procedural/         # How to (操作流程)
└── snapshots/          # 压缩备份
```

### 记忆文件

**Episodic** (事件日志):
- `memory/2026-03-14.md` - 今日日志
- `memory/2026-03-13.md` - 昨日日志

**Semantic** (知识):
- `memory/semantic/internet-skills.md` - 上网技能知识

**Procedural** (流程):
- `memory/procedural/internet-research.md` - 调研流程

### 管理命令

```bash
# 检查压缩风险
bash skills/memory-manager/detect.sh

# 组织记忆
bash skills/memory-manager/organize.sh

# 搜索记忆
bash skills/memory-manager/search.sh episodic "关键词"
bash skills/memory-manager/search.sh semantic "关键词"
bash skills/memory-manager/search.sh procedural "关键词"

# 查看统计
bash skills/memory-manager/stats.sh
```

### Heartbeat 检查

已添加到 `HEARTBEAT.md`:
- 每次心跳检查记忆文件大小
- 定期组织记忆（每天 23:00）
- 压缩前自动创建快照

---

## 📝 重要经验

### 上网调研 (2026-03-14 实战验证)

**四步递进法** (完整流程):
```
Step 1: web_fetch (1-3 秒) → 快速概览
  ↓
Step 2: browser-automation (30-60 秒) → 深度访问
  ↓
Step 3: mediacrawler (60-180 秒) → 精准爬取
  ↓
Step 4: 综合分析 (1-5 分钟) → 生成报告
```

**关键突破**:
1. **browser-automation 修复**: 添加 `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage` 参数
2. **mediacrawler Cookie 登录**: 使用 `--lt cookie` 避免每次扫码，Cookie 位置 `browser_data/zhihu_user_data_dir/Default/Cookies`
3. **实战案例**: 北航调研成功获取 69 条知乎内容 +248 条评论

**故障排查**:
- web_fetch 返回空 → 改用 browser-automation
- 浏览器无法启动 → 检查 Chrome 路径 + 添加启动参数
- MediaCrawler 扫码失败 → 改用 Cookie 登录 (`--lt cookie`)
- Cookie 过期 → 重新扫码或检查 `browser_data/{平台}_user_data_dir/Default/Cookies`

**最佳实践**:
1. 优先使用 `web_fetch`（最快）
2. 需要交互时使用 `browser-automation`
3. 社交媒体数据使用 `mediacrawler` (Cookie 登录)
4. 保存原始数据（JSONL 格式）
5. 控制爬取频率，遵守 robots.txt

**文档位置**:
- 完整 SOP: `RESEARCH-SOP.md`
- 配置速查：`TOOLS.md` (多工具综合调研流程章节)

### 记忆管理

**WAL 协议** (Write-Ahead Log):
- 用户给出重要信息 → 立即写入记忆 → 然后回复
- 避免先回复后保存导致的上下文丢失

**记忆卫生** (每周):
1. 运行 `detect.sh` 检查压缩风险
2. 运行 `organize.sh` 组织记忆
3. 归档已完成的任务
4. 清理无关的向量记忆

---

## 🔧 系统配置

### 浏览器
- **路径**: `/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome`
- **大小**: 385MB
- **安装方式**: MediaCrawler 自动安装

### Playwright
- **版本**: 1.45.0
- **位置**: MediaCrawler-main 项目的 Python 环境

### 工作目录
- **Workspace**: `/home/Matrix/.openclaw/workspace`
- **MediaCrawler**: `/home/Matrix/.openclaw/workspace/MediaCrawler-main`

---

## 📚 技能列表

**已安装技能**:
- ✅ memory-manager - 记忆管理
- ✅ elite-longterm-memory - 高级长期记忆
- ✅ browser-automation-ultra - 浏览器自动化
- ✅ mediacrawler-search - 社交媒体爬虫
- ✅ flux2-image-gen - 图像生成

---

*记忆更新时间：2026-03-14 01:24*
