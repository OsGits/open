# Vaultwarden开源项目详解：轻量级自托管密码管理器部署教程与Bitwarden私有化实战指南

## 一、项目概述

**Vaultwarden** 是一款用 Rust 编写的轻量级 Bitwarden 服务端替代实现，专为自托管场景设计。它完全兼容 Bitwarden 官方客户端（浏览器扩展、桌面应用、移动 App），但资源占用远低于官方服务端（官方基于 .NET，需要约 2GB 内存；Vaultwarden 仅需约 20MB 内存）。项目由 Daniel García 发起并持续维护，是自托管社区中最受欢迎的密码管理解决方案之一。

- **GitHub 地址**：https://github.com/dani-garcia/vaultwarden
- **开源协议**：AGPL-3.0 License
- **Star 数量**：32K+
- **技术栈**：Rust 83.9%、Handlebars 9.9%、TypeScript 4%
- **最新版本**：v1.36.0（2026年5月3日发布）
- **总发布版本数**：83 个
- **被依赖数**：494 个项目使用
- **前身项目**：Bitwarden_RS（后更名为 Vaultwarden）

---

## 二、核心特性解读

### 1. 轻量级架构

| 指标 | Vaultwarden | Bitwarden 官方服务端 |
|------|-------------|---------------------|
| 内存占用 | 约 20MB | 约 2GB |
| 部署方式 | 单一容器 | 多容器编排（8+ 容器） |
| 启动时间 | 秒级 | 分钟级 |
| 磁盘占用 | 约 50MB | 约 1GB+ |
| 数据库 | SQLite/PostgreSQL/MySQL | MSSQL（内置） |

### 2. 完整的 Bitwarden API 兼容

Vaultwarden 实现了 Bitwarden Client API 的绝大部分功能，可直接使用官方客户端连接：

- **个人密码库**：密码、笔记、信用卡、身份信息的存储与管理
- **Send 功能**：安全地临时分享敏感信息（密码、文本、文件）
- **附件上传**：支持为密码条目添加文件附件
- **网站图标**：自动获取并显示网站 Favicon
- **组织管理**：支持创建组织、集合、分组、成员角色管理
- **事件日志**：记录组织内的操作审计日志
- **策略控制**：管理员可设置密码策略、两步登录策略等

### 3. 多因素认证（MFA）

支持多种两步验证方式，全方位保障账户安全：

- **Authenticator（TOTP）**：基于时间的一次性密码
- **Email 邮件验证**：通过邮箱接收验证码
- **FIDO2 / WebAuthn**：硬件安全密钥（如 YubiKey）
- **YubiKey OTP**：YubiKey 一次性密码
- **Duo**：Duo Security 集成

### 4. 紧急访问（Emergency Access）

允许指定紧急联系人，在账户持有者长期未活跃时（可设置等待时间），紧急联系人可申请获取密码库访问权限。

### 5. 管理后台

内置 Web 管理后台，可查看用户列表、管理组织、配置系统参数。

---

## 三、适用场景

| 场景 | 说明 |
|------|------|
| 个人密码管理 | 替代 1Password、LastPass，数据完全自控 |
| 家庭共享密码 | 家庭成员间安全共享 WiFi、流媒体等密码 |
| 团队/企业密码库 | 小型团队统一管理服务器、API 密钥等凭证 |
| VPS/服务器运维 | 低资源服务器上部署，内存占用极低 |
| NAS 自托管 | 群晖、Unraid 等 NAS 设备上轻松运行 |
| 隐私安全优先 | 拒绝将密码存储在第三方云端 |

---

## 四、部署方法详解

### 方法一：Docker 快速部署（推荐）

```bash
docker pull vaultwarden/server:latest

docker run --detach --name vaultwarden \
  --env DOMAIN="https://vw.domain.tld" \
  --volume /vw-data/:/data/ \
  --restart unless-stopped \
  --publish 127.0.0.1:8000:80 \
  vaultwarden/server:latest
```

> **注意**：`DOMAIN` 环境变量必须设置为你实际访问的域名，否则 Web Vault 的加密功能将无法正常工作。

### 方法二：Docker Compose 部署

创建 `compose.yaml` 文件：

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    environment:
      DOMAIN: "https://vw.domain.tld"
    volumes:
      - ./vw-data/:/data/
    ports:
      - "127.0.0.1:8000:80"
```

启动服务：

```bash
docker compose up -d
```

### 方法三：使用 PostgreSQL 数据库（生产推荐）

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    environment:
      DOMAIN: "https://vw.domain.tld"
      DATABASE_URL: "postgresql://vaultwarden:yourpassword@db:5432/vaultwarden"
    volumes:
      - ./vw-data/:/data/
    ports:
      - "127.0.0.1:8000:80"
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    container_name: vaultwarden-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: vaultwarden
      POSTGRES_PASSWORD: yourpassword
      POSTGRES_DB: vaultwarden
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
```

