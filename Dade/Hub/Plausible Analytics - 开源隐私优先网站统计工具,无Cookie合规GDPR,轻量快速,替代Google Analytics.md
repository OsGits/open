# Plausible Analytics开源项目详解：隐私优先网站统计平台部署教程与Google Analytics替代方案

## 一、项目概述

**Plausible Analytics** 是一款开源的隐私优先网站分析工具，轻量级、无 Cookie，完全符合 GDPR、CCPA 和 PECR 法规。它是 Google Analytics 的绝佳替代方案，提供简单、快速、注重隐私的网站统计分析。

Plausible 的设计理念是"只衡量流量，不追踪个人"。不存储任何个人数据、不使用 Cookie、不追踪跨网站用户，所有数据都存储在你的服务器上。目前在 GitHub 上获得 22K+ Stars，被数千个网站信赖使用。

- **GitHub 地址**：https://github.com/plausible/analytics
- **官方网站**：https://plausible.io
- **开源协议**：MIT（社区版）
- **开发语言**：Elixir（后端）+ React（前端）
- **核心定位**：隐私优先、无 Cookie 的网站分析平台

### 1.1 核心特性

| 特性 | 说明 |
| ---- | ---- |
| **隐私优先** | 不使用 Cookie，不追踪个人数据 |
| **GDPR 合规** | 完全符合 GDPR、CCPA、PECR |
| **轻量脚本** | 仅 1KB，对网站性能无影响 |
| **开源透明** | 代码完全开放，可自托管 |
| **简单仪表盘** | 无需培训，一看就懂 |
| **实时数据** | 实时查看访客数据 |
| **无数据锁定** | 可导出所有数据 |

### 1.2 与同类产品对比

| 特性 | Plausible | Google Analytics | Matomo | Fathom |
|------|-----------|-----------------|--------|--------|
| **Cookie** | 无需 | 必须 | 可选 | 无 |
| **隐私合规** | 完全合规 | 需要配置 | 需要配置 | 完全合规 |
| **脚本大小** | ~1KB | ~44KB | ~50KB | ~1KB |
| **开源** | ✅ | ❌ | ✅ | ❌ |
| **自托管** | ✅ | ❌ | ✅ | ✅ |
| **价格** | 低成本 | 免费+增值 | 免费/付费 | 按网站计费 |

---

## 二、系统要求

| 项目 | 最低要求 | 推荐配置 |
| ---- | -------- | -------- |
| CPU | 1 核 | 2 核+ |
| 内存 | 1 GB | 2 GB+ |
| 磁盘 | 10 GB | 30 GB+ |
| 系统 | Ubuntu 20.04+ | Ubuntu 22.04+ |
| PostgreSQL | 12+ | 14+ |
| ClickHouse | 21+ | 22+ |

---

## 三、Docker Compose 部署

### 3.1 创建 docker-compose.yml

```yaml
version: "3.8"

services:
  plausible:
    image: plausible/analytics:latest
    container_name: plausible
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgres://postgres:postgres@db:5432/plausible
      BASE_URL: https://yourdomain.com
      SECRET_KEY_BASE: your-secret-key-base-here
      SMTP_HOST: smtp.example.com
      SMTP_PORT: 587
      SMTP_USER: your-smtp-user
      SMTP_PASS: your-smtp-password
      SMTP_FROM: noreply@yourdomain.com
    depends_on:
      - db
      - clickhouse
      - mail

  db:
    image: postgres:16-alpine
    container_name: plausible_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: plausible
      POSTGRES_PASSWORD: postgres
    volumes:
      - db:/var/lib/postgresql/data

  clickhouse:
    image: clickhouse/clickhouse-server:23-alpine
    container_name: plausible_clickhouse
    restart: unless-stopped
    environment:
      CLICKHOUSE_DB: plausible
    volumes:
      - clickhouse:/var/lib/clickhouse
    ulimits:
      nofile:
        soft: 262144
        hard: 262144

  mail:
    image: bytemark/smtp:latest
    container_name: plausible_mail
    restart: unless-stopped

volumes:
  db:
  clickhouse:
```

### 3.2 启动服务

```bash
# 启动所有服务
docker compose up -d

# 查看日志
docker compose logs -f
```

### 3.3 访问 Plausible

启动后，访问 `http://your-server-ip:8000` 进入注册页面。

---

## 四、生产环境部署

### 4.1 配置环境变量

```bash
# 创建 .env 文件
cat > .env <<EOF
DATABASE_URL=postgres://postgres:your-password@db:5432/plausible
BASE_URL=https://analytics.yourdomain.com
SECRET_KEY_BASE=$(openssl rand64 | base64)
CLICKHOUSE_DATABASE_URL=http://clickhouse:8123/clicks
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-user
SMTP_PASS=your-password
SMTP_FROM=noreply@yourdomain.com
EOF
```

### 4.2 HTTPS 配置

使用 Nginx 反向代理：

```nginx
server {
    listen 443 ssl;
    server_name analytics.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ingest {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 五、注册与添加网站

### 5.1 创建管理员账户

1. 访问 `https://analytics.yourdomain.com`
2. 点击 **创建账户**
3. 填写邮箱和密码
4. 验证邮箱

