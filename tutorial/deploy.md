# NUPACK Development Environment Deployment Tutorial (Windows)

# NUPACK 开发环境部署教程（Windows）

> This tutorial walks you through setting up NUPACK on Windows via Python, and connecting it with AI coding tools for complex computations.
> 本教程介绍如何在 Windows 电脑上通过 Python 使用 NUPACK 进行计算，并接入 AI 编程工具以实现复杂计算。

---

## Part 1: WSL Deployment / 第一部分：WSL 部署

### 1.1 Install WSL / 安装 WSL

Open PowerShell and run:

打开 PowerShell，执行：

```powershell
wsl --install
```

This step takes a while. Wait for it to finish, then restart your computer when prompted.

这一步比较慢，等它自己执行完。安装完成后，按提示重启电脑。

After restart, verify the installation:

重启后，验证安装：

```powershell
wsl --list --verbose
```

If no distribution is installed, check available distributions:

如果没有安装发行版，查看可用列表：

```powershell
wsl --list --online
wsl.exe --install Ubuntu-26.04
```

Another restart may be required.

可能需要再次重启电脑。

After restart, open **WSL Settings** from the Start menu.

重启后，在开始菜单中找到 **WSL Settings** 并打开。

### 1.2 Update System & Install Base Packages / 更新系统并安装基础包

In the WSL terminal:

在 WSL 终端中执行：

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git build-essential cmake
```

### 1.3 Install NUPACK / 安装 NUPACK

Since the NUPACK package requires an older Python version, we need to set up a virtual environment with the correct Python.

因为 NUPACK 包需要旧版本的 Python，需要配置对应版本的 Python 虚拟环境。

First, extract the NUPACK package to a location on your computer (e.g., `D:/`).

首先，将 NUPACK 包解压到电脑的某个位置（例如 `D:/`）。

#### Add deadsnakes PPA for older Python versions / 添加 deadsnakes PPA 获取旧版 Python

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

#### Install Python 3.12 / 安装 Python 3.12

```bash
sudo apt install -y python3.12 python3.12-venv python3.12-dev
```

#### Create virtual environment / 创建虚拟环境

```bash
python3.12 -m venv ~/nupack-env
source ~/nupack-env/bin/activate
```

Verify the Python version:

确认 Python 版本：

```bash
python --version
# Should show: Python 3.12.x
```

#### Install NUPACK / 安装 NUPACK

```bash
pip install /mnt/d/nupack-4.0.2.0/package/nupack-4.0.2.0-cp312-cp312-linux_x86_64.whl
```

Verify the installation:

验证安装：

```bash
python -c "import nupack; print(nupack.version)"
```

### 1.4 Install NUPACK WEBAPP / 安装 NUPACK WEBAPP

At this point, the WSL environment has Python and NUPACK configured. Now install the NUPACK Web App (for simple calculations).

此时 WSL 内部已配制好 Python 和 NUPACK 环境，接下来安装 NUPACK WEBAPP（用于简单的计算）。

#### Clone the repository / 克隆仓库

```bash
git clone https://github.com/Luminave/nupack-webapp.git
cd nupack-webapp
```

> If your terminal cannot connect to GitHub, download the source code as a ZIP from the repository page, extract it to a specific directory on your computer (e.g., `D:/`), then use `cd` to enter the extracted folder.
>
> 如果终端无法连接到 GitHub，请到仓库页面将源码打包下载下来，解压到电脑上的特定目录（如 `D:/`），随后用 `cd` 命令进入解压出来的文件夹。例如：
>
> ```bash
> cd /mnt/d/nupack-webapp
> ```

#### Run the install script / 运行安装脚本

```bash
./install.sh
```

The script will automatically install dependencies. You should see output like:

脚本会自动安装依赖。你将看到类似以下的输出：

```
==============================================
 NUPACK Web 安装程序
==============================================

>>> 检查 Python 版本...
 Python 版本: 3.12.3

>>> 检查 NUPACK 是否已安装...
NUPACK 版本: 4.0.2.0
 ✅ NUPACK 已安装

>>> 安装 Python 依赖...
 ✅ 依赖安装完成

