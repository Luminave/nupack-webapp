# VARNA 快速集成指南

## 🚀 5分钟快速开始

### 第一步：安装依赖（2分钟）

```bash
# 进入项目目录
cd /home/victor/nupack-webapp-release

# 1. 安装Java运行环境
sudo apt install openjdk-11-jre -y

# 2. 安装varnaapi
pip install varnaapi

# 3. 下载VARNA jar文件
mkdir -p lib
cd lib
wget https://varna.lri.fr/bin/VARNAv3-93.jar
cd ..

# 4. 验证安装
python3 test_varna.py
```

### 第二步：集成后端代码（2分钟）

打开 `app.py`，在开头添加导入：

```python
# 在现有导入后添加
import varnaapi
from varnaapi import Structure
import tempfile
import base64
```

在 `app = Flask(__name__)` 后添加配置：

```python
# VARNA配置
VARNA_JAR = os.path.join(os.path.dirname(__file__), 'lib', 'VARNAv3-93.jar')
if os.path.exists(VARNA_JAR):
    varnaapi.set_VARNA(VARNA_JAR)
    print(f"✅ VARNA已加载")
```

将 `varna_api.py` 中的路由代码复制到 `app.py` 的路由部分。

### 第三步：集成前端代码（1分钟）

在 `templates/index.html` 的 `<head>` 部分添加：

```html
<link rel="stylesheet" href="{{ url_for('static', filename='varna_styles.css') }}">
```

在 `</body>` 前添加：

```html
<script src="{{ url_for('static', filename='varna_integration.js') }}"></script>
```

添加VARNA容器：

```html
<!-- 在可视化区域添加 -->
<div id="varna-container" style="display:none;"></div>

<!-- 下载按钮 -->
<div id="varna-downloads" style="display:none;" class="varna-controls">
    <button onclick="VarnaRenderer.downloadSVG()" class="btn btn-primary">
        📥 下载SVG
    </button>
    <button onclick="VarnaRenderer.downloadPNG()" class="btn btn-secondary">
        🖼️ 下载PNG
    </button>
    <button onclick="VarnaRenderer.copySVG()" class="btn btn-secondary">
        📋 复制SVG
    </button>
</div>
```

### 第四步：在现有功能中添加VARNA选项

找到单链分析结果显示函数，添加：

```javascript
// 在显示结果后
VarnaRenderer.integrateSingle(result);
```

## ✅ 测试集成

1. 启动应用：
   ```bash
   python3 app.py
   ```

2. 打开浏览器：http://127.0.0.1:5000

3. 输入测试序列：`GCGCAAAAGCGC`

4. 点击分析，然后点击"🎨 VARNA渲染"

## 🎨 使用示例

### 基础渲染
```javascript
VarnaRenderer.render(
    'GCGCAAAAGCGC',           // 序列
    '((((....))))',           // 结构
    pairsMatrix,              // 配对概率矩阵
    {
        showProbability: true,
        layout: 'naview'
    }
);
```

### 多链结构
```javascript
VarnaRenderer.render(
    'GCGCAAAAGCGC+GCGCTTTTGCGC',  // 两条链
    '((((....))))+((((....))))',
    null,
    { layout: 'radiate' }
);
```

### 增强渲染（带高亮）
```javascript
VarnaRenderer.renderEnhanced(
    sequence,
    structure,
    pairsMatrix,
    {
        title: 'MFE Structure',
        highlightRegions: [
            {start: 0, end: 5, color: '#FFE4B5'}
        ],
        showBases: true,
        showSequence: true
    }
);
```

## 📁 文件结构

```
nupack-webapp-release/
├── app.py                    # 主应用（需修改）
├── varna_api.py              # VARNA API代码（新）
├── test_varna.py             # 测试脚本（新）
├── lib/
│   └── VARNAv3-93.jar        # VARNA jar（需下载）
├── static/
│   ├── varna_integration.js  # 前端JS（新）
│   └── varna_styles.css      # 样式（新）
└── templates/
    └── index.html            # 主页面（需修改）
```

## 🔧 可选配置

### 修改默认布局
```python
# 在 varna_api.py 中修改
layout = data.get('layout', 'naview')  # 改为 'radiate', 'circular', 'linear'
```

### 自定义样式
```javascript
VarnaRenderer.render(sequence, structure, pairsMatrix, {
    style: {
        'baseInnerColor': 'white',
        'baseOuterColor': 'black',
        'baseNameColor': 'blue'
    }
});
```

### 添加更多颜色映射
```python
# 在后端添加自定义颜色方案
color_schemes = {
    'probability': pair_prob.tolist(),
    'custom': custom_colors
}
v.add_colormap(color_schemes['probability'])
```

## 🐛 常见问题

### 1. Java未找到
```bash
# 检查Java
java -version

# 如果未安装
sudo apt install openjdk-11-jre
```

### 2. VARNA jar未找到
```bash
# 检查jar文件
ls -la lib/VARNAv3-93.jar

# 如果缺失，下载
mkdir -p lib && cd lib
wget https://varna.lri.fr/bin/VARNAv3-93.jar
```

### 3. varnaapi导入错误
```bash
pip install varnaapi
```

### 4. SVG不显示
- 检查浏览器控制台是否有错误
- 确认 `/api/varna/status` 返回 `available: true`
- 查看 `/api/visualize/varna` 返回的SVG内容

## 📊 性能优化

### 缓存SVG
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def render_varna_cached(seq, struct, options_hash):
    # 缓存相同参数的渲染结果
    pass
```

### 异步渲染
```python
from threading import Thread

def async_varna_render(data, callback):
    thread = Thread(target=render_and_callback, args=(data, callback))
    thread.start()
```

## 🎯 下一步

- [ ] 添加更多布局选项
- [ ] 实现SVG编辑功能
- [ ] 添加注释工具
- [ ] 支持批量渲染
- [ ] 导出高质量矢量图

## 📚 参考资料

- [VARNA官网](https://varna.lri.fr/)
- [varnaapi文档](https://github.com/VARNA-app/varnaapi)
- [VARNA布局算法](https://varna.lri.fr/index.php?pages=layouts)

---

**集成完成后，你的NUPACK Web App将同时支持：**
- ✅ D3.js交互式力导向图（探索用）
- ✅ VARNA专业渲染（发表用）

🎉 享受高质量的核酸结构可视化！
