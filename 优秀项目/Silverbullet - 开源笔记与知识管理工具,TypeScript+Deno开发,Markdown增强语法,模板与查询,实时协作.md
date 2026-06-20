# Silverbullet开源项目详解：笔记与知识管理工具部署教程与Markdown增强语法实时协作实战指南

## 一、项目概述

**Silverbullet** 是一款现代化的开源笔记和个人知识管理工具，由独立开发者 Zef Hemel 创建。它采用 TypeScript 编写后端服务，前端使用 Web 技术栈（Preact）构建，核心数据存储是纯文本 Markdown 文件，可完全自定义并通过 Git 进行版本控制。Silverbullet 的最大特色是对 Markdown 的增强语法：它支持 Wiki 链接、Hashtag 标签、属性（Frontmatter）、任务语法、模板系统以及强大的 Live Queries（内联查询），用户可以在笔记中动态嵌入数据列表。

Silverbullet 支持两种部署模式：本地单用户模式与自托管服务器多端同步模式。项目目前在 GitHub 上拥有超过 7.2K Stars，最新稳定版本为 0.9.x，配套活跃的社区与丰富的第三方插件，是 Obsidian、Notion、Logseq 等主流笔记工具的极具竞争力的开源替代方案。

- **GitHub 地址**：https://github.com/silverbulletmd/silverbullet
- **官方网站**：https://silverbullet.md
- **开源协议**：MIT License
- **开发语言**：TypeScript（Deno 运行时）+ Preact（前端）
- **核心定位**：基于纯文本 Markdown 的现代化笔记与知识管理平台

### 1.1 与同类产品对比

| 特性 | Silverbullet | Obsidian | Notion | Logseq | AppFlowy |
|------|-------------|----------|--------|--------|----------|
| 开源免费 | ✅ | ❌（个人免费，商业订阅） | ❌（SaaS 商业产品） | ✅ | ✅ |
| 基于纯文本 Markdown | ✅ | ✅ | ❌（私有格式） | ✅（Markdown） | ✅ |
| 自托管部署 | ✅ | ❌（本地应用） | ❌ | ✅（自托管服务器） | ✅ |
| 实时协作 | ✅（基于 WebSocket） | ❌ | ✅ | 有限 | 有限 |
| 增强语法 | ✅（Wiki 链接、标签、属性、Live Queries） | ✅ | ✅ | ✅ | ✅ |
| 模板系统 | ✅ | ✅（付费功能） | ✅ | ✅ | ✅ |
| 内联查询 | ✅（强大） | ✅（付费 DataView 插件） | ✅ | 有限 | ✅ |
| 插件系统 | ✅（Space Script 等） | ✅ | ✅ | ✅ | ✅ |
| 端到端加密同步 | ✅ | 需第三方（如 Syncthing） | 云服务 | ✅ | ✅ |
| 典型适用场景 | 个人知识管理、技术笔记、自托管 | 个人笔记、双向链接 | 团队协作、知识库 | 大纲笔记 | 个人笔记（Notion 替代品） |

---

## 二、核心功能模块详解

### 2.1 增强 Markdown 语法

#### Wiki 链接

```markdown
# 项目笔记

请参见 [[另一个笔记]] 了解更多信息。
你也可以指定别名：[[另一个笔记|这个别名]]
```

- 自动生成交叉链接，导航到对应页面
- 支持命名空间：`projects/2024`

#### Hashtag 标签

```markdown
这是一个带标签的句子 #编程 #Go

# 标签语法示例
- 使用 #个人/家庭 分类到个人命名空间下的家庭标签
```

- 支持多级嵌套标签：`#项目/前端/React`
- 可通过 Query 按标签筛选内容

#### Frontmatter 属性

```markdown
---
title: 我的项目计划
date: 2024-06-20
status: active
tags: ["项目", "工作"]
priority: high
---

# 项目计划

正文内容...
```

- 类似 YAML frontmatter，可在 Query 中按属性筛选

#### Task 语法

```markdown
# 今日任务

- [ ] 撰写技术文档
- [x] 完成代码审查
- [ ] 优先级任务 ⏰ 2024-06-22
- [ ] 需要进一步讨论 👉 需要讨论
```

#### 代码块与语法高亮

- 支持主流编程语言的语法高亮

### 2.2 模板系统（Templates）

#### 模板定义

在 `template/` 目录下创建 Markdown 文件作为模板：

```markdown
<!-- template/daily.md -->

# {{today}} 每日笔记

## 今日计划
- [ ] 

## 今日学习
- {{today}} 学习内容

## 标签
#每日笔记
```

#### 使用模板插入

```
<!-- 在笔记中输入 slash command 或模板插入语法 -->

# 在任何笔记中运行 template/daily 模板即可插入每日笔记
```

### 2.3 Live Queries（内联查询）

