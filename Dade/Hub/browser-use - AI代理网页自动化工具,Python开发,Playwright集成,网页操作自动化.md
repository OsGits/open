# browser-use - AI代理网页自动化工具

> 让网站可被AI代理访问的创新工具，支持Playwright驱动的智能网页操作

---

## 📖 项目介绍

**browser-use** 是一个革命性的开源项目，旨在使现有网站能够被AI代理访问和操作。它通过Playwright提供标准化的网页交互接口，让AI代理能够像人类一样浏览网页、填写表单、点击按钮等操作。

### About

browser-use is an innovative open-source project that enables websites to be accessible to AI agents. It provides standardized interfaces for AI agents to browse web pages, fill forms, click buttons, and perform other actions just like humans, powered by Playwright.

---

## 🔑 核心特点

> 💡 开源地址：https://github.com/browser-use/browser-use

### 主要功能

- 🌐 **网页自动化**：让AI代理能够操作任何网站
- 🤖 **AI兼容**：支持主流AI代理框架集成（LangChain等）
- 🔧 **易于集成**：简单的API设计，快速上手
- 📊 **可视化监控**：实时查看AI代理的网页操作
- 🎯 **通用适配**：不依赖特定网站，适应性强

### 技术栈

- Python 3.10+
- Playwright
- LangChain
- AsyncIO

---

## 🛠️ 安装方法

### 前置要求

- Python 3.10 或更高版本
- pip 包管理器
- 操作系统：Windows / macOS / Linux

### 步骤1：创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv browser-use-env

# 激活虚拟环境
# Windows
browser-use-env\Scripts\activate

# macOS / Linux
source browser-use-env/bin/activate
```

### 步骤2：安装依赖

```bash
# 使用pip安装
pip install browser-use

# 或安装最新开发版本
pip install git+https://github.com/browser-use/browser-use.git
```

### 步骤3：安装浏览器驱动

```bash
# 安装Playwright浏览器（包含Chromium、Firefox、WebKit）
playwright install

# 或仅安装Chromium（推荐，更快）
playwright install chromium
```

### 步骤4：验证安装

```bash
# 运行示例测试
python -c "from browser_use import Browser; print('browser-use installed successfully!')"
```

---

## 📝 快速开始

### 基本使用示例

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

# 初始化语言模型
llm = ChatOpenAI(model="gpt-4")

# 创建浏览器代理
agent = Agent(
    task="在GitHub上搜索browser-use项目",
    llm=llm,
)

# 运行代理
result = agent.run()
print(result)
```

### 高级配置

```python
from browser_use import Agent, BrowserConfig, Browser
from langchain_openai import ChatOpenAI

# 自定义浏览器配置
browser = Browser(
    config=BrowserConfig(
        headless=False,  # 显示浏览器窗口
        disable_security=True,  # 禁用安全限制
    )
)

agent = Agent(
    task="打开百度并搜索'AI'",
    llm=llm,
    browser=browser,
)

result = agent.run()
```

---

## 🔧 Docker部署

### 使用Docker运行

```dockerfile
# Dockerfile
FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安装Playwright
RUN pip install playwright && playwright install chromium

# 安装browser-use
RUN pip install browser-use

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
```

```bash
# 构建并运行
docker build -t browser-use-app .
docker run browser-use-app
```

---

## 📊 项目信息

| 项目 | 信息 |
|------|------|
| GitHub Stars | 74,000+ |
| License | MIT |
| 语言 | Python |
| 最新更新 | 活跃维护 |

---

## 🔗 相关链接

- GitHub: https://github.com/browser-use/browser-use
- 文档: https://docs.browser-use.com
- 示例: https://github.com/browser-use/browser-use/tree/main/examples

---

#### 🔗 方向

[← 返回项目首页](README.md)

---
