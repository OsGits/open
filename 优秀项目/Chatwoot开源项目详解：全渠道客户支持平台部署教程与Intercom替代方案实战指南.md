---
title: Chatwoot开源项目详解：全渠道客户支持平台部署教程与Intercom替代方案实战指南
id: 019edae5-1f55-75d8-9103-1899a39f26aa
date: 2026-06-18 21:21:18
auther: loveos
cover: /upload/1-WDqA.png
excerpt: Chatwoot 是一款现代化的开源客户支持平台，专为帮助企业提供卓越的客户服务体验而设计。它基于 Ruby on Rails 构建，支持全渠道消息整合，将网站在线聊天、邮件、社交媒体等所有客户对话统一到一个强大的收件箱中管理。
permalink: /2026/chatwoot%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE%E8%AF%A6%E8%A7%A3%EF%BC%9A%E5%85%A8%E6%B8%A0%E9%81%93%E5%AE%A2%E6%88%B7%E6%94%AF%E6%8C%81%E5%B9%B3%E5%8F%B0%E9%83%A8%E7%BD%B2%E6%95%99%E7%A8%8B%E4%B8%8Eintercom%E6%9B%BF%E4%BB%A3%E6%96%B9%E6%A1%88%E5%AE%9E%E6%88%98%E6%8C%87%E5%8D%97
categories:
 - Github
tags: 
 - chatwootkai-yuan-ke-fu-xi-tong
 - quan-qu-dao-ke-hu-zhi-chi-ping-tai-da-jian
 - intercomti-dai-fang-an-tui-jian
 - zi-tuo-guan-ke-fu-xi-tong-bu-shu-jiao-cheng
 - kai-yuan-gong-dan-guan-li-xi-tong
 - whatsappke-fu-ji-cheng-fang-an
 - docker
 - github
---

> **开源协议**：MIT
> **GitHub Stars**：31K+
> **核心定位**：开源全渠道客户支持平台，Intercom/Zendesk/Salesforce Service Cloud的自托管替代方案

---

<hyperlink-card href="https://github.com/chatwoot/chatwoot" target="_blank" theme="regular"></hyperlink-card>


## 一、项目概述

**Chatwoot** 是一款现代化的开源客户支持平台，专为帮助企业提供卓越的客户服务体验而设计。它基于 Ruby on Rails 构建，支持全渠道消息整合，将网站在线聊天、邮件、社交媒体等所有客户对话统一到一个强大的收件箱中管理。

Chatwoot的核心理念是**"数据主权+成本可控"**——与SaaS客服工具不同，Chatwoot可以完全自托管，企业对客户数据拥有完全控制权，同时避免了按坐席付费的高昂成本。项目支持多语言，社区活跃，文档完善，已被全球数千家企业采用。

---

## 二、核心特性解读

### 2.1 全渠道统一收件箱

Chatwoot将来自不同渠道的客户对话集中到一个统一的界面中管理：


| 渠道类型 | 支持平台                 | 接入方式   |
| -------- | ------------------------ | ---------- |
| 网站聊天 | Live Chat Widget         | 嵌入JS代码 |
| 电子邮件 | Gmail/Outlook/自定义SMTP | IMAP/SMTP  |
| 即时通讯 | WhatsApp Business API    | 官方API    |
| 即时通讯 | Telegram Bot             | Bot Token  |
| 即时通讯 | Line                     | 官方API    |
| 社交媒体 | Facebook Messenger       | 页面集成   |
| 社交媒体 | Instagram DM             | 商业账户   |
| 社交媒体 | Twitter/X DM             | 开发者API  |
| 短信     | Twilio/SMS               | 短信网关   |

**核心价值**：客服人员无需切换多个平台，在一个界面中处理所有客户咨询。

### 2.2 Captain AI智能客服

Chatwoot内置 **Captain** AI智能客服代理：

- **自动回复**：处理常见问题，减少人工客服工作量
- **智能路由**：根据问题类型自动分配给合适的客服
- **上下文理解**：基于对话历史提供精准回答
- **人工接管**：复杂问题无缝转接人工客服

### 2.3 帮助中心门户

- 内置知识库系统，支持发布帮助文章和FAQ
- 客户自助查找答案，减少重复咨询
- SEO友好的公开帮助页面
- 多语言文章支持

### 2.4 团队协作与效率工具


| 功能            | 说明                     |
| --------------- | ------------------------ |
| 私人笔记与@提及 | 团队内部讨论，客户不可见 |
| 标签分类        | 按主题/优先级组织对话    |
| 快捷回复        | 预设常用回复模板         |
| 自动分配        | 基于客服可用性智能路由   |
| 键盘快捷键      | 快速导航与操作           |
| 命令栏          | 快捷执行常用操作         |
| 营业时间设置    | 管理客户期望响应时间     |
| 客服容量管理    | 平衡团队工作负载         |

