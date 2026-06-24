# Toonflow - AI短剧漫剧创作工具

## 项目信息

| 项目 | 信息 |
|------|------|
| **名称** | Toonflow |
| **类型** | AI创作工具 |
| **语言** | TypeScript/React |
| **Stars** | 470+ |
| **来源** | Gitee |
| **地址** | https://gitee.com/HBAI-Ltd/Toonflow-app |

## 项目介绍

Toonflow 是一款 **AI 短剧漫剧工具**，能够利用 AI 技术将小说自动转化为剧本，并结合 AI 生成的图片和视频，实现高效的短剧创作。借助 Toonflow，可以轻松完成从文字到影像的全流程，让短剧制作变得更加智能与便捷。

**核心功能：**
- 小说自动转剧本
- AI 图片生成
- AI 视频生成
- 角色管理
- 分镜设计
- 多语言支持

**适用场景：**
- 短剧创作者
- 漫剧制作团队
- 内容创作者
- 小说改编
- 自媒体从业者

---

## 安装教程

### 环境要求

- Node.js 18+
- npm 9+ 或 pnpm 8+
- 16GB+ RAM
- NVIDIA GPU（推荐，用于AI生成）

### 方法一：Docker 部署（推荐）

```bash
# 克隆仓库
git clone https://gitee.com/HBAI-Ltd/Toonflow-app.git
cd Toonflow-app

# 启动所有服务
docker-compose up -d

# 访问 http://localhost:3000
```

### 方法二：本地开发

#### 1. 克隆代码

```bash
git clone https://gitee.com/HBAI-Ltd/Toonflow-app.git
cd Toonflow-app
```

#### 2. 安装依赖

```bash
# 使用 npm
npm install

# 或使用 pnpm（推荐）
pnpm install
```

#### 3. 环境配置

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑配置文件
vim .env
```

`.env` 配置示例：
```env
# 应用配置
NEXT_PUBLIC_APP_NAME=Toonflow
NEXT_PUBLIC_API_URL=http://localhost:3000

# AI 服务配置
OPENAI_API_KEY=sk-xxxxx
OPENAI_BASE_URL=https://api.openai.com/v1

# 图片生成服务
IMAGE_PROVIDER=stability  # 或 midjourney/dalle
STABILITY_API_KEY=sk-xxxxx

# 视频生成服务
VIDEO_PROVIDER=runway
RUNWAY_API_KEY=sk-xxxxx

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/toonflow

# 存储配置
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=toonflow
```

#### 4. 数据库初始化

```bash
# 使用 Prisma 迁移数据库
npx prisma generate
npx prisma migrate dev

# 或生产环境
npx prisma migrate deploy
```

#### 5. 启动开发服务器

```bash
# 开发模式
npm run dev

# 生产模式
npm run build
npm run start
```

### 方法三：VPS 部署

#### 1. 安装 Node.js

```bash
# 使用 nvm 安装
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

#### 2. 安装 PM2

```bash
npm install -g pm2
```

#### 3. 部署应用

```bash
# 克隆代码
git clone https://gitee.com/HBAI-Ltd/Toonflow-app.git
cd Toonflow-app

# 安装依赖
npm install --production

# 构建
npm run build

# 使用 PM2 启动
pm2 start npm --name "toonflow" -- start

# 配置 Nginx 反向代理
vim /etc/nginx/conf.d/toonflow.conf
```

#### 4. Nginx 配置

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        proxy_pass http://localhost:3000;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 快速使用

### 1. 创建项目

访问 `http://localhost:3000`，点击「新建项目」。

### 2. 导入小说

```bash
# 支持 TXT、Word、Markdown 格式
# 直接在界面导入或使用 API
curl -X POST http://localhost:3000/api/project/import \
  -F "file=@/path/to/novel.txt" \
  -F "title=我的小说"
```

### 3. 自动生成剧本

```bash
# 通过 AI 自动将小说转换为剧本
curl -X POST http://localhost:3000/api/ai/convert-to-script \
  -H "Content-Type: application/json" \
  -d '{
    "novelId": "novel_uuid",
    "style": "短剧",
    "episodes": 10
  }'
```

### 4. 生成角色

```bash
# 为剧本生成 AI 角色
curl -X POST http://localhost:3000/api/ai/generate-characters \
  -H "Content-Type: application/json" \
  -d '{
    "scriptId": "script_uuid",
    "count": 5
  }'
```

### 5. 生成图片

```bash
# 生成场景或角色图片
curl -X POST http://localhost:3000/api/ai/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "古风庭院，樱花树下，一位白衣女子",
    "style": "水墨画",
    "size": "16:9"
  }'
```

### 6. 生成视频

```bash
# 基于分镜生成视频
curl -X POST http://localhost:3000/api/ai/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "storyboardId": "storyboard_uuid",
    "duration": 30
  }'
```

---

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/project | POST | 创建项目 |
| /api/novel/import | POST | 导入小说 |
| /api/ai/convert-to-script | POST | 小说转剧本 |
| /api/ai/generate-characters | POST | 生成角色 |
| /api/ai/generate-image | POST | 生成图片 |
| /api/ai/generate-video | POST | 生成视频 |
| /api/export/video | POST | 导出视频 |

---

## 常见问题

**Q: 图片生成失败？**
A: 检查 AI 服务 API Key 是否配置正确，或切换图片生成服务商

**Q: 视频生成速度慢？**
A: 使用 GPU 服务器，或调整视频生成参数降低质量

**Q: 如何支持自定义 AI 模型？**
A: 在设置中心编写供应商 TypeScript 逻辑，无需改源码

**Q: 多语言支持哪些？**
A: 中文、英文、日文、韩文、泰文、越南文、俄文

---

## 相关资源

- [Gitee 仓库](https://gitee.com/HBAI-Ltd/Toonflow-app)
- [在线演示](https://toonflow.hbai.tech)
- [使用文档](https://docs.toonflow.hbai.tech)
