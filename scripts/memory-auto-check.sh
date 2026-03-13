#!/bin/bash
# 自动记忆管理脚本 - 在会话开始时自动运行

MEMORY_DIR="/home/Matrix/.openclaw/workspace/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🧠 自动记忆管理启动..."

# 1. 检查是否需要压缩
if [ -f "$MEMORY_DIR/MEMORY.md" ]; then
    SIZE=$(wc -c < "$MEMORY_DIR/MEMORY.md")
    echo "📊 MEMORY.md 大小：$SIZE 字节"
    
    # 如果超过 50KB，自动创建快照
    if [ $SIZE -gt 51200 ]; then
        echo "⚠️  检测到 MEMORY.md 超过 50KB，创建快照..."
        cp "$MEMORY_DIR/MEMORY.md" "$SNAPSHOT_DIR/MEMORY_snapshot_$TIMESTAMP.md"
        echo "✅ 快照已保存：MEMORY_snapshot_$TIMESTAMP.md"
    fi
fi

# 2. 检查每日记忆文件
TODAY=$(date +%Y-%m-%d)
DAILY_FILE="$MEMORY_DIR/$TODAY.md"

if [ ! -f "$DAILY_FILE" ]; then
    echo "📝 创建今日记忆文件：$DAILY_FILE"
    echo "# $TODAY" > "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"
    echo "## 事件记录" >> "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"
fi

# 3. 检查会话历史
if [ -d "$MEMORY_DIR/sessions" ]; then
    SESSION_COUNT=$(ls -1 "$MEMORY_DIR/sessions" 2>/dev/null | wc -l)
    echo "📁 已保存 $SESSION_COUNT 个会话快照"
fi

# 4. 检查语义记忆
if [ -d "$MEMORY_DIR/semantic" ]; then
    SEMANTIC_COUNT=$(ls -1 "$MEMORY_DIR/semantic" 2>/dev/null | wc -l)
    echo "🧠 语义记忆条目：$SEMANTIC_COUNT"
fi

# 5. 检查程序记忆
if [ -d "$MEMORY_DIR/procedural" ]; then
    PROCEDURAL_COUNT=$(ls -1 "$MEMORY_DIR/procedural" 2>/dev/null | wc -l)
    echo "📖 程序记忆条目：$PROCEDURAL_COUNT"
fi

echo "✅ 记忆管理检查完成！"
echo ""
echo "💡 提示："
echo "  - 重要信息会自动保存到 MEMORY.md"
echo "  - 每日事件记录在 memory/YYYY-MM-DD.md"
echo "  - 知识沉淀在 memory/semantic/"
echo "  - 工作流程记录在 memory/procedural/"
