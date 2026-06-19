# Uptime Kuma开源项目详解：自托管服务监控工具部署教程与多渠道告警通知实战指南

## 一、项目概述

**Uptime Kuma** 是一款功能强大、界面精美的自托管服务监控工具，被誉为"免费版的 Uptime Robot"。它能够监控 HTTP(s)、TCP、DNS、Ping、WebSocket、Docker 容器、Steam 游戏服务器等多种服务类型，支持 90 多种通知渠道，并提供美观的可公开分享的状态页面。项目由 Louis Lam 开发，采用 JavaScript + Vue 3 技术栈构建，基于 WebSocket 实现实时数据推送，无需轮询即可获得即时状态更新。

- **GitHub 地址**：https://github.com/louislam/uptime-kuma
- **在线演示**：https://demo.kuma.pet/start-demo
- **开源协议**：MIT License
- **Star 数量**：84.5K+
- **技术栈**：JavaScript 56%、Vue 42.1%、TypeScript 1%
- **最新版本**：v2.3.2（2026年5月3日发布）
- **总发布版本数**：129 个

---

## 二、核心特性解读

### 1. 多协议监控支持

Uptime Kuma 支持监控多种服务类型，覆盖从 Web 应用到基础设施的全方位监控需求：

| 监控类型 | 说明 |
|----------|------|
| HTTP(s) | 网站、API 接口可用性监控 |
| TCP | 端口连通性检测 |
| HTTP(s) Keyword | 页面关键词匹配（检测页面是否包含特定内容） |
| HTTP(s) Json Query | JSON 响应字段值验证 |
| DNS Record | DNS 解析记录监控 |
| Ping (ICMP) | 服务器在线状态检测 |
| WebSocket | WebSocket 连接状态监控 |
| Push | 被动监控（由被监控端主动推送心跳） |
| Steam Game Server | 游戏服务器在线监控 |
| Docker Containers | Docker 容器运行状态监控 |

### 2. 90+ 通知渠道

当服务出现异常时，Uptime Kuma 可通过以下渠道发送告警通知：

- **即时通讯**：Telegram、Discord、Slack、Gotify、Matrix、WeCom（企业微信）、DingTalk（钉钉）、飞书
- **邮件**：SMTP 邮件通知
- **推送服务**：Pushover、Pushbullet、Bark、ntfy
- **Webhook**：自定义 Webhook（可对接任意系统）
- **其他**：PagerDuty、Opsgenie、Prometheus Alertmanager、SMS 等

### 3. 精美状态页面

- 支持创建多个独立状态页面
- 每个状态页面可绑定独立域名
- 公开分享，无需登录即可查看
- 自动展示服务可用率、历史故障记录
- 支持自定义 Logo 和品牌样式

### 4. 高性能实时 UI

- 基于 Vue 3 + WebSocket 构建的响应式界面
- 实时数据推送，无需手动刷新
- 优雅的 Ping 延迟图表
- 证书到期信息展示
- 多语言支持（含中文）

### 5. 安全与权限

- 2FA 双因素认证
- 代理支持（HTTP/SOCKS5）
- 多用户权限管理
- API 密钥管理

---

## 三、适用场景

| 场景 | 说明 |
|------|------|
| 个人项目监控 | 监控个人博客、Side Project 的在线状态 |
| 团队运维 | 统一监控团队所有服务的可用性 |
| SaaS 可用性展示 | 为客户提供公开的服务状态页面 |
| 服务器巡检 | 自动检测服务器端口、Ping 连通性 |
| Docker 编排监控 | 实时监控 Docker 容器运行状态 |
| 游戏服务器 | 监控游戏服务器在线状态和玩家数量 |

---

## 四、部署方法详解

### 方法一：Docker Compose 部署（推荐）

```bash
mkdir uptime-kuma
cd uptime-kuma
curl -o compose.yaml https://raw.githubusercontent.com/louislam/uptime-kuma/master/compose.yaml
docker compose up -d
```

部署完成后，访问 `http://localhost:3001` 即可打开管理界面。

### 方法二：Docker 命令部署

```bash
docker run -d \
  --restart=always \
  -p 3001:3001 \
  -v uptime-kuma:/app/data \
  --name uptime-kuma \
  louislam/uptime-kuma:2
```

