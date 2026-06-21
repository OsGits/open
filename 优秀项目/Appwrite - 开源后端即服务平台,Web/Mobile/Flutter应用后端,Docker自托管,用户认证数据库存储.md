# Appwrite - 开源后端即服务平台,Web/Mobile/Flutter应用后端,Docker自托管,用户认证数据库存储

## 项目概述

Appwrite 是一个面向 Web、移动端和原生应用的开源端到端后端即服务平台，以开发者体验为核心，提供构建生产就绪应用所需的一切服务。Appwrite 将复杂和重复的后端开发工作抽象化，让你能够更快速地构建安全的全栈应用。它包含用户认证、数据库管理、文件存储、图片处理、云函数、消息推送等服务，所有功能都打包成一组 Docker 微服务，支持完全自托管部署。

## 核心特性

### 完整的后端服务

- **用户认证**：支持邮箱密码、手机号、OAuth 多种登录方式
- **数据库**：支持 MongoDB 或 MariaDB，灵活的数据存储
- **文件存储**：大文件上传、下载、管理，支持图片处理
- **云函数**：运行自定义后端逻辑，支持多种运行时
- **消息推送**：向用户发送推送通知
- **实时事件**：WebSocket 实时数据同步

### 开发者友好的设计

- **Web 控制台**：可视化管理和配置所有服务
- **SDK 支持**：40+ 官方 SDK，覆盖主流语言
- **REST API**：完整的 RESTful API
- **CLI 工具**：命令行工具简化开发流程
- **可视化查询**：无需写 SQL，通过 UI 操作数据库

### 安全特性

- **数据加密**：敏感数据自动加密存储
- **基于角色的访问控制**：细粒度权限管理
- **GDPR 合规**：支持数据删除和导出
- **审计日志**：记录所有操作历史

### 自托管优势

- **完全控制**：数据存储在自有服务器
- **无使用限制**：不限制用户数、项目数
- **无平台锁定**：可随时迁移到其他平台
- **开源透明**：代码公开，可审计

## 服务概览

### 核心服务

| 服务 | 功能描述 |
|------|---------|
| Auth | 用户注册、登录、OAuth、 MFA |
| Databases | NoSQL/SQL 数据库、集合、索引 |
| Storage | 文件上传、下载、预览、压缩 |
| Functions | 自定义后端逻辑、计划任务 |
| Messaging | 邮件、短信、推送通知 |
| Realtime | WebSocket 实时数据同步 |

### 安全服务

| 服务 | 功能描述 |
|------|---------|
| Avatars | 自动生成头像、图标、QR 码 |
| Locale | 国家、语言、货币数据 |
| Teams | 团队管理、成员权限 |
| GraphQL | GraphQL API 接口 |

## 技术架构

### 架构设计

```
┌──────────────────────────────────────────────────────────┐
│                    Appwrite 架构                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐      ┌─────────────────────────────────┐│
│  │   Web/移动端 │      │      Appwrite 后端服务          ││
│  │   客户端 SDK │◄────►│                                 ││
│  └─────────────┘      │  ┌───────┐  ┌───────┐  ┌───────┐││
│                        │  │ Auth  │  │  DB   │  │Storage│││
│  ┌─────────────┐      │  └───────┘  └───────┘  └───────┘││
│  │  Web 控制台  │◄────►│                                 ││
│  └─────────────┘      │  ┌───────┐  ┌───────┐  ┌───────┐││
│                        │  │Functions│ │Messaging│ │Realtime│││
│                        │  └───────┘  └───────┘  └───────┘││
│                        └─────────────────────────────────┘│
│                                      │                    │
│                        ┌─────────────┴─────────────┐       │
│                        │     Traefik (反向代理)     │       │
│                        └───────────────────────────┘       │
└──────────────────────────────────────────────────────────┘
```

### 技术栈

- **后端**：PHP (Swoole)
- **数据库**：MariaDB 或 MongoDB
- **缓存**：Redis
- **代理**：Traefik
- **容器**：Docker & Docker Compose

## 部署教程

### 系统要求

