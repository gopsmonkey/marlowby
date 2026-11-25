#!/bin/sh
# Re-render the product photos after changing a box, a plan size or the route.
#   one-time:  npm --prefix tools/render install
#   then:      sh tools/render-shots.sh
set -e
cd "$(dirname "$0")/.."
MARLOWBY_LIVE_SHOTS=1 python3 tools/build.py . > /dev/null   # pages that draw shots live
python3 -m http.server 8799 > /dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null' EXIT
sleep 1
node tools/render/render-shots.mjs http://127.0.0.1:8799/
python3 tools/build.py .                                       # pages that use the saved files
