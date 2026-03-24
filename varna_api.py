"""
VARNA API 扩展模块
将此文件中的代码添加到 app.py 中

使用方法:
1. 在 app.py 开头的导入部分添加 varna 相关导入
2. 配置 VARNA jar 路径
3. 添加 API 路由
"""

# ==================== 导入部分 ====================
# 在 app.py 的导入部分添加:

import varnaapi
from varnaapi import Structure
import tempfile
import base64
import numpy as np

# ==================== 配置部分 ====================
# 在 app = Flask(__name__) 之后添加:

# VARNA 配置
VARNA_JAR = os.path.join(os.path.dirname(__file__), 'lib', 'VARNAv3-93.jar')
VARNA_AVAILABLE = False

def init_varna():
    """初始化VARNA"""
    global VARNA_AVAILABLE
    if os.path.exists(VARNA_JAR):
        try:
            varnaapi.set_VARNA(VARNA_JAR)
            VARNA_AVAILABLE = True
            print(f"✅ VARNA 已加载: {VARNA_JAR}")
        except Exception as e:
            print(f"⚠️  VARNA 加载失败: {e}")
    else:
        print(f"⚠️  VARNA jar 未找到: {VARNA_JAR}")
        print("   请运行: mkdir -p lib && cd lib && wget https://varna.lri.fr/bin/VARNAv3-93.jar")

# 在应用启动时初始化
init_varna()


# ==================== API 路由 ====================
# 在 app.py 的路由部分添加以下路由:

@app.route('/api/varna/status', methods=['GET'])
def varna_status():
    """检查VARNA是否可用"""
    return jsonify({
        'available': VARNA_AVAILABLE,
        'jar_path': VARNA_JAR if VARNA_AVAILABLE else None
    })


