# Stirling-PDF - 开源PDF工具包,Java和SpringBoot开发,替代AdobeAcrobat,Docker自托管,OCR与文档转换

## 项目概述

Stirling-PDF 是一个功能强大的自托管 PDF 工具包，使用 Java/Spring Boot 构建，提供 50+ 种 PDF 操作功能，完全替代 Adobe Acrobat 和 ILovePDF、SmallPDF 等在线服务。项目采用 MIT 许可证（核心功能），支持通过 Docker 快速部署，所有文档处理都在本地服务器完成，确保数据隐私安全。Stirling-PDF 提供合并、拆分、压缩、旋转、OCR 识别、添加密码、签名、格式转换等企业级 PDF 功能，同时支持无文件大小限制的文档处理。

## 核心特性

### PDF 操作功能

| 类别 | 功能 |
|------|------|
| **组织** | 合并、拆分、删除页面、提取页面、重新排序、旋转、缩放 |
| **转换** | PDF→Word、PDF→HTML、PDF→XML、Word/Excel/PPT→PDF、HTML→PDF、Markdown→PDF |
| **安全** | 添加/删除密码、添加水印、内容编辑、签名 PDF |
| **优化** | 压缩、去灰度、删除批注 |
| **OCR** | 扫描件识别、文本提取 |
| **高级** | PDF 比较、修复、扁平化、添加页码、添加图片 |

### 隐私与安全

- **本地处理**：文档完全在自有服务器处理，不上传到第三方
- **无追踪**：不收集用户数据
- **无使用限制**：无文件大小限制，无使用次数限制
- **自托管**：完全控制数据

### 部署灵活性

- **Docker 部署**：一行命令快速部署
- **多版本选择**：Standard（标准）、Fat（完整）、Ultra-Lite（轻量）
- **ARM 支持**：支持树莓派等 ARM 设备
- **API 支持**：提供 REST API，可集成到自动化流程

### OCR 能力

- **内置 Tesseract OCR**：扫描 PDF 自动识别
- **多语言支持**：支持 100+ 种语言识别
- **可搜索 PDF**：将扫描件转换为可搜索的 PDF
- **文本提取**：从 PDF 中提取文本内容

### 文档转换

- **Office 转换**：支持 DOCX、XLSX、PPTX 转 PDF
- **反向转换**：PDF 转 Word、Excel、PowerPoint
- **格式优化**：转换时自动优化排版

## 技术架构

### 架构设计

```
┌──────────────────────────────────────────────────────────┐
│                  Stirling-PDF 架构                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────┐     │
│  │              Web 界面 / API                      │     │
│  ├─────────────────────────────────────────────────┤     │
│  │                                                  │     │
│  │  Spring Boot 应用                                │     │
│  │                                                  │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐   │     │
│  │  │Apache PDF│ │ Tesseract│ │ LibreOffice  │   │     │
│  │  │   Box    │ │   OCR    │ │   转换引擎    │   │     │
│  │  └──────────┘ └──────────┘ └──────────────┘   │     │
│  └─────────────────────────────────────────────────┘     │
│                          │                              │
│  ┌─────────────────────────────────────────────────┐     │
│  │           本地文件系统存储                       │     │
│  └─────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

### 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | Spring Boot (Java 21+) |
| PDF 处理 | Apache PDFBox |
| OCR | Tesseract |
| 文档转换 | LibreOffice |
| 前端 | React + TypeScript + Vite |
| UI 库 | Mantine UI |
| 国际化 | i18next |

### 版本对比

| 版本 | 标签 | 特点 | 适用场景 |
|------|------|------|---------|
| Standard | latest | 平衡功能和大小 | 大多数用户 |
| Fat | latest-fat | 完整字体和工具 | 高质量转换、全格式支持 |
| Ultra-Lite | latest-ultra-lite | 核心功能 | 资源受限设备 |

## 部署教程

### Docker 快速部署

#### 基础部署（无认证）

```bash
docker run -d \
  --name stirling-pdf \
  -p 8080:8080 \
  -v ./stirling-data:/configs \
  stirlingtools/stirling-pdf:latest
