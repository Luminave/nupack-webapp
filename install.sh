#!/bin/bash
# NUPACK Web 安装脚本
# 作者: Victor.Guo

set -e

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
    echo "    1. 访问 https://www.nupack.org/ 注册账号"
    echo "    2. 下载对应版本的安装包"
    echo "    3. 运行: pip install nupack-4.0.x.x-py3-none-any.whl"
    echo ""
    exit 1
fi

# 创建虚拟环境
echo ""
echo ">>> 创建 Python 虚拟环境..."
if [ -d "venv" ]; then
    echo "    虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    echo "    ✅ 虚拟环境创建完成"
fi

# 激活虚拟环境并安装依赖
echo ""
echo ">>> 安装 Python 依赖..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "    ✅ 依赖安装完成"

# 创建项目目录
echo ""
echo ">>> 创建项目目录..."
mkdir -p ~/nupack-projects
echo "    ✅ 项目目录已创建: ~/nupack-projects"

# 设置权限
chmod +x start.sh 2>/dev/null || true

echo ""
echo "=============================================="
echo "   ✅ 安装完成！"
echo "=============================================="
echo ""
echo "启动方式:"
echo "    cd $(pwd)"
echo "    source venv/bin/activate"
echo "    python3 app.py"
echo ""
echo "或者使用启动脚本:"
echo "    ./start.sh"
echo ""
echo "然后在浏览器中打开: http://127.0.0.1:5000"
echo ""
