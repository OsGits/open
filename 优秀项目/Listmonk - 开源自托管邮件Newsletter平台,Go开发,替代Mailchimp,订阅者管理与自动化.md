# Listmonk开源项目详解：自托管邮件Newsletter平台部署教程

## 一、项目概述

**Listmonk** 是一款开源的自托管邮件 Newsletter 和营销自动化平台。它集成了订阅者管理、邮件发送、自动化工作流、分析统计等功能，可以替代 Mailchimp、Substack 等商业服务，让你完全掌控自己的邮件列表和发送策略。

Listmonk 的设计理念是"简单、强大、独立"。它采用 Go 语言开发，单二进制文件即可运行，安装配置极其简单，同时提供专业级的邮件营销功能。项目在 GitHub 上获得 16K+ Stars，被众多博主、开发者和小型企业用于管理 Newsletter 和客户沟通。

- **GitHub 地址**：https://github.com/knadh/listmonk
- **官方网站**：https://listmonk.app
- **开源协议**：AGPL-3.0
- **开发语言**：Go + Vue.js
- **核心定位**：自托管邮件 Newsletter 和营销自动化平台

### 1.1 核心特性

| 特性 | 说明 |
| ---- | ---- |
| **订阅者管理** | 导入导出、标签分组、黑名单 |
| **邮件编辑** | 可视化编辑器，支持 Markdown |
| **模板系统** | 预设模板，自定义模板 |
| **自动化** | 欢迎邮件、自动化序列 |
| **A/B 测试** | 主题和内容的对比测试 |
| **统计分析** | 打开率、点击率、退订率 |
| **SMTP 支持** | 连接任意 SMTP 服务商 |
| **API 接口** | REST API，Webhook |
| **双因素认证** | 支持 2FA 安全登录 |

### 1.2 与同类产品对比

| 特性 | Listmonk | Mailchimp | Substack | SendGrid |
|------|----------|-----------|----------|----------|
| **费用** | 完全免费 | 按订阅者计费 | 按订阅者计费 | 按发送量计费 |
| **数据控制** | 完全私有 | 云服务 | 云服务 | 云服务 |
| **安装** | 简单 | 不需要 | 不需要 | 不需要 |
| **邮件编辑** | 可视化+Markdown | 可视化 | 简单编辑器 | API |
| **自动化** | 支持 | 支持 | 有限 | 支持 |
| **发送限制** | 无（取决于 SMTP） | 按套餐 | 无限制 | 按套餐 |

---

## 二、系统要求

| 项目 | 最低要求 | 推荐配置 |
| ---- | -------- | -------- |
| CPU | 1 核 | 2 核+ |
| 内存 | 512 MB | 1 GB+ |
| 磁盘 | 5 GB | 20 GB+ |
| 系统 | 跨平台 | Linux |
| 数据库 | PostgreSQL 10+ | PostgreSQL 14+ |
| SMTP | 任意 SMTP 服务商 | 专业 SMTP |

---

## 三、安装 Listmonk

### 3.1 二进制安装（推荐）

```bash
# 下载最新版本
wget https://github.com/knadh/listmonk/releases/download/v3.0.0/listmonk_linux_amd64.tar.gz
tar -xzf listmonk_linux_amd64.tar.gz

# 安装
sudo mv listmonk /usr/local/bin/
sudo chmod +x /usr/local/bin/listmonk

# 验证安装
listmonk --version
```

### 3.2 Docker 安装

```bash
# 创建数据目录
mkdir -p listmonk-data

# 启动容器
docker run -d \
  --name listmonk \
  -p 9000:9000 \
  -v $(pwd)/listmonk-data:/listmonk \
  knadh/listmonk:latest
```

### 3.3 Docker Compose 安装

```yaml
version: "3.8"

services:
  listmonk:
    image: knadh/listmonk:latest
    container_name: listmonk
    restart: unless-stopped
    ports:
      - "9000:9000"
    volumes:
      - ./data:/listmonk
    environment:
      - LISTMONK_database__host=db
      - LISTMONK_database__port=5432
      - LISTMONK_database__user=listmonk
      - LISTMONK_database__password=listmonk
      - LISTMONK_database__name=listmonk
      - LISTMONK_app__address=0.0.0.0:9000
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    container_name: listmonk_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: listmonk
      POSTGRES_USER: listmonk
      POSTGRES_PASSWORD: listmonk
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

## 四、配置 Listmonk

### 4.1 初始化配置

```bash
# 初始化数据库和配置
listmonk init

