# 小红书私信功能调研报告

## 调研时间
2026-03-14

## 目标
实现自动化发送私信给用户 `9647151616`

## 已尝试方案

### 1. 网页版 Playwright 自动化
**结果**: ❌ 受限

**发现**:
- 小红书网页版消息页面存在（`/message`, `/inbox` 等）
- 但页面内容很少（截图仅 49KB，说明几乎是空白页）
- 没有找到明显的私信发送入口
- 网页版可能不支持私信功能或需要额外权限

**截图**:
- `step1_message_page.png` (49KB) - 几乎空白
- `search_user_page.png` (1.8MB) - 搜索结果正常

### 2. 直接 API 访问
**结果**: ❌ 未找到公开 API

**发现**:
- `developer.xiaohongshu.com` - 无法访问
- `open.xiaohongshu.com` - 可访问，但未找到私信相关 API
- GitHub 搜索 "xiaohongshu bot" 找到少量项目，但大多是爬虫而非私信

### 3. URL 直接访问
**结果**: ⚠️ 部分有效

**测试的 URL**:
- `https://www.xiaohongshu.com/user/inbox` - 可访问但内容少
- `https://www.xiaohongshu.com/message/list` - 可访问但内容少
- `https://www.xiaohongshu.com/msg` - 可访问但内容少

## 推荐方案

### 方案 A: Airtest 手机 App 自动化 ⭐⭐⭐⭐⭐
**优点**:
- 小红书 App 功能完整
- Airtest 支持 Android/iOS 自动化
- 可以模拟真实用户操作
- 社区活跃，有现成示例

**实施步骤**:
1. 安装 Airtest: `pip install airtest`
2. 连接 Android 模拟器或真机
3. 编写脚本模拟点击和输入
4. 自动化发送私信

**示例代码**:
```python
from airtest.core.api import *

# 启动 App
start_app("com.xiaohongshu")

# 搜索用户
touch(TEXT("搜索"))
text("9647151616")

# 点击用户
touch(TEXT("9647151616"))

# 点击私信
touch(TEXT("私信"))

# 输入消息
text("你好")

# 发送
touch(TEXT("发送"))
```

### 方案 B: 逆向工程 App HTTP 请求 ⭐⭐⭐⭐
**优点**:
- 直接调用 API，效率高
- 可以批量发送

**缺点**:
- 需要逆向工程技能
- 可能有法律风险
- API 可能随时变化

**工具**:
- Charles / Fiddler - 抓包
- Burp Suite - 分析请求
- Python requests - 重放请求

### 方案 C: 第三方服务 ⭐⭐⭐
**搜索关键词**:
- "小红书私信 API"
- "小红书营销工具"
- "小红书代运营"

**注意**: 需要谨慎选择，避免账号被封

### 方案 D: 浏览器扩展 ⭐⭐⭐
**思路**:
- 开发 Chrome 扩展
- 注入 JavaScript 到小红书网页
- 自动填写和提交表单

**前提**: 网页版需要支持私信功能

## 结论

**推荐优先尝试**: Airtest 手机 App 自动化

**理由**:
1. 技术可行，社区支持好
2. 模拟真实用户，风险较低
3. 功能完整，不受网页版限制
4. 可以复用到其他 App 自动化场景

## 下一步

1. **安装 Airtest**: `pip install airtest`
2. **准备 Android 环境**: 使用 Android 模拟器或真机
3. **编写测试脚本**: 先手动操作录制，再优化
4. **测试发送**: 给自己或小范围测试
5. **优化脚本**: 添加异常处理和日志

## 参考资料

- Airtest 官方文档：https://airtest.netease.com/
- Airtest GitHub: https://github.com/AirtestProject/Airtest
- 小红书 App 包名：`com.xiaohongshu` (Android)

---
生成时间：2026-03-14 03:25