---

## 五、进阶配置

### Nginx 反向代理 + HTTPS（必须）

Web Vault 依赖 Web Crypto API，**必须使用 HTTPS** 才能正常工作：

```nginx
server {
    listen 80;
    server_name vw.domain.tld;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name vw.domain.tld;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    client_max_body_size 128M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 启用管理后台

```bash
docker run --detach --name vaultwarden \
  --env DOMAIN="https://vw.domain.tld" \
  --env ADMIN_TOKEN="your_secure_random_token_here" \
  --volume /vw-data/:/data/ \
  --restart unless-stopped \
  --publish 127.0.0.1:8000:80 \
  vaultwarden/server:latest
```

设置 `ADMIN_TOKEN` 后，访问 `https://vw.domain.tld/admin` 即可进入管理后台。

> **安全提示**：务必使用强随机字符串作为 `ADMIN_TOKEN`，切勿使用弱密码。

### 备份策略

```bash
# 备份数据目录（包含数据库和附件）
tar -czf vaultwarden-backup-$(date +%Y%m%d).tar.gz /vw-data/

# 定时备份（crontab，每天凌晨 3 点）
0 3 * * * tar -czf /backup/vaultwarden-$(date +\%Y\%m\%d).tar.gz /vw-data/
```

---

## 六、客户端配置

部署完成后，使用 Bitwarden 官方客户端连接你的私有服务器：

1. **浏览器扩展**：在 Chrome/Firefox/Edge 安装 Bitwarden 扩展，登录时点击齿轮图标，在"自托管"区域填入服务器 URL（如 `https://vw.domain.tld`）
2. **桌面应用**：下载 Bitwarden 桌面客户端，登录页面选择"自托管"，输入服务器地址
3. **移动端**：iOS/Android 下载 Bitwarden App，登录时选择"自托管"选项
4. **CLI 工具**：`bw config server https://vw.domain.tld`

---

## 七、与其他密码管理器对比

| 特性 | Vaultwarden | Bitwarden 官方 | 1Password | LastPass |
|------|-------------|---------------|-----------|----------|
| 自托管 | ✅ | ❌（仅企业版） | ❌ | ❌ |
| 免费使用 | ✅ 完全免费 | 免费版受限 | 付费 | 免费版受限 |
| 内存占用 | ~20MB | ~2GB | N/A | N/A |
| 客户端兼容 | Bitwarden 全系 | Bitwarden 全系 | 专用客户端 | 专用客户端 |
| 开源 | ✅（AGPL-3.0） | ✅（部分） | ❌ | ❌ |
| Send 功能 | ✅ | ✅ | ❌ | ❌ |
| 组织管理 | ✅ | ✅ | ✅ | ✅ |
| FIDO2 支持 | ✅ | ✅ | ✅ | ✅ |

---

## 八、安全建议

### 1. 主密码设置

- 长度至少 16 位
- 包含大小写字母、数字和特殊符号
- 使用密码短语（如 `correct-horse-battery-staple`）更易记忆
- **切勿忘记主密码**，Vaultwarden 不支持密码恢复

### 2. 两步验证

强烈建议开启至少一种两步验证方式（推荐 FIDO2/WebAuthn 硬件密钥）。

### 3. 定期备份

设置定时备份脚本，将数据目录备份到异地存储。

### 4. 保持更新

关注 Vaultwarden 的 Release 页面，及时更新到最新版本以获取安全修复。

---

## 九、总结

Vaultwarden 是自托管密码管理领域的标杆项目。它以 Rust 的高性能和极低资源占用，完美解决了 Bitwarden 官方服务端过于笨重的问题，同时保持了与官方客户端的完全兼容。对于注重隐私安全、拥有 VPS 或 NAS 的用户来说，Vaultwarden 是替代 1Password、LastPass 等商业密码管理器的最佳开源方案。一条 Docker 命令、20MB 内存，即可拥有一个功能完备的私有密码库。

---

**相关资源**

- GitHub 仓库：https://github.com/dani-garcia/vaultwarden
- 项目 Wiki（详细文档）：https://github.com/dani-garcia/vaultwarden/wiki
- Docker Hub：https://hub.docker.com/r/vaultwarden/server
- Bitwarden 官方客户端下载：https://bitwarden.com/download/
- 社区论坛：https://vaultwarden.discourse.group/
- Matrix 群组：https://matrix.to/#/#vaultwarden:matrix.org
