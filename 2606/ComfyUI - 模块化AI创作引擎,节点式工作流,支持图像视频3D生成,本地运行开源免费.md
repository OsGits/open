# ComfyUI - 模块化AI创作引擎

## 项目介绍

ComfyUI 是当前最强大、最模块化的 AI 生成工具，采用节点式图形界面设计。它能让用户通过拖拽连接不同的模块来构建复杂的工作流，无需编码即可实现 AI 图像、视频、3D 模型和音频的生成。作为开源项目，ComfyUI 完全免费，支持本地部署，数据隐私完全由用户掌控。

## 核心特性

### 节点式模块化界面

ComfyUI 的核心创新在于其可视化的节点图形界面。用户可以将加载模型、文本编码、扩散采样、图像解码等各个步骤理解为独立的"节点"，通过连线将其连接成完整的工作流。这种设计让用户对 AI 生成的每个环节都拥有精确的控制权，可以自由调整参数、替换模型、添加预处理和后处理步骤。与传统的一键式 AI 工具相比，ComfyUI 提供了前所未有的灵活性和透明度。

### 广泛的开源模型支持

ComfyUI 原生支持所有主流开源模型，包括文生图模型如 Stable Diffusion 全系列（SD1.x、SD2.x、SDXL、SDXL Turbo）、Flux 系列、Lumina Image 2.0、HiDream、Qwen Image、Hunyuan Image 2.1 等。在视频生成领域支持 Stable Video Diffusion、Mochi、LTX-Video、Seedance 2.0 等前沿模型。此外还支持图像编辑模型如 Omnigen 2、Flux Kontext、HiDream E1.1，3D 生成模型如 TripoSplat、Rodin 2.5 等。ComfyUI 团队承诺在开源模型发布的第一天即提供支持，确保用户能尽快使用最新技术。

### 庞大的社区生态

ComfyUI 拥有极其活跃的开源社区，目前已有超过 5000 个社区扩展插件，共提供 60000+ 个自定义节点。当新模型发布时，社区开发者会迅速实现对应节点；当学术论文发表新技术时，相关扩展往往在几天内就会出现。这种快速迭代的生态使得 ComfyUI 的功能边界在不断扩展，用户可以找到涵盖工作流自动化、专业制作管道集成、AI 预处理与后处理等各类扩展。

### 本地运行与隐私保护

ComfyUI 可完全离线运行，安装设置完成后无需网络连接。用户的创意工作流、模型数据、生成内容都存储在本地机器上，不会被发送到任何外部服务器。这对于有严格数据安全要求的企业用户、对抗网络审查的用户、或仅仅是重视隐私的个人用户都具有重要价值。

### 跨平台支持与多硬件适配

ComfyUI 支持 Windows、Linux、macOS 三大操作系统。在硬件方面，除了广泛支持的 NVIDIA GPU 外，还支持 AMD GPU、Intel GPU、Apple Silicon（M系列芯片）以及华为昇腾等国产硬件。安装方式灵活多样，包括一键桌面应用安装、Windows 便携版、手动安装等多种方式，满足不同用户的需求。

## 应用场景

ComfyUI 适用于多种创意和生产场景。数字艺术家可以使用节点系统精确控制创作流程，实现传统工具难以达到的效果。AI 艺术爱好者可以通过组合不同模型创造独特的视觉效果。专业工作室可以将 ComfyUI 整合到现有的制作管道中，实现批量化和自动化生产。研究人员可以利用其模块化特性快速验证新模型和新算法。游戏开发者可以使用它来生成游戏资产、纹理、角色概念图等。

## 技术架构

ComfyUI 的核心架构基于 Python 和 PyQt构建，采用异步执行引擎处理节点图。模型加载采用多线程磁盘读取技术，显著加速了大型模型的加载过程。支持多种精度选项（FP32、FP16、INT8 等），用户可根据硬件条件在速度和质量间权衡。高级功能包括 MultiGPU 支持，可跨多块 GPU 分配计算任务；XPU 架构优化；智能 RAM 缓存管理等。

## 安装与使用

ComfyUI 提供多种安装方式，适用于不同需求和技术水平的用户。

### 安装方式一：桌面应用安装（推荐新手）

桌面应用是官方推荐的安装方式，提供一键安装、自动更新和图形化管理界面。

