# changedetection.io开源项目详解：网站内容变更监控工具部署教程与自动化告警实战指南

## 一、项目概述

**changedetection.io** 是一款开源的网站内容变更监控工具，可以自动监测网页内容的变化并在发生变化时通过多种渠道发送告警通知。它支持 Discord、Email、Slack、Telegram、Webhook 等多种通知方式，适用于监控价格变化、内容编辑、库存状态、竞品动态等场景。

changedetection.io 的设计理念是"让网页监控变得简单"。它提供可视化的配置界面，无需编写代码即可监控任意网页，是追踪网站变化、实现自动化监控的利器。项目在 GitHub 上获得 24K+ Stars，被广泛应用于电商价格监控、新闻追踪、竞品分析等领域。

- **GitHub 地址**：https://github.com/dgtlmoon/changedetection.io
- **官方网站**：https://changedetection.io
- **开源协议**：AGPL-3.0
- **开发语言**：Python
- **核心定位**：网页内容变更监控与自动化告警平台

### 1.1 核心特性

| 特性 | 说明 |
| ---- | ---- |
| **无代码配置** | 可视化界面，无需编写代码 |
| **多种通知渠道** | Discord、Email、Slack、Telegram、Webhook 等 |
| **CSS 选择器** | 支持精确监控特定元素 |
| **JSON 监控** | 支持 API 响应监控 |
| **价格监控** | 专门的价格变化检测功能 |
| **AI 智能过滤** | 配合 LLM 过滤无关变化 |
| **调度控制** | 可配置检查间隔 |
| **历史记录** | 保存所有变更历史 |

### 1.2 与同类产品对比

| 特性 | changedetection.io | Distill.io | ChangeTower | 自建脚本 |
|------|---------------------|------------|-------------|-----------|
| **费用** | 开源免费 | 付费 | 付费 | 需要维护成本 |
| **部署方式** | 自托管 | 云服务 | 云服务 | 自建 |
| **通知渠道** | 丰富 | 一般 | 丰富 | 需要开发 |
| **使用难度** | 简单 | 简单 | 简单 | 复杂 |
| **可定制性** | 开源可改 | 受限 | 受限 | 完全可定制 |

---

## 二、系统要求

| 项目 | 最低要求 | 推荐配置 |
| ---- | -------- | -------- |
| CPU | 1 核 | 2 核+ |
| 内存 | 512 MB | 1 GB+ |
| 磁盘 | 5 GB | 20 GB+ |
| 系统 | Ubuntu 20.04+ | Ubuntu 22.04+ |
| Docker | 20.10+ | 最新版本 |

---

## 三、Docker 部署

### 3.1 一键启动

```bash
# 创建数据目录
mkdir -p changedetection-data

# 启动容器
docker run -d \
  --name changedetection \
  -p 5000:5000 \
  -v $(pwd)/changedetection-data:/datastore \
  --restart unless-stopped \
  dgtlmoon/changedetection:latest
```

### 3.2 Docker Compose 部署

```yaml
version: "3.8"

services:
  changedetection:
    image: dgtlmoon/changedetection:latest
    container_name: changedetection
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./data:/datastore
    environment:
      - PLAYWRIGHT_BROWSER=1
    depends_on:
      - playwright

  playwright:
    image: dgtlmoon/changedetection:playwright
    container_name: playwright
    restart: unless-stopped
    volumes:
      - ./playwright_cache:/root/.cache/ms-playwright

volumes:
  data:
  playwright_cache:
```

### 3.3 访问 changedetection

启动后，访问 `http://your-server-ip:5000` 进入管理界面。

---

## 四、基本配置

### 4.1 添加监控任务

1. 点击 **Add watch**
2. 填写 URL 和监控配置：
   - **URL**：要监控的网页地址
   - **名称**：给任务起个名字
   - **检查间隔**：多久检查一次

### 4.2 选择器配置

**方式一：使用 CSS 选择器**

在 `Element filter` 中输入 CSS 选择器，精确监控特定元素：

```css
.price
.product-title
#stock-status
```

**方式二：使用 JSONPath（针对 API）**

```json
$.data.price
$.products[0].name
```

### 4.3 触发器配置

在 `Triggers` 中设置触发条件：

```json
{
  "trigger_contains": "In Stock",
  "trigger_contains_not": "Out of Stock"
}
```

---

## 五、通知渠道配置

### 5.1 Discord Webhook

1. 在 Discord 服务器设置中创建 Webhook
2. 复制 Webhook URL
3. 在 changedetection 中配置：

```json
{
  "discord": {
    "webhook_url": "https://discord.com/api/webhooks/xxx/yyy"
  }
}
```

### 5.2 Email 通知

```json
{
  "email": {
    "to": "alert@example.com",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your-email@gmail.com",
    "smtp_password": "your-app-password"
  }
}
```

### 5.3 Slack

```json
{
  "slack": {
    "webhook_url": "https://hooks.slack.com/services/xxx/yyy/zzz"
  }
}
```

### 5.4 Telegram

```json
{
  "telegram": {
    "bot_token": "123456:ABC-DEF...",
    "chat_id": "123456789"
  }
}
```

