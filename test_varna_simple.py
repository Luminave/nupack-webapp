#!/usr/bin/env python3
"""
VARNA 简单测试脚本
测试varnaapi是否正确安装
"""

import os
import sys

print("=" * 60)
print("  VARNA 集成环境检查")
print("=" * 60)
print()

# 1. 检查varnaapi
print("1️⃣  检查 varnaapi...")
try:
    import varnaapi
    print("   ✅ varnaapi 已安装")
    print(f"   版本: {varnaapi.__version__ if hasattr(varnaapi, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"   ❌ varnaapi 未安装: {e}")
    print("   请运行: pip install varnaapi --break-system-packages")
    sys.exit(1)

print()

# 2. 检查VARNA jar
print("2️⃣  检查 VARNA jar文件...")
script_dir = os.path.dirname(__file__)
jar_path = os.path.join(script_dir, 'lib', 'VARNAv3-93.jar')

if os.path.exists(jar_path):
    size_mb = os.path.getsize(jar_path) / (1024 * 1024)
    print(f"   ✅ VARNA jar 已存在")
    print(f"   路径: {jar_path}")
    print(f"   大小: {size_mb:.2f} MB")
else:
    print(f"   ❌ VARNA jar 未找到: {jar_path}")
    print("   请将 VARNAv3-93.jar 复制到 lib/ 目录")
    sys.exit(1)

print()

# 3. 检查numpy
print("3️⃣  检查 numpy...")
try:
    import numpy as np
    print("   ✅ numpy 已安装")
except ImportError:
    print("   ❌ numpy 未安装")
    print("   请运行: pip install numpy --break-system-packages")
    sys.exit(1)

print()

# 4. 配置varnaapi
print("4️⃣  配置 varnaapi...")
try:
    varnaapi.set_VARNA(jar_path)
    print("   ✅ varnaapi 配置成功")
except Exception as e:
    print(f"   ❌ varnaapi 配置失败: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("  ✅ 所有检查通过！VARNA 集成准备就绪")
print("=" * 60)
print()
print("下一步:")
print("  1. 将 varna_api.py 中的代码添加到 app.py")
print("  2. 在前端添加 VARNA 渲染选项")
print("  3. 重启 Flask 应用")
print()
print("注意: 需要安装 Java 运行环境才能生成 SVG")
print("  Ubuntu/Debian: sudo apt install openjdk-11-jre")
print()
