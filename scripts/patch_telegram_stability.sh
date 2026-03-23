#!/usr/bin/env bash
# patch_telegram_stability.sh
#
# Telegram MCP 플러그인 안정성 패치
# - bot.start() Promise 추적 → 폴링 크래시 시 프로세스 종료
# - bot.catch() 글로벌 에러 핸들러 추가
# - MCP transport 끊김 감지 → 깨끗한 종료
#
# 사용법: bash scripts/patch_telegram_stability.sh
# 플러그인 업데이트 후 재적용 필요

set -euo pipefail

PLUGIN_DIR="$HOME/.claude/plugins/cache/claude-plugins-official/telegram"
SERVER_FILE=""

# Find the latest version of the plugin
if [ -d "$PLUGIN_DIR" ]; then
  LATEST_VER=$(ls -1 "$PLUGIN_DIR" | sort -V | tail -1)
  SERVER_FILE="$PLUGIN_DIR/$LATEST_VER/server.ts"
fi

if [ -z "$SERVER_FILE" ] || [ ! -f "$SERVER_FILE" ]; then
  echo "❌ Telegram 플러그인을 찾을 수 없습니다."
  echo "   먼저 플러그인을 설치하세요:"
  echo "   /plugin install telegram@claude-plugins-official"
  exit 1
fi

echo "📍 패치 대상: $SERVER_FILE"

# Check if already patched
if grep -q '\[STABILITY PATCH\]' "$SERVER_FILE"; then
  echo "✅ 이미 패치가 적용되어 있습니다."
  exit 0
fi

# Backup original
cp "$SERVER_FILE" "$SERVER_FILE.bak"
echo "💾 백업 생성: $SERVER_FILE.bak"

# Apply patch using Python for reliable multi-line replacement
python3 -c "
import sys

with open('$SERVER_FILE', 'r') as f:
    content = f.read()

# Patch 1: Replace StdioServerTransport inline → variable + onclose + bot.catch
old1 = 'await mcp.connect(new StdioServerTransport())'
new1 = '''const transport = new StdioServerTransport()
await mcp.connect(transport)

// [STABILITY PATCH] Detect MCP disconnection → clean shutdown
transport.onclose = () => {
  process.stderr.write('telegram channel: MCP transport closed, shutting down\\\n')
  bot.stop()
  process.exit(0)
}

// [STABILITY PATCH] Global error handler for grammy
bot.catch(err => {
  process.stderr.write(\`telegram channel: bot error: \${err.message ?? err}\\\n\`)
})'''

if old1 not in content:
    print('⚠️  Patch 1 대상을 찾을 수 없습니다 (이미 적용되었거나 플러그인 구조 변경)')
    sys.exit(1)

content = content.replace(old1, new1)

# Patch 2: Replace void bot.start → bot.start().catch()
old2 = '''void bot.start({
  onStart: info => {
    botUsername = info.username
    process.stderr.write(\`telegram channel: polling as @\${info.username}\\\n\`)
  },
})'''

new2 = '''bot.start({
  onStart: info => {
    botUsername = info.username
    process.stderr.write(\`telegram channel: polling as @\${info.username}\\\n\`)
  },
}).catch(err => {
  // [STABILITY PATCH] Crash on polling failure instead of zombie state
  process.stderr.write(\`telegram channel: polling crashed: \${err.message ?? err}\\\n\`)
  process.exit(1)
})'''

if old2 not in content:
    print('⚠️  Patch 2 대상을 찾을 수 없습니다 (이미 적용되었거나 플러그인 구조 변경)')
    sys.exit(1)

content = content.replace(old2, new2)

with open('$SERVER_FILE', 'w') as f:
    f.write(content)

print('✅ Python 패치 적용 완료')
"

# Verify patch
if grep -q '\[STABILITY PATCH\]' "$SERVER_FILE" && grep -q 'transport.onclose' "$SERVER_FILE" && grep -q 'polling crashed' "$SERVER_FILE"; then
  echo "✅ 패치 적용 완료!"
  echo ""
  echo "변경사항:"
  echo "  1. bot.catch() — grammy 에러 로깅"
  echo "  2. bot.start().catch() — 폴링 크래시 시 프로세스 종료"
  echo "  3. transport.onclose — MCP 연결 끊김 시 깨끗한 종료"
  echo ""
  echo "⚠️  플러그인 업데이트 후 이 스크립트를 다시 실행하세요."
else
  echo "❌ 패치 적용 실패. 백업에서 복원합니다."
  cp "$SERVER_FILE.bak" "$SERVER_FILE"
  exit 1
fi
