# Maybe Finance - 开源个人财务管理平台,替代Mint与Empower,Rails+React开发,银行账户自动同步,投资组合追踪

## 项目概述

Maybe Finance 是一个功能完整的开源个人财务管理平台，旨在帮助用户全面管理财务和投资。该项目最初是一个商业产品（$249/年），在 2023 年中期由于无法获得融资而关闭源代码。2024 年初，项目以 MIT 许可证完全开源，成为替代 Mint、Personal Capital (Empower)、YNAB 等商业财务管理服务的首选方案。Maybe Finance 支持银行账户自动同步、投资组合追踪、净资产跟踪、预算管理等功能，采用 Rails + React 技术栈构建，界面美观，功能完善。

## 核心特性

### 全面的财务管理

- **净资产跟踪**：实时追踪总资产、负债和净资产
- **账户同步**：支持通过 Plaid（美国/加拿大）或 Synth（欧洲）自动同步银行账户
- **交易分类**：自动或手动对交易进行分类
- **预算管理**：创建和管理月度预算，跟踪支出
- **账单提醒**：设置账单到期提醒，避免逾期

### 投资组合管理

- **多资产支持**：支持股票、ETF、加密货币、房地产等资产
- **实时估值**：自动获取投资组合实时市值
- **历史走势**：查看投资组合历史表现图表
- **资产配置**：分析资产配置比例，优化投资组合
- **退休规划**：基于当前储蓄和预期收益进行退休规划

### 财务分析

- **现金流分析**：月度/年度收入与支出分析
- **趋势追踪**：识别支出模式和趋势
- **债务管理**：追踪贷款、信用卡等负债
- **财务目标**：设定储蓄和还债目标

### 隐私与安全

- **完全自托管**：数据存储在自有服务器
- **无第三方追踪**：不收集用户数据
- **本地加密**：敏感数据本地加密
- **开源透明**：代码公开，可审计

## 技术架构

### 技术栈

```
┌─────────────────────────────────────┐
│         Maybe Finance                │
├─────────────────────────────────────┤
│  前端: React + Tailwind CSS          │
│  后端: Ruby on Rails                 │
│  数据库: PostgreSQL                  │
│  缓存: Redis                         │
│  银行集成: Plaid / Synth             │
└─────────────────────────────────────┘
```

### 架构优势

| 特性 | Maybe Finance | Mint | YNAB |
|------|--------------|------|------|
| 开源免费 | 是 | 否 | $109/年 |
| 银行同步 | 是 | 是 | 需手动导入 |
| 投资追踪 | 是 | 部分 | 否 |
| 自托管 | 是 | 否 | 否 |
| UI 质量 | 优秀 | 一般 | 良好 |

## 部署教程

### Docker 部署（推荐）

#### 前置要求

- Docker 和 Docker Compose
- 2GB RAM 最低要求
- 拥有域名（用于 HTTPS 和 Plaid 集成）

#### 快速部署

```bash
# 创建项目目录
mkdir -p ~/maybe && cd ~/maybe

# 下载官方 Docker Compose 文件
curl -fsSL -o compose.yml \
  https://raw.githubusercontent.com/maybe-finance/maybe/main/compose.example.yml

# 创建环境变量文件
cat > .env << 'EOF'
SECRET_KEY_BASE=$(openssl rand -hex 64)
POSTGRES_PASSWORD=$(openssl rand -hex 16)
EOF

# 生成 SECRET_KEY_BASE
export SECRET_KEY_BASE=$(openssl rand -hex 64)
export POSTGRES_PASSWORD=$(openssl rand -hex 16)

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f maybe
```

#### 访问应用

打开浏览器访问 `http://localhost:3000`（或你的域名），首次访问需要创建账户。

### 完整配置示例

创建 `docker-compose.yml`：

```yaml
services:
  maybe:
    image: ghcr.io/maybe-finance/maybe:stable
    container_name: maybe-finance
    restart: unless-stopped
    ports:
      - "3000:3000"
    env_file: .env
    volumes:
      - maybe_storage:/rails/storage
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    container_name: maybe-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: maybe_finance_production
      POSTGRES_USER: maybe_finance
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U maybe_finance"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  maybe_storage:
```

创建 `.env` 文件：

