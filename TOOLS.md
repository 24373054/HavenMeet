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
