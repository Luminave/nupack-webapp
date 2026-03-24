/**
 * VARNA前端集成代码
 * 将此文件添加到 static/ 目录，并在 index.html 中引入
 */

// VARNA状态
let varnaAvailable = false;
let currentVarnaSVG = null;

/**
 * 检查VARNA是否可用
 */
async function checkVarnaStatus() {
    try {
        const response = await fetch('/api/varna/status');
        const data = await response.json();
        varnaAvailable = data.available;
        
        if (varnaAvailable) {
            console.log('✅ VARNA可用');
            showVarnaOptions();
        } else {
            console.log('⚠️  VARNA不可用');
            hideVarnaOptions();
        }
        
        return varnaAvailable;
    } catch (error) {
        console.error('检查VARNA状态失败:', error);
        varnaAvailable = false;
        return false;
    }
}

/**
 * 显示VARNA选项
 */
function showVarnaOptions() {
    const varnaBtn = document.getElementById('btn-varna-render');
    if (varnaBtn) {
        varnaBtn.style.display = 'inline-block';
        varnaBtn.disabled = false;
    }
    
    const varnaMode = document.getElementById('viz-mode-varna');
    if (varnaMode) {
        varnaMode.disabled = false;
    }
}

/**
 * 隐藏VARNA选项
 */
function hideVarnaOptions() {
    const varnaBtn = document.getElementById('btn-varna-render');
    if (varnaBtn) {
        varnaBtn.style.display = 'none';
    }
    
    const varnaMode = document.getElementById('viz-mode-varna');
    if (varnaMode) {
        varnaMode.disabled = true;
    }
}

/**
 * 使用VARNA渲染结构
 * @param {string} sequence - 序列（多链用+分隔）
 * @param {string} structure - 点括号结构（多链用+分隔）
 * @param {Array} pairsMatrix - 配对概率矩阵（可选）
 * @param {Object} options - 额外选项
 */
async function renderWithVarna(sequence, structure, pairsMatrix = null, options = {}) {
    if (!varnaAvailable) {
        showNotification('VARNA不可用，请检查服务端配置', 'error');
        return;
    }
    
    // 显示加载状态
    const container = document.getElementById('varna-container');
    if (container) {
        container.innerHTML = '<div class="loading">🎨 VARNA渲染中...</div>';
        container.style.display = 'block';
    }
    
    try {
        const response = await fetch('/api/visualize/varna', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                sequence: sequence,
                structure: structure,
                pairs_matrix: pairsMatrix,
                show_probability: options.showProbability !== false,
                layout: options.layout || 'naview',
                style: options.style || {}
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 保存当前SVG
            currentVarnaSVG = data.svg;
            
            // 显示SVG
            if (container) {
                container.innerHTML = data.svg;
                
                // 添加交互功能
                addVarnaInteractions(container);
            }
            
            // 显示下载按钮
            showVarnaDownloadButtons();
            
            showNotification('VARNA渲染完成', 'success');
            
            return data;
        } else {
            throw new Error(data.error || 'VARNA渲染失败');
        }
        
    } catch (error) {
        console.error('VARNA渲染错误:', error);
        
        if (container) {
            container.innerHTML = `
                <div class="error-message">
                    <p>❌ VARNA渲染失败</p>
                    <p class="error-detail">${error.message}</p>
                    ${error.message.includes('VARNA不可用') ? 
                        '<p class="install-hint">请确保已安装Java并下载VARNA jar文件</p>' : ''}
                </div>
            `;
        }
        
        showNotification('VARNA渲染失败: ' + error.message, 'error');
        return null;
    }
}

/**
 * 增强版VARNA渲染
 * @param {string} sequence - 序列
 * @param {string} structure - 结构
 * @param {Array} pairsMatrix - 配对概率矩阵
 * @param {Object} enhancements - 增强选项
 */
async function renderWithVarnaEnhanced(sequence, structure, pairsMatrix, enhancements = {}) {
    if (!varnaAvailable) {
        showNotification('VARNA不可用', 'error');
        return;
    }
    
    const container = document.getElementById('varna-container');
    if (container) {
        container.innerHTML = '<div class="loading">🎨 VARNA增强渲染中...</div>';
        container.style.display = 'block';
    }
    
    try {
        const response = await fetch('/api/visualize/varna/enhanced', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                sequence: sequence,
                structure: structure,
                pairs_matrix: pairsMatrix,
                title: enhancements.title || '',
                highlight_regions: enhancements.highlightRegions || [],
                annotations: enhancements.annotations || [],
                show_sequence: enhancements.showSequence !== false,
                show_bases: enhancements.showBases !== false
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentVarnaSVG = data.svg;
            
            if (container) {
                container.innerHTML = data.svg;
                addVarnaInteractions(container);
            }
            
            showVarnaDownloadButtons();
            showNotification('VARNA增强渲染完成', 'success');
            
            return data;
        } else {
            throw new Error(data.error || '渲染失败');
        }
        
    } catch (error) {
        console.error('VARNA增强渲染错误:', error);
        
        if (container) {
            container.innerHTML = `
                <div class="error-message">
                    <p>❌ 增强渲染失败</p>
                    <p class="error-detail">${error.message}</p>
                </div>
            `;
        }
        
        showNotification('增强渲染失败: ' + error.message, 'error');
        return null;
    }
}

/**
 * 为VARNA SVG添加交互功能
 */
function addVarnaInteractions(container) {
    const svg = container.querySelector('svg');
    if (!svg) return;
    
    // 添加缩放功能
    let scale = 1;
    const minScale = 0.5;
    const maxScale = 3;
    
    svg.style.transformOrigin = 'center';
    
    // 鼠标滚轮缩放
    container.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.1 : 0.1;
        scale = Math.max(minScale, Math.min(maxScale, scale + delta));
        svg.style.transform = `scale(${scale})`;
    });
    
    // 双击重置
    svg.addEventListener('dblclick', () => {
        scale = 1;
        svg.style.transform = 'scale(1)';
    });
}

