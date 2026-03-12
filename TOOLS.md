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

## 📸 飞书图片发送 (Feishu Image Sharing)

### 问题背景
飞书 API 对图片消息发送有限制：
- **私信场景**：可以直接发送图片（使用 `feishu_im_user_message` + `image` 类型）
- **群聊场景**：无法直接发送图片，需要先上传到云空间再分享链接

### 解决方案

#### 1️⃣ 私信发送图片（直接发送）
```javascript
// 使用 feishu_im_user_message 工具
action: send
msg_type: image
receive_id_type: open_id
receive_id: ou_xxx
content: {"image_key": "img_xxx"}
```

#### 2️⃣ 群聊发送图片（上传云空间 + 分享链接）
```javascript
// Step 1: 上传到云空间
feishu_drive_file:
  action: upload
  file_path: /path/to/image.png

// Step 2: 发送文本消息包含链接
feishu_im_user_message:
  action: send
  msg_type: text
  receive_id_type: chat_id
  receive_id: oc_xxx
  content: {"text": "图片已上传到云空间，链接：https://xxx.feishu.cn/file/xxx"}
```

### 工作流程
1. **生成/获取图片** → 保存到本地（如 `/tmp/openclaw/`）
2. **判断场景**：
   - 如果是**私信** → 直接用 `feishu_im_user_message` 发送图片
   - 如果是**群聊** → 先上传云空间，再发送链接文本
3. **上传云空间** → 使用 `feishu_drive_file` 工具
4. **发送消息** → 包含云空间链接的文本消息

### 注意事项
- ✅ 云空间上传的文件会自动出现在用户的"我的空间"
- ✅ 链接格式：`https://xxx.feishu.cn/file/xxx`
- ❌ 群聊中不能直接发送本地图片文件
- ⚠️ 图片需要先移动到 `/tmp/openclaw/` 目录才能被某些工具访问

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
