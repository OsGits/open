# Khoj开源项目详解：AI个人知识库与第二大脑部署教程

## 一、项目概述

**Khoj** 是一款开源的个人 AI 助手，定位为"你的 AI 第二大脑"。它可以帮助你管理个人知识、搜索文档、创建 AI Agent、自动化研究任务等。Khoj 支持接入多种在线和离线的大语言模型（GPT、Claude、Gemini、Llama 等），所有数据默认本地存储，强调隐私保护。

Khoj 的设计理念是"让 AI 成为真正的个人助理"。它可以从你已有的笔记、文档、PDF、网页等资料中学习，然后通过自然语言对话的方式帮助你获取信息、完成任务。不同于 ChatGPT 的通用对话，Khoj 更专注于"你的"知识，能够结合个人上下文给出更有价值的回答。

- **GitHub 地址**：https://github.com/khoj-ai/khoj
- **官方网站**：https://khoj.dev
- **开源协议**：MPL-2.0
- **开发语言**：Python（FastAPI）+ TypeScript
- **核心定位**：个人 AI 第二大脑，支持本地部署的知识管理助手

### 1.1 核心特性

| 特性 | 说明 |
| ---- | ---- |
| **多模型支持** | GPT-4、Claude、Llama、Gemma 等 |
| **多数据源** | PDF、Markdown、Word、Notion、GitHub |
| **多端访问** | Web、Obsidian、Emacs、桌面应用、WhatsApp |
| **语义搜索** | 基于向量的智能语义检索 |
| **Agent 创建** | 自定义知识、角色的 AI Agent |
| **自动化** | 定时任务、Newsletter、提醒通知 |
| **离线支持** | 可完全本地运行 |
| **API 开放** | 提供 REST API |

### 1.2 与同类产品对比

| 特性 | Khoj | Notion AI | ChatGPT | Obsidian |
|------|------|-----------|---------|----------|
| **知识来源** | 本地+在线 | 在线 | 在线 | 本地 |
| **隐私控制** | 完全本地 | 云服务 | 云服务 | 本地 |
| **搜索能力** | 语义搜索 | 关键词 | 语义 | 关键词 |
| **文档理解** | 支持 | 支持 | 支持 | 需插件 |
| **自动化** | Agent+定时 | 有限 | API | 需插件 |
| **开源** | ✅ | ❌ | ❌ | 部分 |

---

## 二、系统要求

| 项目 | 最低要求 | 推荐配置 |
| ---- | -------- | -------- |
| CPU | 2 核 | 4 核+ |
| 内存 | 4 GB | 8 GB+ |
| 磁盘 | 10 GB | 50 GB+ |
| 系统 | Ubuntu 20.04+ | Ubuntu 22.04+ |

---

## 三、Docker 部署（推荐）

### 3.1 一键启动

```bash
docker run -d \
  --name khoj \
  -p 8000:8000 \
  -v khoj_data:/data \
  -e OPENAI_API_KEY=sk-xxxxx \
  --restart unless-stopped \
  khojinai/khoj:latest
```

### 3.2 Docker Compose 部署

```yaml
version: "3.8"

services:
  khoj:
    image: khojinai/khoj:latest
    container_name: khoj
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./data:/data
    environment:
      - OPENAI_API_KEY=sk-xxxxx
      # 可选：使用本地 Ollama
      # OLLAMA_HOST=http://localhost:11434
    environment_file:
      - .env
```

### 3.3 .env 配置示例

```bash
# OpenAI 配置
OPENAI_API_KEY=sk-xxxxx

# 使用本地 Ollama（可选）
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Anthropic 配置（可选）
ANTHROPIC_API_KEY=sk-ant-xxxxx

# 数据库配置
DATABASE_URL=sqlite:///data/khoj.db

# 安全配置
SECRET_KEY=your-secret-key-here
```

### 3.4 访问 Khoj

启动后，访问 `http://your-server-ip:8000` 或 `http://localhost:8000`。

---

## 四、本地安装

### 4.1 使用 pip 安装

```bash
# 创建虚拟环境
python -m venv khoj-env
source khoj-env/bin/activate

# 安装 Khoj
pip install khoj

# 初始化配置
khoj --init
```

### 4.2 启动服务

```bash
# 启动 Khoj
khoj

# 或使用 uvicorn
uvicorn khoj.main:app --host 0.0.0.0 --port 8000
```

### 4.3 使用 Nix

```bash
nix-shell -p khoj
khoj
```

---

## 五、配置与使用

### 5.1 添加数据源

1. 进入 Khoj Web 界面
2. 点击 **Settings → Data Sources**
3. 添加数据源：
   - **文件上传**：直接上传 PDF、Markdown 等
   - **本地文件夹**：指定要索引的文件夹
   - **GitHub**：连接 GitHub 仓库
   - **Notion**：连接 Notion 工作区

### 5.2 支持的文档格式

| 格式 | 说明 |
| ---- | ---- |
| PDF | 学术论文、报告 |
| Markdown | 笔记、文档 |
| Plain Text | 纯文本 |
| Word (.docx) | Office 文档 |
| Org-mode | Emacs 笔记 |
| Notion | 在线笔记 |

### 5.3 搜索功能

使用自然语言搜索你的知识库：

```
"我之前保存的关于 Python 虚拟环境的笔记"
"去年写的项目总结"
"关于 machine learning 的所有文档"
```

### 5.4 对话功能

```
问：基于我上传的论文，总结一下 Transformer 的核心思想
问：根据我的笔记，解释一下 RAG 是什么
问：帮我比较一下 FastAPI 和 Flask 的优缺点
```