/**
 * 显示VARNA下载按钮
 */
function showVarnaDownloadButtons() {
    const downloadDiv = document.getElementById('varna-downloads');
    if (downloadDiv) {
        downloadDiv.style.display = 'block';
    }
}

/**
 * 隐藏VARNA下载按钮
 */
function hideVarnaDownloadButtons() {
    const downloadDiv = document.getElementById('varna-downloads');
    if (downloadDiv) {
        downloadDiv.style.display = 'none';
    }
}

/**
 * 下载VARNA SVG
 */
function downloadVarnaSVG() {
    if (!currentVarnaSVG) {
        showNotification('没有可下载的SVG', 'warning');
        return;
    }
    
    const blob = new Blob([currentVarnaSVG], {type: 'image/svg+xml'});
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `structure_varna_${Date.now()}.svg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    URL.revokeObjectURL(url);
    showNotification('SVG已下载', 'success');
}

/**
 * 下载VARNA PNG（从SVG转换）
 */
function downloadVarnaPNG() {
    if (!currentVarnaSVG) {
        showNotification('没有可转换的SVG', 'warning');
        return;
    }
    
    showNotification('正在转换为PNG...', 'info');
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    // 获取SVG尺寸
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(currentVarnaSVG, 'image/svg+xml');
    const svgElement = svgDoc.querySelector('svg');
    const width = parseInt(svgElement.getAttribute('width') || 800);
    const height = parseInt(svgElement.getAttribute('height') || 600);
    
    // 设置canvas尺寸（2x for high DPI）
    const scale = 2;
    canvas.width = width * scale;
    canvas.height = height * scale;
    ctx.scale(scale, scale);
    
    img.onload = function() {
        // 白色背景
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, width, height);
        
        // 绘制SVG
        ctx.drawImage(img, 0, 0, width, height);
        
        // 下载PNG
        canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `structure_varna_${Date.now()}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showNotification('PNG已下载', 'success');
        }, 'image/png');
    };
    
    img.onerror = function() {
        showNotification('SVG转PNG失败', 'error');
    };
    
    // 设置SVG源
    const svgBlob = new Blob([currentVarnaSVG], {type: 'image/svg+xml;charset=utf-8'});
    img.src = URL.createObjectURL(svgBlob);
}

/**
 * 在单链分析结果中集成VARNA
 */
function integrateVarnaWithSingleAnalysis(result) {
    // 添加VARNA渲染按钮
    const controlsDiv = document.getElementById('single-controls');
    if (!controlsDiv) return;
    
    // 检查是否已有按钮
    if (document.getElementById('btn-varna-render')) return;
    
    const varnaBtn = document.createElement('button');
    varnaBtn.id = 'btn-varna-render';
    varnaBtn.className = 'btn btn-primary';
    varnaBtn.innerHTML = '🎨 VARNA渲染';
    varnaBtn.style.marginLeft = '10px';
    varnaBtn.onclick = () => {
        renderWithVarna(
            result.sequence,
            result.mfe_structure,
            result.pairs_matrix,
            {
                showProbability: true,
                layout: 'naview'
            }
        );
    };
    
    // 添加到控制面板
    const d3Btn = controlsDiv.querySelector('button');
    if (d3Btn && d3Btn.nextSibling) {
        controlsDiv.insertBefore(varnaBtn, d3Btn.nextSibling);
    } else {
        controlsDiv.appendChild(varnaBtn);
    }
    
    // 根据VARNA状态显示/隐藏
    if (varnaAvailable) {
        varnaBtn.style.display = 'inline-block';
    } else {
        varnaBtn.style.display = 'none';
    }
}

/**
 * 在多链分析结果中集成VARNA
 */
function integrateVarnaWithTubeAnalysis(complexes) {
    // 为每个复合物添加VARNA渲染选项
    complexes.forEach((comp, index) => {
        const containerId = `complex-${index}`;
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const varnaBtn = document.createElement('button');
        varnaBtn.className = 'btn btn-secondary btn-sm';
        varnaBtn.innerHTML = '🎨 VARNA';
        varnaBtn.style.marginTop = '5px';
        varnaBtn.onclick = () => {
            renderWithVarna(
                comp.sequence,
                comp.mfe_structure,
                null,  // 多链暂不使用配对概率
                {
                    showProbability: false,
                    layout: 'radiate'
                }
            );
        };
        
        if (varnaAvailable) {
            container.appendChild(varnaBtn);
        }
    });
}

/**
 * 复制VARNA SVG到剪贴板
 */
async function copyVarnaSVGToClipboard() {
    if (!currentVarnaSVG) {
        showNotification('没有SVG可复制', 'warning');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(currentVarnaSVG);
        showNotification('SVG已复制到剪贴板', 'success');
    } catch (error) {
        console.error('复制失败:', error);
        showNotification('复制失败', 'error');
    }
}

// 页面加载时检查VARNA状态
document.addEventListener('DOMContentLoaded', () => {
    checkVarnaStatus();
});

// 导出函数（供外部调用）
window.VarnaRenderer = {
    check: checkVarnaStatus,
    render: renderWithVarna,
    renderEnhanced: renderWithVarnaEnhanced,
    downloadSVG: downloadVarnaSVG,
    downloadPNG: downloadVarnaPNG,
    copySVG: copyVarnaSVGToClipboard,
    integrateSingle: integrateVarnaWithSingleAnalysis,
    integrateTube: integrateVarnaWithTubeAnalysis
};