>>> 创建项目目录...
 ✅ 项目目录已创建: ~/nupack-projects

==============================================
 ✅ 安装完成！
==============================================
```

#### Start the server / 启动服务器

Make sure you are still in the project directory, then run:

确保仍在项目文件夹中，然后执行：

```bash
./start.sh
```

You should see:

你将看到：

```
==============================================
 🧬 NUPACK Web
==============================================

 本地访问: http://127.0.0.1:5000

 按 Ctrl+C 停止服务
==============================================
```

#### Open in browser / 在浏览器中打开

Open your computer's browser and visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to start using NUPACK Web App.

打开电脑浏览器，访问 [http://127.0.0.1:5000](http://127.0.0.1:5000) 即可开始使用。

> **Note / 注意：** If you cannot access the page, the port may be blocked or in use. In this case, consider installing Ubuntu 26.04 with a desktop environment in VMware, follow the same installation steps, and access the interface using the virtual machine's own browser.
>
> 如果访问不了，可能是端口被屏蔽或占用。如遇这种情况，建议在 VMware 中安装带有图形界面的 Ubuntu 26.04，按照相同方法安装好后，用虚拟机本身的浏览器访问操作界面。

---

## Part 2: VS Code + WSL + Claude Code + MiMo / 第二部分：VS Code + WSL + Claude Code + MiMo

> **Note:** This section uses the MiMo model as an example. You can also use other VS Code extensions or other large language models.
>
> **提示：** 此步骤以 MiMo 模型作为例子，你也可以使用其他的 VS Code 插件或者其他大语言模型。

### 2.1 Install VS Code / 安装 VS Code

Download and install VS Code from the official website.

从官网下载并安装 VS Code。

🔗 [https://code.visualstudio.com/](https://code.visualstudio.com/)

### 2.2 Install Claude Code Extension / 安装 Claude Code 插件

1. Open VS Code
2. Install the **Claude Code for VS Code** extension
3. Open Settings and search for `Claude Code`
4. Check **Disable Login Prompt** to skip login

### 2.3 Configure API / 配置 API

In settings, find **Environment Variables** and add the following under `claudeCode.environmentVariables`:

在设置中找到 **Environment Variables**，在 `claudeCode.environmentVariables` 中添加以下配置：

```json
{
    "name": "ANTHROPIC_BASE_URL",
    "value": "https://api.xiaomimimo.com/anthropic"
},
{
    "name": "ANTHROPIC_AUTH_TOKEN",
    "value": "your-api-key-here"
},
{
    "name": "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "value": "mimo-v2-flash"
},
{
    "name": "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "value": "mimo-v2-flash"
},
{
    "name": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "value": "mimo-v2-flash"
}
```

Replace `your-api-key-here` with your actual API key. Use the Anthropic-format API interface for configuration.

将 `your-api-key-here` 替换为你的实际 API key。选择 anthropic 格式的 API 接口来配置。

Restart VS Code after configuration. You should see the Claude Code chat interface.

配置完成后重启 VS Code，即可看到 Claude Code 的聊天界面。

### 2.4 Install WSL Extension / 安装 WSL 插件

1. Press **Ctrl + Shift + P** to open the Command Palette
2. Type `WSL: Connect to WSL` and select it
3. VS Code will automatically connect to WSL

After successful connection:
- A green **WSL: Ubuntu** indicator appears in the bottom-left corner

连接成功后：
- VS Code 左下角会显示绿色的 **WSL: Ubuntu** 字样

You'll need to reinstall Python and Claude Code extensions in the WSL environment, but no reconfiguration is needed.

需要在 WSL 环境中重新安装 Python 和 Claude Code 插件，但无需重新配置。

### 2.5 Disconnect from WSL / 退出 WSL 环境

To exit the WSL environment:

如果要退出 WSL 环境：

1. Look at the green **WSL: Ubuntu** indicator in the bottom-left corner
2. Click it to open the Command Palette
3. Select **Close Remote Connection**
4. VS Code will restart and return to Windows local mode

---

*Document by Victor.Guo | NUPACK Web App*
