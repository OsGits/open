# Coolify开源项目详解：开源自托管PaaS平台部署教程与HerokuNetlify替代方案实战指南

## 一、项目概述

**Coolify** 是一款开源的自托管平台即服务（PaaS）解决方案，可以看作是 Heroku、Netlify、Vercel 的开源替代品。它帮助用户在自有硬件上管理服务器、应用程序和数据库，只需配置一个 SSH 连接即可。支持管理 VPS、物理服务器、Raspberry Pi 等各类设备。

Coolify 的核心理念是"拥有云的便利，但运行在自己的服务器上"。它不依赖任何特定云服务商，所有应用和数据库的配置都保存在你的服务器上。即使停止使用 Coolify，你仍然可以继续管理正在运行的资源。

- **GitHub 地址**：https://github.com/coollabsio/coolify
- **官方网站**：https://coolify.io
- **开源协议**：Apache 2.0
- **开发语言**：TypeScript + Vue + Go
- **核心定位**：开源自托管 PaaS，一键部署应用到自有服务器

### 1.1 核心特性

| 特性 | 说明 |
| ---- | ---- |
| **一键部署** | 支持 Git 仓库一键部署 |
| **多框架支持** | Node.js、Python、PHP、Go、Rust、Docker 等 |
| **数据库支持** | PostgreSQL、MySQL、MongoDB、Redis 等 |
| **反向代理** | 自动配置 Nginx + 免费 SSL |
| **Docker 管理** | 可视化 Docker 容器管理 |
| **资源监控** | 实时监控 CPU、内存、网络 |
| **团队协作** | 支持多用户和团队 |
| **SSH 接入** | 支持添加远程服务器 |

### 1.2 与同类产品对比

| 特性 | Coolify | Heroku | Netlify | Vercel |
|------|---------|--------|---------|--------|
| **费用** | 仅服务器费用 | 按 dyno 计费 | 按带宽计费 | 按用量计费 |
| **数据控制** | 完全私有 | 云服务 | 云服务 | 云服务 |
| **数据库** | 完全控制 | 插件市场 | 有限 | 有限 |
| **灵活性** | 极高 | 一般 | 一般 | 一般 |
| **学习曲线** | 中等 | 低 | 低 | 低 |

---

## 二、系统要求

### 2.1 Coolify 服务器要求

| 项目 | 最低要求 | 推荐配置 |
| ---- | -------- | -------- |
| CPU | 1 核 | 2 核+ |
| 内存 | 1 GB | 2 GB+ |
| 磁盘 | 10 GB | 50 GB+ |
| 系统 | Ubuntu 20.04+ / Debian 11+ | Ubuntu 22.04+ |

### 2.2 目标服务器要求

Coolify 可以管理多台目标服务器，每台服务器要求：

| 项目 | 要求 |
| ---- | ---- |
| SSH 访问 | 需要 SSH 密钥登录 |
| Docker | 需要安装 Docker |
| 网络 | 需要可以访问互联网 |

---

## 三、安装 Coolify

### 3.1 一键安装

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

### 3.2 安装后配置

1. 访问 `https://your-server-ip:3000`
2. 首次访问会引导创建管理员账户
3. 配置 SSH 密钥
4. 添加第一台服务器

### 3.3 Docker 单容器部署

```bash
docker run -d \
  --name coolify \
  -p 3000:3000 \
  -p 80:80 \
  -p 443:443 \
  -v /var/lib/coolify:/data \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  coollabsio/coolify:latest
```

---

## 四、添加服务器

### 4.1 本地 Docker 模式

默认安装后，Coolify 会自动使用本地 Docker 实例。

### 4.2 添加远程服务器

1. 进入 **服务器** 页面
2. 点击 **添加新服务器**
3. 填写服务器信息：
   - 服务器名称
   - 服务器 IP 地址
   - SSH 端口（默认 22）
   - SSH 用户名
   - SSH 密钥
