# MediaCrawler Search Skill

这是一个包装 MediaCrawler 的 OpenClaw Skill，用于快速进行多平台网络搜索。

## 快速开始

### 1. 安装依赖

```bash
cd /home/Matrix/.openclaw/workspace/MediaCrawler-main
pip3 install playwright
playwright install
```

### 2. 使用脚本搜索

```bash
# 搜索小红书
python3 /home/Matrix/.openclaw/workspace/skills/mediacrawler-search/search.py \
  --platform xhs \
  --keywords "编程副业，编程兼职"

# 搜索抖音
python3 /home/Matrix/.openclaw/workspace/skills/mediacrawler-search/search.py \
  --platform dy \
  --keywords "AI 教程"

# 搜索 B 站
python3 /home/Matrix/.openclaw/workspace/skills/mediacrawler-search/search.py \
  --platform bili \
  --keywords "Python 编程"
```

### 3. 查看结果

结果保存在 `/home/Matrix/.openclaw/workspace/MediaCrawler-main/data/` 目录下

## 平台列表

| 平台 | 代码 | 说明 |
|------|------|------|
| 小红书 | xhs | 生活方式分享平台 |
| 抖音 | dy | 短视频平台 |
| 快手 | ks | 短视频平台 |
| B 站 | bili | 视频社区 |
| 微博 | wb | 社交媒体 |
| 贴吧 | tieba | 论坛社区 |
| 知乎 | zhihu | 问答社区 |

## 注意事项

⚠️ **重要提醒：**
- 仅供学习研究，请勿用于商业用途
- 遵守目标平台的使用条款和 robots.txt
- 控制爬取频率，避免对平台造成干扰
- 首次运行需要扫码登录

## 在 OpenClaw 中使用

当需要搜索网络信息时，可以调用这个 Skill：

```
搜索小红书上的"AI 绘画教程"相关内容
```

我会自动调用 MediaCrawler 进行爬取，然后返回搜索结果。
