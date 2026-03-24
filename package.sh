#!/bin/bash
# NUPACK Web 打包脚本
# 将项目打包为可分发的压缩包

VERSION="1.4.0"
PACKAGE_NAME="nupack-webapp-v${VERSION}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_NAME="$(basename "$SCRIPT_DIR")"

echo "=============================================="
echo "   NUPACK Web 打包工具"
echo "=============================================="
echo ""
echo "版本: v${VERSION}"
echo "项目目录: ${SCRIPT_DIR}"
echo "输出文件: ${PARENT_DIR}/${PACKAGE_NAME}.tar.gz"
echo ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo ">>> 创建临时目录: $TEMP_DIR"

# 复制项目文件（排除不必要的文件）
echo ">>> 复制项目文件..."
rsync -a \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.log' \
    --exclude='.DS_Store' \
    --exclude='*.swp' \
    --exclude='*.swo' \
    --exclude='test_*.py' \
    --exclude='test_*.html' \
    --exclude='VARNA_INTEGRATION_*.md' \
    --exclude='VARNA_QUICKSTART.md' \
    --exclude='varna_api.py' \
    "${SCRIPT_DIR}/" "${TEMP_DIR}/${PACKAGE_NAME}/"

# 删除临时测试文件
echo ">>> 清理测试文件..."
rm -f "${TEMP_DIR}/${PACKAGE_NAME}/test_"* 2>/dev/null
rm -f "${TEMP_DIR}/${PACKAGE_NAME}/VARNA_INTEGRATION_"* 2>/dev/null
rm -f "${TEMP_DIR}/${PACKAGE_NAME}/VARNA_QUICKSTART.md" 2>/dev/null
rm -f "${TEMP_DIR}/${PACKAGE_NAME}/varna_api.py" 2>/dev/null

# 切换到输出目录
cd "$PARENT_DIR"

# 创建压缩包
echo ">>> 创建压缩包..."
tar -czf "${PACKAGE_NAME}.tar.gz" -C "${TEMP_DIR}" "${PACKAGE_NAME}"

# 计算文件大小
PACKAGE_SIZE=$(du -h "${PACKAGE_NAME}.tar.gz" | awk '{print $1}')

# 清理临时目录
echo ">>> 清理临时文件..."
rm -rf "${TEMP_DIR}"

echo ""
echo "=============================================="
echo "   ✅ 打包完成！"
echo "=============================================="
echo ""
echo "📦 文件名: ${PACKAGE_NAME}.tar.gz"
echo "📊 大小: ${PACKAGE_SIZE}"
echo "📍 位置: ${PARENT_DIR}/${PACKAGE_NAME}.tar.gz"
echo ""
echo "使用方法："
echo "  tar -xzf ${PACKAGE_NAME}.tar.gz"
echo "  cd ${PACKAGE_NAME}"
echo "  ./install.sh"
echo ""
