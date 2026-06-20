# Authentik开源项目详解：开源身份认证提供者部署教程与SSO单点登录解决方案

## 一、项目概述

**Authentik** 是一款开源的身份认证提供者（IdP），专为现代 SSO（单点登录）设计。它支持 SAML 2.0、OAuth2/OIDC、LDAP、RADIUS 等多种认证协议，适用于从个人实验室到大型生产集群的各种场景。

Authentik 的设计理念是"安全、开源、可自托管的身份认证平台"。它可以完美替代 Okta、Auth0、Microsoft Entra ID、Ping Identity 等商业 IdP，同时保持对数据的完全控制。项目在 GitHub 上获得 30K+ Stars，是自托管身份认证领域最受欢迎的开源解决方案。

- **GitHub 地址**：https://github.com/goauthentik/authentik
- **官方网站**：https://goauthentik.io
- **开源协议**：MIT
- **开发语言**：Python（Django）+ TypeScript
- **核心定位**：开源身份认证提供者，支持 SSO、SAML、OAuth2

### 1.1 核心特性

| 特性 | 说明 |
| ---- | ---- |
| **多协议支持** | SAML 2.0、OAuth2、OIDC、LDAP、RADIUS |
| **单点登录** | 一次登录，访问所有应用 |
| **用户管理** | 内置用户管理和邀请系统 |
| **LDAP 集成** | 集成现有目录服务 |
| **强密码策略** | 可配置密码复杂度要求 |
| **MFA 支持** | 支持 TOTP、WebAuthn 等多因素认证 |
| **社交登录** | 支持 Google、GitHub 等社交账号登录 |
| **审计日志** | 完整的登录和操作审计日志 |

### 1.2 与同类产品对比

| 特性 | Authentik | Okta | Auth0 | Keycloak |
|------|------------|------|-------|----------|
| **协议支持** | SAML/OIDC/LDAP | SAML/OIDC | SAML/OIDC | SAML/OIDC |
| **用户界面** | 现代美观 | 优秀 | 优秀 | 一般 |
| **学习曲线** | 中等 | 低 | 低 | 陡峭 |
| **开源** | ✅ | ❌ | ❌ | ✅ |
| **自托管** | ✅ | ❌ | ❌ | ✅ |
| **Active Directory** | LDAP 集成 | 原生支持 | 集成 | 集成 |

---

## 二、系统要求

| 项目 | 最低要求 | 推荐配置 |
| ---- | -------- | -------- |
| CPU | 1 核 | 2 核+ |
| 内存 | 2 GB | 4 GB+ |
| 磁盘 | 10 GB | 30 GB+ |
| 系统 | Ubuntu 20.04+ | Ubuntu 22.04+ |
| PostgreSQL | 13+ | 14+ |
| Redis | 6+ | 7+ |

---

## 三、Docker Compose 部署

### 3.1 创建 docker-compose.yml

```yaml
version: "3.8"

services:
  postgresql:
    image: postgres:16-alpine
    container_name: authentik_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: authentik
      POSTGRES_USER: authentik
      POSTGRES_PASSWORD: your-postgres-password
    volumes:
      - postgresql_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: authentik_redis
    restart: unless-stopped

  authentik:
    image: goauthentik.io/authentik:latest
    container_name: authentik
    restart: unless-stopped
    ports:
      - "9000:9000"
      - "9443:9443"
    environment:
      AUTHENTIK_POSTGRES_HOST: postgresql
      AUTHENTIK_POSTGRES_NAME: authentik
      AUTHENTIK_POSTGRES_USER: authentik
      AUTHENTIK_POSTGRES_PASSWORD: your-postgres-password
      AUTHENTIK_REDIS_HOST: redis
      AUTHENTIK_SECRET_KEY: your-secret-key
      AUTHENTIK_ERROR_REPORTING__ENABLED: "false"
    volumes:
      - ./authentik_data:/data
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - postgresql
      - redis

volumes:
  postgresql_data:
```

### 3.2 启动服务

