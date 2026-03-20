#!/usr/bin/env python3
"""
NUPACK Web Interface - 本地可视化核酸分析工具
"""

from flask import Flask, render_template, request, jsonify
from nupack import *
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

# 项目保存目录
PROJECTS_DIR = os.path.expanduser('~/nupack-projects')
os.makedirs(PROJECTS_DIR, exist_ok=True)

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

# ==================== API 路由 ====================

@app.route('/api/analyze/single', methods=['POST'])
def analyze_single():
    """单链分析"""
    try:
        data = request.json
        sequence = data.get('sequence', '').upper().strip()
        material = data.get('material', 'dna')
        temp = float(data.get('temperature', 37))
        sodium = float(data.get('sodium', 1.0))
        magnesium = float(data.get('magnesium', 0.0))
        
        # 验证序列
        valid_chars = set('ACGT') if material == 'dna' else set('ACGU')
        if not all(c in valid_chars for c in sequence):
            return jsonify({'error': f'无效序列。{material.upper()} 序列只能包含 {", ".join(valid_chars)}'})
        
        if len(sequence) < 1:
            return jsonify({'error': '序列不能为空'})
        
        # 创建模型
        model = Model(material=material, celsius=temp, sodium=sodium, magnesium=magnesium)
        
        # 创建链和复合物
        strand = Strand(sequence, name='Input')
        comp = Complex([strand], name='Input')
        
        # 使用 complex_analysis 获取完整信息
        comp_result = complex_analysis([comp], model=model, compute=['mfe', 'pairs', 'ensemble_size'])
        
        # 获取结果
        result = comp_result[comp]
        mfe_struct = result.mfe[0].structure
        mfe_energy = result.mfe[0].energy
        
        # 获取配对概率矩阵
        pairs = result.pairs
        
        # 构建返回数据
        result_data = {
            'sequence': sequence,
            'mfe_structure': str(mfe_struct),
            'mfe_energy': float(mfe_energy),
            'ensemble_size': int(result.ensemble_size),
            'pairs_matrix': pairs.to_array().tolist(),
            'length': len(sequence)
        }
        
        return jsonify(result_data)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})


@app.route('/api/analyze/subopt', methods=['POST'])
def analyze_subopt():
    """次优结构分析 - 返回多个可能的结构"""
    try:
        data = request.json
        sequence = data.get('sequence', '').upper().strip()
        material = data.get('material', 'dna')
        temp = float(data.get('temperature', 37))
        sodium = float(data.get('sodium', 1.0))
        magnesium = float(data.get('magnesium', 0.0))
        
        # 次优结构参数
        energy_gap = float(data.get('energy_gap', 3.0))  # 能量窗口 (kcal/mol)
        max_structures = int(data.get('max_structures', 20))  # 最大结构数
        
        # 验证序列
        valid_chars = set('ACGT') if material == 'dna' else set('ACGU')
        if not all(c in valid_chars for c in sequence):
            return jsonify({'error': f'无效序列。{material.upper()} 序列只能包含 {", ".join(valid_chars)}'})
        
        if len(sequence) < 1:
            return jsonify({'error': '序列不能为空'})
        
        # 创建模型
        model = Model(material=material, celsius=temp, sodium=sodium, magnesium=magnesium)
        
        # 创建链
        strand = Strand(sequence, name='Input')
        comp = Complex([strand], name='Input')
        
        # 使用 subopt 获取次优结构
        subopt_result = subopt(comp, energy_gap, model)
        
        # 获取配对概率矩阵（用于底部显示）
        comp = Complex([strand], name='Input')
        comp_result = complex_analysis([comp], model=model, compute=['pairs', 'ensemble_size'])
        pairs = comp_result[comp].pairs
        ensemble_size = int(comp_result[comp].ensemble_size)
        
        # 整理结构数据
        structures = []
        total_prob = 0.0
        
        for i, struct_result in enumerate(subopt_result[:max_structures]):
            energy = float(struct_result.energy)
            structure_str = str(struct_result.structure)
            
            # 计算玻尔兹曼概率
            # P ∝ exp(-ΔG / RT)
            # R = 0.001987 kcal/(mol·K)
            R = 0.001987
            T_kelvin = temp + 273.15
            boltzmann_factor = np.exp(-energy / (R * T_kelvin))
            
            structures.append({
                'index': i + 1,
                'structure': structure_str,
                'energy': energy,
                'boltzmann_factor': boltzmann_factor,
                'sequence': sequence
            })
            total_prob += boltzmann_factor
        
        # 归一化概率
        for s in structures:
            s['probability'] = s['boltzmann_factor'] / total_prob if total_prob > 0 else 0
        
        # 按概率排序
        structures.sort(key=lambda x: x['probability'], reverse=True)
        for i, s in enumerate(structures):
            s['index'] = i + 1
        
        result_data = {
            'sequence': sequence,
            'structures': structures,
            'total_structures': len(structures),
            'energy_gap': energy_gap,
            'pairs_matrix': pairs.to_array().tolist(),
            'ensemble_size': ensemble_size,
            'length': len(sequence)
        }
        
        return jsonify(result_data)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})


