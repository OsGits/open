# Gitea 开源项目详解：轻量级自托管 Git 服务平台部署教程与团队协作实战指南

## 一、项目概述

### 1.1 什么是 Gitea

Gitea 是一款用 Go 语言编写的开源、轻量级、自托管的 Git 服务平台。它旨在以最低的资源消耗在几乎任何能够运行 Go 语言的平台上提供完整的 Git 代码托管能力，包括代码仓库管理、代码审查、问题跟踪、Wiki、软件包注册和 CI/CD 流水线等一站式开发协作服务。Gitea 是 Gogs 项目的社区分支，拥有更开放的治理模式与更活跃的开发社区，已成为许多中小企业、科研机构与个人开发者搭建私有代码托管平台的首选。

**项目官方地址：** https://github.com/go-gitea/gitea

### 1.2 项目特点与核心功能

Gitea 主要特点包括但不限于：

| 特性 | 说明 |
|------|------|
| 轻量高效 | Go 语言编译的单一二进制文件，内存占用通常仅约 50MB，可在树莓派等边缘设备上流畅运行 |
| 一站式集成 | 内置 Git 托管、代码审查 Pull Request、问题跟踪、Wiki、软件包管理、CI/CD |
| 多数据库支持 | 支持 SQLite、MySQL、PostgreSQL、MSSQL 多种数据库 |
| 跨平台部署 | 提供 Linux、Windows、macOS、ARM 等多平台安装包与 Docker 镜像 |
| 易于安装 | 支持 Docker、二进制文件、源代码编译等多种安装方式 |
| 高度可定制 | 丰富的配置选项与主题系统，支持插件扩展 |
| 多语言支持 | 界面内置多语言支持（含简体中文） |
| 安全可靠 | SSH/HTTPS 支持，内置双因素认证 2FA、LFS、Webhook |
| 低资源占用 | 相比 GitLab 等重方案更适合中小团队 |

### 1.3 Gitea 与 GitLab / GitHub Enterprise 对比

| 对比项 | Gitea | GitLab | GitHub Enterprise |
|--------|--------|--------|------------------|
| 开发语言 | Go | Ruby / Go | Ruby / Go |
| 内存占用 | ~50MB | ~2GB | ~4GB |
| 部署难度 | 简单 | 复杂 | 中等 |
| 功能完整度 | ★★★★☆ | ★★★★★ | ★★★★★ |
| 自定义程度 | 高 | 中 | 低 |
| 社区活跃度 | 高 | 高 | 中 |
| 开源协议 | MIT | MIT | 商业 |
| 适用场景 | 中小型团队、个人开发 | 大型企业、DevOps 团队 | 企业私有部署 |

## 二、Gitea 核心功能模块详解

### 2.1 代码仓库管理

Gitea 提供完整的 Git 仓库管理能力：

- 支持创建、克隆、推送、拉取、分支管理、合并请求等标准 Git 操作
- 仓库权限精细控制（组织、团队、协作者三级权限）
- 代码历史记录查看与文件差异对比
- Git LFS 大文件存储支持
- 贡献者统计与代码活跃度分析
- 仓库镜像与复刻 Fork 功能
- 受保护分支规则配置

### 2.2 代码审查（Pull Request）

Gitea 内置代码审查工作流：

- 基于分支的合并请求
- 代码行内评论与建议
- 请求审核者分配与审批流程
- 冲突检测与自动合并选项
- 持续集成状态检查
- 代码差异彩色高亮显示

### 2.3 问题跟踪与团队协作

- 完整的 Issue 系统，支持里程碑、标签、看板视图
- 项目看板（Project Board）任务管理
- 组织与团队管理
- 讨论评论与 @提及通知
- 内置 Wiki 文档系统

### 2.4 CI/CD 集成

- 支持通过 Webhook 与 Drone、Jenkins、GitHub Actions 等 CI/CD 工具集成
- 内置 Actions 流水线功能（Gitea Actions），可替代 GitHub Actions 自建
- 自动化构建、测试、部署流程
- 多环境部署支持

### 2.5 软件包管理（Package Registry）

Gitea 内置通用软件包注册中心，支持多种包格式：