4. 点击 **连接测试**
5. 测试通过后保存

### 4.3 在目标服务器上配置 SSH

```bash
# 在目标服务器上执行
# 1. 创建 coolify 用户
sudo adduser coolify
sudo usermod -aG docker coolify

# 2. 配置 SSH 密钥
sudo -u coolify mkdir -p ~/.ssh
sudo -u coolify chmod 700 ~/.ssh

# 3. 将公钥添加到 authorized_keys
# 将本地公钥内容复制到服务器
sudo -u coolify tee ~/.ssh/authorized_keys <<EOF
your-public-key-here
EOF

sudo -u coolify chmod 600 ~/.ssh/authorized_keys

# 4. 配置 sudo 免密（用于 Docker 操作）
echo "coolify ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/coolify
```

---

## 五、部署应用程序

### 5.1 支持的应用类型

| 类型 | 说明 |
| ---- | ---- |
| 静态网站 | HTML、CSS、JS |
| Node.js | Express、NestJS、Next.js |
| Python | Django、Flask、FastAPI |
| PHP | Laravel、WordPress |
| Go | Gin、Echo |
| Rust | Actix |
| Docker | 任意 Docker 镜像 |
| 数据库 | PostgreSQL、MySQL、MongoDB 等 |

### 5.2 从 Git 部署

1. 进入 **项目** 页面
2. 点击 **创建新项目**
3. 选择源代码提供商（GitHub、GitLab、Bitbucket）
4. 授权访问仓库
5. 选择要部署的仓库
6. 配置构建和部署设置

### 5.3 部署配置示例

**Next.js 应用**：

```yaml
build_command: npm run build
port: 3000
health_check_path: /
```

**Django 应用**：

```yaml
build_command: pip install -r requirements.txt && python manage.py migrate
start_command: gunicorn myproject.wsgi:application
port: 8000
```

**Go 应用**：

```yaml
build_command: go build -o app
start_command: ./app
port: 8080
```

### 5.4 环境变量配置

在部署设置中添加环境变量：

```bash
DATABASE_URL=postgres://user:pass@host:5432/db
REDIS_URL=redis://host:6379
API_KEY=your-secret-key
```

---

## 六、数据库管理

### 6.1 创建数据库

1. 进入 **数据库** 页面
2. 点击 **创建新数据库**
3. 选择数据库类型：
   - PostgreSQL
   - MySQL
   - MariaDB
   - MongoDB
   - Redis
4. 配置数据库名称和凭据
5. 选择要部署的服务器
6. 点击创建

### 6.2 连接到数据库

创建后，Coolify 会提供连接信息：

```bash
# PostgreSQL
postgres://username:password@hostname:5432/databasename

# MySQL
mysql://username:password@hostname:3306/databasename

# Redis
redis://hostname:6379
```

### 6.3 数据库持久化

数据库数据存储在服务器的持久化卷中，重启不会丢失数据。

---

## 七、反向代理与 SSL

### 7.1 自动配置

Coolify 自动配置 Nginx 作为反向代理，并为所有域名启用 Let's Encrypt 免费 SSL 证书。

### 7.2 自定义域名

1. 在应用设置中添加域名
2. 配置 DNS 记录指向服务器 IP
3. Coolify 自动获取 SSL 证书

### 7.3 SSL 证书管理

证书自动续期，无需手动操作。

---

## 八、团队协作

### 8.1 邀请团队成员

1. 进入 **团队设置**
2. 点击 **邀请成员**
3. 输入成员邮箱
4. 选择角色权限
5. 发送邀请

### 8.2 角色权限

| 角色 | 权限 |
| ---- | ---- |
| Owner | 完整管理员权限 |
| Admin | 管理服务器和项目 |
| Developer | 部署和管理应用 |
| Viewer | 只读访问 |

---

## 九、持续部署

### 9.1 自动部署

配置 Git Webhook，实现代码推送后自动部署：