- **CPU**：2 核心
- **内存**：4GB RAM
- **交换空间**：2GB
- **磁盘**：10GB+
- **Docker**：Docker Engine 20.10+
- **Docker Compose**：v2

### Docker 安装（推荐）

#### 快速安装

```bash
# Linux/macOS
docker run -it --rm \
  --publish 20080:20080 \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  --volume "$(pwd)"/appwrite:/usr/src/code/appwrite:rw \
  --entrypoint="install" \
  appwrite/appwrite:1.9.0

# Windows (CMD)
docker run -it --rm ^
  --publish 20080:20080 ^
  --volume //var/run/docker.sock:/var/run/docker.sock ^
  --volume "%cd%"/appwrite:/usr/src/code/appwrite:rw ^
  --entrypoint="install" ^
  appwrite/appwrite:1.9.0

# Windows (PowerShell)
docker run -it --rm `
    --publish 20080:20080 `
    --volume /var/run/docker.sock:/var/run/docker.sock `
    --volume ${pwd}/appwrite:/usr/src/code/appwrite:rw `
    --entrypoint="install" `
    appwrite/appwrite:1.9.0
```

安装向导将引导你完成配置：

1. **设置主机名**：输入你的域名或 IP
2. **选择数据库**：MongoDB 或 MariaDB
3. **配置邮箱**：SMTP 配置
4. **创建管理员账户**
5. **完成安装**

访问 `http://localhost:20080` 开始配置。

#### Docker Compose 安装

```bash
# 创建项目目录
mkdir -p appwrite && cd appwrite

# 下载官方配置
wget -q -O docker-compose.yml https://raw.githubusercontent.com/appwrite/appwrite/v1.9.0/docker-compose.yml
wget -q -O .env https://raw.githubusercontent.com/appwrite/appwrite/v1.9.0/.env.example

# 编辑环境变量（可选）
nano .env

# 启动服务
docker compose up -d

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f
```

等待几分钟让所有服务启动，然后访问 `http://localhost` 或你的域名。

### 一键部署平台