```bash
# 启动所有服务
docker compose up -d

# 初始化数据库
docker compose exec authentik authentik migrate

# 创建管理员账户
docker compose exec authentik authentik createsuperuser
```

### 3.3 访问 Authentik

- 访问 `http://your-server-ip:9000` 或 `https://your-domain:9443`
- 默认管理员用户名：`akadmin`

---

## 四、Kubernetes Helm 部署

### 4.1 添加 Helm 仓库

```bash
helm repo add authentik https://charts.goauthentik.io
helm repo update
```

### 4.2 安装 Authentik

```bash
helm install authentik authentik/authentik \
  --set authentik.secret_key=your-secret-key \
  --set postgresql.auth.password=your-db-password \
  -n authentik --create-namespace
```

---

## 五、基本配置

### 5.1 配置管理员

首次登录后，进入 **Settings → Admin Interface** 进行配置。

### 5.2 配置 SSL/HTTPS

**方式一：使用 Authentik 内置 SSL**

```yaml
environment:
  AUTHENTIK_OUTPOSTS__TYPE: authentik
  AUTHENTIK_LISTEN__HTTPS: ":9443"
  AUTHENTIK_LISTEN__HTTP: ":9000"
```

**方式二：使用 Nginx 反向代理**

```nginx
server {
    listen 443 ssl;
    server_name auth.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /outpost.goauthentik.io {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
    }
}
```

---

## 六、集成应用

### 6.1 创建应用程序

1. 进入 **Applications → Applications**
2. 点击 **Create**
3. 填写应用信息：
   - 名称
   - slug（URL 标识）
   - 描述
4. 点击 **Create**

### 6.2 配置 OIDC 提供者

对于支持 OIDC 的应用：

```yaml
Client ID: your-client-id
Client Secret: your-client-secret
Authorization URL: https://auth.yourdomain.com/application/o/authorize/
Token URL: https://auth.yourdomain.com/application/o/token/
User Info URL: https://auth.yourdomain.com/application/o/userinfo/
```

### 6.3 配置 SAML 提供者

对于使用 SAML 的应用：

```xml
Entity ID: https://auth.yourdomain.com/application/saml/your-app/slk/
ACS URL: https://your-app.com/saml/acs/
SLO URL: https://your-app.com/saml/slo/
```

### 6.4 常用应用集成示例

**Nextcloud**：

1. 在 Authentik 创建应用，获取 client_id 和 secret
2. 在 Nextcloud 安装 **OpenID Connect** 应用
3. 配置 Nextcloud：

```yaml
'overwrite.cli.url' => 'https://cloud.yourdomain.com',
'openid_connect' => [
    'provider_url' => 'https://auth.yourdomain.com',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
],
```

**Proxmox**：

1. 在 Authentik 创建 OIDC 提供者
2. 在 Proxmox 配置：

```
Realm: authentik
Client ID: your-client-id
Client Secret: your-client-secret
Issuer URL: https://auth.yourdomain.com/application/o/your-app/
```

---

## 七、用户管理

### 7.1 创建用户

1. 进入 **Directory → Users**
2. 点击 **Create User**
3. 填写用户信息：
   - 用户名
   - 邮箱
   - 姓名
   - 密码
4. 点击 **Create**

### 7.2 用户组管理

1. 进入 **Directory → Groups**
2. 点击 **Create Group**
3. 添加组成员

### 7.3 LDAP 配置

启用内置 LDAP 提供者：

1. 进入 **Settings → LDAP**
2. 启用 LDAP 提供者
3. 配置绑定用户
4. 测试连接

---

## 八、MFA 多因素认证

### 8.1 启用 MFA

1. 进入 **Directory → Users**
2. 选择用户
3. 点击 **Authenticators**
4. 添加 TOTP 或 WebAuthn

### 8.2 全局强制 MFA

1. 进入 **Settings → Flows**
2. 编辑默认登录流程
3. 添加 MFA 阶段

---

## 九、社交登录配置

### 9.1 配置 GitHub 登录

