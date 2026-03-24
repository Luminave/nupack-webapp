#!/bin/bash
# NUPACK Web 安装脚本
# 作者: Victor.Guo
# 版本: v1.4.0

echo "=============================================="
echo "   NUPACK Web 安装程序 v1.3.0"
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
    echo "    2. 运行: pip install nupack --break-system-packages"
    echo "    3. 激活许可证: nupack-license --user 'your_email' --key 'your_key'"
    echo ""
    exit 1
fi

# 检查 Java 是否已安装（VARNA需要）
echo ""
echo ">>> 检查 Java 运行环境..."
if java -version 2>&1 | grep -q "version"; then
    JAVA_VERSION=$(java -version 2>&1 | head -1 | awk -F '"' '{print $2}')
    echo "    ✅ Java 已安装 (版本: $JAVA_VERSION)"
else
    echo "    ⚠️  Java 未安装，正在安装 OpenJDK..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y openjdk-11-jre-headless
        echo "    ✅ OpenJDK 11 已安装"
    elif command -v yum &> /dev/null; then
        sudo yum install -y java-11-openjdk-headless
        echo "    ✅ OpenJDK 11 已安装"
    else
        echo "    ❌ 无法自动安装 Java，请手动安装 Java Runtime Environment"
        echo "    VARNA 功能将无法使用"
    fi
fi

# 安装 Python 依赖
echo ""
echo ">>> 安装 Python 依赖..."
pip install -r requirements.txt --break-system-packages -q
echo "    ✅ 依赖安装完成"

# 创建 lib 目录并下载 VARNA jar
echo ""
echo ">>> 检查 VARNA..."
mkdir -p lib
VARNA_JAR="lib/VARNAv3-93.jar"

if [ -f "$VARNA_JAR" ]; then
    echo "    ✅ VARNA 已存在"
else
    echo "    正在下载 VARNA..."
    if wget -q "http://varna.lri.fr/bin/VARNAv3-93.jar" -O "$VARNA_JAR"; then
        echo "    ✅ VARNA 下载完成"
    else
        echo "    ⚠️  VARNA 自动下载失败"
        echo "    请手动下载："
        echo "    http://varna.lri.fr/bin/VARNAv3-93.jar"
        echo "    并放置到 lib/ 目录下"
    fi
fi

# 创建项目目录
echo ""
echo ">>> 创建项目目录..."
mkdir -p ~/nupack-projects
echo "    ✅ 项目目录已创建: ~/nupack-projects"

# 创建桌面启动脚本
echo ""
echo ">>> 创建桌面启动脚本..."

# 获取项目绝对路径
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_DIR="$HOME/Desktop"

# 创建桌面启动脚本
if [ -d "$DESKTOP_DIR" ]; then
    cat > "$DESKTOP_DIR/NUPACK-Web.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=NUPACK Web
Comment=Nucleic Acid Structure Analysis Tool
Exec=bash -c "cd '$PROJECT_DIR' && python3 app.py & sleep 2 && xdg-open http://127.0.0.1:5000"
Icon=$PROJECT_DIR/static/icon.png
Terminal=true
Categories=Science;Biology;
StartupNotify=true
EOF
    
    # 设置可执行权限
    chmod +x "$DESKTOP_DIR/NUPACK-Web.desktop"
    
    # Ubuntu 需要允许桌面图标
    if command -v gio &> /dev/null; then
        gio set "$DESKTOP_DIR/NUPACK-Web.desktop" metadata::trusted true 2>/dev/null
    fi
    
    echo "    ✅ 桌面启动脚本已创建"
    echo "    📍 位置: $DESKTOP_DIR/NUPACK-Web.desktop"
else
    echo "    ⚠️  桌面目录不存在，跳过创建桌面启动脚本"
fi

# 创建快捷启动脚本
cat > "$PROJECT_DIR/start.sh" << 'EOFSTART'
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
EOFSTART

chmod +x "$PROJECT_DIR/start.sh"
echo "    ✅ 启动脚本已更新: start.sh"

echo ""
echo "=============================================="
echo "   ✅ 安装完成！"
echo "=============================================="
echo ""
echo "启动方式："
echo ""
echo "  方法1：双击桌面图标"
echo "    NUPACK-Web"
echo ""
echo "  方法2：运行启动脚本"
echo "    ./start.sh"
echo ""
echo "  方法3：直接运行"
echo "    python3 app.py"
echo "    然后打开浏览器: http://127.0.0.1:5000"
echo ""
echo "🎨 VARNA 功能："
echo "  支持高质量的 RNA/DNA 二级结构可视化"
echo "  点击 VARNA 按钮即可下载 SVG 图片"
echo ""
echo "📚 文档："
echo "  README.md - 使用说明"
echo "  https://docs.nupack.org/"
echo ""
