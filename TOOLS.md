# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## 🚨 安全红线 (Safety Rules)

**这台服务器是学校实验室的服务器，运行着重要进程和隐私数据！**

### 允许的文件夹
- `/home/Matrix/yz/havenmeet/` - OpenClaw 安装目录（pnpm 本地安装，使用 `pnpx` 执行命令）
- `/home/Matrix/.openclaw/` - OpenClaw 工作区（配置文件、workspace 等）

### 严格禁止
- ❌ **不能**修改上述两个文件夹以外的任何文件
- ❌ **不能**删除任何文件
- ❌ **不能**修改其他部分的系统配置环境
- ❌ **不能**在其它目录创建或写入文件

**在执行任何可能影响系统的操作前，必须先确认路径在上述允许范围内！**

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## 🎨 图像生成 (Flux2)

**使用方式：**
```bash
cd /home/Matrix/.openclaw/workspace/skills/flux2-image-gen && python3 scripts/flux2_generate.py \
  --prompt "图片描述" \
  --filename "2026-03-12-hh-mm-ss-name.png" \
  --width 1024 \
  --height 1024
```

**重要：**
- ❌ 不要用 `./scripts/flux2_generate.py`（权限不够）
- ✅ 用 `python3 scripts/flux2_generate.py`（直接运行）
- API URL: `https://ptp.matrixlabs.cn`
- 生成时间：5-30 秒
- 推荐分辨率：1024x1024 或 1024x1408（竖图）

**参数：**
- `--prompt`: 图片描述（必填）
- `--filename`: 输出文件名（必填，建议用时间戳）
- `--width/--height`: 宽高（256-2048，默认 1024）
- `--steps`: 扩散步数（1-50，默认 4）
- `--cfg`: CFG 缩放（默认 1.0）

**示例：**
```bash
python3 scripts/flux2_generate.py \
  --prompt "A candid snapshot of an elderly person walking by a riverbank" \
  --filename "2026-03-12-18-09-50-elderly-river-walk.png" \
  --width 1024 --height 1024
```

## 📊 社交媒体爬虫与分析 (MediaCrawler)

**项目路径**: `/home/Matrix/.openclaw/workspace/MediaCrawler-main`  
**Skill 文档**: `/home/Matrix/.openclaw/workspace/skills/mediacrawler-search/SKILL.md`

### 🎯 何时使用此能力

**当用户需要以下能力时，立即调用 MediaCrawler：**

1. **舆情监控** - "帮我看看网上对 XX 的评价"、"了解 XX 话题的舆论"
2. **资讯收集** - "爬取小红书/知乎上关于 XX 的讨论"、"收集行业趋势数据"
3. **竞品分析** - "分析竞品在社交媒体上的表现"、"看看用户反馈"
4. **市场调研** - "了解目标用户群体的偏好"、"收集用户关注点"
5. **内容创作** - "帮我写小红书推文"、"基于数据创作内容"
6. **学术研究** - "爬取学术讨论"、"分析研究热点"

### 核心能力
- ✅ **数据爬取** - 小红书、知乎、抖音、B 站等多平台
- ✅ **数据分析** - 互动量统计、内容分类、趋势分析、可视化
- ✅ **报告生成** - Markdown 报告、飞书文档上传
- ✅ **内容创作** - 基于数据分析创作推文 + Flux.2 配图

### 🚀 快速使用

#### 场景 1: 爬取小红书数据（扫码登录）
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

# 方式 A: 扫码登录（推荐）
python3 main.py \
  --platform xhs \
  --lt qrcode \
  --type search \
  --keywords "OpenClaw" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes

# 方式 B: Cookie 登录（需要预先获取）
python3 main.py \
  --platform xhs \
  --lt cookie \
  --type search \
  --keywords "OpenClaw"
```

#### 场景 2: 爬取知乎数据（扫码登录）
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

python3 main.py \
  --platform zhihu \
  --lt qrcode \
  --type search \
  --keywords "OpenClaw" \
  --get_comment yes \
  --save_data_option jsonl \
  --headless yes
```

#### 场景 3: 生成分析报告
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main

# 小红书报告
python3 generate_openclaw_report.py \
  --platform xhs \
  --contents-file data/xhs/jsonl/search_contents_2026-03-13.jsonl \
  --comments-file data/xhs/jsonl/search_comments_2026-03-13.jsonl \
  --output openclaw_xhs_report.md

# 知乎报告
python3 generate_openclaw_report.py \
  --platform zhihu \
  --contents-file data/zhihu/jsonl/search_contents_2026-03-13.jsonl \
  --comments-file data/zhihu/jsonl/search_comments_2026-03-13.jsonl \
  --output openclaw_zhihu_report.md