1. 在 GitHub Developer Settings 创建 OAuth App
2. 设置回调 URL：`https://auth.yourdomain.com/source/github/your-source-slug/callback/`
3. 在 Authentik 创建 Source：
   - 进入 **Sources → Social Sources**
   - 创建 GitHub Source
   - 填入 Client ID 和 Secret

### 9.2 支持的社交登录

| 提供商 | 配置难度 |
| ---- | -------- |
| Google | 简单 |
| GitHub | 简单 |
| Twitter/X | 中等 |
| Discord | 简单 |
| Microsoft | 中等 |
| Facebook | 简单 |

---

## 十、审计日志

### 10.1 查看日志

1. 进入 **Audit Logs**
2. 查看所有认证和授权事件

### 10.2 日志内容

- 登录尝试（成功/失败）
- 密码更改
- MFA 操作
- 应用访问
- 用户管理操作

---

## 十一、常见问题与解决方案

### 11.1 首次登录失败

**解决方案**：
```bash
# 重置管理员密码
docker compose exec authentik authentik createsuperuser --force
```

### 11.2 OIDC 回调失败

**解决方案**：
1. 检查 Redirect URI 配置是否正确
2. 确认 Redirect URI 完全匹配（包括 trailing slash）
3. 检查时间同步

### 11.3 LDAP 连接问题

**解决方案**：
1. 确认 LDAP 端口开放
2. 检查绑定 DN 和密码
3. 查看日志获取详细信息

### 11.4 邮件发送失败

**解决方案**：
```yaml
environment:
  AUTHENTIK_EMAIL__USE_TLS: "true"
  AUTHENTIK_EMAIL__HOST: smtp.example.com
  AUTHENTIK_EMAIL__PORT: 587
  AUTHENTIK_EMAIL__USERNAME: user
  AUTHENTIK_EMAIL__PASSWORD: password
  AUTHENTIK_EMAIL__FROM: authentik@yourdomain.com
```

---

## 十二、安全建议

| 建议 | 说明 |
| ---- | ---- |
| **HTTPS** | 强制使用 HTTPS |
| **强密码** | 配置密码复杂度要求 |
| **MFA** | 强制所有用户启用 MFA |
| **定期更新** | 及时更新 Authentik 版本 |
| **审计日志** | 定期审查日志 |
| **备份** | 定期备份数据库 |

---

## 十三、性能优化

### 13.1 增加 worker 数量

```yaml
environment:
  AUTHENTIK_TASK_WORKERS: 4
  AUTHENTIK_TASK_TIMEOUT: 3600
```

### 13.2 Redis 缓存配置

```yaml
environment:
  AUTHENTIK_CACHE__TIMEOUT: 300
  AUTHENTIK_CACHE_REDIS: "redis://redis:6379/1"
```

---

## 十四、社区与生态

| 资源 | 地址 |
| ---- | ---- |
| **GitHub** | https://github.com/goauthentik/authentik |
| **官网** | https://goauthentik.io |
| **文档** | https://docs.goauthentik.io |
| **Discord** | https://goauthentik.io/discord |
| **Helm Chart** | https://charts.goauthentik.io |

---

## 总结

Authentik 是一款功能强大且美观的开源身份认证平台，它提供了商业 IdP 的核心功能，同时保持了开源和自托管的灵活性。无论是个人用户保护自建服务，还是企业构建完整的 SSO 体系，Authentik 都能提供出色的解决方案。

它的核心优势在于：

- **功能完整**：支持 SAML、OAuth2、OIDC、LDAP、RADIUS 等所有主流协议
- **界面美观**：现代化的管理界面，易于使用
- **易于集成**：预置了大量常用应用的集成模板
- **开源透明**：代码完全开放，社区活跃
- **扩展性强**：支持自定义协议和提供方

对于希望摆脱商业 IdP 依赖、追求数据主权的企业和个人来说，Authentik 是一个极佳的选择。

> **立即体验**：访问 https://goauthentik.io 了解更多，或使用 Docker Compose 部署自托管版本。
