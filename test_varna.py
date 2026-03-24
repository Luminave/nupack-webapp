#!/usr/bin/env python3
"""
VARNA集成测试脚本
测试VARNA是否正确安装并可以生成SVG
"""

import os
import sys

def check_java():
    """检查Java环境"""
    import subprocess
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Java已安装")
            print(f"   版本: {result.stderr.split()[2] if result.stderr else 'Unknown'}")
            return True
        return False
    except FileNotFoundError:
        print("❌ Java未安装")
        print("   请运行: sudo apt install openjdk-11-jre")
        return False
    except Exception as e:
        print(f"❌ Java检查失败: {e}")
        return False


def check_varna_jar():
    """检查VARNA jar文件"""
    script_dir = os.path.dirname(__file__)
    jar_path = os.path.join(script_dir, 'lib', 'VARNAv3-93.jar')
    
    if os.path.exists(jar_path):
        size_mb = os.path.getsize(jar_path) / (1024 * 1024)
        print(f"✅ VARNA jar已存在: {jar_path}")
        print(f"   大小: {size_mb:.2f} MB")
        return jar_path
    else:
        print(f"❌ VARNA jar未找到: {jar_path}")
        print("   请下载:")
        print("   mkdir -p lib && cd lib")
        print("   wget https://varna.lri.fr/bin/VARNAv3-93.jar")
        return None


def check_varnaapi():
    """检查varnaapi库"""
    try:
        import varnaapi
        print(f"✅ varnaapi已安装")
        return True
    except ImportError:
        print("❌ varnaapi未安装")
        print("   请运行: pip install varnaapi")
        return False


def test_varna_rendering(jar_path):
    """测试VARNA渲染功能"""
    try:
        import varnaapi
        from varnaapi import Structure
        
        # 设置VARNA路径
        varnaapi.set_VARNA(jar_path)
        
        # 测试简单结构
        print("\n🧪 测试VARNA渲染...")
        v = Structure(
            sequence="GCGCAAAAGCGC",
            structure="((((....))))"
        )
        
        output_path = "test_varna_output.svg"
        v.savefig(output=output_path)
        
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"✅ SVG生成成功: {output_path}")
            print(f"   大小: {size_kb:.2f} KB")
            
            # 显示SVG前几行
            with open(output_path, 'r') as f:
                lines = f.readlines()[:5]
                print("\n   SVG预览（前5行）:")
                for line in lines:
                    print(f"   {line.rstrip()}")
            
            # 保留测试文件用于查看
            print(f"\n   💡 打开 {output_path} 查看渲染效果")
            return True
        else:
            print("❌ SVG文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ VARNA渲染测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_probability(jar_path):
    """测试带配对概率着色的渲染"""
    try:
        import varnaapi
        from varnaapi import Structure
        import numpy as np
        
        print("\n🧪 测试配对概率着色...")
        varnaapi.set_VARNA(jar_path)
        
        # 模拟配对概率矩阵
        sequence = "GCGCAAAAGCGC"
        structure = "((((....))))"
        length = len(sequence)
        
        # 创建假的配对概率矩阵（实际使用时从NUPACK获取）
        pairs_matrix = np.zeros((length, length))
        
        # 模拟高概率配对
        pairs = [(0, 11), (1, 10), (2, 9), (3, 8)]
        for i, j in pairs:
            pairs_matrix[i, j] = 0.95
            pairs_matrix[j, i] = 0.95
        
        # 计算每个碱基的配对概率
        pair_prob = np.zeros(length)
        stack = []
        for i, c in enumerate(structure):
            if c == '(':
                stack.append(i)
            elif c == ')':
                j = stack.pop()
                prob = pairs_matrix[i, j]
                pair_prob[i] = prob
                pair_prob[j] = prob
        
        # 创建VARNA结构
        v = Structure(structure=structure, sequence=sequence)
        v.add_colormap(pair_prob.tolist())
        
        output_path = "test_varna_colored.svg"
        v.savefig(output=output_path)
        
        if os.path.exists(output_path):
            print(f"✅ 带颜色的SVG生成成功: {output_path}")
            print(f"   💡 打开文件查看配对概率着色效果")
            return True
        return False
        
    except Exception as e:
        print(f"❌ 配对概率着色测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multi_chain(jar_path):
    """测试多链结构渲染"""
    try:
        import varnaapi
        from varnaapi import Structure
        
        print("\n🧪 测试多链结构...")
        varnaapi.set_VARNA(jar_path)
        
        # 多链序列和结构
        # 两条互补链形成双螺旋
        sequence = "GCGCAAAAGCGC&GCGCTTTTGCGC"
        structure = "((((....))))&((((....))))"
        
        v = Structure(structure=structure, sequence=sequence)
        
        output_path = "test_varna_multichain.svg"
        v.savefig(output=output_path)
        
        if os.path.exists(output_path):
            print(f"✅ 多链SVG生成成功: {output_path}")
            print(f"   💡 打开文件查看多链结构")
            return True
        return False
        
    except Exception as e:
        print(f"❌ 多链测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("  VARNA 集成测试")
    print("=" * 60)
    
    # 1. 检查Java
    if not check_java():
        print("\n❌ 环境检查失败，请先安装Java")
        return 1
    
    # 2. 检查varnaapi
    if not check_varnaapi():
        print("\n❌ 环境检查失败，请先安装varnaapi")
        return 1
    
    # 3. 检查VARNA jar
    jar_path = check_varna_jar()
    if not jar_path:
        print("\n❌ 环境检查失败，请先下载VARNA jar")
        return 1
    
    print("\n" + "=" * 60)
    print("  环境检查通过，开始功能测试")
    print("=" * 60)
    
    # 4. 基础渲染测试
    success1 = test_varna_rendering(jar_path)
    
    # 5. 配对概率着色测试
    success2 = test_with_probability(jar_path)
    
    # 6. 多链测试
    success3 = test_multi_chain(jar_path)
    
    print("\n" + "=" * 60)
    print("  测试结果总结")
    print("=" * 60)
    
    if success1 and success2 and success3:
        print("✅ 所有测试通过！VARNA集成准备就绪")
        print("\n下一步:")
        print("1. 将VARNA API代码添加到 app.py")
        print("2. 在前端添加VARNA渲染选项")
        print("3. 重启Flask应用")
        return 0
    else:
        print("❌ 部分测试失败，请检查错误信息")
        return 1


if __name__ == '__main__':
    sys.exit(main())
