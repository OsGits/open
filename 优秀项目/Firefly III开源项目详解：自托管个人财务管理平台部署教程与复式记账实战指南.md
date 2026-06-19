# Firefly III开源项目详解：自托管个人财务管理平台部署教程与复式记账实战指南

## 一、项目概述

**Firefly III** 是一款免费开源的个人财务管理软件，专为自托管场景设计。它采用复式记账（Double-Entry Bookkeeping）原则，帮助用户追踪收入与支出、管理预算、设置储蓄目标，并通过丰富的图表和报告提供财务洞察。项目由 James Cole（JC5）发起并持续维护，起源于荷兰，遵循欧盟数据隐私理念，永远不会在未经用户明确授权的情况下联系外部服务器。

- **GitHub 地址**：https://github.com/firefly-iii/firefly-iii
- **官方文档**：https://docs.firefly-iii.org/
- **在线演示**：https://demo.firefly-iii.org/
- **开源协议**：AGPL-3.0 License
- **Star 数量**：15K+
- **技术栈**：PHP 61%、JavaScript 24%、Twig 8.3%、Vue 2.7%
- **最新版本**：v6.6.3（2026年5月21日发布）
- **总发布版本数**：327 个
- **总提交数**：23,175+ Commits

---

## 二、核心特性解读

### 1. 复式记账系统（Double-Entry Bookkeeping）

Firefly III 采用专业的复式记账原则，每笔交易都会在至少两个账户中记录（借方和贷方），确保财务数据的准确性和平衡性。这种记账方式源自传统会计学，比简单的收支记录更严谨可靠。

### 2. 预算管理

- 为不同类别设置月度或年度预算
- 实时追踪预算执行情况
- 超支预警提醒
- 预算与实际支出对比分析

### 3. 储蓄目标（Piggy Banks）

设定具体储蓄目标（如旅行基金、应急储备），系统会自动追踪进度，帮助用户养成储蓄习惯。

### 4. 规则引擎（Rule-Based Transaction Handling）

强大的自动化规则系统：

- 根据交易描述自动分类
- 自动为交易添加标签
- 自动设置预算归属
- 批量处理历史交易

### 5. 多币种支持

支持任意货币，自动汇率转换，适合跨境收支、多币种资产管理的用户。

### 6. 丰富的财务报表

| 报表类型 | 说明 |
|----------|------|
| 收支报告 | 按类别、标签、预算维度分析 |
| 资产负债表 | 净资产实时概览 |
| 预算执行报告 | 预算 vs 实际对比 |
| 分类汇总 | 支出结构可视化 |
| 趋势分析 | 收入/支出历史趋势图 |

### 7. 数据导入

支持通过外部工具导入银行数据：

- CSV 文件导入
- OFX/QFX 格式
- 银行 API 对接（需第三方工具）
- 手动录入

### 8. 安全特性

- 2FA 双因素认证
- 自托管隔离，数据不上传云端
- REST JSON API（覆盖几乎所有功能）
- 用户认证与权限管理

---

## 三、适用场景

| 场景 | 说明 |
|------|------|
| 个人财务管理 | 追踪日常收支、管理预算、分析消费习惯 |
| 家庭账本 | 家庭成员共享记账、共同管理家庭财务 |
| 自由职业者 | 项目收入追踪、税务准备、发票管理 |
| 小型企业 | 基础财务记账、费用分类、报表导出 |
| 储蓄规划 | 设定储蓄目标、追踪进度、实现财务目标 |
| 跨境收支 | 多币种管理、汇率追踪、海外资产记录 |

---

## 四、部署方法详解

### 方法一：Docker Compose 部署（推荐）

创建 `docker-compose.yml` 文件：

```yaml
services:
  app:
    image: fireflyiii/core:latest
    hostname: app
    container_name: firefly_iii_core
    restart: always
    volumes:
      - firefly_iii_upload:/var/www/html/storage/upload
    env_file: .env
    ports:
      - 8080:8080
    depends_on:
      - db

  db:
    image: mariadb:lts
    hostname: db
    container_name: firefly_iii_db
    restart: always
    environment:
      - MYSQL_RANDOM_ROOT_PASSWORD=yes
      - MYSQL_USER=firefly
      - MYSQL_PASSWORD=secret_firefly_password
      - MYSQL_DATABASE=firefly
    volumes:
      - firefly_iii_db:/var/lib/mysql

  cron:
    image: fireflyiii/core:latest
    container_name: firefly_iii_cron
    restart: always
    env_file: .env
    entrypoint: /usr/local/bin/cron.sh
    depends_on:
      - app

volumes:
  firefly_iii_upload:
  firefly_iii_db:
```

创建 `.env` 配置文件：

```bash
# 基本配置
APP_ENV=local
APP_DEBUG=false
APP_URL=http://localhost:8080
APP_KEY=your-32-char-random-key-here

# 数据库配置
DB_CONNECTION=mysql
DB_HOST=db
DB_PORT=3306
DB_DATABASE=firefly
DB_USERNAME=firefly
DB_PASSWORD=secret_firefly_password

# 时区和语言
DEFAULT_LANGUAGE=zh_CN
DEFAULT_CURRENCY=CNY
TZ=Asia/Shanghai
```

启动服务：

```bash
docker compose up -d
```

访问 `http://localhost:8080` 完成初始化设置。

> **注意**：`APP_KEY` 必须是 32 位随机字符串，可通过 `openssl rand -base64 24` 生成。

### 方法二：Docker 命令部署