```bash
# 应用密钥
SECRET_KEY_BASE=your-64-char-secret-key-here

# 数据库配置
DB_HOST=postgres
DB_PORT=5432
DB_NAME=maybe_finance_production
DB_USERNAME=maybe_finance
DB_PASSWORD=your-strong-password

# 应用 URL（必填，用于会话 cookie）
APP_DOMAIN=finance.yourdomain.com
RAILS_FORCE_SSL=true

# 邮件配置（用于密码重置、通知）
SMTP_ADDRESS=smtp.youremail.com
SMTP_PORT=587
SMTP_USERNAME=finance@yourdomain.com
SMTP_PASSWORD=your-smtp-password
SMTP_DOMAIN=yourdomain.com
MAILER_FROM=finance@yourdomain.com

# 银行数据提供商（美国/加拿大选 Plaid，欧洲选 Synth）
# Plaid 选项
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret
PLAID_ENV=production

# Synth 选项（欧洲）
# SYNTH_API_KEY=your-synth-api-key

# 自托管模式
SELF_HOSTED=true
```

### 手动部署（开发环境）

```bash
# 克隆仓库
git clone https://github.com/maybe-finance/maybe.git
cd maybe

# 安装依赖
pnpm install

# 复制环境变量
cp .env.example .env

# 生成密钥
openssl rand -hex 64  # 填入 SECRET_KEY_BASE

# 数据库迁移
pnpm prisma:migrate:dev

# 启动开发服务
pnpm dev
```

## 银行账户集成

### Plaid 设置（美国/加拿大）

1. 注册 [Plaid Dashboard](https://dashboard.plaid.com/)
2. 创建应用，获取 `PLAID_CLIENT_ID` 和 `PLAID_SECRET`
3. 在 `.env` 中配置：

```bash
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ENV=sandbox  # 测试环境
# 或
PLAID_ENV=production  # 生产环境
```

4. 在 Maybe Finance 界面中连接银行账户

### Synth 设置（欧洲）

1. 注册 [Synth](https://www.synth.ai/)
2. 获取 API 密钥
3. 配置：

```bash
SYNTH_API_KEY=your_synth_api_key
```

### 手动导入（无 Plaid/Synth）

如果不想使用自动同步，可以手动导入交易记录：

1. 从银行导出 CSV 文件
2. 在 Maybe Finance 中导入
3. 手动分类交易

## Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name finance.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name finance.yourdomain.com;

    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 备份与恢复

### 备份数据库

```bash
# 备份
docker exec maybe-postgres pg_dump -U maybe_finance > backup.sql

# 恢复
docker exec -i maybe-postgres psql -U maybe_finance < backup.sql
```

### 备份文件

```bash
# 备份整个数据目录
tar -czf maybe-backup.tar.gz ~/maybe/
```

## 更新 Maybe Finance

```bash
cd ~/maybe

# 拉取最新镜像
docker compose pull

# 重启服务
docker compose up -d

# 查看日志确认更新成功
docker compose logs -f maybe
```

## 常见问题

### Q: Maybe Finance 是免费的吗？

A: 是的，Maybe Finance 采用 MIT 许可证，完全免费使用。没有付费功能或订阅要求。

### Q: 数据存储在哪里？

A: 如果自托管，数据完全存储在你的服务器上。如果使用官方托管服务，数据存储在他们的服务器上。

### Q: 支持哪些银行？

A: 通过 Plaid 集成，支持 12,000+ 金融机构，涵盖美国、加拿大、英国的主要银行。

### Q: 是否支持多货币？

A: 是的，Maybe Finance 支持多货币账户和交易。

### Q: 如何获取技术支持？

A: 可以通过 GitHub Issues 报告问题，也可以在 Discord 社区寻求帮助。

## 项目资源

- **GitHub**: https://github.com/maybe-finance/maybe
- **官网**: https://maybe finance.com/
- **文档**: https://docs.maybe.finance/
- **社区**: Discord 社区

## 与同类产品对比

| 特性 | Maybe Finance | Firefly III | Actual Budget |
|------|--------------|-------------|--------------|
| 技术栈 | Rails + React | PHP + Laravel | Electron/Node |
| UI 质量 | 优秀 | 良好 | 良好 |
| 银行自动同步 | Plaid/Synth | 手动导入 | SimpleFin |
| 投资追踪 | 是 | 否 | 否 |
| GitHub Stars | 37K+ | 16K+ | 17K+ |
| 最佳用途 | Mint/Empower 替代 | 手动记账 | 零基预算 |

---

*最后更新：2026-06-21*
