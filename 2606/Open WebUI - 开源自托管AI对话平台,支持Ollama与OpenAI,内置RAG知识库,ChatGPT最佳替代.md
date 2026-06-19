---
title: Open WebUI - 开源自托管AI对话平台,支持Ollama与OpenAI,内置RAG知识库,ChatGPT最佳替代
id: 019ed0ca-e8c0-72b2-9da9-ede42c585797
date: 2026-06-16 22:17:04
auther: loveos
cover: /upload/demo.png
excerpt: 项目简介 Open WebUI 是一款功能丰富、用户友好的开源自托管 AI 对话平台，被誉为自建版 ChatGPT 的最佳选择。项目采用 Python（FastAPI）开发后端、Svelte 构建前端，支持完全离线运行，可连接 Ollama 本地模型和 OpenAI 兼容 API（包括 LMStud
permalink: /2026/wei-ming-ming-wen-zhang
categories:
 - Github
tags: 
 - aidui-hua-ping-tai
 - zi-tuo-guan-chatgpt
 - ollama
 - Project.Recommendation
 - github
 - docker
 - Source.Code.Recommendation
---

### 项目简介

Open WebUI 是一款功能丰富、用户友好的**开源自托管 AI 对话平台**，被誉为自建版 ChatGPT 的最佳选择。项目采用 Python（FastAPI）开发后端、Svelte 构建前端，支持完全离线运行，可连接 Ollama 本地模型和 OpenAI 兼容 API（包括 LMStudio、GroqCloud、Mistral、OpenRouter 等）。Open WebUI 内置 RAG（检索增强生成）引擎，支持文档上传与知识库问答，提供语音通话、图片生成、Web 搜索等高级功能。

Open WebUI 在 GitHub 上拥有超过 80k Stars，是开源 AI 应用领域最受欢迎的项目之一，界面设计精美，支持多语言（含中文），提供 PWA 移动端应用体验。

### 界面预览

![demo.png](/upload/demo.png)
Open WebUI 提供类似 ChatGPT 的现代化对话界面，左侧为对话历史列表，右侧为主聊天区域，支持深色/浅色主题切换，界面简洁美观，支持桌面端和移动端自适应布局。

### 核心功能

- **多模型支持**：同时连接 Ollama 本地模型和 OpenAI 兼容 API，支持在对话中切换不同模型
- **内置 RAG 知识库**：上传 PDF、Word、Excel 等文档，通过 9 种向量数据库实现本地知识检索问答
- **Web 搜索集成**：支持 15+ 搜索引擎（SearXNG、Google、Brave、DuckDuckGo、Bing 等），将搜索结果注入对话
- **语音与视频通话**：集成多种语音识别（Whisper、Deepgram）和语音合成引擎，支持免提语音对话
- **图片生成与编辑**：支持 DALL-E、ComfyUI、AUTOMATIC1111 等引擎进行 AI 绘图和图片编辑
- **模型构建器**：通过 Web 界面直接创建和管理 Ollama 模型，无需命令行操作
- **Python 函数调用**：内置代码编辑器，支持编写纯 Python 函数扩展 LLM 能力
- **Markdown 和 LaTeX**：完整支持 Markdown 渲染和 LaTeX 数学公式显示
- **多用户与权限管理**：支持用户组、角色权限控制（RBAC），适合团队和企业部署
- **企业级认证**：支持 LDAP/AD、OAuth、SCIM 2.0 自动化用户配置、SSO 单点登录
- **PWA 移动应用**：支持添加到手机主屏幕，获得原生应用体验
- **Pipeline 插件系统**：通过 Python 插件框架扩展功能，支持速率限制、用量监控、实时翻译等
- **多数据库支持**：SQLite（可选加密）、PostgreSQL，支持 S3/GCS/Azure Blob 云存储
- **水平扩展**：Redis 支持会话管理和 WebSocket，支持多节点负载均衡部署
- **OpenTelemetry 可观测性**：内置链路追踪、指标和日志监控支持

### 仓库信息

- **GitHub 地址**：https://github.com/open-webui/open-webui
- **官方文档**：https://docs.openwebui.com/
- **社区市场**：https://openwebui.com/
- **开发语言**：Python / Svelte / TypeScript
- **开源协议**：MIT License
- **Stars 数量**：80k+

### 安装方式

#### 方式一：Docker 一键部署（推荐）

**连接本地 Ollama：**

```
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**连接远程 Ollama：**

```
docker run -d -p 3000:8080 \
  -e OLLAMA_BASE_URL=https://your-ollama-server \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**仅使用 OpenAI API：**

```
docker run -d -p 3000:8080 \
  -e OPENAI_API_KEY=your_secret_key \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**NVIDIA GPU 加速：**

```
docker run -d -p 3000:8080 \
  --gpus all \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:cuda
```

**Open WebUI + Ollama 一体化容器：**

```
docker run -d -p 3000:8080 \
  --gpus=all \
  -v ollama:/root/.ollama \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:ollama
```

#### 方式二：Python pip 安装

```
# 安装（需要 Python 3.11+）
pip install open-webui

# 启动服务
open-webui serve

# 访问 http://localhost:8080
```

#### 方式三：Kubernetes / Helm 部署

```
# 使用 Helm 安装
helm repo add open-webui https://helm.openwebui.com/
helm install open-webui open-webui/open-webui
```

#### 方式四：Docker Compose 完整部署

```
# 下载官方 docker-compose.yaml
wget https://github.com/open-webui/open-webui/raw/main/docker-compose.yaml
docker compose up -d
```

### 使用场景

- **个人 AI 助手**：自建类似 ChatGPT 的对话服务，连接本地大模型，完全免费无限使用
- **企业知识库问答**：上传企业文档，通过 RAG 实现智能问答，替代商业 AI 搜索服务
- **团队 AI 平台**：多用户权限管理，统一分配模型资源，审计日志追踪
- **AI 开发测试**：连接多种 LLM API，对比不同模型效果，测试 Prompt 效果
- **隐私敏感场景**：所有对话数据存储在本地服务器，不经过任何第三方服务
- **教育与科研**：为学生和研究人员提供 AI 工具，数据不出校园

### 与同类产品对比

| 特性         | Open WebUI     | ChatGPT       | ChatBox | LobeChat    |
| ------------ | -------------- | ------------- | ------- | ----------- |
| 部署方式     | 自托管         | 仅云端        | 桌面端  | 自托管/云端 |
| 数据隐私     | 完全本地       | OpenAI 服务器 | 本地    | 取决于部署  |
| 开源协议     | MIT            | 闭源          | 开源    | 开源        |
| RAG 知识库   | 内置           | Plus 付费     | 不支持  | 插件支持    |
| 多模型切换   | 支持           | 不支持        | 支持    | 支持        |
| 图片生成     | 内置           | DALL-E        | 不支持  | 插件支持    |
| 语音通话     | 内置           | Plus 付费     | 不支持  | 不支持      |
| 用户权限管理 | RBAC           | 不支持        | 不支持  | 基础        |
| 使用成本     | 免费（自托管） | 订阅付费      | 免费    | 免费        |