Silverbullet 的核心功能是通过查询嵌入动态数据：

#### List 查询

```markdown
<!-- 查询所有带 #编程 标签的页面 -->

```query
page select name where tags = "编程" render [[template/page-link]]
```

#### Task 查询

```markdown
<!-- 查询所有未完成的任务 -->

```query
task where done = false order by created desc render "task"
```

#### Table 查询

```markdown
<!-- 查询所有标记为 active 的项目页面 -->

```query
page select name, status, date where status = "active" render "table"
```

### 2.4 页面 / 命名空间 / 标签

| 概念 | 说明 |
|------|------|
| Page（页面） | 每一个 Markdown 文件 |
| Namespace（命名空间） | 类似文件夹：`projects/projectA` 中的 `projects/` |
| Tag（标签） | #开头的分类标记 |
| Frontmatter 属性 | 页面元数据：`title: xxx`、`status: active` |

### 2.5 插件系统

| 官方插件 | 功能 |
|----------|------|
| Space Script | 使用 JavaScript 脚本扩展功能 |
| Custom Widget | 自定义渲染组件 |
| Editor Extension | 扩展编辑器功能 |
| Git Sync | 自动 Git 同步 |
| E2E 加密 | 端到端加密同步 |
| Slack Sync | 与 Slack 集成 |
| Tasks / Calendar | 任务与日历同步 |

---

## 三、技术架构与实现原理

### 3.1 整体架构

```
[用户浏览器（Preact UI）]
         │
         │ WebSocket 实时同步 + HTTP API
         ▼
