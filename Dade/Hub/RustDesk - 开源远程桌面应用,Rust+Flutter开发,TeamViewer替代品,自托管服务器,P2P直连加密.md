# RustDesk - 开源远程桌面应用,Rust+Flutter开发,TeamViewer替代品,自托管服务器,P2P直连加密

## 项目概述

RustDesk 是一款功能完整的开源远程桌面应用，使用 Rust 语言核心和 Flutter UI 构建，设计用于自托管场景，是 TeamViewer 和 AnyDesk 的开源替代方案。项目支持 Linux、Windows、macOS、iOS 和 Android 全平台，提供了文件传输、剪贴板同步、音频转发、多显示器支持等企业级功能。最重要的是，RustDesk 的服务器组件完全开源，用户可以自建中继服务器，确保所有远程桌面流量都在自有基础设施上传输，真正实现数据主权。

## 核心特性

### 全平台支持

- **桌面端**：Linux、Windows、macOS
- **移动端**：iOS、Android
- **Web 端**：浏览器直接访问，无需安装客户端
- **统一体验**：所有平台使用相同的 Rust 核心，功能一致

### 自托管能力

- **开源服务器**：完全开源的 rendezvous（中转）和 relay（中继）服务器
- **P2P 直连**：优先尝试 TCP 打洞建立直连，失败才走中继
- **端到端加密**：使用 NaCl/libsodium box 加密，中继服务器无法解密内容
- **完全可控**：数据完全在自有服务器上传输

### 远程控制功能

- **无人值守访问**：设置固定密码，随时远程连接，无需对方操作
- **文件传输**：拖拽式文件传输，直接在会话中传输文件
- **剪贴板同步**：文本和文件剪贴板双向同步
- **音频转发**：远程机器音频流传输到本地
- **多显示器支持**：在会话工具栏中切换不同显示器

### 连接稳定性

- **NAT 穿透**：自动检测 NAT 类型，尝试最优连接路径
- **中继回退**：直连失败时自动切换到中继服务器
- **自动重连**：网络波动时自动重连
- **带宽优化**：自适应带宽，调整画质和帧率

## 技术架构

### 架构设计

```
┌─────────────────────────────────────────────────────┐
│              RustDesk 网络架构                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐│
│  │ 客户端 A │◄──────►│ H BBS   │◄──────►│ 客户端 B ││
│  │ (ID:123) │         │(中转服务器)│         │(ID:456) ││
│  └─────────┘         └─────────┘         └─────────┘│
│       │                   │                   │     │
│       │    P2P 直连       │    中继转发        │     │
│       └───────────────────┘───────────────────┘     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 服务器组件

| 组件 | 端口 | 协议 | 功能 |
|------|------|------|------|
| H BBS | 21115 | TCP | NAT 类型测试 |
| H BBS | 21116 | TCP+UDP | ID 注册和心跳 |
| H BBR | 21117 | TCP | 中继流量 |
| Web Client | 21118-21119 | TCP | Web 客户端 WebSocket |

## 部署教程

### 客户端安装

#### Linux 安装

**Debian/Ubuntu：**

```bash
# 下载最新版本的 .deb 包
wget https://github.com/rustdesk/rustdesk/releases/download/1.4.6/rustdesk-1.4.6-x86_64.deb

# 安装
sudo dpkg -i rustdesk-1.4.6-x86_64.deb

# 修复依赖
sudo apt-get install -f
```

**Fedora/RHEL：**

```bash
# 下载 .rpm 包
wget https://github.com/rustdesk/rustdesk/releases/download/1.4.6/rustdesk-1.4.6-0.x86_64.rpm

# 安装
sudo rpm -i rustdesk-1.4.6-0.x86_64.rpm
```

**Arch Linux (AUR)：**

```bash
# 使用 yay
yay -S rustdesk-bin

# 或使用稳定版
yay -S rustdesk
```

**Flatpak：**

```bash
flatpak install flathub com.rustdesk.RustDesk
```

#### Windows 安装

1. 从 [GitHub Releases](https://github.com/rustdesk/rustdesk/releases) 下载 `.exe` 或 `.msi` 安装包
2. 运行安装程序
3. 安装完成后自动启动

#### macOS 安装

```bash
# 使用 Homebrew
brew install --cask rustdesk

# 或从官网下载 DMG 文件
```

#### Android/iOS 安装

从应用商店搜索 "RustDesk" 或访问 [官网](https://rustdesk.com/) 下载。

### 自托管服务器部署

#### Docker 部署（推荐）

```bash
# 创建目录
mkdir -p ~/rustdesk-server && cd ~/rustdesk-server