### 2.5 客户数据管理

- **联系人管理**：客户档案与交互历史
- **客户分群**：基于属性进行目标沟通
- **主动营销**：Campaign功能主动触达客户
- **自定义属性**：存储额外客户数据
- **聊天前表单**：对话开始前收集用户信息

### 2.6 丰富的第三方集成


| 集成类型   | 支持平台                     |
| ---------- | ---------------------------- |
| 团队协作   | Slack                        |
| 聊天机器人 | Dialogflow                   |
| 电商       | Shopify（查看订单）          |
| 项目管理   | Linear                       |
| 翻译       | Google Translate（实时翻译） |
| 内部工具   | Dashboard Apps嵌入           |

### 2.7 数据分析与报告

- 实时对话监控（Live View）
- 对话/客服/收件箱/标签/团队报告
- CSAT客户满意度评分
- 可下载的离线报告
- 运营数据可视化

---

## 三、系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      前端界面层                              │
│         (Vue.js SPA / 客服工作台 / 管理后台)                 │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Ruby on Rails API                       │
│     (RESTful API / WebSocket实时通信 / 后台任务)             │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐    ┌────────▼────────┐   ┌───────▼──────┐
│  PostgreSQL  │    │     Redis       │   │  Sidekiq     │
│  (主数据库)   │    │  (缓存/会话)     │   │ (后台队列)   │
└──────────────┘    └─────────────────┘   └──────────────┘
```

---

## 四、部署指南

### 4.1 环境要求


| 资源类型   | 最低配置 | 推荐配置  |
| ---------- | -------- | --------- |
| CPU        | 2核      | 4核+      |
| 内存       | 4GB      | 8GB+      |
| 磁盘       | 20GB     | 50GB+ SSD |
| PostgreSQL | >= 12    | 最新版    |
| Redis      | >= 5.0   | 最新版    |
| Node.js    | >= 18    | 最新LTS   |
| Ruby       | >= 3.1   | 最新版    |

### 4.2 Docker Compose一键部署（推荐）

**步骤1：克隆仓库**

```bash
git clone https://github.com/chatwoot/chatwoot.git
cd chatwoot
```

**步骤2：配置环境变量**

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置关键配置：

```bash
# 数据库配置
POSTGRES_HOST=postgres
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DATABASE=chatwoot_production

# Redis配置
REDIS_URL=redis://redis:6379

# 应用密钥（生成随机字符串）
SECRET_KEY_BASE=your_random_secret_key

# 域名配置
FRONTEND_URL=https://chat.yourdomain.com

# SMTP邮件配置（用于发送通知）
SMTP_ADDRESS=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# 可选：RAILS_ENV=production
```

**步骤3：启动服务**

```bash
docker compose -f docker-compose.production.yaml up -d
```

**步骤4：初始化数据库**

```bash
docker compose -f docker-compose.production.yaml exec rails bundle exec rails db:chatwoot_prepare
```

**步骤5：创建管理员账户**

```bash
docker compose -f docker-compose.production.yaml exec rails bundle exec rails c

# 在Rails控制台中执行
Account.create!(name: "Your Company", domain: "yourdomain")
User.create!(email: "admin@yourdomain.com", password: "secure_password", name: "Admin")
```

**步骤6：访问系统**

打开浏览器访问 `http://localhost:3000` 或配置的域名。

### 4.3 Heroku一键部署

Chatwoot官方提供Heroku一键部署按钮：

