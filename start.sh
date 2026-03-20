#!/bin/bash
# NUPACK Web 启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

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
