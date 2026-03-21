# NUPACK Web - 核酸结构可视化分析工具

> 📝 **说明**：本文档由 AI 撰写。如果你是初次使用的小白用户，强烈建议先阅读这篇详细的图文安装教程：
> 
> 🔗 **[知乎专栏：NUPACK Web 小白安装教程](https://zhuanlan.zhihu.com/p/2018702350303380650)**

一个基于 Flask + NUPACK 的本地化核酸分析网页界面，提供直观的可视化操作体验。

## ✨ 功能特性

### 🔬 单链分析
- 计算最小自由能 (MFE) 结构
- 配对概率矩阵可视化
- **次优结构分析** - 探索能量相近的多种可能结构
- 力导向图可视化二级结构
- 自定义配对概率渐变颜色

### 🧬 多链分析
- 多条链的试管分析
- 复合物浓度分布饼图
- 交互式结构预览和详情查看

### 🎨 序列设计
- 结构域定义
- 目标复合物设计
- 多次设计尝试，自动选择最优结果

### 📦 其他功能
- 中英文界面切换
- 深色/浅色主题
- 导出 PNG 图片、JSON 数据、CSV 矩阵
- Jupyter Lab 集成
- 响应式设计

## 📋 系统要求

- Python 3.8+
- NUPACK 4.0+ (需要有效的许可证)

## 🚀 快速安装

> ⚠️ **警告**：以下快速安装方法会直接向系统 Python 环境安装包，**可能会影响系统原有的 Python 环境**。
> 
> 如果你是有经验的开发者，或系统中已有其他 Python 项目，**强烈建议使用虚拟环境安装**（见下方"专业安装"）。

### 1. 安装 NUPACK

首先需要在 NUPACK 官网注册并获取许可证：https://www.nupack.org/

```bash
# 安装 NUPACK
pip install nupack --break-system-packages

# 激活许可证（替换为你的许可证密钥）
nupack-license --user "your_email@example.com" --key "your_license_key"
```

### 2. 安装 NUPACK Web

```bash
# 克隆仓库
git clone https://github.com/Luminave/nupack-webapp.git

# 进入目录
cd nupack-webapp

# 运行安装脚本
./install.sh
```

### 3. 启动应用

```bash
./start.sh
```

然后在浏览器中打开：http://127.0.0.1:5000

---

### 一键安装（复制粘贴）

```bash
git clone https://github.com/Luminave/nupack-webapp.git && cd nupack-webapp && ./install.sh && ./start.sh
```

---

## 🔬 专业安装（使用虚拟环境）

如果你是有经验的开发者，建议使用 Python 虚拟环境，避免影响系统环境：

```bash
# 克隆仓库
git clone https://github.com/Luminave/nupack-webapp.git
cd nupack-webapp

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 NUPACK（首次安装）
pip install nupack
nupack-license --user "your_email@example.com" --key "your_license_key"

# 安装依赖
pip install -r requirements.txt

# 启动
python3 app.py
```

---

## 📖 使用示例

### 单链分析示例
```
序列: GCGCAAAAGCGC
```
这是一个能形成发卡结构的序列，可以测试次优结构分析功能。

### 多链分析示例
```
链 A: GCGCAAAAGCGC
链 B: GCGCTTTTGCGC
浓度: 各 1e-6 M
```
两条互补链会形成双链复合物。

### 序列设计示例
```
结构域: a = N10
目标链: S1 = a, S2 = ~a
目标复合物: S1,S2 结构为 ..........+..........
```
设计两条互补的 10nt 链。

## 🔧 配置说明

应用默认运行在 `127.0.0.1:5000`，如需修改：

```python
# 在 app.py 末尾修改
app.run(host='0.0.0.0', port=8080, debug=False)
```

## 📁 项目结构

```
nupack-webapp/
├── app.py              # Flask 主应用
├── requirements.txt    # Python 依赖
├── install.sh          # 安装脚本
├── start.sh            # 启动脚本
├── README.md           # 说明文档
├── LICENSE             # 许可证
└── templates/
    └── index.html      # 主页面模板
```

## ❓ 常见问题

**Q: 提示 `ModuleNotFoundError: No module named 'nupack'`**
> A: NUPACK 未安装或未激活许可证，请先完成 NUPACK 安装

**Q: 提示 `ModuleNotFoundError: No module named 'flask'`**
> A: 运行 `pip install flask` 或重新运行 `./install.sh`

**Q: 端口 5000 被占用**
> A: 修改 `app.py` 最后一行的 `port=5000` 为其他端口

**Q: 安装脚本执行无权限**
> A: 运行 `chmod +x install.sh start.sh` 添加执行权限

## 🙏 致谢

- [NUPACK](https://www.nupack.org/) - 核酸结构预测软件
- [D3.js](https://d3js.org/) - 数据可视化库
- [Flask](https://flask.palletsprojects.com/) - Web 框架

## 📄 许可证

本项目仅供学习和研究使用。使用 NUPACK 功能需要遵守 NUPACK 的许可协议。

---

**Author**: Victor.Guo  
**GitHub**: https://github.com/Luminave/nupack-webapp