1. 在项目设置中启用 **自动部署**
2. 配置要监听的分支
3. 保存 Webhook URL

### 9.2 部署钩子

```bash
# 手动触发部署
curl -X POST https://your-coolify.comapi/v1/deploy \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR-API-KEY"
```

---

## 十、资源监控

### 10.1 查看资源使用

进入应用详情页面，可以查看：

- CPU 使用率
- 内存使用量
- 网络流量
- 磁盘 I/O

### 10.2 设置告警

配置资源告警阈值：

```bash
# 当 CPU 超过 80% 时发送通知
# 在应用设置中配置
CPU_THRESHOLD=80
MEMORY_THRESHOLD=90
```

---

## 十一、常见问题与解决方案

### 11.1 SSH 连接失败

**解决方案**：
1. 检查 SSH 密钥是否正确配置
2. 确认 SSH 端口是否正确
3. 检查防火墙是否开放 SSH 端口
4. 验证 SSH 密钥权限：`chmod 600 ~/.ssh/authorized_keys`

### 11.2 Docker 操作失败

**解决方案**：
```bash
# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER
newgrp docker

# 或者使用 rootless 模式
docker run -d \
  --name coolify \
  -v /var/run/docker.sock:/var/run/docker.sock \
  ...
```

### 11.3 域名 SSL 证书获取失败

**解决方案**：
1. 确认 DNS 记录已正确配置
2. 检查域名是否可访问：`ping yourdomain.com`
3. 确认端口 80 和 443 未被占用
4. 检查 Let's Encrypt 限制

### 11.4 部署超时

**解决方案**：
1. 增加构建超时时间
2. 检查网络连接
3. 优化构建脚本
4. 使用国内镜像源

---

## 十二、迁移与备份

### 12.1 备份 Coolify 数据

```bash
# 备份数据目录
tar -czf coolify-backup-$(date +%Y%m%d).tar.gz /var/lib/coolify
```

### 12.2 恢复 Coolify

```bash
# 停止服务
docker stop coolify

# 恢复数据
tar -xzf coolify-backup.tar.gz -C /

# 重启服务
docker start coolify
```

---

## 十三、安全建议

| 建议 | 说明 |
| ---- | ---- |
| **SSH 密钥** | 使用强密钥，定期轮换 |
| **防火墙** | 仅开放必要端口（22, 80, 443） |
| **SSL** | 所有域名强制 HTTPS |
| **定期更新** | 及时更新 Coolify 版本 |
| **备份** | 定期备份数据目录 |
| **访问控制** | 限制管理界面访问 |

---

## 十四、社区与生态

| 资源 | 地址 |
| ---- | ---- |
| **GitHub** | https://github.com/coollabsio/coolify |
| **官网** | https://coolify.io |
| **文档** | https://coolify.io/docs |
| **Discord** | https://discord.gg/coolify |
| **云服务** | https://app.coolify.io |

---

## 总结

Coolify 是一款极具实用价值的开源 PaaS 平台，它让个人开发者和小型团队能够以极低的成本拥有类似 Heroku 的部署体验。与传统的服务器管理方式相比，Coolify 大幅简化了应用部署、数据库管理、SSL 证书配置等工作，让你能够专注于代码开发而不是运维。

它的核心优势在于：

- **零成本替代商业 PaaS**：只需支付服务器费用，省去昂贵的平台费用
- **完全私有**：所有数据和资源都在自己的服务器上
- **一键部署**：支持多种语言和框架，Git 推送即可部署
- **自动运维**：自动配置 Nginx、SSL、数据库等
- **可扩展**：支持添加多台服务器，轻松扩展

对于希望降低云服务成本、追求数据主权、或者在自有基础设施上部署应用的开发者来说，Coolify 是一个绝佳的选择。

> **立即体验**：访问 https://coolify.io 了解更多信息，或执行 `curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash` 一键安装。