1. 访问 [Chatwoot Heroku部署页面](https://www.chatwoot.com/docs/self-hosted/deployment/heroku)
2. 点击部署按钮
3. 配置环境变量
4. 完成部署

### 4.4 DigitalOcean 1-Click K8s部署

```bash
# 在DigitalOcean控制台中选择Chatwoot 1-Click App
# 或使用doctl命令行工具
doctl kubernetes 1-click install chatwoot
```

### 4.5 其他部署方式

- **AWS EC2**：使用官方AMI镜像
- **Google Cloud Platform**：使用Cloud Run或GKE
- **Azure**：使用容器实例或AKS
- **独立服务器**：手动安装Ruby/Node/PostgreSQL/Redis

详细部署文档：[https://chatwoot.com/deploy](https://chatwoot.com/deploy)

---

## 五、快速上手实战

### 5.1 配置网站Live Chat

1. 登录Chatwoot管理后台
2. 进入 **Settings > Inboxes > Add Inbox**
3. 选择 **Website** 渠道
4. 填写网站名称和域名
5. 复制生成的JavaScript代码
6. 将代码粘贴到网站 `<head>` 标签中

```html
<script>
  (function(d,t) {
    var BASE_URL="https://your-chatwoot-domain.com";
    var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
    g.src=BASE_URL+"/packs/js/sdk.js";
    g.defer = true;
    g.async = true;
    s.parentNode.insertBefore(g,s);
    g.onload=function(){
      window.chatwootSDK.run({
        websiteToken: 'YOUR_WEBSITE_TOKEN',
        baseUrl: BASE_URL
      })
    }
  })(document,"script");
</script>
```

### 5.2 连接WhatsApp Business

1. 进入 **Settings > Inboxes > Add Inbox**
2. 选择 **WhatsApp** 渠道
3. 填写WhatsApp Business API凭证：
   - Phone Number ID
   - Business Account ID
   - Access Token
4. 完成验证并启用

### 5.3 配置邮件渠道

1. 进入 **Settings > Inboxes > Add Inbox**
2. 选择 **Email** 渠道
3. 填写IMAP/SMTP服务器信息
4. 设置转发邮箱地址
5. 测试连接并保存

### 5.4 设置快捷回复（Canned Responses）

1. 进入 **Settings > Canned Responses**
2. 点击 **Add Canned Response**
3. 填写快捷代码和内容：


| 快捷代码   | 内容                                                 |
| ---------- | ---------------------------------------------------- |
| `greeting` | 您好！感谢您联系我们，请问有什么可以帮助您的？       |
| `closing`  | 如果还有其他问题，请随时联系我们。祝您有愉快的一天！ |
| `escalate` | 这个问题需要更专业的支持，我将为您转接高级客服。     |

4. 在对话中输入 `/greeting` 即可快速插入

### 5.5 配置自动化规则

1. 进入 **Settings > Automation**
2. 创建新规则：

```
规则名称：新对话自动分配
触发条件：对话创建
条件：渠道 = Website
动作：分配给客服组 "在线客服"
        添加标签 "网站咨询"
        发送自动回复 "您好，已收到您的消息，客服将尽快回复。"
```

### 5.6 集成Slack

1. 进入 **Settings > Integrations > Slack**
2. 点击 **Connect Slack**
3. 授权Chatwoot访问你的Slack工作区
4. 选择要接收通知的频道
5. 配置完成后，所有新对话将自动推送到Slack

### 5.7 API集成示例

Chatwoot提供完整的REST API：

```bash
# 获取对话列表
curl -X GET "https://your-chatwoot-domain.com/api/v1/accounts/1/conversations" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json"

# 发送消息
curl -X POST "https://your-chatwoot-domain.com/api/v1/accounts/1/conversations/1/messages" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一条通过API发送的消息",
    "message_type": "outgoing",
    "private": false
  }'
```

---

## 六、应用场景


| 场景         | 解决方案                   | 价值                 |
| ------------ | -------------------------- | -------------------- |
| 电商客服     | 整合网站聊天+WhatsApp+邮件 | 统一处理所有客户咨询 |
| SaaS产品支持 | 嵌入Live Chat+帮助中心     | 降低客服响应时间50%+ |
| 在线教育     | 多渠道学生咨询管理         | 提升学生满意度       |
| 金融服务     | 自托管确保数据合规         | 满足监管要求         |
| 跨境电商     | 多语言+多时区支持          | 服务全球客户         |
| 创业公司     | 替代Intercom/Zendesk       | 节省80%+客服工具成本 |

---

## 七、社区与生态

- **官方网站**：[https://www.chatwoot.com](https://www.chatwoot.com)
- **官方文档**：[https://www.chatwoot.com/help-center](https://www.chatwoot.com/help-center)
- **部署指南**：[https://chatwoot.com/deploy](https://chatwoot.com/deploy)
- **API文档**：[https://www.chatwoot.com/developers/api](https://www.chatwoot.com/developers/api)
- **Discord社区**：[https://discord.gg/cJXdrwS](https://discord.gg/cJXdrwS)
- **翻译贡献**：[https://translate.chatwoot.com](https://translate.chatwoot.com)
- **Captain AI文档**：[https://chwt.app/captain-docs](https://chwt.app/captain-docs)

---

## 八、总结

Chatwoot作为GitHub上31K+ Stars的开源客户支持平台，凭借其**全渠道统一收件箱、AI智能客服、自托管数据主权、丰富的第三方集成**四大核心优势，正在成为企业替代Intercom、Zendesk等商业SaaS客服工具的首选方案。

无论是初创公司希望节省客服工具成本，还是大型企业需要满足数据合规要求，Chatwoot都提供了成熟且可扩展的解决方案。通过简单的Docker Compose部署，你可以在30分钟内拥有一个功能完善的全渠道客服平台。

> **立即体验**：访问 [https://github.com/chatwoot/chatwoot](https://github.com/chatwoot/chatwoot) 获取源码，或前往 [https://www.chatwoot.com](https://www.chatwoot.com) 了解云端版本。
