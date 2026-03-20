# NUPACK Web - 核酸结构可视化分析工具

一个基于 Flask + NUPACK 的本地化核酸分析网页界面，提供直观的可视化操作体验。

![Screenshot](https://via.placeholder.com/800x400?text=NUPACK+Web+Screenshot)

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

## 🚀 安装步骤

### 1. 安装 NUPACK

首先需要在 NUPACK 官网注册并获取许可证：https://www.nupack.org/

```bash
# 安装 NUPACK
pip install -U nupack

# 激活许可证（替换为你的许可证密钥）
nupack-license --user "your_email@example.com" --key "your_license_key"
```

### 2. 安装 NUPACK Web

```bash
# 下载或克隆项目
git clone https://github.com/your-username/nupack-webapp.git
cd nupack-webapp

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python app.py
```

然后在浏览器中打开：http://127.0.0.1:5000

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

## ⌨️ 快捷操作

| 点击区域 | 功能 |
|---------|------|
| 🧬 | 显示彩蛋 |
| NUPACK | 跳转 NUPACK 官网 |
| Web | 跳转作者主页 |

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
├── start.sh           # 启动脚本
├── templates/
│   └── index.html     # 主页面模板
└── static/            # 静态资源（如有）
```

## 🙏 致谢

- [NUPACK](https://www.nupack.org/) - 核酸结构预测软件
- [D3.js](https://d3js.org/) - 数据可视化库
- [Flask](https://flask.palletsprojects.com/) - Web 框架

## 📄 许可证

本项目仅供学习和研究使用。使用 NUPACK 功能需要遵守 NUPACK 的许可协议。

---

**Author**: Victor.Guo  
**Powered by**: OpenClaw