```

#### 创建 docker-compose.yml

```yaml
services:
  stirling-pdf:
    image: stirlingtools/stirling-pdf:latest
    container_name: stirling-pdf
    ports:
      - '8080:8080'
    volumes:
      - ./stirling-data:/configs
    restart: unless-stopped
```

```bash
# 启动服务
docker compose up -d

# 访问应用
# http://localhost:8080
```

### 完整功能部署（含 OCR 和文档转换）

```yaml
services:
  stirling-pdf:
    image: stirlingtools/stirling-pdf:latest
    container_name: stirling-pdf
    ports:
      - '8080:8080'
    volumes:
      # OCR 语言文件
      - ./stirling-data/tessdata:/usr/share/tessdata
      # 配置和数据库
      - ./stirling-data/configs:/configs
      # 日志
      - ./stirling-data/logs:/logs
      # 自定义文件
      - ./stirling-data/customFiles:/customFiles
      # 自动化配置
      - ./stirling-data/pipeline:/pipeline
    environment:
      # 禁用认证（生产环境建议启用）
      - SECURITY_ENABLELOGIN=false
      # 界面语言
      - LANGS=en_GB
      # 系统语言
      - SYSTEM_DEFAULTLOCALE=en-GB
    restart: unless-stopped
```

```bash
# 创建目录
mkdir -p stirling-data/{tessdata,configs,logs,customFiles,pipeline}

# 下载 OCR 语言包（英文）
wget -O stirling-data/tessdata/eng.traineddata \
  https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# 下载中文语言包（可选）
wget -O stirling-data/tessdata/chi_sim.traineddata \
  https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata

# 启动服务
docker compose up -d
```

### 启用用户认证

```yaml
services:
  stirling-pdf:
    image: stirlingtools/stirling-pdf:latest
    environment:
      - SECURITY_ENABLELOGIN=true
      # 用户名密码
      - SECURITY_DEFAULTUsername=admin
      - SECURITY_DEFAULTPASSWORD=your-secure-password
```

首次访问后建议立即修改默认密码。

### 树莓派/低配设备部署（Ultra-Lite）

```yaml
services:
  stirling-pdf:
    image: stirlingtools/stirling-pdf:latest-ultra-lite
    ports:
      - '8080:8080'
    volumes:
      - ./stirling-data:/configs
    restart: unless-stopped
```

## 高级配置

### 界面语言

支持 30+ 种语言：

```yaml
environment:
  - LANGS=zh_CN    # 简体中文
  # 其他选项: en_GB, fr_FR, de_DE, es_ES, ja_JP, ko_KR, etc.
```

### HTTPS 配置

使用 Caddy 反向代理（推荐）：

```yaml
# docker-compose.yml
services:
  stirling-pdf:
    image: stirlingtools/stirling-pdf:latest
    volumes:
      - ./stirling-data:/configs
    restart: unless-stopped

  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - ./caddy-data:/data
    depends_on:
      - stirling-pdf
```

创建 `Caddyfile`：

```
pdf.yourdomain.com {
    reverse_proxy stirling-pdf:8080
}
```

```bash
docker compose up -d
```

### 资源限制

```yaml
services:
  stirling-pdf:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
        reservations:
          memory: 2G
          cpus: '1.0'
```

### 自定义 Logo

```bash
# 复制自定义 logo 到 customFiles 目录
cp your-logo.png ./stirling-data/customFiles/logo.png

# 配置
```

## API 使用

Stirling-PDF 提供 REST API，支持自动化工作流：

### 合并 PDF

```bash
curl -X POST "http://localhost:8080/api/v1/general/merge-pdfs" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document1.pdf" \
  -F "file=@document2.pdf" \
  -o merged.pdf
```

### 压缩 PDF

```bash
curl -X POST "http://localhost:8080/api/v1/security/compress-pdfs" \
  -F "file=@large.pdf" \
  -o compressed.pdf
```

### OCR 识别

```bash
curl -X POST "http://localhost:8080/api/v1/specific/ocr-pdf" \
  -F "file=@scanned.pdf" \
  -F "languages=eng" \
  -o searchable.pdf
