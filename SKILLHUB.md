# Skillhub 技能商店

## 📦 已安装的技能列表

### 1️⃣ 文件管理类
- **filesystem-1-0-0** - 高级文件系统操作（递归搜索、批量复制/移动/删除、目录分析）
- **file-converter** - 文件格式转换（JSON/YAML/XML/CSV/Markdown 互转）
- **file-sorter** - 智能文件分类（按类型/大小/日期/关键词）

### 2️⃣ 日程与日历类
- **calendar-manager** - 日历管理（读取日程、创建事件、设置提醒）
- **lunar-calendar** - 中国农历查询（公历/农历转换、黄历宜忌、24 节气）

### 3️⃣ 浏览器自动化类
- **browser-automation-ultra** - 零 token 浏览器自动化（Playwright + CDP 锁管理）

### 4️⃣ 代码分析类
- **code-project-analyzer** - 代码项目自动分析（结构识别、技术栈检测、自动生成文档）
- **code-review-sr** - AI 代码审查（bug 检测、安全漏洞、性能问题）

### 5️⃣ 日常助手类
- **briefing** - 每日简报（日历、待办、天气汇总）

### 6️⃣ Skillhub 相关
- **find-skills** - 查找技能（Skillhub 搜索功能）
- **skillhub-preference** - Skillhub 偏好配置

### 7️⃣ 自定义技能
- **flux2-image-gen** - Flux.2 图像生成
- **mediacrawler-search** - 社交媒体爬虫与分析（小红书/知乎）

---

## 🔧 Skillhub 使用指南

### 搜索技能
```bash
skillhub search <关键词>
# 示例：skillhub search calendar
```

### 安装技能
```bash
skillhub install <技能名>
# 示例：skillhub install filesystem-1-0-0
```

### 查看已安装技能
```bash
ls -la /home/Matrix/.openclaw/workspace/skills/
```

### 卸载技能
```bash
# 直接删除技能目录
rm -rf /home/Matrix/.openclaw/workspace/skills/<技能名>
```

---

## 📊 技能分类汇总

| 类别 | 技能数量 | 主要功能 |
|------|---------|---------|
| 文件管理 | 3 | 文件系统操作、格式转换、文件分类 |
| 日程日历 | 2 | 日程管理、农历查询 |
| 浏览器 | 1 | 浏览器自动化 |
| 代码分析 | 2 | 项目分析、代码审查 |
| 日常助手 | 1 | 每日简报 |
| Skillhub | 2 | 技能查找、配置 |
| 自定义 | 2 | 图像生成、社交媒体爬取 |

**总计**: 13 个技能

---

## 🚀 常用场景

### 文件管理
- 需要批量处理文件 → `filesystem-1-0-0`
- 需要转换文件格式 → `file-converter`
- 需要整理文件 → `file-sorter`

### 日程管理
- 查看/创建日程 → `calendar-manager`
- 查询农历/节气 → `lunar-calendar`

### 代码开发
- 分析项目结构 → `code-project-analyzer`
- 代码审查 → `code-review-sr`

### 浏览器自动化
- 自动化网页操作 → `browser-automation-ultra`

### 日常使用
- 获取每日简报 → `briefing`

---

## 📝 更新日志

- **2026-03-14**: 初始安装 Skillhub，安装 10 个常用技能
- **安装源**: 腾讯镜像 `https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com`

---

## 🔗 相关链接

- **Skillhub 官网**: https://skillhub.com
- **腾讯镜像**: https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com
- **CLI 路径**: `/home/Matrix/.local/bin/skillhub`
- **Skills 目录**: `/home/Matrix/.openclaw/workspace/skills/`
