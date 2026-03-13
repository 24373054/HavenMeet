# 🧠 记忆管理系统

**目标**: 永远不需要手动 reset，自动管理长期记忆。

---

## 🏗️ 架构

```
会话中 (Hot)
    ↓
每日记忆 (Warm) - memory/YYYY-MM-DD.md
    ↓
长期记忆 (Cold) - MEMORY.md
    ↓
语义记忆 (Knowledge) - memory/semantic/
    ↓
程序记忆 (How-to) - memory/procedural/
    ↓
快照备份 (Archive) - memory/snapshots/
```

---

## 🔄 自动化流程

### 1. 会话开始时
```bash
# 自动运行（已在 HEARTBEAT.md 配置）
scripts/memory-auto-check.sh
```

**检查项**:
- ✅ MEMORY.md 大小（超过 50KB 自动快照）
- ✅ 今日记忆文件是否存在
- ✅ 语义记忆是否完整

### 2. 会话进行中
- **自动记录**: 重要决策、关键信息写入 `memory/YYYY-MM-DD.md`
- **实时同步**: 定期将重要信息迁移到 `MEMORY.md`
- **分类存储**: 
  - 事实知识 → `memory/semantic/`
  - 工作流程 → `memory/procedural/`

### 3. 会话结束时
```bash
# 自动运行
scripts/memory-save-session.sh <session_id>
```

**操作**:
- ✅ 保存会话摘要
- ✅ 检查 MEMORY.md 大小
- ✅ 必要时创建快照
- ✅ 更新今日记忆

### 4. 每小时（Cron 任务）
```bash
# 自动运行（已配置 cron）
skills/memory-manager/organize.sh
```

**操作**:
- ✅ 整理记忆文件
- ✅ 更新语义索引
- ✅ 清理过期快照

---

## 📁 文件结构

```
memory/
├── MEMORY.md                    # 长期记忆（核心）
├── 2026-03-14.md              # 今日记忆
├── episodic/                   # 事件日志
│   ├── 2026-03-14.md
│   └── ...
├── semantic/                   # 知识沉淀
│   ├── 用户偏好.md
│   ├── 项目信息.md
│   └── ...
├── procedural/                 # 工作流程
│   ├── 记忆管理.md
│   ├── 浏览器自动化.md
│   └── ...
├── sessions/                   # 会话快照
│   ├── session_xxx_20260314_010200.md
│   └── ...
└── snapshots/                  # MEMORY.md 快照
    ├── MEMORY_20260314_010000.md
    └── ...
```

---

## 🚨 自动保护机制

### 1. 大小限制
- **MEMORY.md > 50KB** → 自动创建快照
- **MEMORY.md > 100KB** → 自动压缩并整理
- **会话长度 > 80%** → 提前保存上下文

### 2. 定期备份
- **每小时** → 检查并整理
- **每天 23:00** → 归档当日记忆
- **每周日** → 清理过期快照

### 3. 智能检索
```bash
# 搜索记忆
skills/memory-manager/search.sh <关键词>

# 查看统计
skills/memory-manager/stats.sh
```

---

## 💡 使用指南

### 记住重要信息
```bash
# 手动添加
echo "- 重要信息" >> memory/2026-03-14.md

# 或写入语义记忆
echo "## 新知识" >> memory/semantic/主题.md
```

### 查找历史记忆
```bash
# 搜索
grep -r "关键词" memory/

# 查看今日
cat memory/2026-03-14.md

# 查看长期记忆
cat memory/MEMORY.md
```

### 清理旧数据
```bash
# 清理 30 天前的快照
find memory/snapshots/ -name "*.md" -mtime +30 -delete
```

---

## 🎯 目标

**零手动干预**:
- ✅ 不需要手动 reset
- ✅ 不需要手动整理
- ✅ 不需要担心丢失
- ✅ 自动备份和恢复

**智能管理**:
- ✅ 自动检测压缩风险
- ✅ 自动创建快照
- ✅ 自动整理记忆
- ✅ 自动检索信息

---

**最后更新**: 2026-03-14 01:02