@app.route('/api/visualize/varna', methods=['POST'])
def visualize_varna():
    """使用VARNA生成结构可视化SVG
    
    请求参数:
    - sequence: 序列 (多链用+分隔)
    - structure: 点括号结构 (多链用+分隔)
    - pairs_matrix: 配对概率矩阵 (可选)
    - show_probability: 是否显示配对概率着色 (默认True)
    - layout: 布局算法 (naview, radiate, circular, linear)
    - style: 样式选项 (字典)
    
    返回:
    - svg: SVG内容
    - svg_base64: Base64编码的SVG
    """
    try:
        if not VARNA_AVAILABLE:
            return jsonify({
                'error': 'VARNA不可用。请确保已安装Java并下载VARNA jar文件。',
                'install_instructions': {
                    'java': 'sudo apt install openjdk-11-jre',
                    'varna': 'cd lib && wget https://varna.lri.fr/bin/VARNAv3-93.jar'
                }
            }), 503
        
        data = request.json
        sequence = data.get('sequence', '').upper().strip()
        structure = data.get('structure', '').strip()
        pairs_matrix = data.get('pairs_matrix', None)
        
        # 可选参数
        show_probability = data.get('show_probability', True)
        layout = data.get('layout', 'naview')
        style = data.get('style', {})
        
        # 验证输入
        if not sequence or not structure:
            return jsonify({'error': '序列和结构不能为空'}), 400
        
        # 处理多链序列
        # NUPACK格式: "SEQ1+SEQ2" → VARNA格式: "SEQ1&SEQ2"
        seq_varna = sequence.replace('+', '&')
        struct_varna = structure.replace('+', '&')
        
        # 用于计算的纯净序列（无分隔符）
        seq_calc = sequence.replace('+', '')
        struct_calc = structure.replace('+', '')
        
        # 创建VARNA结构对象
        try:
            v = Structure(
                structure=struct_varna,
                sequence=seq_varna
            )
        except Exception as e:
            return jsonify({'error': f'VARNA结构创建失败: {str(e)}'}), 400
        
        # 设置布局算法
        if layout in ['naview', 'radiate', 'circular', 'linear']:
            try:
                v.set_layout(layout)
            except:
                pass  # 使用默认布局
        
        # 配对概率着色
        if show_probability and pairs_matrix:
            try:
                P = np.array(pairs_matrix)
                pair_prob = np.zeros(len(seq_calc))
                
                # 解析配对关系
                stack = []
                for i, c in enumerate(struct_calc):
                    if i >= len(seq_calc):
                        break
                    if c == '(':
                        stack.append(i)
                    elif c == ')':
                        if stack:
                            j = stack.pop()
                            if i < P.shape[0] and j < P.shape[1]:
                                prob = float(P[i, j])
                                pair_prob[i] = prob
                                pair_prob[j] = prob
                
                # 添加颜色映射
                v.add_colormap(pair_prob.tolist())
            except Exception as e:
                print(f"⚠️  配对概率着色失败: {e}")
        
        # 应用自定义样式
        if style:
            try:
                v.set_options(style)
            except:
                pass
        
        # 生成SVG
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False, mode='w') as tmp:
            output_path = tmp.name
        
        v.savefig(output=output_path)
        
        # 读取SVG
        with open(output_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # 清理临时文件
        try:
            os.unlink(output_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'svg': svg_content,
            'svg_base64': base64.b64encode(svg_content.encode()).decode(),
            'info': {
                'sequence': sequence,
                'structure': structure,
                'layout': layout,
                'chains': len(sequence.split('+'))
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualize/varna/enhanced', methods=['POST'])
def visualize_varna_enhanced():
    """增强版VARNA可视化 - 支持更多自定义选项
    
    额外参数:
    - highlight_regions: 高亮区域列表 [{"start": 0, "end": 5, "color": "#FF0000"}]
    - annotations: 注释列表 [{"position": 5, "text": "mutation", "color": "#0000FF"}]
    - title: 标题
    - show_sequence: 是否显示序列编号
    - show_bases: 是否显示碱基字母
    """
    try:
        if not VARNA_AVAILABLE:
            return jsonify({'error': 'VARNA不可用'}), 503
        
        data = request.json
        sequence = data.get('sequence', '').upper().strip()
        structure = data.get('structure', '').strip()
        pairs_matrix = data.get('pairs_matrix', None)
        
        # 增强参数
        highlight_regions = data.get('highlight_regions', [])
        annotations = data.get('annotations', [])
        title = data.get('title', '')
        show_sequence = data.get('show_sequence', True)
        show_bases = data.get('show_bases', True)
        
        # 处理序列
        seq_varna = sequence.replace('+', '&')
        struct_varna = structure.replace('+', '&')
        seq_calc = sequence.replace('+', '')
        struct_calc = structure.replace('+', '')
        
        # 创建结构
        v = Structure(structure=struct_varna, sequence=seq_varna)
        
        # 配对概率着色
        if pairs_matrix:
            P = np.array(pairs_matrix)
            pair_prob = np.zeros(len(seq_calc))
            stack = []
            for i, c in enumerate(struct_calc):
                if i >= len(seq_calc):
                    break
                if c == '(':
                    stack.append(i)
                elif c == ')':
                    if stack:
                        j = stack.pop()
                        if i < P.shape[0] and j < P.shape[1]:
                            prob = float(P[i, j])
                            pair_prob[i] = prob
                            pair_prob[j] = prob
            v.add_colormap(pair_prob.tolist())
        
        # 高亮区域
        for region in highlight_regions:
            try:
                start = int(region.get('start', 0))
                end = int(region.get('end', 1))
                color = region.get('color', '#FFFF00')
                v.add_highlight_region(start=start, end=end, color=color)
            except:
                pass
        
        # 样式选项
        options = {
            'drawBackbone': True,
            'drawBases': show_bases,
            'fillBases': True,
            'baseNum': show_sequence,
            'title': title if title else ''
        }
        
        try:
            v.set_options(options)
        except:
            pass
        
        # 生成SVG
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            output_path = tmp.name
        
        v.savefig(output=output_path)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        try:
            os.unlink(output_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'svg': svg_content,
            'svg_base64': base64.b64encode(svg_content.encode()).decode()
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ==================== 辅助函数 ====================

def get_chain_colors(chain_index):
    """获取链颜色（用于多链显示）"""
    colors = [
        '#FF6B6B',  # 红
        '#4ECDC4',  # 青
        '#45B7D1',  # 蓝
        '#96CEB4',  # 绿
        '#FFEAA7',  # 黄
        '#DDA0DD',  # 紫
        '#98D8C8',  # 薄荷
        '#F7DC6F'   # 金
    ]
    return colors[chain_index % len(colors)]


# ==================== 集成到现有API ====================

# 修改 analyze_single 函数，添加VARNA数据
def enhance_single_analysis_result(result_data):
    """为单链分析结果添加VARNA渲染信息"""
    result_data['varna_available'] = VARNA_AVAILABLE
    if VARNA_AVAILABLE:
        # 添加VARNA渲染端点信息
        result_data['varna_endpoint'] = '/api/visualize/varna'
    return result_data

# 在 analyze_single 返回前调用:
# result_data = enhance_single_analysis_result(result_data)
# return jsonify(result_data)


# ==================== 使用示例 ====================

"""
前端调用示例:

// 基础VARNA渲染
async function renderWithVarna(sequence, structure, pairsMatrix) {
    const response = await fetch('/api/visualize/varna', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            sequence: sequence,
            structure: structure,
            pairs_matrix: pairsMatrix,
            show_probability: true,
            layout: 'naview'
        })
    });
    
    const data = await response.json();
    
    if (data.success) {
        // 显示SVG
        document.getElementById('varna-container').innerHTML = data.svg;
    }
}

// 增强版渲染（带高亮和注释）
async function renderEnhanced(sequence, structure, pairsMatrix) {
    const response = await fetch('/api/visualize/varna/enhanced', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            sequence: sequence,
            structure: structure,
            pairs_matrix: pairsMatrix,
            title: 'MFE Structure',
            highlight_regions: [
                {start: 0, end: 5, color: '#FFE4B5'}
            ],
            show_sequence: true,
            show_bases: true
        })
    });
    
    const data = await response.json();
    // ...
}
"""
