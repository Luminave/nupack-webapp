# NUPACK Web v1.5.0 - 本地部署NUPACK，核酸结构可视化分析工具

> 🌐 **[English Documentation / 英文文档](README_EN.md)**

> 📖 **详细教程**：
> - [📘 新手指南](tutorial/guide.md) — 功能使用说明
> - [📖 部署教程](tutorial/deploy.md) — Windows (WSL) 完整安装步骤

一个基于 Flask + NUPACK 的本地化核酸分析网页界面，提供直观的可视化操作体验。

## 🆕 v1.5.0 更新日志

### 🔬 高级模式
- 新增「高级模式」：输入序列 + dot-bracket 结构表达式，直接可视化
- 支持粘贴配对概率矩阵或调用 NUPACK 重新计算
- 有矩阵时碱基按配对概率着色，无矩阵时按碱基类型着色
- 支持 VARNA 导出（有无矩阵均可）

### 🌡️ 配对概率矩阵增强
- 所有热力图新增渐变色条（颜色参考）
- 所有热力图新增「📥 导出图片」按钮（3x 高清 PNG）

### 📖 教程系统
- 新增在线教程页面（`/tutorial`），marked.js 渲染 markdown
- 新手指南：功能使用说明，中英对照
- 部署教程：Windows WSL 完整安装步骤

### 🔧 Bug 修复
- 次优结构分析 `Too many suboptimal structures` 崩溃修复
- 能量窗口自动模式（根据序列长度自动选择合适的 gap）
- VARNA 导出图片裁剪修复（自动添加 viewBox + 边距）
- VARNA 导出配对概率着色修复
- JavaScript 语法错误修复（页面卡死问题）
- 多链分析新增「查看所有结构」和「查看原始数据」按钮

### 📦 其他更新
- 版本号更新至 v1.5.0
- 顶部导航栏新增「📘 新手指南」和「🔄 检查更新」按钮
- 捐赠链接更新为爱发电 (ifdian.net)

---

## 🆕 v1.4.0 更新日志

### 🎨 VARNA结构导出
- 集成VARNA引擎，支持导出发表级RNA/DNA二级结构图
- 高质量矢量图（SVG格式），配对概率渐变着色
- 多链结构支持，引用提示

### 📦 其他更新
- 桌面启动脚本，自动打开浏览器
- Java 自动安装检测

## 🆕 v1.3.0 更新日志

### 🔄 自动布局
- 核苷酸按序列顺序分布在圆周上，D3.js 力导向模拟自动布局
- 紧凑布局、确定布局、旋转功能
- 多链模式、缩放改进、线宽调节

## ✨ 功能特性

### 🔬 单链分析
- 计算最小自由能 (MFE) 结构
- 配对概率矩阵可视化
- 次优结构分析（自动/手动能量窗口）
- 力导向图可视化，支持交互操作

### 🧬 多链分析
- 多条链的试管分析
- 复合物浓度分布饼图
- 所有结构列表 + 原始数据查看

### 🎨 序列设计
- 结构域定义（N/R/Y 等符号支持）
- 目标复合物设计，自动选择最优结果

### 🧪 高级模式
- 输入序列 + dot-bracket 直接可视化
- 配对概率矩阵输入/重算
- VARNA 导出

### 📦 其他功能
- 中英文界面切换 / 深色浅色主题
- 碱基颜色自定义
- 配对概率矩阵热力图（渐变色条 + 导出图片）
- 导出 PNG、JSON、CSV
- 检查更新（GitHub 版本对比）

## 📋 系统要求

- Python 3.8+（推荐 3.12）
- NUPACK 4.0+
- Java 11+（完整版，VARNA 功能需要）

## 🚀 快速安装

### Linux / macOS

```bash
# 克隆仓库
git clone https://github.com/Luminave/nupack-webapp.git
cd nupack-webapp

# 运行安装脚本
./install.sh

# 启动
./start.sh
```

浏览器打开：http://127.0.0.1:5000

### Windows (WSL)

详见 [📖 部署教程](tutorial/deploy.md)，包含完整的 WSL + Python + NUPACK 安装步骤。

简要步骤：
1. 安装 WSL (`wsl --install`) 并配置 Ubuntu
2. 安装 Python 3.12 并创建虚拟环境
3. 安装 NUPACK wheel 包
4. 克隆本仓库并运行 `./install.sh` + `./start.sh`
5. 在 Windows 浏览器中访问 http://127.0.0.1:5000

## 🔬 虚拟环境安装

```bash
git clone https://github.com/Luminave/nupack-webapp.git
cd nupack-webapp
python3 -m venv venv
source venv/bin/activate
pip install nupack
pip install -r requirements.txt
python3 app.py
```

## 📖 使用示例

### 单链分析
```
序列: GCGCAAAAGCGC
```
可形成发卡结构，测试次优结构分析功能。

### 多链分析
```
链 A: GCGCAAAAGCGC (1e-6 M)
链 B: GCGCTTTTGCGC (1e-6 M)
```

### 序列设计
```
结构域: a = N10
目标链: S1 = a, S2 = ~a
目标复合物: S1,S2 结构为 ..........+..........
```

## ❓ 常见问题

**Q: `ModuleNotFoundError: No module named 'nupack'`**
> NUPACK 未安装，请先完成安装

**Q: `ModuleNotFoundError: No module named 'flask'`**
> 运行 `pip install flask` 或 `./install.sh`

**Q: 端口 5000 被占用**
> 修改 `app.py` 最后一行的端口号

**Q: 安装脚本无权限**
> 运行 `chmod +x install.sh start.sh`

## 🙏 致谢

- [NUPACK](https://www.nupack.org/) - 核酸结构预测软件
- [D3.js](https://d3js.org/) - 数据可视化库
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [VARNA](https://varna.lisn.upsaclay.fr/) - RNA 结构可视化工具

## 📄 许可证

本项目仅供学习和研究使用。使用 NUPACK 功能需要遵守 NUPACK 的许可协议。

---

**Author**: Victor.Guo
**GitHub**: https://github.com/Luminave/nupack-webapp