| 平台 | 部署链接 |
|------|---------|
| DigitalOcean | [点击部署](https://marketplace.digitalocean.com/apps/appwrite) |
| AWS | [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-2hiaeo2px4md6) |
| Google Cloud | Cloud Run / Compute Engine |
| Akamai | [Linode Marketplace](https://www.linode.com/marketplace/apps/appwrite/) |

### Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name appwrite.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name appwrite.yourdomain.com;

    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 配置与使用

### 初始设置

1. 访问 Appwrite 控制台
2. 使用管理员邮箱登录
3. 创建第一个项目
4. 获取项目 ID 和 API Key

### 创建第一个应用

1. 在控制台点击 **创建项目**
2. 选择平台（Web、iOS、Android、Flutter）
3. 获取平台配置（hostname、API Key）
4. 安装 SDK 并开始开发

### 启用服务

在项目设置中启用所需服务：

```bash
# 控制台路径
# 项目设置 → 产品 → 选择需要的服务 → 启用
```

### 环境变量详解

`.env` 文件常用配置：

```bash
# 应用配置
_APP_ENV=production
_APP_DOMAIN=appwrite.yourdomain.com
_APP_PROTOCOL=https

# 数据库
_APP_DB(provider)=mariadb  # 或 mongodb
_APP_DB_HOST=mariadb
_APP_DB_PORT=3306

# Redis
_APP_REDIS_HOST=redis
_APP_REDIS_PORT=6379
_APP_REDIS_PASS=

# 安全
_APP_OPENSSL_KEY_V1=your-64-char-secret
_APP_EXAMPLE_SECRET=another-secret

# SMTP 邮件
_SMTP_HOST=smtp.mailtrap.io
_SMTP_PORT=2525
_SMTP_USERNAME=your-username
_SMTP_PASSWORD=your-password
_SMTP_FROM=app@mail.com
```

## SDK 使用示例

### JavaScript

```bash
npm install appwrite
```

```javascript
import { Client, Account, ID } from "appwrite";

const client = new Client()
  .setEndpoint("https://cloud.appwrite.io/v1")
  .setProject("<PROJECT_ID>");

const account = new Account(client);

// 注册
async function register(email, password, name) {
  await account.create(ID.unique(), email, password, name);
  await account.createEmailSession(email, password);
}

// 获取当前用户
async function getCurrentUser() {
  return await account.get();
}
```

### Flutter

```bash
flutter pub add appwrite
```

```dart
import 'package:appwrite/appwrite.dart';

final client = Client()
  .setEndpoint('https://cloud.appwrite.io/v1')
  .setProject('<PROJECT_ID>');

final account = Account(client);

Future<void> register(String email, String password, String name) async {
  await account.create(
    ID.unique(),
    email,
    password,
    name,
  );
  await account.createEmailSession(email, password);
}
```

### Python

```bash
pip install appwrite
```

```python
from appwrite.client import Client
from appwrite.services.account import Account

client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project('<PROJECT_ID>')

account = Account(client)

# 注册
account.create(
    user_id='unique()',
    email='user@example.com',
    password='password',
    name='User Name'
)

# 登录
account.create_email_session(
    email='user@example.com',
    password='password'
)
```

## 云函数开发

### 创建函数

1. 控制台 → Functions → 创建函数
2. 选择运行时（Node.js、Python、PHP、Ruby、Go、Dart）
3. 上传代码或连接 Git 仓库
4. 配置触发器

### 示例：Node.js 函数

```javascript
module.exports = async function (req, res) {
  const { name } = req.payload;
  
  res.json({
    message: `Hello, ${name}!`,
    timestamp: new Date().toISOString()
  });
};
```

### 函数执行

```bash
# 使用 CLI 部署
appwrite functions create \
  --name "my-function" \
  --runtime "node-18.0"

# 调用函数
appwrite functions createExecution \
  --function-id "<FUNCTION_ID>"
```

## 数据备份

### 备份数据库

```bash
# MariaDB
docker exec appwrite-mariadb mysqldump -u root -p appwrite > backup.sql

# MongoDB
docker exec appwrite-mongodb mongodump --archive=backup.archive
```

### 备份文件存储

```bash
tar -czf appwrite-storage-backup.tar.gz /path/to/appwrite/appwrite/storage
```

### 完整备份脚本

```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker exec appwrite-mariadb mysqldump -u root -p${DB_ROOT_PASS} --all-databases > $BACKUP_DIR/db_$DATE.sql

# 备份存储
tar -czf $BACKUP_DIR/storage_$DATE.tar.gz /path/to/appwrite/appwrite/storage

# 保留最近 7 天的备份
find $BACKUP_DIR -mtime +7 -delete
```

## 更新 Appwrite

```bash
cd appwrite

# 拉取最新镜像
docker compose pull

# 重启服务
docker compose up -d

# 查看日志确认更新
docker compose logs -f appwrite
```

## 常见问题

### Q: Appwrite 是否有使用限制？

A: 自托管版本没有使用限制。Appwrite Cloud 有免费层限制，但自托管完全免费无限使用。

### Q: 支持哪些数据库？

A: 支持 MariaDB（默认）和 MongoDB。可以在安装时选择。

### Q: 如何升级？

A: 使用 Docker Compose 时，只需拉取新镜像并重启即可。注意查看升级文档中的重大变更。

### Q: 是否支持 ARM 架构？

A: 是的，Appwrite 支持 ARM64 架构，可以在树莓派等设备上运行。

### Q: 如何获取帮助？

A: 访问 [Appwrite Discord](https://appwrite.io/discord) 社区，或查看 [官方文档](https://appwrite.io/docs)。

## 项目资源

- **GitHub**: https://github.com/appwrite/appwrite
- **官网**: https://appwrite.io/
- **文档**: https://appwrite.io/docs
- **Discord**: https://appwrite.io/discord
- **SDK**: https://github.com/appwrite/sdk-for-*

## 适用场景

1. **移动应用后端**：快速为 iOS/Android 应用搭建后端服务
2. **SaaS 产品**：构建多租户应用
3. **创业项目**：减少后端开发工作量，专注核心功能
4. **学习项目**：了解完整应用架构
5. **企业内部工具**：完全控制数据，满足合规要求

---

*最后更新：2026-06-21*