---

## 六、Agent 创建

### 6.1 创建自定义 Agent

1. 进入 **Agents → Create Agent**
2. 配置 Agent：
   - **名称**：给你的 Agent 起名
   - **角色**：设定 Agent 的职责
   - **知识库**：关联相关文档
   - **模型**：选择使用的 LLM

### 6.2 Agent 示例

**研究助手 Agent**：

```yaml
name: research-assistant
persona: "你是一个专业的研究助手，擅长阅读论文和总结要点"
model: claude-3-sonnet
knowledge_sources:
  - papers/
tools:
  - web_search
  - document_search
```

**代码审查 Agent**：

```yaml
name: code-reviewer
persona: "你是一个资深的代码审查员，关注代码质量和最佳实践"
model: gpt-4
knowledge_sources:
  - codebase/
tools:
  - github
  - file_search
```

### 6.3 Agent 自动化

配置定时任务：

```yaml
schedule: "0 9 * * *"  # 每天早上9点
action: "总结今日新闻并发给我"
```

---

## 七、Obsidian 集成

### 7.1 安装 Obsidian 插件

1. 在 Obsidian 中打开 **Settings → Community Plugins**
2. 搜索 **Khoj**
3. 安装并启用插件

### 7.2 配置连接

1. 在 Obsidian 中打开 Khoj 插件设置
2. 输入 Khoj 服务器地址：`http://localhost:8000`
3. 获取并输入 API Key

### 7.3 使用方式

在 Obsidian 中使用 Khoj：

```
/khoj search <query>
/khoj chat <question>
```

---

## 八、API 使用

### 8.1 获取 API Key

1. 进入 Khoj **Settings → API**
2. 创建新的 API Key
3. 复制保存

### 8.2 搜索 API

```bash
curl -X GET "http://localhost:8000/api/search?q=your+query" \
  -H "Authorization: Bearer YOUR-API-KEY"
```

### 8.3 对话 API

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Authorization: Bearer YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What is RAG?",
    "model": "gpt-4"
  }'
```

### 8.4 Python SDK

```python
from khoj import Khoj

client = Khoj(api_key="your-api-key")

# 搜索
results = client.search("machine learning notes")

# 对话
response = client.chat("Explain RAG in simple terms")
```

---

## 九、离线模式

### 9.1 使用 Ollama 本地模型

```yaml
# .env 配置
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# 不使用任何在线 API
```

### 9.2 完全离线部署

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 下载模型
ollama pull llama3.2

# 3. 启动 Ollama
ollama serve

# 4. 启动 Khoj（不配置任何在线 API）
docker run -d \
  --name khoj \
  -p 8000:8000 \
  -v khoj_data:/data \
  -e OLLAMA_HOST=http://localhost:11434 \
  -e OLLAMA_MODEL=llama3.2 \
  khojinai/khoj:latest
```

---

## 十、常见问题与解决方案

### 10.1 文档索引失败

**解决方案**：
1. 检查文件格式是否支持
2. 确认文件编码（推荐 UTF-8）
3. 检查文件是否损坏
4. 查看日志获取详细信息

### 10.2 模型连接失败

**解决方案**：
1. 确认 API Key 正确
2. 检查网络连接
3. 验证 API 额度
4. 尝试使用本地 Ollama

### 10.3 搜索结果不准确

**解决方案**：
1. 上传更多相关文档
2. 优化文档结构
3. 使用更精确的查询语句
4. 调整 Top K 参数

### 10.4 性能问题

**解决方案**：
1. 增加服务器内存
2. 使用 SSD 存储
3. 减少同时索引的文档数量
4. 启用向量化缓存

---

## 十一、安全与隐私

### 11.1 数据存储

- 所有文档默认存储在本地
- 向量数据库本地存储
- 可以完全离线运行

### 11.2 安全建议

| 建议 | 说明 |
| ---- | ---- |
| **HTTPS** | 生产环境配置 HTTPS |
| **API Key** | 妥善保管 API Key |
| **访问控制** | 配置反向代理认证 |
| **定期更新** | 及时更新版本 |

---

## 十二、社区与生态

| 资源 | 地址 |
| ---- | ---- |
| **GitHub** | https://github.com/khoj-ai/khoj |
| **官网** | https://khoj.dev |
| **文档** | https://docs.khoj.dev |
| **Discord** | https://discord.gg/BDgyabRM6e |
| **云服务** | https://app.khoj.dev |

---

## 十三、总结

Khoj 是一款极具创新性的开源 AI 工具，它通过将大语言模型与个人知识库相结合，真正实现了"AI 第二大脑"的概念。与通用的 AI 助手不同，Khoj 真正理解"你的"知识，能够基于个人文档和上下文给出更有价值的回答。

它的核心优势在于：

- **隐私优先**：数据完全本地存储，可完全离线运行
- **多模型支持**：支持 GPT、Claude、Llama 等各种模型
- **多数据源**：支持 PDF、Markdown、Word、Notion 等格式
- **多端访问**：Web、Obsidian、Emacs、WhatsApp 都可以使用
- **Agent 自动化**：创建自定义 Agent 实现自动化任务

对于希望构建个人知识管理系统、实现文档智能问答、打造专属 AI 助手的用户来说，Khoj 是一个非常值得尝试的选择。

> **立即体验**：访问 https://khoj.dev 了解更多，或执行 `docker run -d -p 8000:8000 -v khoj_data:/data khojinai/khoj:latest` 一键部署。
