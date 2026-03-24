# 更新日志 / Changelog

## [v1.4.0] - 2026-03-24

### 🎨 新增功能 / New Features

#### VARNA结构导出 / VARNA Structure Export
- ✅ 集成VARNA引擎，支持导出发表级的RNA/DNA二级结构图
- ✅ 高质量矢量图（SVG格式），可直接用于论文发表
- ✅ 配对概率渐变着色
- ✅ 多链结构支持（自动分隔显示）
- ✅ 引用提示功能（用于论文发表时引用VARNA文献）

#### 桌面启动脚本 / Desktop Launcher
- ✅ 自动创建桌面图标（NUPACK-Web.desktop）
- ✅ 双击即可启动应用并自动打开浏览器

#### 自动化安装 / Automated Installation
- ✅ 自动检测并安装Java运行环境（OpenJDK 11）
- ✅ 自动下载VARNA jar文件

### 🔧 改进 / Improvements

- 📐 **布局优化** - 左右面板比例改为1:2，序列输入框更宽更易操作
- 🔄 **启动脚本增强** - 自动检测端口占用、自动打开浏览器
- 📦 **打包优化** - 排除测试文件和开发文档，包体积减小

### 🐛 修复 / Bug Fixes

- 🧬 **多链VARNA渲染修复** - 正确处理NUPACK格式（+）和VARNA格式（&）的分隔符转换
- 🧬 **多链结构分隔符问题** - 修复`&`字符被当作核苷酸显示的问题
- 🧬 **序列与结构长度不匹配** - 保存原始mfeStructure用于VARNA渲染
- 📄 **HTML重复内容清理** - 修复页面卡死问题

### 📚 技术细节 / Technical Details

#### VARNA集成 / VARNA Integration
- 新增VARNA状态检查API：`/api/varna/status`
- 新增VARNA可视化API：`/api/visualize/varna`
- VARNA jar文件路径：`lib/VARNAv3-93.jar`
- 引用文献：Darty K, Denise A, Ponty Y. VARNA: Interactive drawing and editing of the RNA secondary structure. Bioinformatics. 2009;25(15):1974-1975.

#### 多链格式转换 / Multi-Chain Format Conversion
```javascript
// NUPACK格式：SEQ1+SEQ2，STRUCT1+STRUCT2
// VARNA格式：SEQ1&SEQ2，STRUCT1&STRUCT2
const varnaSequence = originalSeq.replace(/\+/g, '&');
const varnaStructure = originalStruct.replace(/\+/g, '&');
```

---

## [v1.3.0] - 2026-03-21

### 🔄 新增功能 / New Features

#### 自动布局 / Auto Layout
- 核苷酸按序列顺序均匀分布在圆周上作为初始位置
- D3.js力导向模拟实现自动化美观布局
- 氢键吸引力、共价键约束力、节点排斥力

#### 其他功能 / Other Features
- 📦 紧凑布局（不稳定）
- 🔒 确定布局（不稳定）
- 🔃 旋转功能（不稳定）
- 🎨 多链模式 - 不同链使用不同颜色
- 🔍 缩放改进 - 支持无限缩放
- 📏 核苷酸大小自定义
- 🖊️ 线宽调节
- 💾 下载项目ZIP包
- ☕ 捐赠入口
- 📝 版本号显示

---

## [v1.2.0] - 2026-03-15

### ✨ 新增功能 / New Features

- 次优结构分析
- 配对概率矩阵可视化
- 中英文界面切换
- 深色/浅色主题
- 导出PNG图片、JSON数据、CSV矩阵

---

## [v1.0.0] - 2026-03-01

### 🎉 首次发布 / Initial Release

- 单链分析（MFE结构计算）
- 多链分析（试管分析、复合物浓度分布）
- 序列设计
- D3.js交互式可视化
