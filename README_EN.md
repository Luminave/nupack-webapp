# NUPACK Web v1.5.0 - Nucleic Acid Structure Visualization Tool

> 📖 **Tutorials**:
> - [📘 User Guide](tutorial/guide.md) — Feature documentation
> - [📖 Deployment Guide](tutorial/deploy.md) — Windows (WSL) installation steps

A localized web interface for nucleic acid analysis based on Flask + NUPACK, providing an intuitive visualization experience.

**[中文文档 / Chinese Documentation](README.md)**

## 🆕 v1.5.0 Changelog

### 🔬 Advanced Mode
- New "Advanced Mode": input sequence + dot-bracket structure, direct visualization
- Support pasting pairing probability matrix or recalculating via NUPACK
- Bases colored by probability (with matrix) or by type (without)
- VARNA export available with or without matrix

### 🌡️ Pairing Probability Matrix Enhancements
- Gradient color legend bar added to all heatmaps
- "📥 Export Image" button on all heatmaps (3x high-res PNG)

### 📖 Tutorial System
- Online tutorial pages (`/tutorial`) rendered with marked.js
- User Guide: feature documentation, bilingual (EN/ZH)
- Deployment Guide: complete Windows WSL installation steps

### 🔧 Bug Fixes
- Fixed `Too many suboptimal structures` crash in subopt analysis
- Auto energy gap mode (automatic gap selection based on sequence length)
- Fixed VARNA export image clipping (auto viewBox + padding)
- Fixed VARNA export probability coloring
- Fixed JavaScript syntax errors (page freeze issue)
- Added "View All Structures" and "View Raw Data" to multi-strand analysis

### 📦 Other Updates
- Version updated to v1.5.0
- Header: new "📘 Guide" and "🔄 Check Update" buttons
- Donate link updated to ifdian.net

---

## 🆕 v1.4.0 Changelog

### 🎨 VARNA Structure Export
- VARNA engine integration for publication-quality RNA/DNA secondary structure visualization
- High-quality SVG vector graphics with probability gradient coloring
- Multi-chain structure support with citation prompt

### 📦 Other Updates
- Desktop launcher script, auto browser launch
- Java auto-detection and installation

## 🆕 v1.3.0 Changelog

### 🔄 Auto Layout
- Force-directed layout algorithm using D3.js
- Compact layout, lock layout, rotate features
- Multi-chain mode, improved zoom, line width control

## ✨ Features

### 🔬 Single-Strand Analysis
- Minimum Free Energy (MFE) structure calculation
- Pairing probability matrix visualization
- Suboptimal structure analysis (auto/manual energy gap)
- Force-directed graph visualization with interactive controls

### 🧬 Multi-Strand Analysis
- Test tube analysis with multiple strands
- Complex concentration distribution pie chart
- All structures list + raw data view

### 🎨 Sequence Design
- Domain definition (N/R/Y notation support)
- Target complex design with automatic optimal selection

### 🧪 Advanced Mode
- Input sequence + dot-bracket for direct visualization
- Pairing probability matrix input/recalculation
- VARNA export

### 📦 Other Features
- Chinese/English interface / Dark/Light theme
- Customizable base colors
- Pairing probability heatmap (gradient legend + export)
- PNG, JSON, CSV export
- Check for updates (GitHub version comparison)

## 📋 System Requirements

- Python 3.8+ (3.12 recommended)
- NUPACK 4.0+
- Java 11+ (full version, required for VARNA)

## 🚀 Quick Installation

### Linux / macOS

```bash
# Clone repository
git clone https://github.com/Luminave/nupack-webapp.git
cd nupack-webapp

# Run installation script
./install.sh

# Start
./start.sh
```

Open in browser: http://127.0.0.1:5000

### Windows (WSL)

See [📖 Deployment Guide](tutorial/deploy.md) for complete WSL + Python + NUPACK installation steps.

Quick steps:
1. Install WSL (`wsl --install`) and set up Ubuntu
2. Install Python 3.12 and create virtual environment
3. Install NUPACK wheel package
4. Clone this repo and run `./install.sh` + `./start.sh`
5. Open http://127.0.0.1:5000 in Windows browser

## 🔬 Virtual Environment Installation

```bash
git clone https://github.com/Luminave/nupack-webapp.git
cd nupack-webapp
python3 -m venv venv
source venv/bin/activate
pip install nupack
pip install -r requirements.txt
python3 app.py
```

## 📖 Usage Examples

### Single-Strand Analysis
```
Sequence: GCGCAAAAGCGC
```
Forms a hairpin structure — good for testing suboptimal analysis.

### Multi-Strand Analysis
```
Strand A: GCGCAAAAGCGC (1e-6 M)
Strand B: GCGCTTTTGCGC (1e-6 M)
```

### Sequence Design
```
Domain: a = N10
Target strands: S1 = a, S2 = ~a
Target complex: S1,S2 structure ..........+..........
```

## ❓ FAQ

**Q: `ModuleNotFoundError: No module named 'nupack'`**
> NUPACK is not installed. Please complete installation first.

**Q: `ModuleNotFoundError: No module named 'flask'`**
> Run `pip install flask` or `./install.sh`

**Q: Port 5000 is occupied**
> Change the port in the last line of `app.py`

**Q: Installation script has no permission**
> Run `chmod +x install.sh start.sh`

## 🙏 Acknowledgments

- [NUPACK](https://www.nupack.org/) - Nucleic acid structure prediction
- [D3.js](https://d3js.org/) - Data visualization library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [VARNA](https://varna.lisn.upsaclay.fr/) - RNA structure visualization

## 📄 License

This project is for learning and research purposes only. Use of NUPACK requires compliance with the NUPACK license agreement.

---

**Author**: Victor.Guo
**GitHub**: https://github.com/Luminave/nupack-webapp
