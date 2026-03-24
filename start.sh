#!/bin/bash
# NUPACK Web 快捷启动脚本
# 双击此文件即可自动启动并打开浏览器

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "   🧬 NUPACK Web v1.3.0"
echo "=============================================="
echo ""

# 检查端口是否被占用
if lsof -i:5000 >/dev/null 2>&1; then
    echo "⚠️  端口 5000 已被占用"
    echo "   正在尝试停止旧进程..."
    pkill -f "python.*app.py" 2>/dev/null
    sleep 1
fi

# 检查 NUPACK
if ! python3 -c "from nupack import *" 2>/dev/null; then
    echo "❌ NUPACK 未安装或未激活许可证"
    echo ""
    echo "请先安装 NUPACK:"
    echo "  1. pip install nupack --break-system-packages"
    echo "  2. nupack-license --user 'your_email' --key 'your_key'"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

# 启动 Flask 应用
echo ">>> 启动服务器..."
python3 app.py &
FLASK_PID=$!

# 等待应用启动
sleep 2

# 检查是否启动成功
if ! ps -p $FLASK_PID > /dev/null 2>&1; then
    echo "❌ 启动失败，请检查错误信息"
    read -p "按回车键退出..."
    exit 1
fi

# 自动打开浏览器
echo ">>> 打开浏览器..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://127.0.0.1:5000 2>/dev/null
elif command -v gnome-open &> /dev/null; then
    gnome-open http://127.0.0.1:5000 2>/dev/null
elif command -v open &> /dev/null; then
    open http://127.0.0.1:5000 2>/dev/null
else
    echo ""
    echo "请手动打开浏览器访问: http://127.0.0.1:5000"
fi

echo ""
echo "=============================================="
echo "   ✅ 服务已启动"
echo "=============================================="
echo ""
echo "📍 访问地址: http://127.0.0.1:5000"
echo "🛑 停止服务: 在此终端按 Ctrl+C"
echo "🎨 VARNA: 点击橙红色按钮下载高质量结构图"
echo ""
echo "提示: 关闭此终端窗口将停止服务"
echo ""

# 等待用户按 Ctrl+C
wait $FLASK_PID