如需限制仅本地访问：

```bash
docker run -d \
  --restart=always \
  -p 127.0.0.1:3001:3001 \
  -v uptime-kuma:/app/data \
  --name uptime-kuma \
  louislam/uptime-kuma:2
```

### 方法三：非 Docker 部署（Node.js）

**环境要求**：
- Node.js >= 20.4
- Git
- PM2（后台进程管理）

```bash
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma
npm run setup

# 方式一：直接运行
node server/server.js

# 方式二（推荐）：使用 PM2 后台运行
npm install pm2 -g && pm2 install pm2-logrotate
pm2 start server/server.js --name uptime-kuma

# 设置开机自启
pm2 startup && pm2 save
```

---

## 五、进阶配置

### 反向代理配置（Nginx）

```nginx
server {
    listen 80;
    server_name status.yourdomain.com;

    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 配置 Telegram 通知

1. 在 Telegram 中搜索 `@BotFather`，创建一个 Bot 并获取 Token
2. 在 Uptime Kuma 管理界面中进入 `设置` → `通知` → `添加通知`
3. 选择 `Telegram`，填入 Bot Token 和 Chat ID
4. 保存后，在监控项中关联该通知渠道

### 配置企业微信（WeCom）通知

1. 在企业微信管理后台创建应用，获取 Corp ID、Agent ID 和 Secret
2. 在 Uptime Kuma 中添加 `WeCom` 通知类型
3. 填入对应参数并测试连接

### 状态页面自定义

1. 进入 `状态页面` → `添加新的状态页面`
2. 设置页面标题、描述、域名
3. 选择要展示的监控分组
4. 上传自定义 Logo
5. 发布状态页面，将域名指向 Uptime Kuma 服务器

---

## 六、与其他监控工具对比

| 特性 | Uptime Kuma | Uptime Robot | Pingdom | Zabbix |
|------|-------------|--------------|---------|--------|
| 自托管 | ✅ | ❌ | ❌ | ✅ |
| 免费使用 | ✅ 完全免费 | 50 个监控点免费 | 付费 | ✅ |
| 状态页面 | ✅ 多页面 | ✅ 单页面 | ✅ | 需插件 |
| 通知渠道 | 90+ | 20+ | 10+ | 20+ |
| 监控间隔 | 20 秒 | 1 分钟（免费） | 1 分钟 | 自定义 |
| UI 美观度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 部署难度 | 极简 | 无需部署 | 无需部署 | 复杂 |
| Docker 监控 | ✅ | ❌ | ❌ | ✅ |

---

## 七、实用技巧

### 监控间隔设置

- **关键业务服务**：建议 20 秒（最低支持）
- **一般网站/API**：建议 60 秒
- **非关键服务**：建议 5 分钟（减少资源消耗）

### 关键词监控实战

监控 API 接口时，可使用 HTTP(s) Keyword 类型检测返回内容是否包含 `"status":"ok"` 等关键词，避免仅检测 HTTP 状态码而忽略业务逻辑错误。

### Push 被动监控

对于内网服务或无法从外部访问的服务，可使用 Push 类型监控。在被监控端配置定时任务，定期向 Uptime Kuma 推送心跳信号：

```bash
# cron 定时推送心跳（每 60 秒）
* * * * * curl -s "https://your-uptime-kuma/api/push/your-push-token?status=up&msg=OK&ping=100ms"
```

---

## 八、总结

Uptime Kuma 是一款将"免费、自托管、高颜值"三者完美结合的服务监控工具。它以极低的部署成本（一条 Docker 命令）提供了媲美商业产品的监控能力，90+ 通知渠道确保告警不遗漏，精美的状态页面可直接面向客户展示服务可用性。对于个人开发者、中小团队以及注重数据主权的企业而言，Uptime Kuma 是替代 Uptime Robot 和 Pingdom 的最佳开源方案。

---

**相关资源**

- GitHub 仓库：https://github.com/louislam/uptime-kuma
- 在线演示：https://demo.kuma.pet/start-demo
- 安装文档：https://github.com/louislam/uptime-kuma/wiki
- 更新指南：https://github.com/louislam/uptime-kuma/wiki/How-to-Update
- 社区讨论：https://www.reddit.com/r/UptimeKuma/