**下载地址**：访问 [https://www.comfy.org/download](https://www.comfy.org/download) 下载 ComfyUI 官方桌面客户端。

**安装步骤**：

1. 根据操作系统选择对应的安装包（Windows/macOS/Linux）
2. 运行安装程序，按照向导提示完成安装
3. 首次启动时，桌面应用会自动检测 NVIDIA GPU 驱动并下载必要的依赖
4. 首次运行会自动下载默认模型（如 SDXL），需要等待下载完成
5. 启动完成后，浏览器会自动打开 ComfyUI 界面

**优点**：
- 安装过程全自动，适合没有技术背景的用户
- 内置模型管理器，可方便地下载和管理各种模型
- 自动更新功能，保持版本最新
- 内置扩展管理器，一键安装社区节点

**缺点**：
- 不包含最新的代码更新（相对于 Git 版本可能有延迟）
- 对某些自定义工作流的支持可能不完整

---

### 安装方式二：Windows 便携版

便携版适合希望获取最新功能、有一定技术基础的用户。无需安装，下载后直接运行。

**下载地址**：从 GitHub Releases 页面下载压缩包
- 官方版本：[ComfyUI Release](https://github.com/comfyanonymous/ComfyUI/releases)
- 独立完整包（推荐国内用户，包含模型下载）：[BTBTC 镜像站](https://btbtc.fun/download/comfyui/)

**安装步骤**：

1. 下载最新版本的 ZIP 压缩包（约 500MB-1GB）
2. 解压到任意目录（建议使用纯英文路径）
3. 运行 `run_cpu.bat`（仅 CPU 运行）或 `run_nvidia_gpu.bat`（NVIDIA GPU）或 `run_edit.bat`（编辑模式启动）
4. 等待模型下载完成后，浏览器自动打开界面

**常用启动脚本说明**：

| 脚本文件 | 适用场景 |
|---------|---------|
| run_nvidia_gpu.bat | NVIDIA 显卡用户（推荐） |
| run_cpu.bat | 无独立显卡，仅使用 CPU |
| run_edit.bat | 使用编辑器模式启动 |
| directml.bat | AMD 显卡（DirectML） |

**进阶配置**：

如需自定义启动参数，可创建快捷方式并修改目标：
```
.\python_embeded\python.exe -s ComfyUI\main.py --listen 0.0.0.0 --port 8188 --force-fp16
```

常用参数：
- `--listen 0.0.0.0`：允许局域网其他设备访问
- `--port 8188`：自定义端口号
- `--force-fp16`：强制使用半精度，降低显存占用
- `--lowvram`：针对显存较小的显卡优化
- `--novnc`：启用无头模式（无界面运行）

**优点**：
- 下载即用，无需安装环境
- 获取 Git 最新提交的功能
- 可同时运行多个不同版本
- 便于备份和迁移

**缺点**：
- 需要手动检查和安装更新
- 不包含自动模型下载功能
- 需要手动安装依赖扩展

---

### 安装方式三：手动安装（开发者/全平台）

手动安装方式适合所有操作系统，支持各类 GPU（NVIDIA/AMD/Intel/Apple Silicon/华为昇腾），也方便开发者参与项目开发。

**前置要求**：
- Python 3.11+ 环境
- Git 版本控制工具
- 对应 GPU 的驱动和计算库

**安装步骤**：

1. **克隆仓库**：
```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

2. **创建虚拟环境**（推荐）：
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. **安装依赖**：
```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/<你的平台>
pip install -r requirements.txt
```

常用 PyTorch 下载源：
| 平台 | 下载 URL |
|-----|---------|
| NVIDIA CUDA 12.1 | `https://download.pytorch.org/whl/cu121` |
| NVIDIA CUDA 12.4 | `https://download.pytorch.org/whl/cu124` |
| AMD ROCm (Linux) | `https://download.pytorch.org/whl/rocm6.1` |
| Apple Silicon | 使用默认 PyPI 源即可 |

4. **下载模型**：
```bash
# 创建模型目录
mkdir -p models/checkpoints models/vae models/lora

# 可使用官方模型下载脚本（需要科学上网）
python scripts/download_models.py

# 或手动下载模型放入对应目录
# SDXL 模型：https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
```

5. **启动 ComfyUI**：
```bash
# 仅 CPU 模式
python main.py --cpu

# NVIDIA GPU（推荐）
python main.py

# AMD GPU（Linux）
python main.py --directml
```

**NVIDIA 显卡优化参数**：
```bash
# 低显存配置（4-6GB）
python main.py --lowvram --force-fp16

# 中等显存配置（8-12GB）
python main.py --force-fp16

# 高性能配置（24GB+）
python main.py --fp16-e4m3fn
```

**Apple Silicon (M1/M2/M3) 配置**：
```bash
pip install torch torchvision torchaudio
pip install --pre MPS backend
python main.py
```

**华为昇腾配置**：
```bash
pip install torch-npu  # 需要安装 CANN 工具链
python main.py
```

**优点**：
- 完全控制，可自定义所有配置
- 第一时间体验最新功能
- 支持所有硬件平台
- 便于调试和开发
- 可安装任意扩展和自定义节点

**缺点**：
- 需要手动管理依赖和环境
- 更新需要手动拉取最新代码
- 对用户技术要求较高

---

### 安装后的基本使用

**模型存放位置**：
| 模型类型 | 存放目录 |
|---------|---------|
| Checkpoint（大模型） | `models/checkpoints/` |
| VAE | `models/vae/` |
| LoRA | `models/loras/` |
| Embedding | `models/embeddings/` |
| ControlNet | `models/controlnet/` |
| IP-Adapter | `models/ipadapter/` |

**常用快捷键**：
- `Ctrl + 鼠标滚轮`：缩放画布
- `空格 + 拖拽`：平移画布
- `Ctrl + S`：保存工作流为 JSON
- `Ctrl + V`：从剪贴板加载工作流
- `双击空白处`：搜索添加节点

**安装社区扩展**：
1. 在界面右下角找到 "Manager" 按钮
2. 点击 "Install Custom Nodes"
3. 搜索并选择要安装的扩展
4. 重启 ComfyUI 生效

## 总结

ComfyUI 代表了开源 AI 生成工具的最高水平，它将复杂的 AI 模型能力通过模块化节点界面呈现给用户，实现了专业级控制与易用性的平衡。活跃的社区生态保证了项目的持续进化，跨平台支持和广泛的硬件适配使其具有极佳的可访问性。无论是个人创作者还是专业团队，ComfyUI 都是探索 AI 创意边界的强大平台。

**开源协议**：GPL-3.0

**GitHub**：https://github.com/comfyanonymous/ComfyUI

**官方网站**：https://www.comfy.org