```

### 添加水印

```bash
curl -X POST "http://localhost:8080/api/v1/security/watermark-pdf" \
  -F "fileInput=@document.pdf" \
  -F "watermarkType=text" \
  -F "text=CONFIDENTIAL" \
  -F "opacity=0.3" \
  -o watermarked.pdf
```

### 完整 API 文档

访问 `http://localhost:8080/swagger-ui/index.html` 查看完整 API 文档。

## 流水线自动化

Stirling-PDF 支持创建自动化流水线，批量处理 PDF：

### 创建流水线

```json
{
  "name": "OCR and Compress",
  "operations": [
    {
      "operation": "ocr",
      "languages": ["eng", "chi_sim"]
    },
    {
      "operation": "compress"
    }
  ],
  "outputFormat": "pdf"
}
```

### 执行流水线

```bash
curl -X POST "http://localhost:8080/api/v1/pipeline/run" \
  -H "Content-Type: application/json" \
  -d @pipeline.json \
  -F "files=@*.pdf" \
  -o processed.zip
```

## 备份与恢复

### 备份配置

```bash
tar -czf stirling-backup-$(date +%Y%m%d).tar.gz ./stirling-data/
```

### 恢复配置

```bash
tar -xzf stirling-backup-20240101.tar.gz
docker compose down
docker compose up -d
```

## 更新 Stirling-PDF

### Docker Compose 方式

```bash
# 拉取最新镜像
docker compose pull

# 重启服务
docker compose up -d

# 查看日志
docker compose logs -f stirling-pdf
```

### Docker Run 方式

```bash
# 停止并删除旧容器
docker stop stirling-pdf
docker rm stirling-pdf

# 拉取最新镜像
docker pull stirlingtools/stirling-pdf:latest

# 使用原始命令重新运行
docker run -d \
  --name stirling-pdf \
  -p 8080:8080 \
  -v ./stirling-data:/configs \
  stirlingtools/stirling-pdf:latest
```

数据会保留在 `stirling-data` 目录中。

## 常见问题

### Q: Stirling-PDF 是否免费？

A: 核心功能采用 MIT 许可证免费使用。部分高级功能（外部数据库、Google Drive 集成、SSO）需要付费计划。

### Q: 支持哪些语言？

A: 支持 30+ 种界面语言，OCR 支持 100+ 种语言。

### Q: 是否有文件大小限制？

A: 自托管版本没有文件大小限制，可以处理超大 PDF。

### Q: 是否支持批量处理？

A: 是的，支持通过 API 和流水线进行批量处理。

### Q: 如何报告问题或贡献代码？

A: 访问 [GitHub Issues](https://github.com/Stirling-Tools/Stirling-PDF/issues) 报告问题，或提交 Pull Request 贡献代码。

## 与同类服务对比

| 特性 | Stirling-PDF | Adobe Acrobat | ILovePDF | SmallPDF |
|------|-------------|--------------|---------|---------|
| 费用 | 免费开源 | $155/年 | 免费/付费 | 免费/付费 |
| 自托管 | 支持 | 不支持 | 不支持 | 不支持 |
| 隐私 | 极高 | 低 | 低 | 低 |
| 功能数 | 50+ | 100+ | 30+ | 20+ |
| API | 支持 | 支持 | 不支持 | 不支持 |
| 无限制 | 是 | 是 | 有限制 | 有限制 |

## 项目资源

- **GitHub**: https://github.com/Stirling-Tools/Stirling-PDF
- **官网**: https://stirlingtools.com/
- **文档**: https://docs.stirlingpdf.com/
- **Docker Hub**: https://hub.docker.com/r/stirlingtools/stirling-pdf

## 适用场景

1. **企业文档处理**：自动化 PDF 转换、压缩、合并工作流
2. **律师事务所**：处理敏感法律文档，不上传第三方
3. **学术研究**：批量 OCR 识别、数据提取
4. **个人使用**：替代在线 PDF 工具，保护隐私
5. **开发者集成**：通过 API 集成到现有系统

---

*最后更新：2026-06-21*
