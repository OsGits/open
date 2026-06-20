# Seafile开源项目详解：开源云存储与文件同步平台部署教程

## 一、项目概述

**Seafile** 是一款开源的云存储和文件同步平台，采用客户端-服务器架构，支持跨平台文件同步、共享和协作。它由北京Seafile公司开发，自2012年起已服务全球数百万用户，被广泛应用于高校、企业和个人NAS场景。

Seafile 的核心特点是采用类似 Git 的增量同步机制——文件被分块存储，只传输变化的部分，这使得它的同步速度远快于 Nextcloud 等传统方案。另一个杀手级功能是**库级端到端加密**，每个库可以设置独立的密码，服务器只存储加密后的数据块，永远无法读取用户文件。项目在 GitHub 上获得 12K+ Stars。

- **GitHub 地址**：https://github.com/haiwen/seafile
- **官方网站**：https://www.seafile.com
- **开源协议**：AGPLv3（社区版）
- **开发语言**：Python（C）+ JavaScript
- **核心定位**：高性能自托管云存储和文件同步平台

### 1.1 核心特性

| 特性 | 说明 |
| ---- | ---- |
| **增量同步** | 块级同步，仅传输变化部分，速度极快 |
| **端到端加密** | 库级加密，服务器无法读取用户数据 |
| **虚拟磁盘** | SeaDrive 客户端，访问云端文件如本地磁盘 |
| **协作编辑** | 内置 SeaDoc 协作文档编辑器 |
| **版本控制** | 保留文件所有历史版本 |
| **文件锁定** | 防止并发编辑冲突 |
| **知识库** | 内置 Wiki 功能 |
| **审计日志** | 完整的操作审计日志 |

### 1.2 与同类产品对比

| 特性 | Seafile | Nextcloud | Dropbox | Google Drive |
|------|---------|-----------|---------|--------------|
| **同步速度** | 最快 | 较慢 | 快 | 快 |
| **端到端加密** | 库级免费 | 付费插件 | ❌ | ❌ |
| **虚拟磁盘** | SeaDrive | ❌ | ❌ | ❌ |
| **块存储** | ✅ | ❌ | 未知 | 未知 |
| **RAM 占用** | ~200MB | ~500MB+ | 云服务 | 云服务 |
| **数据库** | SQLite/MySQL | MySQL/PostgreSQL | 云服务 | 云服务 |

---

## 二、系统要求

| 项目 | 最低要求 | 推荐配置 |
| ---- | -------- | -------- |
| CPU | 1 核 | 2 核+ |
| 内存 | 1 GB | 2 GB+ |
| 磁盘 | 10 GB | 50 GB+ |
| 系统 | Ubuntu 18.04+ | Ubuntu 22.04+ |
| 数据库 | MySQL 5.7+ | MySQL 8.0 |

---

## 三、Docker Compose 部署

### 3.1 创建配置

```bash
mkdir -p seafile-compose && cd seafile-compose
```

### 3.2 创建 docker-compose.yml

```yaml
version: "3.8"

services:
  db:
    image: mariadb:10.11
    container_name: seafile_db
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: "${MARIADB_ROOT}"
      MARIADB_AUTO_UPGRADE: "true"
    volumes:
      - db:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password

  memcached:
    image: memcached:1.6-alpine
    container_name: seafile_memcached
    restart: unless-stopped
    entrypoint: memcached -m 256

  seafile:
    image: seafileltd/seafile-mc:latest
    container_name: seafile
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      DB_HOST: db
      DB_ROOT_PASSWD: "${MARIADB_ROOT}"
      TIME_ZONE: "Asia/Shanghai"
      SEAFILE_ADMIN_EMAIL: "${ADMIN_EMAIL}"
      SEAFILE_ADMIN_PASSWORD: "${ADMIN_PASSWORD}"
      SEAFILE_SERVER_LETSENCRYPT: "false"
      SEAFILE_SERVER_HOSTNAME: "${DOMAIN}"
    volumes:
      - seafile_data:/shared
    depends_on:
      - db
      - memcached

volumes:
  db:
  seafile_data:
```

### 3.3 创建 .env 文件

```bash
cat > .env <<EOF
MARIADB_ROOT=your-mysql-root-password
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your-admin-password
DOMAIN=files.example.com
EOF
```

### 3.4 启动服务

```bash
docker compose up -d

# 查看日志
docker compose logs -f
```

### 3.5 访问 Seafile

启动后，访问 `http://your-server-ip:8080`，使用管理员账号登录。

---

## 四、HTTPS 配置

### 4.1 使用 Caddy（推荐）

```bash
# Caddyfile
files.example.com {
    reverse_proxy localhost:8080
}
```

### 4.2 使用 Nginx

```nginx
server {
    listen 443 ssl;
    server_name files.example.com;

    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;

    client_max_body_size 10G;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /seafhttp {
        proxy_pass http://127.0.0.1:8082;
        rewrite ^/seafhttp(.*)$ $1 break;
    }
}
```

---

## 五、客户端使用

### 5.1 下载客户端

从 https://www.seafile.com/download 下载客户端（支持 Windows、macOS、Linux）。

### 5.2 连接服务器

1. 打开 Seafile 客户端
2. 点击 **添加账号**
3. 服务器地址：`https://files.example.com`
4. 输入用户名和密码