import numpy as np


@app.route('/api/analyze/tube', methods=['POST'])
def analyze_tube():
    """多链试管分析"""
    try:
        data = request.json
        strands_data = data.get('strands', [])
        material = data.get('material', 'dna')
        temp = float(data.get('temperature', 37))
        sodium = float(data.get('sodium', 1.0))
        magnesium = float(data.get('magnesium', 0.0))
        max_size = int(data.get('max_size', 2))
        
        if not strands_data:
            return jsonify({'error': '请至少添加一条链'})
        
        # 创建模型
        model = Model(material=material, celsius=temp, sodium=sodium, magnesium=magnesium)
        
        # 创建链
        strand_objects = []
        for i, strand_info in enumerate(strands_data):
            seq = strand_info['sequence'].upper().strip()
            conc = float(strand_info.get('concentration', 1e-6))
            name = strand_info.get('name', f'Strand_{i+1}')
            
            # 验证序列
            valid_chars = set('ACGT') if material == 'dna' else set('ACGU')
            if not all(c in valid_chars for c in seq):
                return jsonify({'error': f'链 "{name}" 包含无效字符'})
            
            strand = Strand(seq, name=name)
            strand_objects.append((strand, conc))
        
        # 创建试管
        strands_dict = {s: c for s, c in strand_objects}
        tube = Tube(strands=strands_dict, complexes=SetSpec(max_size=max_size), name='AnalysisTube')
        
        # 分析试管
        results = tube_analysis(tubes=[tube], model=model)
        tube_result = results[tube]
        
        # 整理复合物结果
        complexes_data = []
        for comp_spec, conc in tube_result.complex_concentrations.items():
            # 获取复合物的链
            comp_strands = comp_spec.strands
            
            # 组合序列显示
            sequences = [str(s) for s in comp_strands]
            full_seq = '+'.join(sequences)
            
            # 获取 MFE 结构和能量
            try:
                mfe_result = mfe(strands=comp_strands, model=model)
                mfe_struct = str(mfe_result[0].structure)
                mfe_energy = float(mfe_result[0].energy)
            except Exception as e:
                mfe_struct = 'N/A'
                mfe_energy = 0.0
            
            comp_data = {
                'name': str(comp_spec.name),
                'sequence': full_seq,
                'concentration': float(conc),
                'mfe_structure': mfe_struct,
                'mfe_energy': mfe_energy
            }
            complexes_data.append(comp_data)
        
        # 按浓度排序
        complexes_data.sort(key=lambda x: x['concentration'], reverse=True)
        
        result_data = {
            'complexes': complexes_data,
            'total_complexes': len(complexes_data)
        }
        
        return jsonify(result_data)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})


