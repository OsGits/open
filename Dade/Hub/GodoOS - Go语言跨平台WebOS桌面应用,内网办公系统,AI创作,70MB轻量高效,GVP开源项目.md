# GodoOS - Go语言开发的跨平台WebOS桌面应用

> 专为内网办公打造的高效操作系统，GVP最有价值开源项目，70MB轻量高效

---

## 📖 项目介绍

**GodoOS** 是一款专为内网办公打造的高效操作系统，基于Go语言开发。它集成了Word、Excel、PPT、PDF、聊天、白板、思维导图等多个办公系统工具，支持AI创作、知识库和原生文件存储，为用户提供一站式办公解决方案。

### About

GodoOS is an efficient operating system designed for intranet office, developed in Go language. It integrates Word, Excel, PPT, PDF, chat, whiteboard, mind mapping and other office tools, supporting AI creation, knowledge base and native file storage for a one-stop office solution.

---

## 🔑 核心特点

> 💡 开源地址：https://gitee.com/godoos/godoos

### 主要功能

- 🖥️ **Windows风格界面**：操作简便，易于上手
- 🤖 **AI创作功能**：内置AI引擎，支持多种创作任务
- 📦 **应用商店**：丰富的应用生态，可无限扩展
- 🔒 **安全可靠**：零污染、无插件依赖、纯净安全
- ⚡ **轻量高效**：打包后仅70MB，低资源消耗
- 🌐 **跨平台支持**：兼容Windows、Linux、macOS

### 技术栈

- Go语言后端
- 前端技术栈（Web技术）
- 低资源消耗设计

---

## 🛠️ 安装方法

### 方式一：直接下载（推荐，最快）

前往 releases 页面下载对应平台的压缩包：

- Windows: 下载 `godoos-windows-x.x.x.zip`
- Linux: 下载 `godoos-linux-x.x.x.tar.gz`
- macOS: 下载 `godoos-macos-x.x.x.tar.gz`

#### Windows 安装

```bash
# 1. 解压下载的ZIP文件
unzip godoos-windows-x.x.x.zip

# 2. 进入目录
cd godoos-windows-x.x.x

# 3. 双击运行 godoos.exe 或在命令行运行
.\godoos.exe
```

#### Linux 安装

```bash
# 1. 下载对应架构的版本
wget https://gitee.com/godoos/godoos/releases/latest/download/godoos-linux-amd64.tar.gz

# 2. 解压
tar -xzf godoos-linux-amd64.tar.gz

# 3. 赋予执行权限
chmod +x godoos

# 4. 运行
./godoos

# 或安装到系统目录（可选）
sudo mv godoos /usr/local/bin/
godoos
```

#### macOS 安装

```bash
# 1. 下载
curl -O https://gitee.com/godoos/godoos/releases/latest/download/godoos-macos.tar.gz

# 2. 解压
tar -xzf godoos-macos.tar.gz

# 3. 运行
open godoos.app

# 或在终端运行
./godoos
```

---

### 方式二：从源码编译

#### 前置要求

- Go 1.20 或更高版本
- Git
- GCC（用于编译CGO依赖）

#### 编译步骤

```bash
# 1. 克隆项目
git clone https://gitee.com/godoos/godoos.git

# 2. 进入项目目录
cd godoos

# 3. 下载依赖
go mod download

# 4. 编译前端（如有前端构建脚本）
# Windows
go run scripts/build_frontend.go windows

# Linux/macOS
go run scripts/build_frontend.go

# 5. 编译主程序
# Windows
go build -o godoos.exe cmd/godoos/main.go

# Linux
go build -o godoos cmd/godoos/main.go

# macOS
go build -o godoos cmd/godoos/main.go

# 6. 运行
./godoos
```

---

### 方式三：使用Docker（服务器部署）

```bash
# 拉取镜像
docker pull godoos/godoos:latest

# 运行容器
docker run -d \
  --name godoos \
  -p 8080:8080 \
  -v /path/to/data:/app/data \
  godoos/godoos:latest

# 访问 http://localhost:8080
```

---

## 📝 快速开始

### 首次运行

1. 双击 `godoos.exe` 或在终端运行 `./godoos`
2. 首次启动会自动初始化系统
3. 默认无需登录，直接进入桌面环境

### 基本操作

- **桌面**：与Windows类似的桌面环境
- **开始菜单**：点击左下角开始按钮
- **文件管理**：内置文件管理器
- **应用商店**：从应用商店安装更多应用

### AI功能使用

```bash
# 配置文件位置
# Windows: %APPDATA%/godoos/config.json
# Linux: ~/.config/godoos/config.json
# macOS: ~/Library/Application Support/godoos/config.json

# 配置AI服务（需要自行部署或使用第三方API）
{
  "ai": {
    "provider": "openai",  // 或 "ollama", "claude" 等
    "api_key": "your-api-key",
    "endpoint": "https://api.openai.com/v1"
  }
}
```

### 应用开发

创建自定义应用的目录结构：

```
myapp/
├── manifest.json      # 应用清单
├── index.html         # 主页面
├── icon.png          # 应用图标
└── assets/           # 资源文件
```

```json
// manifest.json 示例
{
  "name": "我的应用",
  "version": "1.0.0",
  "description": "这是一个示例应用",
  "main": "index.html",
  "icon": "icon.png",
  "window": {
    "width": 800,
    "height": 600
  }
}
```

---

## 🔧 系统配置

### 配置文件路径

```bash
# 查看配置文件位置
godoos --config

# 常见配置项
# config.json:
{
  "theme": "light",           // 主题：light / dark
  "language": "zh-CN",         // 语言
  "autoStart": true,          // 开机自启
  "port": 8080,              // 服务端口
  "dataDir": "./data",       // 数据目录
  "enableAI": true,          // 启用AI功能
  "network": {
    "enable": true,          // 启用网络功能
    "autoConnect": true      // 自动连接内网用户
  }
}
```

### 端口占用处理

```bash
# 如果端口被占用，可以修改配置或使用命令行参数
godoos --port 8888

# 或修改 config.json
{
  "port": 8888
}
```

---

## 📊 项目信息

| 项目 | 信息 |
|------|------|
| 开源协议 | 开源（具体见仓库） |
| 语言 | Go + Web前端 |
| 平台 | Gitee GVP |
| 荣誉 | Gitee最有价值开源项目 |
| 安装包大小 | ~70MB |

### 特色亮点

- ✅ 无需联网，全开源可二次开发
- ✅ 零配置，下载即用
- ✅ 自动连接内网用户，即时通讯
- ✅ 支持自定义应用开发
- ✅ 低资源占用，适合老旧设备

---

## 🔗 相关链接

- Gitee: https://gitee.com/godoos/godoos
- GitHub镜像: https://github.com/godoos/godoos
- 官方网站: https://www.godoos.com
- 文档: https://docs.godoos.com

---

#### 🔗 方向

[← 返回项目首页](README.md)

---