# 编辑配置文件
nano listmonk.toml
```

### 4.2 配置文件示例

```toml
[app]
# 应用地址
address = "0.0.0.0:9000"
# 上传目录
upload_dir = "/var/lib/listmonk/uploads"

[db]
host = "localhost"
port = 5432
user = "listmonk"
password = "your-password"
name = "listmonk"
ssl_mode = "disable"

[smtp]
# SMTP 配置
host = "smtp.example.com"
port = 587
username = "your-smtp-username"
password = "your-smtp-password"
from_email = "newsletter@example.com"
from_name = "My Newsletter"

[mailer]
# 并发发送数
max_connections = 10
# 重试次数
max_msg_retries = 3
# 发送间隔（毫秒）
message_rate_limit = 100
```

### 4.3 启动服务

```bash
# 前台运行
listmonk server

# 或后台运行
nohup listmonk server > listmonk.log 2>&1 &
```

---

## 五、Nginx 反向代理

### 5.1 HTTPS 配置

```nginx
server {
    listen 443 ssl;
    server_name newsletter.example.com;

    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;

    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 六、基本使用

### 6.1 访问管理后台

访问 `http://your-server-ip:9000`，首次登录会要求创建管理员账户。

### 6.2 创建订阅表单

1. 进入 **Lists → Forms**
2. 点击 **Create Form**
3. 自定义表单字段
4. 获取嵌入代码

```html
<!-- 复制此代码到你的网站 -->
<form action="https://your-listmonk.com/subscribe" method="POST">
  <input type="email" name="email" placeholder="Your email" required>
  <button type="submit">Subscribe</button>
</form>
```

### 6.3 导入订阅者

1. 进入 **Subscribers**
2. 点击 **Import**
3. 上传 CSV 或 JSON 文件

**CSV 格式示例**：

```csv
email,name,tags
user1@example.com,John Doe,premium
user2@example.com,Jane Smith,free
```

---

## 七、发送邮件

### 7.1 创建邮件模板

1. 进入 **Templates**
2. 点击 **New Template**
3. 使用可视化编辑器或 Markdown 编写

**模板变量**：

```markdown
Subject: Welcome to {{ .ListName }}!

Hi {{ .Subscriber.FirstName }},

Thank you for subscribing to our newsletter.

Best regards,
The {{ .ListName }} Team

Unsubscribe: {{ .Subscriber.URL }}
```

### 7.2 创建邮件活动

1. 进入 **Campaigns**
2. 点击 **New Campaign**
3. 填写邮件信息：
   - 收件人列表
   - 邮件主题
   - 邮件内容
4. 预览并发送

### 7.3 定时发送

```yaml
# 配置定时发送
send_at: "2024-12-25T09:00:00Z"
```

---

## 八、自动化

### 8.1 创建自动化序列

1. 进入 **Campaigns → Automations**
2. 点击 **New Automation**
3. 配置触发条件

### 8.2 欢迎邮件序列

```yaml
# 触发：订阅者加入列表
trigger:
  type: "subscription"
  list_ids: [1]

# 步骤
steps:
  - delay: 0
    action: send_campaign
    campaign_id: welcome_email

  - delay: 86400  # 1天后
    action: send_campaign
    campaign_id: getting_started

  - delay: 604800  # 7天后
    action: send_campaign
    campaign_id: best_practices
```

### 8.3 行为触发

| 触发类型 | 说明 |
| ---- | ---- |
| 订阅 | 新订阅者加入 |
| 打开邮件 | 订阅者打开某封邮件 |
| 点击链接 | 订阅者点击邮件中的链接 |
| 日期 | 特定日期（如生日） |

---

## 九、统计分析

### 9.1 查看统计数据

| 指标 | 说明 |
| ---- | ---- |
| 发送数 | 已发送的邮件总数 |
| 打开数 | 邮件被打开的次数 |
| 点击数 | 链接被点击的次数 |
| 退订数 | 退订的订阅者数 |
| 反弹数 | 发送失败的邮件数 |

### 9.2 A/B 测试

1. 创建 A/B 测试活动
2. 配置多个版本（主题或内容不同）
3. 设置分流比例
4. 系统自动选择表现更好的版本

---

## 十、API 使用

### 10.1 获取 API Key

1. 进入 **Settings → API Keys**
2. 创建新的 API Key

### 10.2 订阅者 API

```bash
# 获取订阅者列表
curl -H "Authorization: Token YOUR-API-KEY" \
  https://your-listmonk.com/api/subscribers

# 添加订阅者
curl -X POST -H "Authorization: Token YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"John Doe"}' \
  https://your-listmonk.com/api/subscribers

# 批量导入
curl -X POST -H "Authorization: Token YOUR-API-KEY" \
  -d '{"subscribers":[{"email":"a@a.com"},{"email":"b@b.com"}]}' \
  https://your-listmonk.com/api/subscribers/import
```

### 10.3 发送邮件 API

```bash
curl -X POST -H "Authorization: Token YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "list_ids": [1],
    "subject": "Test Email",
    "body": "<p>This is a test email</p>",
    "send": true
  }' \
  https://your-listmonk.com/api/campaigns
```

---

## 十一、SMTP 配置

### 11.1 使用 SendGrid

```toml
[smtp]
host = "smtp.sendgrid.net"
port = 587
username = "apikey"
password = "SG.xxxxxx"
```

### 11.2 使用 Mailgun

```toml
[smtp]
host = "smtp.mailgun.org"
port = 587
username = "postmaster@yourdomain.com"
password = "your-mailgun-password"
```

### 11.3 使用 Amazon SES

```toml
[smtp]
host = "email-smtp.us-east-1.amazonaws.com"
port = 587
username = "AKIAxxxxx"
password = "xxxxx"
```

---

## 十二、常见问题与解决方案

### 12.1 邮件发送失败

**解决方案**：
1. 检查 SMTP 配置是否正确
2. 确认 SMTP 账户有发送权限
3. 检查防火墙是否开放 SMTP 端口
4. 查看发送日志

### 12.2 邮件进入垃圾箱

**解决方案**：
1. 配置 SPF、DKIM、DMARC 记录
2. 避免垃圾邮件关键词
3. 保持良好的发送频率
4. 使用专业 SMTP 服务

### 12.3 订阅者导入失败

**解决方案**：
1. 检查 CSV 格式是否正确
2. 确认邮箱格式有效
3. 检查是否超过发送限制

### 12.4 性能问题

**解决方案**：
1. 增加并发连接数
2. 使用性能更好的数据库
3. 配置 Redis 缓存

---

## 十三、安全建议

| 建议 | 说明 |
| ---- | ---- |
| **HTTPS** | 强制使用 HTTPS |
| **强密码** | 使用强管理员密码 |
| **双因素认证** | 启用 2FA |
| **定期更新** | 及时更新 Listmonk 版本 |
| **备份** | 定期备份数据库 |
| **发送限制** | 配置合理的发送限制 |

---

## 十四、社区与生态

| 资源 | 地址 |
| ---- | ---- |
| **GitHub** | https://github.com/knadh/listmonk |
| **官网** | https://listmonk.app |
| **文档** | https://listmonk.app/docs |
| **Demo** | https://demo.listmonk.app |

---

## 总结

Listmonk 是一款功能强大且易于使用的开源邮件 Newsletter 平台。它提供了商业邮件服务（如 Mailchimp）的核心功能，同时保持了数据的完全私有和使用的零成本。对于需要管理邮件订阅、发送 Newsletter、实现自动化营销的个人博主和小型企业来说，Listmonk 是一个极佳的选择。

它的核心优势在于：

- **完全免费**：无订阅者数量限制，无发送量限制
- **开源透明**：代码完全开放，数据完全私有
- **安装简单**：单二进制文件，无需复杂配置
- **功能完整**：订阅管理、邮件编辑、自动化、分析统计
- **API 完善**：方便与现有系统集成

对于希望摆脱商业邮件服务依赖、掌控自己邮件列表和发送策略的用户来说，Listmonk 是一个非常值得推荐的选择。

> **立即体验**：访问 https://listmonk.app 了解更多，或下载安装包体验。