```

#### 场景 4: 生成配图（Flux.2）
```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
python3 generate_xhs_images.py
```

### 📱 扫码登录详细流程

**小红书扫码**:
1. 运行程序 → 自动生成二维码图片
2. 上传二维码到飞书云盘 → 获取链接
3. 发送链接到群聊 → 用户扫码
4. 用户用手机小红书 App 扫码 → 程序自动开始爬取

**知乎扫码**:
1. 运行程序 → 生成二维码
2. 上传到云盘并发送链接
3. 用户用知乎 App 扫码
4. 扫码后自动爬取

**注意事项**:
- ⏱️ 二维码有效期约 120 秒
- 📱 需要手机 App 扫码
- 🔄 扫码失败需重新生成
- ⚡ 扫码后程序自动开始爬取

### 📊 完整工作流程

```
1. 爬取数据 → MediaCrawler 搜索关键词
   ↓
2. 数据保存 → JSONL 格式（笔记 + 评论）
   ↓
3. 生成报告 → analyze 脚本生成 Markdown 报告
   ↓
4. 上传文档 → 飞书文档分享
   ↓
5. 创作推文 → 基于数据创作 + Flux.2 配图
   ↓
6. 发布内容 → 手动发布到小红书/知乎
```

### 📁 输出文件

- `data/xhs/jsonl/search_contents_YYYY-MM-DD.jsonl` - 小红书笔记数据
- `data/xhs/jsonl/search_comments_YYYY-MM-DD.jsonl` - 小红书评论数据
- `data/zhihu/jsonl/search_contents_YYYY-MM-DD.jsonl` - 知乎回答数据
- `data/zhihu/jsonl/search_comments_YYYY-MM-DD.jsonl` - 知乎评论数据
- `openclaw_xhs_report.md` - 分析报告

### 🛠️ 相关脚本

| 脚本 | 功能 | 路径 |
|------|------|------|
| `main.py` | 主爬虫程序 | `/workspace/MediaCrawler-main/main.py` |
| `generate_openclaw_report.py` | 报告生成 | `/workspace/MediaCrawler-main/generate_openclaw_report.py` |
| `generate_xhs_images.py` | 配图生成 | `/workspace/MediaCrawler-main/generate_xhs_images.py` |
| `generate_full_docs.py` | 完整文档生成 | `/workspace/MediaCrawler-main/generate_full_docs.py` |

### ⚠️ 注意事项

- ⚠️ **仅供学习研究**，请勿用于商业用途
- ⚠️ **需要扫码登录**，首次运行需手机 APP 扫码
- ⚠️ **控制爬取频率**，避免对平台造成干扰
- ⚠️ **XHS 图片截断**，图片 URL 可能被截断为 `htt`
- ⚠️ **小红书限制**，只能获取 `desc` 字段，完整正文需点击链接查看
- ⚠️ **知乎优势**，可以获取完整回答正文

### 📚 完整文档

详细使用指南：`/home/Matrix/.openclaw/workspace/skills/mediacrawler-search/SKILL.md`

### 🎯 实战案例

**案例 1: OpenClaw 热度分析**
- 爬取 40 篇小红书笔记 + 163 条知乎回答
- 总互动量 152 万次
- 生成分析报告 + 小红书推文

**案例 2: 知识库构建**
- 爬取多平台数据
- 导入飞书知识空间
- 结构化存储原始数据 + 分析报告 + 可视化图表

---

## 📦 Skillhub 技能商店

**安装时间**: 2026-03-14  
**安装源**: 腾讯镜像 `https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com`  
**CLI 路径**: `/home/Matrix/.local/bin/skillhub`  
**Skills 目录**: `/home/Matrix/.openclaw/workspace/skills/`

### 🎯 已安装技能（13 个）

#### 文件管理类
- ✅ **filesystem-1-0-0** - 高级文件系统操作
- ✅ **file-converter** - 文件格式转换（JSON/YAML/CSV/Markdown）
- ✅ **file-sorter** - 智能文件分类

#### 日程日历类
- ✅ **calendar-manager** - 日历管理（创建/读取/提醒）
- ✅ **lunar-calendar** - 中国农历查询（公历/农历转换、黄历、节气）

#### 浏览器自动化
- ✅ **browser-automation-ultra** - 零 token 浏览器自动化

#### 代码分析类
- ✅ **code-project-analyzer** - 项目结构自动分析
- ✅ **code-review-sr** - AI 代码审查

#### 日常助手
- ✅ **briefing** - 每日简报（日历 + 待办 + 天气）

#### Skillhub 工具
- ✅ **find-skills** - 技能搜索
- ✅ **skillhub-preference** - 偏好配置

#### 自定义技能
- ✅ **flux2-image-gen** - Flux.2 图像生成
- ✅ **mediacrawler-search** - 社交媒体爬虫

### 🚀 快速使用

#### 搜索技能
```bash
skillhub search <关键词>
# 示例：skillhub search calendar
```

#### 安装技能
```bash
skillhub install <技能名>
# 示例：skillhub install filesystem-1-0-0
```

#### 查看已安装技能
```bash
ls -la /home/Matrix/.openclaw/workspace/skills/
```

### 📊 技能使用场景

| 需求 | 推荐技能 |
|------|---------|
| 批量文件操作 | `filesystem-1-0-0` |
| 格式转换 | `file-converter` |
| 文件整理 | `file-sorter` |
| 日程管理 | `calendar-manager` |
| 农历查询 | `lunar-calendar` |
| 网页自动化 | `browser-automation-ultra` |
| 项目分析 | `code-project-analyzer` |
| 代码审查 | `code-review-sr` |
| 每日简报 | `briefing` |
| 社交媒体爬取 | `mediacrawler-search` |
| 图像生成 | `flux2-image-gen` |

### 📄 详细文档

完整技能列表和使用指南：`/home/Matrix/.openclaw/workspace/SKILLHUB.md`

---

## 📸 飞书消息发送 (Feishu Message Sending)

### ⚠️ 重要原则
**永远使用机器人身份发送消息！**
- ✅ 使用 `message` 工具（机器人身份）
- ❌ 禁止使用 `feishu_im_user_message` 工具（用户身份）
- 原因：用用户身份发送的消息会显示为用户本人发送，容易造成混淆

### 问题背景
飞书 API 对图片/文件消息发送有限制：
- **私信场景**：机器人可以直接发送图片
- **群聊场景**：机器人无法直接发送图片，需要先上传到云空间再分享链接

### 解决方案

#### 1️⃣ 发送文本消息（机器人身份）
```javascript
// 使用 message 工具（推荐！）
message:
  action: send
  channel: feishu
  to: oc_xxx  # 群聊 ID 或 ou_xxx 用户 ID
  message: "消息内容"
