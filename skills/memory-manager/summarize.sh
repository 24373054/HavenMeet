#!/bin/bash
# Session Summarizer - generates summary of current session for context refresh

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
SUMMARY_FILE="$MEMORY_DIR/episodic/$(date +%Y-%m-%d).md"
STATE_FILE="$MEMORY_DIR/.memory-manager-state.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧠 Session Summarizer${NC}"
echo ""
echo "Generating session summary..."
echo ""

# Get timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Create summary header
echo "" >> "$SUMMARY_FILE"
echo "## Session Summary ($timestamp)" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# This is a placeholder - in production, this would:
# 1. Read recent conversation history from session
# 2. Use AI to generate a concise summary
# 3. Extract key decisions, actions, and context
# 4. Save to episodic memory

echo "**Manual Summary Placeholder**" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "To implement automatic session summarization:" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "1. **Option A**: Use OpenClaw's session_history tool to fetch recent messages" >> "$SUMMARY_FILE"
echo "2. **Option B**: Parse conversation log files if available" >> "$SUMMARY_FILE"
echo "3. **Option C**: Implement in-memory summarization via AI agent" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "**Current Session Context**:" >> "$SUMMARY_FILE"
echo "- Discussing: Context window management and auto-refresh" >> "$SUMMARY_FILE"
echo "- Goal: Prevent unexpected session interruptions" >> "$SUMMARY_FILE"
echo "- Solution: Monitor usage → Auto-summarize at 80% → Refresh session" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# Update state
if command -v jq >/dev/null 2>&1; then
    jq --arg ts "$timestamp" '.last_summary = $ts' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

echo -e "${GREEN}✓ Summary saved to:${NC} $SUMMARY_FILE"
echo ""
echo "Next steps:"
echo "  1. Review the summary above"
echo "  2. Use /new to start fresh session"
echo "  3. Agent will load summary from MEMORY.md on startup"
echo ""
echo "Tip: Add this to HEARTBEAT.md for automatic monitoring:"
echo "  - Every 10 messages: Run context-monitor.sh"
echo "  - If usage > 80%: Generate summary and suggest refresh"