@app.route('/api/analyze/complex', methods=['POST'])
def analyze_complex():
    """分析复合物结构，返回配对概率矩阵"""
    try:
        data = request.json
        sequence = data.get('sequence', '').upper().strip()
        structure = data.get('structure', '').strip()
        material = data.get('material', 'dna')
        temp = float(data.get('temperature', 37))
        
        # 移除链分隔符（多链序列中用 + 连接）
        clean_seq = sequence.replace('+', '')
        clean_struct = structure.replace('+', '')
        
        if len(clean_seq) < 1:
            return jsonify({'error': '序列不能为空'})
        
        # 创建模型
        model = Model(material=material, celsius=temp)
        
        # 创建单链并分析
        strand = Strand(clean_seq, name='Complex')
        comp = Complex([strand], name='Complex')
        
        # 获取配对概率矩阵
        comp_result = complex_analysis([comp], model=model, compute=['pairs'])
        result = comp_result[comp]
        pairs = result.pairs
        
        return jsonify({
            'sequence': clean_seq,
            'structure': clean_struct,
            'pairs_matrix': pairs.to_array().tolist()
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})


@app.route('/api/energy', methods=['POST'])
def calc_energy():
    """计算特定结构的自由能"""
    try:
        data = request.json
        sequence = data.get('sequence', '').upper().strip()
        structure = data.get('structure', '').strip()
        material = data.get('material', 'dna')
        temp = float(data.get('temperature', 37))
        
        # 创建模型
        model = Model(material=material, celsius=temp)
        
        # 创建链并计算能量
        strand = Strand(sequence, name='Input')
        comp = Complex([strand], structure)
        
        # 计算能量
        energy = comp.energy(model)
        
        return jsonify({
            'sequence': sequence,
            'structure': structure,
            'energy': float(energy)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/design/complex', methods=['POST'])
def design_complex():
    """设计复合物序列"""
    try:
        data = request.json
        
        # 获取参数
        material = data.get('material', 'dna')
        temp = float(data.get('temperature', 37))
        sodium = float(data.get('sodium', 1.0))
        magnesium = float(data.get('magnesium', 0.0))
        trials = int(data.get('trials', 3))
        
        # 获取结构域定义
        domains_def = data.get('domains', [])
        strands_def = data.get('strands', [])
        complexes_def = data.get('complexes', [])
        
        # 创建模型
        model = Model(material=material, celsius=temp, sodium=sodium, magnesium=magnesium)
        
        # 创建结构域
        domains = {}
        for d in domains_def:
            domains[d['name']] = Domain(d['sequence'], name=d['name'])
        
        # 创建目标链
        target_strands = {}
        for s in strands_def:
            # 解析结构域列表
            domain_list = []
            for domain_name in s['domains']:
                if domain_name.startswith('~'):
                    # 反向互补
                    base_name = domain_name[1:]
                    if base_name in domains:
                        domain_list.append(~domains[base_name])
                else:
                    if domain_name in domains:
                        domain_list.append(domains[domain_name])
            
            target_strands[s['name']] = TargetStrand(domain_list, name=s['name'])
        
        # 创建目标复合物
        target_complexes = []
        for c in complexes_def:
            strand_list = [target_strands[s] for s in c['strands']]
            target_complexes.append(TargetComplex(strand_list, c['structure'], name=c['name']))
        
        # 运行设计
        my_design = complex_design(complexes=target_complexes, model=model)
        results = my_design.run(trials=trials)
        
        # 整理结果
        design_results = []
        for i, result in enumerate(results):
            # 获取序列
            sequences = {}
            for domain, seq in result.domains.items():
                sequences[domain.name] = str(seq)
            
            # 构建链序列
            strand_sequences = {}
            for strand_name, target_strand in target_strands.items():
                seq_parts = []
                strand_def = next((s for s in strands_def if s['name'] == strand_name), None)
                if strand_def:
                    for domain_name in strand_def['domains']:
                        if domain_name.startswith('~'):
                            base_name = domain_name[1:]
                            if base_name in sequences:
                                # 反向互补
                                seq = sequences[base_name]
                                seq_parts.append(seq[::-1].translate(str.maketrans('ATGC', 'TACG')))
                        else:
                            if domain_name in sequences:
                                seq_parts.append(sequences[domain_name])
                    strand_sequences[strand_name] = ''.join(seq_parts)
            
            design_results.append({
                'trial': i + 1,
                'ensemble_defect': float(result.ensemble_defect),
                'domains': sequences,
                'strands': strand_sequences
            })
        
        # 按缺陷排序
        design_results.sort(key=lambda x: x['ensemble_defect'])
        
        return jsonify({
            'success': True,
            'results': design_results,
            'total_trials': len(results)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})


@app.route('/api/project/save', methods=['POST'])
def save_project():
    """保存分析项目"""
    try:
        data = request.json
        
        # 生成项目目录名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_name = data.get('name', f'nupack_project_{timestamp}')
        project_dir = os.path.join(PROJECTS_DIR, project_name)
        
        # 创建项目目录
        os.makedirs(project_dir, exist_ok=True)
        
        # 保存分析结果
        results_file = os.path.join(project_dir, 'analysis_results.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(data.get('results', {}), f, indent=2, ensure_ascii=False)
        
        # 创建Jupyter笔记本
        notebook = create_notebook(data)
        notebook_file = os.path.join(project_dir, 'analysis.ipynb')
        with open(notebook_file, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)
        
        # 保存参数信息
        params_file = os.path.join(project_dir, 'parameters.json')
        with open(params_file, 'w', encoding='utf-8') as f:
            json.dump({
                'material': data.get('material', 'dna'),
                'temperature': data.get('temperature', 37),
                'sodium': data.get('sodium', 1.0),
                'magnesium': data.get('magnesium', 0.0),
                'created_at': timestamp
            }, f, indent=2)
        
        return jsonify({
            'success': True,
            'project_dir': project_dir,
            'notebook_file': notebook_file
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})


@app.route('/api/jupyter/open', methods=['POST'])
def open_jupyter():
    """打开Jupyter笔记本"""
    try:
        data = request.json
        project_dir = data.get('project_dir', PROJECTS_DIR)
        
        # 检查目录是否存在
        if not os.path.exists(project_dir):
            return jsonify({'error': '项目目录不存在'})
        
        # 启动jupyter lab
        subprocess.Popen(
            ['jupyter', 'lab', '--no-browser', project_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        return jsonify({
            'success': True,
            'message': 'Jupyter Lab 已启动',
            'url': 'http://localhost:8888'
        })
        
    except FileNotFoundError:
        return jsonify({'error': '未找到 jupyter 命令，请确保已安装 Jupyter'})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})


def create_notebook(data):
    """创建包含分析代码的Jupyter笔记本"""
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# NUPACK 分析项目\n",
                    "\n",
                    f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                    "\n",
                    "此笔记本包含本次分析的完整数据和可视化代码。"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 导入必要的库\n",
                    "from nupack import *\n",
                    "import json\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "# 加载分析结果\n",
                    "with open('analysis_results.json', 'r') as f:\n",
                    "    results = json.load(f)\n",
                    "\n",
                    "print('分析结果已加载')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 设置物理参数\n",
                    f"material = '{data.get('material', 'dna')}'\n",
                    f"temperature = {data.get('temperature', 37)}\n",
                    f"sodium = {data.get('sodium', 1.0)}\n",
                    f"magnesium = {data.get('magnesium', 0.0)}\n",
                    "\n",
                    "model = Model(material=material, celsius=temperature, sodium=sodium, magnesium=magnesium)\n",
                    "print(f'模型: {material}, {temperature}°C')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 查看分析结果\n",
                    "print('=== 分析结果 ===')\n",
                    "print(json.dumps(results, indent=2, ensure_ascii=False)[:2000])"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 绘制配对概率矩阵\n",
                    "if 'pairs_matrix' in results:\n",
                    "    pairs = np.array(results['pairs_matrix'])\n",
                    "    plt.figure(figsize=(8, 8))\n",
                    "    plt.imshow(pairs, cmap='Blues', vmin=0, vmax=1)\n",
                    "    plt.colorbar(label='配对概率')\n",
                    "    plt.title(f'配对概率矩阵\\n序列: {results.get(\"sequence\", \"\")}')\n",
                    "    plt.xlabel('位置')\n",
                    "    plt.ylabel('位置')\n",
                    "    plt.tight_layout()\n",
                    "    plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    return notebook


# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 50)
    print("NUPACK Web Interface")
    print("请在浏览器中打开: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host='127.0.0.1', port=5000, debug=True)
