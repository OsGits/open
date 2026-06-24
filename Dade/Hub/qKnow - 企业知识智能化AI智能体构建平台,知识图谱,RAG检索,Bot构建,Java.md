# qKnow - 企业知识智能化AI智能体构建平台

## 项目信息

| 项目 | 信息 |
|------|------|
| **名称** | qKnow |
| **类型** | AI智能体平台 |
| **语言** | Java |
| **Stars** | 607 |
| **来源** | Gitee GVP |
| **地址** | https://gitee.com/qiantongtech/qKnow |

## 项目介绍

qKnow 是一套面向企业**知识智能化**与**行业 AI 应用**场景的开源 AI 智能体构建平台，围绕**知识图谱**、**知识库 RAG**、**Bot 构建**与**开箱即用的 AI 应用**等核心能力，支持企业文档、结构化数据、业务知识和专家经验的统一接入与智能化沉淀。

**核心功能：**
- 知识图谱构建与管理
- 知识库 RAG 检索增强生成
- Bot 智能体构建
- 开箱即用 AI 应用
- 企业文档统一接入
- 智能问答平台

**适用场景：**
- 企业知识中枢建设
- 智能问答平台
- 智能体开发平台
- 行业深度 AI 解决方案
- 开发者二次开发

**在线演示：**
- 开源版演示：https://demo.qknow.ai （账号：qKnow 密码：qKnow123）
- 在线文档：https://community.qknow.ai

---

## 安装教程

### 环境要求

- JDK 17+
- Maven 3.8+
- MySQL 8.0+ / PostgreSQL 14+
- Redis 6.0+
- 16GB+ RAM
- 100GB+ 存储空间

### 方法一：Docker 一键部署（推荐）

```bash
# 下载部署脚本
git clone https://gitee.com/qiantongtech/qKnow.git
cd qKnow/deploy/docker

# 修改配置文件
vim .env

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

`.env` 配置文件示例：
```env
# 数据库配置
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/qknow
SPRING_DATASOURCE_USERNAME=qknow
SPRING_DATASOURCE_PASSWORD=your_password

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# LLM配置（支持多种大模型）
LLM_PROVIDER=openai  # 或 qwen/yi/etc
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
```

### 方法二：手动部署

#### 1. 数据库初始化

```sql
-- 创建数据库
CREATE DATABASE qknow DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'qknow'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON qknow.* TO 'qknow'@'%';
FLUSH PRIVILEGES;
```

#### 2. 后端服务部署

```bash
# 克隆代码
git clone https://gitee.com/qiantongtech/qKnow.git
cd qKnow

# 修改配置文件
vim qknow-server/src/main/resources/application.yml

# 打包
mvn clean package -DskipTests

# 运行
java -jar qknow-server/target/qknow-server.jar
```

#### 3. 前端部署

```bash
cd qknow-ui

# 安装依赖
npm install

# 修改 API 地址
vim .env
# VITE_API_BASE_URL=http://localhost:8080

# 构建
npm run build

# 部署到 Nginx
cp -r dist /usr/share/nginx/html
```

#### 4. Nginx 配置

```nginx
server {
    listen 80;
    server_name your_domain.com;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket 支持
    location /ws {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 快速使用

### 1. 登录系统

访问部署地址，使用演示账号登录：
- 账号：qKnow
- 密码：qKnow123

### 2. 创建知识库

```bash
# 通过 API 创建知识库
curl -X POST http://localhost:8080/api/knowledge/base \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token" \
  -d '{
    "name": "产品知识库",
    "description": "公司产品相关文档",
    "embedModel": "text-embedding-ada-002"
  }'
```

### 3. 上传文档

支持格式：PDF、Word、TXT、Markdown、Excel、PPT

```bash
# 上传单个文档
curl -X POST http://localhost:8080/api/knowledge/document/upload \
  -F "file=@/path/to/document.pdf" \
  -F "baseId=knowledge_base_id"
```

### 4. 构建 Bot

```bash
# 创建 Bot
curl -X POST http://localhost:8080/api/bot \
  -H "Content-Type: application/json" \
  -d '{
    "name": "客服助手",
    "description": "智能客服机器人",
    "model": "gpt-4",
    "knowledgeBases": ["base_id_1", "base_id_2"],
    "prompt": "你是一个专业的客服助手..."
  }'
```

### 5. 对话测试

```bash
# 发起对话
curl -X POST http://localhost:8080/api/chat/chat \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "bot_id",
    "query": "产品有哪些功能？"
  }'
```

---

## Docker Compose 完整配置

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: qknow
      MYSQL_USER: qknow
      MYSQL_PASSWORD: qknow_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  minio:
    image: minio/minio
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

  qknow:
    image: qiantongtech/qknow:latest
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/qknow
      SPRING_DATASOURCE_USERNAME: qknow
      SPRING_DATASOURCE_PASSWORD: qknow_password
      REDIS_HOST: redis
      MINIO_ENDPOINT: http://minio:9000
    depends_on:
      - mysql
      - redis
      - minio

volumes:
  mysql_data:
  minio_data:
```

---

## API 接口文档

启动服务后访问：`http://localhost:8080/swagger-ui.html`

| 模块 | 接口前缀 | 说明 |
|------|----------|------|
| 知识库 | /api/knowledge | 知识库管理 |
| Bot | /api/bot | Bot构建管理 |
| 文档 | /api/document | 文档处理 |
| 对话 | /api/chat | 智能对话 |
| 用户 | /api/user | 用户管理 |

---

## 常见问题

**Q: 启动失败，数据库连接错误？**
A: 检查 MySQL 版本（需8.0+），确认数据库和用户已创建

**Q: 知识库检索效果不好？**
A: 尝试更换 Embedding 模型，或调整向量检索参数

**Q: 如何接入自己的大模型？**
A: 在系统设置中配置 LLM，提供 API Key 和 Base URL

**Q: 支持哪些文件格式？**
A: PDF、Word、TXT、Markdown、Excel、PPT、图片（OCR）

---

## 相关资源

- [Gitee 仓库](https://gitee.com/qiantongtech/qKnow)
- [在线文档](https://community.qknow.ai)
- [演示地址](https://demo.qknow.ai)
- [专业版演示](https://pro-demo.qknow.ai)