# 下载官方 Docker Compose 配置
wget rustdesk.com/oss.yml -O docker-compose.yml

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f
```

#### 独立 Docker 容器

```bash
# 运行 rendezvous 服务器 (hbbs)
docker run --name hbbs -d \
  --publish 21115:21115 \
  --publish 21116:21116 \
  --publish 21116:21116/udp \
  --volume ~/hbbs-data:/root \
  --net=host \
  rustdesk/rustdesk-server hbbs

# 运行 relay 服务器 (hbbr)
docker run --name hbbr -d \
  --publish 21117:21117 \
  --volume ~/hbbr-data:/root \
  --net=host \
  rustdesk/rustdesk-server hbbr
```

#### 手动编译部署

```bash
# 克隆服务器仓库
git clone https://github.com/rustdesk/rustdesk-server.git
cd rustdesk-server

# 编译
cargo build --release

# 运行 rendezvous 服务器
./target/release/hbbs -k _

# 运行 relay 服务器（新终端）
./target/release/hbbr
```

### 防火墙配置

如果使用 UFW 防火墙：

```bash
# 开放必要端口
sudo ufw allow 21114:21119/tcp
sudo ufw allow 21116/udp

# 启用防火墙
sudo ufw enable
```

### 客户端配置自托管服务器

1. 打开 RustDesk 客户端
2. 进入 **设置 → 网络**
3. 填写服务器信息：
   - **ID 服务器**：你的服务器 IP 或域名:21116
   - **Key**：从服务器日志中获取的公钥
   - **中继服务器** 和 **API 服务器**：留空（自动识别）
4. 保存配置

获取服务器 Key：

```bash
# 查看 hbbs 容器日志
docker logs hbbs

# 输出示例：
# [2025-01-01 12:00:00] INFO  - Public key written to id_ed25519/id_ed25519.pub
# Key: OjH1Yxxxxx...  # 复制这个 Key
```

## 高级配置

### Web 客户端部署

如果需要通过浏览器访问远程桌面：

```yaml
# docker-compose.yml 添加 web 选项
services:
  hbbs:
    ports:
      - "21115:21115"
      - "21116:21116"
      - "21116:21116/udp"
      - "21118:21118"  # Web 客户端

  hbbr:
    ports:
      - "21117:21117"
      - "21119:21119"  # Web 客户端中继
```

访问 `http://your-server:21118/` 使用 Web 客户端。

### Nginx 反向代理（可选）

```nginx
server {
    listen 80;
    server_name rustdesk.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:21118;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### 设置无人值守访问

1. 在远程机器上打开 RustDesk
2. 进入 **设置 → 安全**
3. 启用 **允许无人值守访问**
4. 设置固定密码（不是临时密码）
5. 保存设置

现在可以从控制端直接输入远程 ID 和固定密码进行连接。

## 使用场景

### 远程办公

- 访问办公室电脑上的文件和应用程序
- 支持在家工作场景
- 数据完全在自有服务器上传输

### 技术支持

- 为家人朋友提供远程技术支持
- 中小企业客户服务
- 无需第三方服务

### 服务器管理

- 远程管理 Linux 服务器
- 无需 SSH 的图形界面管理
- 方便不熟悉命令行的用户

## 与同类产品对比

| 特性 | RustDesk | TeamViewer | AnyDesk |
|------|----------|-----------|---------|
| 开源 | AGPL-3.0 | 否 | 否 |
| 自托管服务器 | 支持 | 不支持 | 不支持 |
| 免费个人使用 | 是 | 限制 | 限制 |
| 跨平台 | 全平台 | 全平台 | 全平台 |
| Web 客户端 | 支持 | 部分支持 | 支持 |
| 端到端加密 | 是 | 是 | 是 |
| P2P 直连 | 是 | 部分 | 部分 |

## 常见问题

### Q: RustDesk 是否真的免费？

A: 是的，RustDesk 对个人和商业使用都免费。项目采用 AGPL-3.0 许可证。

### Q: 自托管服务器是否必须？

A: 不是必须的。RustDesk 默认使用官方托管的服务器进行连接建立。但如果你需要更高的隐私保护或控制，可以自建服务器。

### Q: 为什么连接有时走中继？

A: 当两台机器处于复杂 NAT 环境无法直连时，会自动切换到中继服务器。中继流量是加密的，服务器无法解密内容。

### Q: 如何获取帮助或报告问题？

A: 访问 [GitHub Issues](https://github.com/rustdesk/rustdesk/issues) 报告问题，或加入 Discord 社区寻求帮助。

## 项目资源

- **GitHub**: https://github.com/rustdesk/rustdesk
- **官网**: https://rustdesk.com/
- **服务器仓库**: https://github.com/rustdesk/rustdesk-server
- **文档**: https://github.com/rustdesk/rustdesk/wiki
- **社区**: Discord 服务器

---

*最后更新：2026-06-21*
