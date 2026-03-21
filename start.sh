#!/bin/bash
# NUPACK Web 启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "=============================================="
echo "   🧬 NUPACK Web"
echo "=============================================="
echo ""
echo "   本地访问: http://127.0.0.1:5000"
echo ""
echo "   按 Ctrl+C 停止服务"
echo "=============================================="
echo ""

python3 app.py