```bash
docker run -d \
  --name=firefly_iii_core \
  --restart=always \
  -v firefly_iii_upload:/var/www/html/storage/upload \
  -p 8080:8080 \
  -e APP_KEY=your-32-char-random-key-here \
  -e DB_CONNECTION=sqlite \
  fireflyiii/core:latest
```

SQLite 模式适合快速体验，生产环境建议使用 MariaDB/MySQL。

### 方法三：传统服务器部署

**环境要求**：
- PHP 8.2+
- MySQL 8.0+ / MariaDB 10.6+ / PostgreSQL 16+
- Composer
- Node.js + NPM（前端构建）

```bash
# 克隆仓库
git clone https://github.com/firefly-iii/firefly-iii.git
cd firefly-iii

# 安装 PHP 依赖
composer install --no-dev --prefer-dist

# 安装前端依赖并构建
npm install && npm run build

# 复制环境配置
cp .env.example .env

# 生成应用密钥
php artisan key:generate

# 配置数据库连接（编辑 .env 文件）
# 执行数据库迁移
php artisan migrate:refresh --seed

# 创建管理员账户
php artisan firefly-iii:create-admin

# 启动服务
php artisan serve
```

---

## 五、进阶配置

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name finance.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name finance.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    root /var/www/firefly-iii/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### 定时任务配置

Firefly III 需要定时任务来处理周期性交易和报告生成：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每分钟执行）
* * * * * cd /var/www/firefly-iii && /usr/bin/php artisan schedule:run >> /dev/null 2>&1
```

Docker 部署时，上述 `docker-compose.yml` 中的 `cron` 服务已自动处理。

### 数据备份

```bash
# 备份数据库
docker exec firefly_iii_db mysqldump -u firefly -psecret_firefly_password firefly > firefly-backup-$(date +%Y%m%d).sql

# 备份上传文件
docker run --rm -v firefly_iii_upload:/data -v $(pwd):/backup alpine tar czf /backup/firefly-uploads-$(date +%Y%m%d).tar.gz -C /data .
```

### 启用 2FA

1. 登录 Firefly III 管理后台
2. 进入 `选项` → `个人资料` → `双因素认证`
3. 使用 Authenticator App（如 Google Authenticator）扫描二维码
4. 输入验证码完成绑定

---

## 六、核心功能使用指南

### 创建账户

Firefly III 使用账户体系管理资金流动：

| 账户类型 | 用途 |
|----------|------|
| 资产账户 | 银行账户、现金、电子钱包 |
| 支出账户 | 商家、服务提供商 |
| 收入账户 | 雇主、客户、收入来源 |
| 负债账户 | 信用卡、贷款 |

### 记录交易

1. 点击 `交易` → `新建取款/存款/转账`
2. 选择来源账户和目标账户
3. 填写金额、日期、描述
4. 选择分类和预算
5. 保存

### 设置预算

1. 进入 `预算` → `新建预算`
2. 设置预算名称和金额
3. 选择适用的账户
4. 系统会自动将匹配的交易归入该预算

### 创建储蓄目标

1. 进入 `储蓄罐` → `新建储蓄罐`
2. 设定目标金额和截止日期
3. 定期向储蓄罐转入资金
4. 实时查看进度百分比

---

## 七、与其他财务管理工具对比

| 特性 | Firefly III | Actual Budget | GnuCash | Mint（已关闭） |
|------|-------------|---------------|---------|----------------|
| 自托管 | ✅ | ✅ | ✅ | ❌ |
| 复式记账 | ✅ | ❌ | ✅ | ❌ |
| 预算管理 | ✅ | ✅（零基预算） | ❌ | ✅ |
| 多币种 | ✅ | ✅ | ✅ | ❌ |
| 储蓄目标 | ✅ | ❌ | ❌ | ❌ |
| 规则引擎 | ✅ | ✅ | ❌ | ❌ |
| 数据导入 | ✅（CSV/OFX） | ✅（OFX/CSV） | ✅（QIF/OFX） | 自动银行同步 |
| 开源 | ✅（AGPL-3.0） | ✅（MIT） | ✅（GPL） | ❌ |
| Web 界面 | ✅ | ✅ | ❌ | ✅ |
| 移动 App | 第三方 | 第三方 | ❌ | ✅ |

---

## 八、生态与扩展

Firefly III 拥有活跃的第三方生态：

- **Firefly III Importer**：官方数据导入工具，支持银行 CSV 自动导入
- **第三方移动 App**：如 "Waterfly III"（Android）、"Firefly III Mobile"
- **API 集成**：完整的 REST API，可与其他系统集成
- **Home Assistant 集成**：在智能家居面板中展示财务数据

---

## 九、总结

Firefly III 是一款将专业会计理念与个人财务管理完美结合的开源工具。它以复式记账为核心，配合预算管理、储蓄目标、规则引擎等功能，帮助用户真正"看清钱的去向"。对于厌倦了 Excel 记账、不愿将财务数据上传云端、又希望获得专业级财务分析的用户而言，Firefly III 是最佳的开源自托管方案。一条 Docker Compose 命令即可部署，数据完全由自己掌控。

---

**相关资源**

- GitHub 仓库：https://github.com/firefly-iii/firefly-iii
- 官方文档：https://docs.firefly-iii.org/
- 在线演示：https://demo.firefly-iii.org/
- 数据导入工具：https://github.com/firefly-iii/data-importer
- 社区讨论：https://github.com/firefly-iii/firefly-iii/discussions
- Mastodon 动态：https://fosstodon.org/@ff3