### 5.2 添加网站

1. 登录后点击 **添加网站**
2. 填写网站信息：
   - 网站域名（如 `example.com`）
   - 网站名称
3. 点击创建

### 5.3 安装统计脚本

将提供的 JavaScript 脚本添加到网站：

```html
<script async defer src="https://analytics.yourdomain.com/js/script.js"></script>
```

或者使用自托管版本的无依赖脚本：

```html
<script>
  window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }
  plausible('pageview')
</script>
<script defer src="https://analytics.yourdomain.com/js/script.js"></script>
```

---

## 六、功能使用

### 6.1 查看统计数据

Plausible 提供以下统计报表：

| 报表 | 说明 |
| ---- | ---- |
| **仪表盘** | 核心指标概览 |
| **访客** | 访客来源、地理位置、设备信息 |
| **页面** | 热门页面、跳出率、停留时间 |
| **漏斗** | 转化漏斗分析 |
| **爬虫** | 爬虫和机器人流量 |
| **设置** | 网站和用户设置 |

### 6.2 自定义事件

```javascript
// 跟踪自定义事件
plausible('Sign Up', { props: { method: 'Google' } })

// 跟踪下载
plausible('Download', { props: { file: 'guide.pdf' } })

// 跟踪外链点击
plausible('Outbound Link', { props: { url: 'https://example.com' } })
```

### 6.3 漏斗分析

创建转化漏斗：

1. 进入 **漏斗** 页面
2. 点击 **创建漏斗**
3. 添加漏斗步骤：
   - 第1步：访问首页
   - 第2步：访问产品页
   - 第3步：注册
4. 查看转化率

### 6.4 目标追踪

```javascript
// 跟踪目标完成
plausible('Signup')
```

---

## 七、高级配置

### 7.1 反垃圾邮件配置

在环境变量中启用：

```bash
DISABLE_AUTH=false
ENABLE_EMAIL_VERIFICATION=true
```

### 7.2 多用户支持

Plausible 支持多用户和团队协作：

1. 进入 **设置 → 团队**
2. 邀请成员
3. 设置角色权限

### 7.3 邮件通知

配置每日/每周统计报告：

1. 进入 **网站设置 → 邮件报告**
2. 启用定期报告
3. 设置收件人

---

## 八、数据导出

### 8.1 导出 CSV

在统计页面，点击 **导出 → CSV** 下载数据。

### 8.2 API 导出

```bash
curl -H "Authorization: Bearer YOUR-API-KEY" \
  "https://analytics.yourdomain.com/api/v1/stats/aggregate" \
  "?site_id=your-site-id&period=6m&metrics=pageviews,visitors"
```

---

## 九、常见问题与解决方案

### 9.1 统计数据不准确

**解决方案**：
1. 确认脚本正确安装：`View Source` 检查
2. 禁用广告拦截器
3. 检查是否被 CDN 缓存

### 9.2 ClickHouse 连接失败

**解决方案**：
```bash
# 检查 ClickHouse 日志
docker compose logs clickhouse

# 手动初始化数据库
docker exec -it plausible_clickhouse clickhouse-client
CREATE DATABASE IF NOT EXISTS plausible;
```

### 9.3 邮件发送失败

**解决方案**：
1. 检查 SMTP 配置
2. 确认邮件服务商支持
3. 使用 SendGrid、Mailgun 等服务

### 9.4 性能问题

**解决方案**：
1. 增加 ClickHouse 内存
2. 配置适当的 `ulimits`
3. 使用独立的 ClickHouse 服务器

---

## 十、安全与隐私

### 10.1 GDPR 合规

Plausible 完全符合 GDPR 要求：

- 不收集个人数据
- 不使用 Cookie
- 不追踪跨网站用户
- 支持数据删除请求
- 提供数据处理协议（DPA）

### 10.2 安全建议

| 建议 | 说明 |
| ---- | ---- |
| **HTTPS** | 强制使用 HTTPS |
| **防火墙** | 限制访问端口 |
| **定期备份** | 备份数据库 |
| **更新版本** | 及时更新 |

---

## 十一、社区与生态

| 资源 | 地址 |
| ---- | ---- |
| **GitHub** | https://github.com/plausible/analytics |
| **官网** | https://plausible.io |
| **文档** | https://plausible.io/docs |
| **Demo** | https://plausible.io/plausible.io |
| **Discord** | 通过官网联系 |

---

## 总结

Plausible Analytics 是一款极具吸引力的网站分析替代方案，它以隐私为核心，提供了 Google Analytics 的核心功能，同时完全避免了 Cookie 和个人数据追踪的问题。对于注重隐私的网站所有者 GDPR 合规要求的机构，Plausible 是理想的选择。

它的核心优势在于：

- **隐私优先**：不使用 Cookie，不追踪个人，符合 GDPR
- **轻量快速**：仅 1KB 脚本，对网站性能无影响
- **简单易用**：仪表盘简洁明了，无需培训
- **开源透明**：代码完全开放，可自托管
- **成本可控**：相比 GA4 高级版，价格更加透明

> **立即体验**：访问 https://plausible.io 了解更多，或使用 Docker Compose 部署自托管版本。