[Silverbullet Server（TypeScript / Deno 运行时）
    │
    ▼
[可插拔 Storage 后端]
    ├── Local 文件系统（默认）
    ├── S3 存储（对象存储）
    ├── DenoKV（键值存储）
    └── Git 存储（Git 后端）
```

### 3.2 核心组件

| 组件 | 说明 |
|------|------|
| Silverbullet Server | TypeScript 编写的 Web 服务，默认 3000 端口 |
| Silverbullet UI | Preact 编写的前端 UI |
| Pluggable Storage Backend | 支持本地文件系统、S3、DenoKV、Git 等多种存储 |
| WebSocket | 用于多端实时同步 |
| SB-* 自定义语法 | Silverbullet 扩展语法解析器 |

### 3.3 存储后端

- **默认：本地文件系统** - 所有 Markdown 文件存储在一个目录下
- **S3 存储** - 将笔记存储在 S3 兼容的对象存储
- **DenoKV** - Deno 内置的键值存储
- **Git 存储** - 存储在 Git 仓库中，支持版本控制

### 3.4 实时同步

- 多端通过 WebSocket 连接
- 任意一端修改都会实时同步到服务器
- 服务器通过广播通知所有连接的客户端

---

## 四、快速上手：Docker 部署实战

### 4.1 Docker CLI 部署

```bash
docker run -d \
  --name silverbullet \
  -p 3000:3000 \
  -e SB_USER=admin:your-password \
  -v ./space:/space \
  --restart=unless-stopped \
  zefhemel/silverbullet:latest
```

- 访问 `http://<主机IP>:3000`
- 使用 `admin / your-password` 登录

### 4.2 Docker Compose 部署（推荐）

```yaml
version: "3.8"

services:
  silverbullet:
    image: zefhemel/silverbullet:latest
    container_name: silverbullet
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - SB_AUTH=true
      - SB_USER=admin:your-strong-password
      - SB_AUTH_TOKEN=your-secret-token-for-api
      - TZ=Asia/Shanghai
    volumes:
      - ./space:/space
```

启动：

```bash
docker compose up -d
docker compose logs -f
```

### 4.3 环境变量说明

| 环境变量 | 说明 |
|----------|------|
| `SB_USER` | 用户名:密码（如 `admin:pass`），启用基本认证 |
| `SB_AUTH` | `true` 启用认证，`false` 关闭认证 |
| `SB_AUTH_TOKEN` | API Token，用于 API 调用 |
| `SB_FOLDER` | 自定义存储目录（默认 `/space`） |
| `TZ` | 时区设置 |

### 4.4 首次使用

1. 访问 `http://<主机IP>:3000` 并登录
2. 点击左上角的 `New Page` 创建第一个页面
3. 输入页面名称并开始编辑
4. 使用 `[[链接]]`、`#标签`、`--- Frontmatter ---` 等增强语法

---

## 五、手动部署（Deno 安装方式）

### 5.1 安装 Deno

```bash
# macOS/Linux
curl -fsSL https://deno.land/x/install/install.sh | sh

# Windows (PowerShell)
iwr https://deno.land/x/install/install.ps1 -useb | iex
```

### 5.2 安装并启动 Silverbullet

```bash
# 安装
deno install -f -A --unstable -n silverbullet https://get.silverbullet.md

# 创建笔记目录
mkdir -p ~/Notes
cd ~/Notes

# 启动服务
silverbullet --user admin:your-password .
```

访问 `http://localhost:3000`

### 5.3 升级

```bash
silverbullet upgrade
```

### 5.4 从源码运行

```bash
# 克隆仓库
git clone https://github.com/silverbulletmd/silverbullet.git
cd silverbullet

# 安装依赖并构建
deno task build:web

# 运行
deno task server ~/Notes --user admin:password
```

---

## 六、Markdown 增强语法详解

### 6.1 Wiki 链接

```markdown
# 项目文档

参见 [[技术架构]] 了解系统架构。
点击 [[项目计划|项目计划页面]] 查看详细计划。
支持目录链接：[[projects/projectA/README]]
```

### 6.2 Hashtag 标签

```markdown
# 分类系统

支持多级标签：#项目/前端/React
多个标签可在同一页面使用：#学习 #笔记
```

### 6.3 Frontmatter 属性

```markdown
---
title: 项目计划
created: 2024-06-20
status: active
priority: high
tags: ["项目", "工作"]
---

# 项目计划正文

...
```

### 6.4 Task 语法

```markdown
# 任务列表

- [ ] 未完成任务
- [x] 已完成任务
- [ ] 带截止日期的任务 ⏰ 2024-06-25
- [ ] 需要讨论 👉 讨论笔记
```

### 6.5 Query 块

#### List 查询

```query
page select name where tags = "项目" render "[[{{name}}]]"
```

#### Task 查询

```query
task where done = false and tags = "工作" order by created desc render "task"
```

#### Table 查询

```query
page select name, status, date where status = "active" render "table"
```

#### 嵌入其他页面

```markdown
<!-- 嵌入某个页面的全文 -->

{{[[另一个页面]]}}
```

### 6.6 模板系统

#### 创建模板

在 `template/` 目录下创建 Markdown 文件，例如 `template/daily.md`：

```markdown
# {{today}} 每日笔记

## 今日计划
- [ ] 

## 学习与总结
- 

## 会议记录
- 

## 标签
#每日笔记
```

#### 在其他页面使用模板

在笔记中输入 `/template/daily` 或通过模板命令插入模板。

---

## 七、插件系统与自定义功能

### 7.1 Space Script

Space Script 是 Silverbullet 的脚本系统，通过 JavaScript 扩展功能：

```javascript
// 在 .space/scripts/my-script.js 中创建脚本

export function helloWorld() {
  return "Hello, Silverbullet!";
}

export function getRecentNotes(count = 10) {
  return syscall("space.listPages")
    .then(pages => pages
      .sort((a, b) => b.lastModified - a.lastModified)
      .slice(0, count));
}
```

在 Markdown 中调用：

```markdown
{{helloWorld()}}
```

### 7.2 Custom Widget

通过 Space Script 创建自定义渲染组件：

```javascript
export function renderGreeting(name) {
  return `<div style="color: #4a90e2; font-size: 18px;">Hello, ${name}!</div>`;
}
```

### 7.3 Editor Extension

扩展编辑器功能，例如自定义语法高亮、自动补全等。

### 7.4 官方插件库

Silverbullet 提供了官方插件库，可通过 Plugs 命令安装：

```
在 UI 中进入 Settings → Plugs → Add plug
```

---

## 八、API 接口与自动化集成

### 8.1 REST API

```bash
# 设置 API Token
export SB_TOKEN="your-secret-token"

# 列出所有页面
curl -H "Authorization: Bearer $SB_TOKEN" http://127.0.0.1:3000/.pages.json

# 获取指定页面内容
curl -H "Authorization: Bearer $SB_TOKEN" http://127.0.0.1:3000/%E4%B8%AD%E6%96%87%E9%A1%B5%E9%9D%A2.md

# 创建/更新页面
curl -X PUT -H "Authorization: Bearer $SB_TOKEN" \
  -H "Content-Type: text/markdown" \
  --data-binary "# 新页面\n\n内容" \
  http://127.0.0.1:3000/new-page.md
```

### 8.2 WebSocket API

Silverbullet 使用 WebSocket 实现实时同步：

```javascript
// JavaScript 示例
const socket = new WebSocket("ws://127.0.0.1:3000/.ws");
socket.onopen = () => {
  console.log("WebSocket 已连接");
};
socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  console.log("收到消息:", data);
};
```

### 8.3 通过 Git 自动同步

```bash
# 在 space 目录初始化 Git
cd /path/to/space
git init
git add .
git commit -m "initial"

# 设置定时任务（每 5 分钟提交一次）
*/5 * * * * cd /path/to/space && git add -A && git commit -m "auto sync" && git push
```

---

## 九、同步方案与多端使用

### 9.1 本地 Git 同步

- 将 space 目录纳入 Git 版本控制
- 多端通过 Git pull/push 同步
- 简单可靠，支持历史版本

### 9.2 云盘同步

- 将 space 目录放在 Syncthing、Nextcloud、OneDrive 等云盘目录
- 借助云盘服务实现多端同步
- 简单方便，但不保证多端同时编辑时的一致性

### 9.3 自托管服务器多端同步

- 在公网 VPS 上部署 Silverbullet
- 多设备通过浏览器访问 `https://notes.example.com`
- 使用 Nginx 反代 + Let's Encrypt HTTPS
- 真正的实时同步

```nginx
server {
    listen 443 ssl http2;
    server_name notes.example.com;

    ssl_certificate     /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 9.4 端到端加密

- 使用 E2E 加密插件
- 使用密码加密存储内容
- 服务端无法读取明文

---

## 十、常见问题与故障排查

### 10.1 无法登录

- 检查 `SB_USER` 环境变量格式是否正确：`username:password`
- 检查容器日志：`docker logs silverbullet`

### 10.2 WebSocket 连接失败

- 确保反代正确配置 `Upgrade` 和 `Connection` 头
- 确保防火墙未阻止 WebSocket

### 10.3 文件保存失败

- 检查 space 目录权限是否正确：`chmod -R 755 /path/to/space`
- 检查磁盘空间是否充足

### 10.4 数据备份

```bash
# 备份 space 目录
tar czf silverbullet-backup-$(date +%Y%m%d).tar.gz /path/to/space

# 使用 Git 做版本控制
cd /path/to/space
git add -A
git commit -m "backup $(date)"
```

### 10.5 升级 Silverbullet

```bash
docker pull zefhemel/silverbullet:latest
docker stop silverbullet
docker rm silverbullet
# 重新创建容器
```

---

## 十一、社区生态与学习资源

| 项目 | 用途 | 地址 |
|------|------|------|
| 官方文档 | 完整使用手册与 API 文档 | https://silverbullet.md/ |
| Silverbullet 论坛 | 社区交流 | https://github.com/silverbulletmd/silverbullet/discussions |
| Awesome Silverbullet | 第三方插件与资源集合 | https://github.com/silverbulletmd/awesome-silverbullet |
| Silverbullet Plugs | 官方插件库 | https://silverbullet.md/🔌_Plugs |
| Silverbullet Demo | 在线演示 | https://play.silverbullet.md/ |
| Silverbullet 博客 | 官方博客与更新 | https://silverbullet.md/Blog |

---

## 十二、使用场景与案例参考

### 12.1 个人知识管理

使用 Silverbullet 构建个人第二大脑（Zettelkasten）：
- 每一个笔记是一个 Markdown 文件
- 使用 Wiki 链接建立笔记之间的关系
- 使用 Hashtag 组织笔记分类
- 使用 Live Queries 动态生成索引页面

### 12.2 项目文档管理

- 为每个项目创建命名空间
- 使用 Frontmatter 记录项目状态
- 使用 Task 语法跟踪项目任务
- 使用 Live Queries 自动生成任务列表

### 12.3 每日笔记与日记

- 使用模板系统创建每日笔记模板
- 使用 Live Queries 查询一周内完成的任务
- 使用标签组织生活与工作

### 12.4 团队协作与知识共享

- 在自托管服务器上部署 Silverbullet
- 多用户通过浏览器访问同一空间
- 使用 Git 做版本控制与冲突解决

### 12.5 与 Obsidian / Notion / Logseq 的选择

| 工具 | 推荐场景 |
|------|----------|
| Silverbullet | 纯文本 Markdown、自托管、实时协作、增强语法、内联查询 |
| Obsidian | 本地 Markdown 编辑器、强大的双向链接、插件生态丰富 |
| Notion | 团队协作、块级编辑、多数据库功能、但非开源且数据存储在云端 |
| Logseq | 大纲式笔记、Outliner 用户体验、开源支持 |
| AppFlowy | Notion 替代品、开源免费、适合简单笔记与任务管理 |

---

## 总结

Silverbullet 凭借纯文本 Markdown 存储与强大的增强语法，为自托管笔记领域带来了新的思路。它不依赖任何外部数据库，所有笔记都以标准 Markdown 文件保存，可完全通过 Git 进行版本控制，也能在任何支持 Markdown 的编辑器中打开。它的 Wiki 链接、Hashtag 标签、Frontmatter 属性、Task 语法以及 Live Queries 内联查询功能，使笔记具备了动态数据处理能力，配合模板系统可实现复杂的工作流自动化。对于追求数据主权与自托管的用户，Silverbullet + Docker 部署构成了一个既简洁又强大的个人知识管理平台。配合端到端加密和多端实时同步，Silverbullet 也正在成为 Obsidian 和 Notion 的有力竞争者，值得所有自托管爱好者尝试。
