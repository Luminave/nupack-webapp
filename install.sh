#!/bin/bash
# NUPACK Web 安装脚本
# 作者: Victor.Guo

echo "=============================================="
echo "   NUPACK Web 安装程序"
echo "=============================================="
echo ""

# 检查 Python 版本
echo ">>> 检查 Python 版本..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "    Python 版本: $PYTHON_VERSION"

# 检查 NUPACK 是否已安装
echo ""
echo ">>> 检查 NUPACK 是否已安装..."
if python3 -c "from nupack import *; print('NUPACK 版本:', __import__('nupack').__version__)" 2>/dev/null; then
    echo "    ✅ NUPACK 已安装"
else
    echo "    ❌ NUPACK 未安装！"
    echo ""
    echo "请先安装 NUPACK:"
    echo "    1. 访问 https://www.nupack.org/ 注册账号并获取许可证"
    echo "    2. 运行: pip install nupack"
    echo "    3. 激活许可证: nupack-license --user 'your_email' --key 'your_key'"
    echo ""
    exit 1
fi

# 安装 Python 依赖
echo ""
echo ">>> 安装 Python 依赖..."
pip install -r requirements.txt -q
echo "    ✅ 依赖安装完成"

# 创建项目目录
echo ""
echo ">>> 创建项目目录..."
mkdir -p ~/nupack-projects
echo "    ✅ 项目目录已创建: ~/nupack-projects"

echo ""
echo "=============================================="
echo "   ✅ 安装完成！"
echo "=============================================="
echo ""
echo "启动方式:"
echo "    ./start.sh"
echo ""
echo "    或直接运行:"
echo "    python3 app.py"
echo ""
echo "然后在浏览器中打开: http://127.0.0.1:5000"
echo ""