- npm (JavaScript/Node.js
- Maven (Java)
- PyPI (Python)
- NuGet (.NET)
- Go Modules
- Container (Docker/OCI)
- Helm (Kubernetes)
- Cargo (Rust)

## 三、系统要求与部署前准备

### 3.1 硬件要求

| 部署规模 | CPU 核心 | 内存 | 磁盘空间 |
|----------|----------|------|----------|
| 个人/小团队（<10 人） | 1 核 | 512MB | 10GB |
| 中型团队（10-50 人） | 2 核 | 1GB | 50GB |
| 企业级（50-500 人） | 4 核 | 2GB | 200GB |

### 3.2 软件要求

- 操作系统：Linux（推荐 Ubuntu 20.04/22.04、CentOS 7/8）、Windows、macOS
- Docker 与 Docker Compose（Docker 部署方式需要）
- Git 客户端
- 数据库（可选，SQLite 无需额外安装）
- 反向代理（可选，生产环境建议配置 Nginx 或 Apache）
- SSL 证书（可选，推荐使用 Let's Encrypt）

### 3.3 域名与网络准备

- 一枚可用的域名（可选但推荐，如 git.example.com）
- 域名已解析到部署服务器的 IP 地址
- 开放以下端口：
  - 3000（Web 界面，HTTP）
  - 22 或 2222（SSH Git 操作端口）
  - 443（如配置 HTTPS）

## 四、部署方式一：Docker Compose 安装（推荐生产环境）

Docker Compose 方式将所有服务（Gitea、数据库、Redis 等）统一容器化管理，部署简单、维护方便、扩展性强，是生产环境推荐的首选方案。

### 4.1 安装 Docker 与 Docker Compose

首先确保服务器上已安装 Docker 与 Docker Compose。如尚未安装，可按以下步骤安装：

**在 Ubuntu/Debian 上安装 Docker：

```bash
# 更新包索引
sudo apt update

# 安装必要的依赖
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 添加 Docker 官方 APT 仓库
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# 更新包索引并安装 Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 启动并设置为开机启动
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
sudo docker --version
sudo docker compose version
```

**在 CentOS/RHEL 上安装 Docker：**

```bash
# 安装必要的依赖
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加 Docker 官方仓库
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker 并设置为开机启动
sudo systemctl start docker
sudo systemctl enable docker
```

### 4.2 创建项目目录结构

```bash
sudo mkdir -p /opt/gitea/{data,postgres,redis}
cd /opt/gitea
```

目录作用说明：

- `data/`：挂载 Gitea 的主数据目录（仓库、配置、日志等）
- `postgres/`：挂载 PostgreSQL 数据库数据目录
- `redis/`：挂载 Redis 数据目录

### 4.3 创建 Docker Compose 配置文件

在 `/opt/gitea/` 目录下创建 `docker-compose.yml` 文件：

```bash
sudo tee docker-compose.yml << 'EOF'
version: "3"

networks:
  gitea:
    external: false

services:
  server:
    image: gitea/gitea:latest
    container_name: gitea_server
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=postgres
      - GITEA__database__HOST=db:5432
      - GITEA__database__NAME=gitea
      - GITEA__database__USER=gitea
      - GITEA__database__PASSWD=your_secure_password_here
    restart: always
    networks:
      - gitea
    volumes:
      - ./data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000
      - "2222:22"
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    container_name: gitea_db
    environment:
      - POSTGRES_USER=gitea
      - POSTGRES_PASSWORD=your_secure_password_here
      - POSTGRES_DB=gitea
    restart: always
    networks:
      - gitea
    volumes:
      - ./postgres:/var/lib/postgresql/data

  redis:
    image: redis:9-alpine
    container_name: gitea_redis
    restart: always
    networks:
      - gitea
    volumes:
      - ./redis:/data
    command: "redis-server --appendonly yes"
EOF
```

**注意：** 请将 `your_secure_password_here` 替换为一个安全的高强度密码。

### 4.4 启动 Gitea 服务

```bash
cd /opt/gitea
sudo docker compose up -d
```

`-d` 参数表示在后台运行容器。

查看容器运行状态：

```bash
sudo docker compose ps
```

查看日志：

```bash
sudo docker compose logs -f server
```

### 4.5 完成首次安装配置向导

访问 `http://your_server_ip:3000`，进入 Gitea 的首次安装配置页面：

**数据库设置：** 保持默认即可（Docker Compose 已经通过环境变量配置好了）。

**常规设置：**

- 站点名称：您的 Gitea 实例名称
- 仓库根目录：`/data/git/repositories`（容器内路径，已挂载，勿改）
- LFS 根目录：`/data/git/lfs`（同上）
- SSH 服务器端口：填写 `2222`（与 docker-compose.yml 中映射的主机端口）
- SSH 服务器域名：填写服务器 IP 或域名
- Gitea 基本 URL：填写 `http://your_domain_or_ip:3000/`
- 管理员账号设置：设置管理员用户名和密码

填写完毕后，点击「立即安装」按钮完成初始化。

### 4.6 使用 Docker（rootless 模式）安装

rootless 镜像以非 root 用户运行 Gitea，安全性更高。创建 `docker-compose.yml`：

```bash
sudo tee docker-compose.yml << 'EOF'
version: "3"

networks:
  gitea:
    external: false

services:
  server:
    image: docker.gitea.com/gitea:1.26.2-rootless
    container_name: gitea_rootless
    restart: always
    volumes:
      - ./data:/var/lib/gitea
      - ./config:/etc/gitea
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "2222:2222"
EOF
```

**注意：** rootless 镜像使用 Gitea 内置 SSH 功能，不支持 OpenSSH。如需 OpenSSH，请使用标准镜像。

设置目录权限：

```bash
sudo chown -R 1000:1000 ./data ./config
```

启动服务：

```bash
sudo docker compose up -d
```

### 4.7 使用 MySQL 数据库（可选方案

如果您偏好 MySQL，可将 docker-compose.yml 中数据库部分替换为 MySQL：

```yaml
  db:
    image: mysql:8.0
    container_name: gitea_db
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=your_root_password_here
      - MYSQL_DATABASE=gitea
      - MYSQL_USER=gitea
      - MYSQL_PASSWORD=your_secure_password_here
    volumes:
      - ./mysql:/var/lib/mysql
    networks:
      - gitea
```

对应修改 Gitea 服务环境变量：

```yaml
      - GITEA__database__DB_TYPE=mysql
      - GITEA__database__HOST=db:3306
```

### 4.8 使用 SQLite 数据库（单机极简方案）

如只需单机极简部署，可省略数据库服务，使用 SQLite：

```yaml
version: "3"

services:
  server:
    image: gitea/gitea:latest
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
    volumes:
      - ./data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "2222:22"
```

## 五、部署方式二：二进制文件安装

二进制安装方式适合无法使用 Docker 或希望对系统进行更精细化控制的场景。

### 5.1 环境准备

**创建 Git 用户：

```bash
sudo useradd -m -d /home/git -s /bin/bash git
```

**安装依赖：**

```bash
# Ubuntu/Debian
sudo apt install -y git

# CentOS/RHEL
sudo yum install -y git
```

### 5.2 下载并安装 Gitea 二进制文件

**方式一：通过脚本自动下载最新版本：

```bash
# 获取最新版本号
VERSION=$(curl -s https://api.github.com/repos/go-gitea/gitea/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")

# 下载二进制文件
sudo wget -O /usr/local/bin/gitea https://dl.gitea.com/gitea/${VERSION}/gitea-${VERSION}-linux-amd64

# 赋予执行权限
sudo chmod +x /usr/local/bin/gitea

# 验证安装
gitea --version
```

**方式二：手动下载指定版本：**

访问 [Gitea 官方下载页面](https://dl.gitea.com/gitea/)，选择合适的版本和架构后下载。

例如，下载 1.26.2 版本（amd64）：

```bash
sudo wget -O /usr/local/bin/gitea https://dl.gitea.com/gitea/1.26.2/gitea-1.26.2-linux-amd64
sudo chmod +x /usr/local/bin/gitea
```

### 5.3 创建必要的目录结构

```bash
sudo mkdir -p /var/lib/gitea/{custom,data,log}
sudo chown -R git:git /var/lib/gitea/
sudo chmod -R 750 /var/lib/gitea/
sudo mkdir /etc/gitea
sudo chown root:git /etc/gitea
sudo chmod 770 /etc/gitea
```

### 5.4 配置 Systemd 服务

创建 systemd 服务文件 `/etc/systemd/system/gitea.service`：

```bash
sudo tee /etc/systemd/system/gitea.service << 'EOF'
[Unit]
Description=Gitea (Git with a cup of tea)
After=syslog.target
After=network.target
After=postgresql.service
After=mysqld.service
After=redis.service

[Service]
# 限制类型，限制可以读取的内存大小。
# 如使用 SQLite，此处设置为无限制。
#LimitMEMLOCK=infinity
LimitNOFILE=65535
RestartSec=2s
Type=simple
User=git
Group=git
WorkingDirectory=/var/lib/gitea/
# 使用 gitea web --config /etc/gitea/app.ini
ExecStart=/usr/local/bin/gitea web --config /etc/gitea/app.ini
Restart=always
Environment=USER=git HOME=/home/git GITEA_WORK_DIR=/var/lib/gitea

[Install]
WantedBy=multi-user.target
EOF
```

启用并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable gitea
sudo systemctl start gitea
```

验证服务状态：

```bash
sudo systemctl status gitea
```

### 5.5 完成首次安装配置

访问 `http://your_server_ip:3000`，按提示完成数据库和常规设置。

## 六、部署方式三：从源代码编译安装

源码编译方式适合需要定制化部署或特定平台编译场景。

### 6.1 安装编译依赖

- Go 1.21 或更高版本
- Node.js 16.x 或更高版本
- pnpm 包管理器
- Git
- make

**在 Ubuntu/Debian 上安装依赖：

```bash
sudo apt update
sudo apt install -y golang nodejs npm make git
sudo npm install -g pnpm
```

### 6.2 克隆源代码

```bash
cd ~
git clone https://github.com/go-gitea/gitea.git
cd gitea

# 检出最新稳定版本
git checkout $(git describe --tags $(git rev-list --tags --max-count=1))
```

### 6.3 构建后端与前端

```bash
# 构建后端（包含 SQLite 支持）
TAGS="bindata sqlite sqlite_unlock_notify" make backend

# 构建前端
make frontend

# 构建完成后，生成的二进制文件在当前目录
./gitea web
```

### 6.4 安装与二进制方式类似步骤5。完成后将 `gitea` 二进制文件复制到系统路径：

```bash
sudo cp gitea /usr/local/bin/gitea
sudo chmod +x /usr/local/bin/gitea
```

## 七、部署方式四：在 Kubernetes 上部署（进阶方案

在 Kubernetes 集群上部署 Gitea 可使用官方 Helm Chart。

### 7.1 安装 Helm

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 7.2 添加 Helm 仓库并安装 Gitea

```bash
helm repo add gitea-charts https://dl.gitea.com/charts/
helm repo update

# 创建命名空间
kubectl create namespace gitea

# 安装 Gitea
helm install gitea gitea-charts/gitea --namespace gitea
```

### 7.3 自定义配置

创建 `values.yaml` 文件：

```yaml
ingress:
  enabled: true
  hosts:
    - host: git.example.com
      paths:
        - path: /
          pathType: Prefix

gitea:
  config:
    server:
      DOMAIN: git.example.com
      ROOT_URL: https://git.example.com
    database:
      DB_TYPE: postgres
```

使用自定义配置安装：

```bash
helm install gitea gitea-charts/gitea --namespace gitea -f values.yaml
```

## 八、部署方式五：包管理器安装

### 8.1 macOS Homebrew 安装

```bash
brew tap gitea/tap
brew install gitea

# 启动服务
brew services start gitea
```

### 8.2 Arch Linux 安装

```bash
sudo pacman -S gitea
sudo systemctl enable --now gitea
```

### 8.3 FreeBSD Ports 安装

```bash
cd /usr/ports/www/gitea
sudo make install clean
```

## 九、Nginx 反向代理与 HTTPS 配置（生产环境推荐）

### 9.1 安装 Nginx 与 Certbot

```bash
# Ubuntu/Debian
sudo apt install -y nginx certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install -y nginx certbot python3-certbot-nginx
```

### 9.2 配置 Nginx 反向代理

创建配置文件 `/etc/nginx/conf.d/gitea.conf`：

```nginx
server {
    listen 80;
    server_name git.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 9.3 获取并配置 HTTPS：

```bash
sudo certbot --nginx -d git.example.com
```

### 9.4 验证 Nginx 配置并重启：

```bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## 十、Gitea 基础使用指南

### 10.1 创建第一个仓库

登录 Gitea 后，点击右上角「+」选择「新建仓库」，填写仓库名称、描述、是否公开等信息，点击「创建仓库」。

### 10.2 将本地仓库推送到 Gitea

```bash
# 在本地项目目录
git init
git add .
git commit -m "Initial commit"
git remote add origin http://git.example.com/username/repo.git
git push -u origin main
```

### 10.3 配置 SSH 密钥

```bash
# 生成 SSH 密钥对
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥复制到剪贴板
cat ~/.ssh/id_ed25519.pub
```

在 Gitea 个人设置页面「SSH/GPG密钥」粘贴公钥内容，添加 SSH 公钥。

### 10.4 创建组织与团队协作

- 在 Gitea 中，组织是管理多个仓库的集合。
- 点击右上角「+」选择「新建组织」，填写组织名称并设置组织描述。
- 在组织设置中可以创建团队，设置团队权限，邀请成员加入组织。
- 在团队中设置仓库的访问权限（读、写、管理权限级别）。

## 十一、常见问题排查

### 11.1 无法启动容器 / 容器启动后立即退出

检查 Docker Compose 日志：

```bash
sudo docker compose logs
```

常见原因：

- 端口被占用：检查 3000 端口是否被其他服务占用
- 目录权限问题：确保数据目录属主与容器内 UID/GID 匹配
- 数据库连接问题：检查数据库连接配置

### 11.2 SSH 连接失败

- 检查 SSH 端口映射是否正确
- 确认 SSH 密钥是否正确添加到 Gitea 用户设置
- 检查容器内 SSH 服务是否正常启动

### 11.3 升级 Gitea

**Docker Compose 方式升级：**

```bash
cd /opt/gitea
sudo docker compose pull
sudo docker compose up -d
```

**二进制方式升级：**

```bash
sudo systemctl stop gitea
sudo wget -O /usr/local/bin/gitea https://dl.gitea.com/gitea/新版本号/gitea-新版本号-linux-amd64
sudo chmod +x /usr/local/bin/gitea
sudo systemctl start gitea
```

## 十二、备份与恢复

### 12.1 备份数据

**Docker Compose 方式：**

```bash
# 停止容器
cd /opt/gitea
sudo docker compose stop

# 备份数据目录
sudo tar -czf gitea-backup-$(date +%Y%m%d).tar.gz /opt/gitea/

# 启动容器
sudo docker compose start
```

### 12.2 备份数据库

PostgreSQL 备份：

```bash
sudo docker exec -t gitea_db pg_dump -U gitea gitea > gitea-db-backup.sql
```

MySQL 备份：

```bash
sudo docker exec gitea_db mysqldump -u gitea -p gitea > gitea-db-backup.sql
```

## 十三、Gitea 实际应用场景

### 13.1 个人开发者私人代码托管

- 备份个人代码项目，不受第三方代码托管平台的依赖
- 在树莓派等低功耗设备上部署，实现个人代码仓库
- 轻量的持续集成与自动部署流程

### 13.2 中小团队内部代码协作

- 团队成员管理与权限控制
- 代码审查与合并请求工作流
- Issue 跟踪与项目管理
- 内部 CI/CD 自动化

### 13.3 企业级代码托管平台

- 高可用架构部署
- LDAP/Active Directory 集成
- 安全审计与日志记录
- 与企业现有工具链集成

### 13.4 开源项目镜像与代码托管

- 从 GitHub/GitLab 迁移项目
- 镜像同步多个代码托管平台
- 自建开源项目主页与社区

## 十四、Gitea 生态与插件

Gitea 拥有丰富的第三方工具与插件生态：

- **Gitea Actions**：内置 CI/CD 流水线功能，可替代 GitHub Actions
- **Drone CI**：流行的容器化 CI/CD 平台，与 Gitea 无缝集成
- **Woodpecker CI**：开源的 CI/CD 工具
- **Tea**：Gitea 官方命令行工具
- **Gitea Bot**：自动化机器人
- **多种主题与插件**：美化 Gitea 界面

## 十五、总结

Gitea 以其轻量、高效、易用的特性，成为自托管 Git 服务平台的优秀选择。无论是个人开发者、小型团队，还是需要在企业内部搭建代码托管平台，Gitea 都能提供一个功能完整、资源消耗低、部署简便、易于维护的解决方案。通过 Docker Compose、二进制、源代码编译等多种部署方式，灵活满足不同场景的需求。配合丰富的插件生态与完善的文档，Gitea 能够帮助团队高效地进行代码管理与团队协作。

如果您希望拥有一个完全自主掌控的代码托管平台，同时又不想承担 GitLab 等高资源消耗方案的负担，那么 Gitea 将是一个理想的选择。
