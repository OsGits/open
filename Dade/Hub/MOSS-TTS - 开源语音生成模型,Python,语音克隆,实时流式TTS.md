# MOSS-TTS - 开源语音生成模型

## 项目信息

| 项目 | 信息 |
|------|------|
| **名称** | MOSS-TTS |
| **类型** | AI语音生成 |
| **语言** | Python |
| **Stars** | 2,700+ |
| **来源** | GitHub (OpenMOSS) |
| **地址** | https://github.com/OpenMOSS/MOSS-TTS |

## 项目介绍

MOSS-TTS 是一款开源语音和声音生成模型系列，专为高保真、多说话人对话、语音克隆和实时流式 TTS 设计。它涵盖从稳定的长时间语音生成到环境音效的各个方面。

**核心特点：**
- 开源 TTS 可与商业 API 媲美
- 支持语音克隆
- 实时流式 TTS
- 环境音效生成
- 多说话人支持
- 无需按字符计费，无速率限制

**适用场景：**
- 语音应用开发者
- 播客制作
- 无障碍工具
- 需要 TTS 但不想支付 API 费用的场景

---

## 安装教程

### 环境要求

- Python 3.8+
- CUDA 11.7+ (GPU推理)
- 16GB+ RAM

### 方法一：pip 安装

```bash
# 安装基础版本
pip install moss-tts

# 或从源码安装
git clone https://github.com/OpenMOSS/MOSS-TTS.git
cd MOSS-TTS
pip install -e .
```

### 方法二：Docker 部署

```bash
# 拉取镜像
docker pull ghcr.io/openmoss/moss-tts:latest

# 运行容器
docker run -p 7860:7860 --gpus all \
  -v ./output:/app/output \
  ghcr.io/openmoss/moss-tts:latest
```

### 方法三：本地开发环境

```bash
# 克隆仓库
git clone https://github.com/OpenMOSS/MOSS-TTS.git
cd MOSS-TTS

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 下载预训练模型
python -m moss_tts download --model moss-tts-v1

# 运行演示
python -m moss_tts serve
```

---

## 快速使用

### 命令行使用

```bash
# 文本转语音
moss-tts synthesize --text "你好，欢迎使用MOSS-TTS" --output speech.wav

# 使用特定说话人
moss-tts synthesize --text "Hello world" --speaker alice --output hello.wav

# 语音克隆
moss-tts clone --reference audio.wav --text "这是克隆的声音" --output cloned.wav
```

### Python API

```python
from moss_tts import MOSS

# 初始化模型
tts = MOSS("moss-tts-v1")

# 基础合成
audio = tts.synthesize("你好，MOSS-TTS是一个开源的语音生成模型")
tts.save(audio, "output.wav")

# 多说话人
audio = tts.synthesize(
    text="欢迎收听今天的节目",
    speaker="female_teacher",
    speed=1.0
)

# 语音克隆
audio = tts.clone(
    reference="reference.wav",
    text="这是克隆后的声音"
)
```

### Gradio Web UI

```bash
# 启动 Web 界面
python -m moss_tts.gradio

# 访问 http://localhost:7860
```

---

## API 服务

### 启动 API 服务

```bash
# 启动 FastAPI 服务
python -m moss_tts.api --port 8000

# 或使用 uvicorn
uvicorn moss_tts.api:app --host 0.0.0.0 --port 8000
```

### API 调用示例

```bash
# curl 调用
curl -X POST http://localhost:8000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "你好", "speaker": "default"}' \
  --output output.wav
```

```python
import requests

response = requests.post(
    "http://localhost:8000/synthesize",
    json={"text": "你好，MOSS-TTS", "speaker": "default"}
)
with open("output.wav", "wb") as f:
    f.write(response.content)
```

---

## 模型列表

| 模型 | 描述 | 适用场景 |
|------|------|----------|
| MOSS-TTS-Local-Transformer-v1.5 | 基础模型，支持流式 | 通用TTS |
| MOSS-TTS-SLM-v1 | 轻量级模型 | 低资源设备 |
| MOSS-Clone | 语音克隆 | 个性化声音 |

---

## 常见问题

**Q: GPU显存不足怎么办？**
A: 使用量化版本或选择轻量级模型 SLM

**Q: 如何支持中文？**
A: 模型默认支持多语言，中文无需额外配置

**Q: 实时流式输出如何实现？**
A: 使用 `--stream` 参数或 Python API 的 `stream_synthesize()` 方法

---

## 相关资源

- [GitHub 仓库](https://github.com/OpenMOSS/MOSS-TTS)
- [模型下载](https://huggingface.co/OpenMOSS/MOSS-TTS)
- [在线演示](https://huggingface.co/spaces/OpenMOSS/MOSS-TTS)
- [Discord 社区](https://discord.gg/openmoss)
