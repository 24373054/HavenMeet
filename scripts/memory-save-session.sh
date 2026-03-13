#!/bin/bash
# 会话结束时自动保存记忆

MEMORY_DIR="/home/Matrix/.openclaw/workspace/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_ID="$1"  # 传入会话 ID

echo "💾 保存会话记忆..."

# 1. 保存当前会话的摘要
if [ -n "$SESSION_ID" ]; then
    SESSION_FILE="$MEMORY_DIR/sessions/session_${SESSION_ID}_${TIMESTAMP}.md"
    echo "# 会话 $SESSION_ID - $(date +%Y-%m-%d\ %H:%M)" > "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"
    echo "## 会话摘要" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"
    echo "（此处应包含会话的关键信息摘要）" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"
    echo "## 重要决策" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"
    echo "- （记录会话中的重要决策）" >> "$SESSION_FILE"
    
    echo "✅ 会话已保存：$SESSION_FILE"
fi

# 2. 检查 MEMORY.md 大小
if [ -f "$MEMORY_DIR/MEMORY.md" ]; then
    SIZE=$(wc -c < "$MEMORY_DIR/MEMORY.md")
    
    if [ $SIZE -gt 51200 ]; then
        echo "⚠️  MEMORY.md 超过 50KB ($SIZE 字节)"
        echo "📦 创建快照..."
        
        # 创建快照
        cp "$MEMORY_DIR/MEMORY.md" "$SNAPSHOT_DIR/MEMORY_$TIMESTAMP.md"
        
        # 清理旧快照（保留最近 10 个）
        cd "$SNAPSHOT_DIR"
        ls -1t MEMORY_*.md 2>/dev/null | tail -n +11 | xargs -r rm
        
        echo "✅ 快照已保存，旧快照已清理"
    fi
fi

# 3. 更新今日记忆
TODAY=$(date +%Y-%m-%d)
DAILY_FILE="$MEMORY_DIR/$TODAY.md"

if [ -f "$DAILY_FILE" ]; then
    echo "" >> "$DAILY_FILE"
    echo "## $(date +%H:%M) - 会话结束" >> "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"
    echo "- 会话 ID: $SESSION_ID" >> "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"
fi

echo "✅ 记忆保存完成！"