### 5.5 Webhook

```json
{
  "webhook": {
    "url": "https://your-api.com/webhook",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer your-token"
    }
  }
}
```

---

## 六、AI 智能过滤

### 6.1 配置 OpenAI

```json
{
  "ai": {
    "provider": "openai",
    "api_key": "sk-xxxxx",
    "model": "gpt-4"
  }
}
```

### 6.2 智能规则示例

**价格监控**：

```json
{
  "prompt": "Only notify me when the price drops below $50. Ignore all other changes."
}
```

**库存监控**：

```json
{
  "prompt": "Alert me when the item comes back in stock. Ignore price changes and other content updates."
}
```

**内容变更**：

```json
{
  "prompt": "Ignore navigation and footer changes. Only notify me about main content changes."
}
```

### 6.3 Ollama 本地 AI

```json
{
  "ai": {
    "provider": "ollama",
    "base_url": "http://localhost:11434",
    "model": "llama3.2"
  }
}
```

---

## 七、高级功能

### 7.1 密码保护页面

对于需要登录的页面：

1. 选择 **Method: Advanced**
2. 设置 `Request headers`：

```json
{
  "Cookie": "session=your-session-cookie"
}
```

或使用 Basic Auth：

```json
{
  "Authorization": "Basic base64(username:password)"
}
```

### 7.2 POST 请求

```json
{
  "request_method": "POST",
  "request_body": "username=admin&password=secret"
}
```

### 7.3 代理配置

```json
{
  "proxy": "http://proxy.example.com:8080"
}
```

### 7.4 提取器

使用 XPath 或 Regex 提取特定内容：

```json
{
  "json_extract": "$.data.items[*].price",
  "xpath_extract": "//span[@class='price']/text()",
  "regex_extract": "Price: \\$([0-9.]+)"
}
```

---

## 八、常见问题与解决方案

### 8.1 页面无法抓取

**解决方案**：
1. 启用 Playwright 模式（支持 JavaScript 渲染）
2. 增加等待时间
3. 检查是否有反爬机制

### 8.2 误报频繁

**解决方案**：
1. 使用 CSS 选择器精确锁定元素
2. 配置触发器条件
3. 启用 AI 过滤
4. 增加检查间隔

### 8.3 通知发送失败

**解决方案**：
1. 检查 Webhook URL 是否正确
2. 确认通知渠道的 API 限制
3. 查看 changedetection 日志

### 8.4 性能问题

**解决方案**：
1. 减少监控任务数量
2. 增加检查间隔
3. 使用 SQLite 以外的数据库

---

## 九、API 接口

### 9.1 添加监控任务

```bash
curl -X POST http://localhost:5000/api/watch \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/product",
    "tag": ["product", "monitor"],
    "interval": 3600
  }'
```

### 9.2 获取监控状态

```bash
curl http://localhost:5000/api/watch
```

### 9.3 触发检查

```bash
curl -X POST http://localhost:5000/api/watch/1/check
```

---

## 十、安全建议

| 建议 | 说明 |
| ---- | ---- |
| **网络隔离** | 避免监控内网敏感页面 |
| **访问控制** | 配置反向代理认证 |
| **数据备份** | 定期备份数据目录 |
| **更新版本** | 及时更新最新版本 |

---

## 十一、使用场景

### 11.1 电商价格监控

```json
{
  "url": "https://amazon.com/dp/B09V3KXJPB",
  "css_selector": ".a-price-whole",
  "trigger_contains": "29"
}
```

### 11.2 库存监控

```json
{
  "url": "https://store.nvidia.com/product/gpu",
  "css_selector": "#add-to-cart-button",
  "trigger_not_contains": "Out of Stock"
}
```

### 11.3 新闻追踪

```json
{
  "url": "https://news.example.com/tech",
  "css_selector": "article h2",
  "trigger_contains": "AI"
}
```

---

## 十二、社区与生态

| 资源 | 地址 |
| ---- | ---- |
| **GitHub** | https://github.com/dgtlmoon/changedetection.io |
| **官网** | https://changedetection.io |
| **文档** | https://changedetection.io/docs |
| **Docker Hub** | https://hub.docker.com/r/dgtlmoon/changedetection |

---

## 总结

changedetection.io 是一款非常实用的开源监控工具，它让网页内容监控变得前所未有的简单。无论是监控电商价格、追踪竞品动态、关注新闻更新，还是实现各种自动化监控场景，changedetection.io 都能提供出色的解决方案。

它的核心优势在于：

- **开源免费**：无需付费即可使用全部功能
- **简单易用**：可视化配置，无需编写代码
- **通知丰富**：支持多种主流通知渠道
- **AI 智能**：配合 LLM 过滤无关变化，减少误报
- **灵活定制**：支持 CSS 选择器、XPath、JSONPath 等精确提取

对于需要监控网站变化、实现自动化告警的用户来说，changedetection.io 是一个极具价值的选择。

> **立即体验**：执行 `docker run -d -p 5000:5000 -v $(pwd)/data:/datastore dgtlmoon/changedetection:latest` 一键部署，然后访问 `http://localhost:5000` 开始使用。