```

#### 2️⃣ 群聊发送图片（上传云空间 + 分享链接）
```javascript
// Step 1: 上传到云空间
feishu_drive_file:
  action: upload
  file_path: /path/to/image.png
// 返回：{"file_name": "xxx.png", "size": 123456}

// Step 2: 获取 doc_token（通过 get_meta 查询）
feishu_drive_file:
  action: get_meta
  request_docs: [{"doc_token": "xxx", "doc_type": "file"}]

// Step 3: 用机器人身份发送包含链接的消息
message:
  action: send
  channel: feishu
  to: oc_xxx
  message: "🔗 图片链接：https://keentropy.feishu.cn/file/{doc_token}"
```

**⚠️ 链接格式重要说明：**
- ✅ 正确格式：`https://keentropy.feishu.cn/file/{doc_token}`
- `doc_token` 是飞书返回的唯一标识符（如 `QjvDb1mERoxzR2xGPiIc3wUPn6c`）
- ❌ **不是文件名！** 不能用 `https://keentropy.feishu.cn/file/文件名.png`
- 需要通过 `feishu_drive_file get_meta` 获取文件的 `doc_token`
- 示例：
  - ✅ `https://keentropy.feishu.cn/file/QjvDb1mERoxzR2xGPiIc3wUPn6c`
  - ❌ `https://keentropy.feishu.cn/file/2026-03-12-18-44-havenmeet-robot.png`

#### 3️⃣ 私信发送图片（机器人身份）
```javascript
// 使用 message 工具发送图片
message:
  action: send
  channel: feishu
  to: ou_xxx
  media: /path/to/image.png
```

### 工作流程
1. **生成/获取文件** → 保存到本地（如 `/tmp/openclaw/`）
2. **判断场景**：
   - **群聊** → 上传云空间 + 发送链接文本
   - **私信** → 直接发送图片/文件
3. **发送消息** → **永远使用 `message` 工具（机器人身份）**

### 注意事项
- ✅ **永远用机器人身份**发送消息（`message` 工具）
- ❌ **禁止用用户身份**发送消息（`feishu_im_user_message` 工具）
- ✅ 云空间上传的文件会自动出现在用户的"我的空间"
- ✅ 链接格式：`https://xxx.feishu.cn/file/xxx`
- ⚠️ 图片需要先移动到 `/tmp/openclaw/` 目录才能被某些工具访问
- ⚠️ 用用户身份发送的消息需要用户手动撤销，会造成困扰

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