### 5.3 同步库

1. 登录后，右键点击要同步的库
2. 选择 **同步此库到本地**
3. 选择本地文件夹位置

---

## 六、端到端加密

### 6.1 创建加密库

1. 点击 **创建库**
2. 勾选 **加密**
3. 设置库密码
4. 确认密码

> ⚠️ **重要**：Seafile 无法恢复此密码，如果丢失，数据将无法恢复！

### 6.2 工作原理

```
你的设备
  ↓ 用库密码加密文件（AES-256）
  ↓ 只发送加密后的数据块
服务器存储：[加密块1] [加密块2] [元数据]
服务器：永远无法读取文件内容（没有密码）

另一台设备
  ↓ 下载加密块
  ↓ 输入库密码解密
  ↓ 显示可读文件
```

### 6.3 在新设备上解锁

1. 在新设备上同步加密库
2. 输入库密码
3. 文件在本地解密后显示

---

## 七、SeaDrive 虚拟磁盘

### 7.1 安装 SeaDrive

从 https://www.seafile.com/download 下载 SeaDrive 客户端。

### 7.2 配置 SeaDrive

1. 打开 SeaDrive
2. 设置服务器地址：`https://files.example.com`
3. 登录账号
4. 选择要映射为虚拟磁盘的库

### 7.3 使用方式

虚拟磁盘像本地硬盘一样工作：
- 文件保存在云端，按需下载
- 不占用本地存储空间
- 离线时仍可查看已缓存内容

---

## 八、SeaDoc 协作编辑

### 8.1 创建 SeaDoc

1. 进入库
2. 点击 **新建 → SeaDoc**
3. 输入文档名称

### 8.2 协作编辑

1. 打开 SeaDoc
2. 点击右上角 **共享**
3. 设置协作者权限
4. 协作者可以通过链接实时编辑

### 8.3 支持格式

- Markdown
- 富文本
- 表格
- 代码块

---

## 九、管理功能

### 9.1 用户管理

1. 进入 **系统管理**
2. 点击 **用户**
3. 创建/编辑/禁用用户

### 9.2 库管理

1. 查看所有库
2. 转移库所有权
3. 清理过期文件

### 9.3 存储管理

配置外部存储（S3/Azure/GCS）：

```yaml
# Seafile 配置
SEAFILE_STORAGE_CLASS = {
    'my-storage': {
        'backend': 's3',
        'bucket': 'my-bucket',
        'key': 'access-key',
        'secret': 'secret-key',
        'host': 's3.amazonaws.com',
    }
}
```

---

## 十、API 使用

### 10.1 获取 Token

```bash
curl -X POST https://files.example.com/api2/auth-token/ \
  -d "username=admin@example.com&password=your-password"
```

### 10.2 上传文件

```bash
curl -X POST https://files.example.com/api2/repos/{repo-id}/upload-link/ \
  -H "Authorization: Token {your-token}"

# 使用返回的上传链接上传
curl -X POST {upload-link} \
  -F file=@example.txt
```

---

## 十一、常见问题与解决方案

### 11.1 同步失败

**解决方案**：
1. 检查网络连接
2. 确认服务器地址正确
3. 清理客户端缓存后重试

### 11.2 库密码忘记

**解决方案**：
❌ 无法恢复！库密码无法重置，请妥善保管。

### 11.3 存储空间不足

**解决方案**：
1. 清理不需要的文件
2. 配置外部 S3 存储
3. 添加更多硬盘并配置 RAID

### 11.4 性能优化

**解决方案**：
1. 启用 Memcached
2. 使用 SSD 硬盘
3. 配置 Redis 缓存
4. 优化数据库配置

---

## 十二、安全建议

| 建议 | 说明 |
| ---- | ---- |
| **HTTPS** | 强制使用 HTTPS |
| **强密码** | 使用强库密码和账户密码 |
| **双因素认证** | 启用 2FA |
| **定期备份** | 定期备份数据库和文件 |
| **访问控制** | 配置防火墙限制访问 |

---

## 十三、社区与生态

| 资源 | 地址 |
| ---- | ---- |
| **GitHub** | https://github.com/haiwen/seafile |
| **官网** | https://www.seafile.com |
| **文档** | https://help.seafile.com |
| **论坛** | https://forum.seafile.com |

---

## 总结

Seafile 是一款高性能、功能全面的开源云存储平台。它的增量同步机制使得文件同步速度远超同类产品，而库级端到端加密功能更是为注重隐私的用户提供了强有力的数据保护。结合虚拟磁盘 SeaDrive 和协作文档 SeaDoc，Seafile 能够满足从个人使用到团队协作的多种场景需求。

它的核心优势在于：

- **同步速度快**：块级增量同步，比 Nextcloud 快数倍
- **端到端加密**：库级免费加密，服务器无法读取数据
- **虚拟磁盘**：SeaDrive 让云端文件如本地般使用
- **资源占用低**：最低仅需 200MB 内存
- **功能完整**：版本控制、文件锁定、协作编辑一应俱全

对于需要自托管私有云盘、追求数据主权和同步性能的用户来说，Seafile 是一个极佳的选择。

> **立即体验**：访问 https://www.seafile.com 了解更多，或使用 Docker Compose 部署自托管版本。
