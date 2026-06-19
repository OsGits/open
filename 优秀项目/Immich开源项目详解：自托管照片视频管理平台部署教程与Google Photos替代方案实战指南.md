---
title: Immich开源项目详解：自托管照片视频管理平台部署教程与Google Photos替代方案实战指南
id: 019ed93f-917f-75be-b490-0190a6898597
date: 2026-06-18 13:41:53
auther: loveos
cover: /upload/1-iQGE.png
excerpt: 开源协议：AGPL-3.0 GitHub Stars：75K+ 核心定位：高性能自托管照片和视频管理解决方案，Google Photos的最佳开源替代品 一、项目概述 Immich 是一款高性能的自托管照片和视频管理平台，专为希望摆脱Google Photos等云服务、将珍贵影像数据掌握在自己手中的
permalink: /2026/immich---kai-yuan-zi-tuo-guan-zhao-pian-shi-pin-guan-li-ping-tai-gao-xing-neng-si-you-xiang-ce-ren-lian-shi-bie-yu-aisou-suo-ti-dai-google-photos
categories:
 - Github
tags: 
 - Project.Recommendation
 - github
 - docker
 - zi-tuo-guan-xiang-ce
 - zhao-pian-guan-li
 - airen-lian-shi-bie
 - google-photos
---

> **开源协议**：AGPL-3.0
> **GitHub Stars**：75K+
> **核心定位**：高性能自托管照片和视频管理解决方案，Google Photos的最佳开源替代品

---

<hyperlink-card href="https://github.com/immich-app/immich" target="_blank" theme="regular"></hyperlink-card>


## 一、项目概述

**Immich** 是一款高性能的自托管照片和视频管理平台，专为希望摆脱Google Photos等云服务、将珍贵影像数据掌握在自己手中的用户而设计。它提供手机自动备份、智能人脸识别、地图视图、共享相册等核心功能，体验与Google Photos几乎一致，但数据完全存储在你自己的服务器上。

Immich由TypeScript（服务端+Web）和Dart（移动端）构建，支持iOS、Android、Web三端，具备机器学习驱动的智能搜索能力。项目社区活跃，更新频繁，已被全球数万家庭和摄影爱好者采用，是目前开源相册领域最成熟、功能最完善的选择。

---

## 二、核心特性解读

### 2.1 多端自动备份


| 功能                  | 移动端(iOS/Android) | Web端 |
| --------------------- | ------------------- | ----- |
| 照片/视频上传与查看   | ✅                  | ✅    |
| 打开App时自动备份     | ✅                  | N/A   |
| 后台自动备份          | ✅                  | N/A   |
| 选择性相册备份        | ✅                  | N/A   |
| 下载到本地设备        | ✅                  | ✅    |
| 离线支持              | ✅                  | ❌    |
| LivePhoto/MotionPhoto | ✅                  | ✅    |
| 360度全景图           | ❌                  | ✅    |
| RAW格式支持           | ✅                  | ✅    |

### 2.2 AI智能搜索

Immich内置机器学习能力，支持多维度智能搜索：

- **人脸识别与聚类**：自动识别照片中的人物并分组
- **物体识别**：搜索"猫"、"海滩"、"蛋糕"等关键词
- **CLIP语义搜索**：基于自然语言描述搜索照片（如"去年夏天在海边的合影"）
- **EXIF元数据搜索**：按相机型号、镜头、光圈、快门速度等筛选
- **地理位置搜索**：在地图上按区域查找照片

### 2.3 相册与分享

- **个人相册**：创建自定义相册分类管理
- **共享相册**：与家人朋友共享特定相册
- **伙伴共享**：与伴侣互相共享照片，自动合并时间线
- **公开分享**：生成公开链接分享照片/相册
- **收藏与归档**：标记收藏照片，归档不需要的内容
- **文件夹视图**：按原始文件夹结构浏览

### 2.4 地图与时间线

- **全局地图**：在交互式地图上查看所有带GPS信息的照片
- **时间线视图**：按时间顺序浏览照片，支持可拖拽滚动条快速跳转
- **回忆功能**："X年前的今天"自动推送回忆照片

### 2.5 多用户支持

- **多用户隔离**：每个用户拥有独立的照片库和账户
- **管理员功能**：通过Web端管理用户、监控存储使用
- **OAuth支持**：支持第三方OAuth认证登录
- **API Keys**：支持通过API密钥进行程序化访问

### 2.6 用户自定义存储结构

Immich允许用户自定义照片在服务器上的存储目录结构，例如：

```
/photos/2024/01/01/
/photos/2024/旅行/日本/
```

---

## 三、系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      客户端层                                │
│     (iOS App / Android App / Web界面 / CLI / API)           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Immich Server (TypeScript)                │
│     (REST API / WebSocket / 资源管理 / 用户管理)            │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐    ┌────────▼────────┐   ┌───────▼──────┐
│  PostgreSQL  │    │     Redis       │   │  ML引擎       │
│  (元数据存储) │    │  (缓存/队列)     │   │ (人脸/CLIP)  │
└──────────────┘    └─────────────────┘   └──────────────┘
```

---

## 四、部署指南

### 4.1 环境要求


| 资源类型       | 最低配置              | 推荐配置（大量照片） |
| -------------- | --------------------- | -------------------- |
| CPU            | 2核                   | 4核+                 |
| 内存           | 2GB                   | 8GB+                 |
| 磁盘           | 10GB（系统）+照片存储 | SSD + NAS            |
| Docker         | >= 20.10              | 最新版               |
| Docker Compose | >= v2.0               | 最新版               |

### 4.2 一键安装脚本

```bash
# 下载并执行安装脚本
curl -fsSL https://raw.githubusercontent.com/immich-app/immich/main/install.sh | bash
```

### 4.3 Docker Compose部署（推荐）

**步骤1：下载配置文件**

```bash
mkdir immich-app && cd immich-app

# 下载docker-compose.yml和.env文件
wget https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml
wget https://github.com/immich-app/immich/releases/latest/download/.env
```

**步骤2：修改环境变量**

编辑 `.env` 文件：

```bash
# 上传目录（存放照片的实际位置）
UPLOAD_LOCATION=/path/to/your/photos

# 数据库配置
DB_HOSTNAME=immich_postgres
DB_USERNAME=immich
DB_PASSWORD=your_secure_password
DB_DATABASE_NAME=immich

# Redis配置
REDIS_HOSTNAME=immich_redis

# 机器学习配置（可选）
MACHINE_LEARNING_HOST=immich_machine_learning
MACHINE_LEARNING_PORT=3003
```

**步骤3：启动服务**

```bash
docker compose up -d
```

**步骤4：验证启动**

```bash
docker compose ps
docker compose logs -f immich_server
```

**步骤5：访问Web界面**

打开浏览器访问 `http://localhost:2283`，完成初始管理员账户注册。

### 4.4 硬件转码加速（可选）

如果需要视频转码加速，可配置硬件加速：

```bash
# 在.env中添加
HWACCEL=vaapi        # Intel核显
# HWACCEL=nvenc       # NVIDIA显卡
# HWACCEL=qsv         # Intel Quick Sync
```

### 4.5 外部存储挂载

将NAS或外部硬盘挂载到Immich：

```yaml
# docker-compose.yml中添加volume映射
services:
  immich_server:
    volumes:
      - /mnt/nas/photos:/usr/src/app/upload  # NAS照片目录
      - /mnt/external:/external-media         # 外部硬盘
```

---

## 五、快速上手实战

### 5.1 注册管理员账户

1. 打开 `http://localhost:2283`
2. 注册管理员账户（第一个注册的用户自动成为管理员）
3. 设置管理员邮箱和密码

### 5.2 手机端配置自动备份

1. 在App Store/Google Play搜索 **Immich** 下载
2. 打开App，输入服务器地址：`http://你的服务器IP:2283`
3. 使用管理员账户登录
4. 进入 **设置 → 备份**
5. 开启 **自动备份**
6. 选择要备份的相册
7. 设置备份条件（WiFi下、充电时等）

### 5.3 上传已有照片

**方式一：手机App上传**

- 打开Immich App → 选择照片 → 上传

**方式二：Web端上传**

- 打开Web界面 → 点击上传按钮 → 选择文件

**方式三：命令行批量导入**

```bash
# 使用Immich CLI批量导入
docker exec -it immich_server immich upload /path/to/photos
```

### 5.4 创建共享相册

1. 在Web端或App中点击 **相册 → 创建相册**
2. 选择要添加的照片
3. 点击 **分享 → 共享相册**
4. 邀请其他用户或生成分享链接

### 5.5 使用智能搜索

- **按人物搜索**：点击人脸图标，选择人物查看所有相关照片
- **按地点搜索**：在地图上点击区域查看照片
- **按关键词搜索**：搜索"海滩"、"猫"、"生日"等
- **按EXIF搜索**：搜索相机型号"iPhone 15 Pro"

### 5.6 配置伙伴共享

1. 进入 **设置 → 伙伴共享**
2. 输入伙伴的邮箱地址
3. 伙伴接受后，双方照片自动合并到时间线
4. 适合情侣/家庭成员共享回忆

### 5.7 设置公开分享

1. 选择照片或相册
2. 点击 **分享 → 生成公开链接**
3. 设置访问密码和过期时间
4. 分享链接给朋友查看

---

## 六、数据备份策略

Immich官方强烈建议遵循 **3-2-1备份原则**：


| 备份层级    | 说明           | 推荐方案                    |
| ----------- | -------------- | --------------------------- |
| **3份数据** | 原始 + 2份备份 | Immich + NAS + 云存储       |
| **2种介质** | 不同存储类型   | 本地SSD + 外部硬盘          |
| **1份异地** | 异地容灾       | Backblaze B2 / S3 / 异地NAS |

```bash
# 使用rsync定期备份Immich数据
rsync -avz /path/to/immich/upload/ /path/to/backup/nas/immich/
```

---

## 七、应用场景


| 场景              | 解决方案                     | 价值                 |
| ----------------- | ---------------------------- | -------------------- |
| 家庭照片管理      | 全家手机自动备份到家庭服务器 | 永久保存家庭回忆     |
| 摄影师作品管理    | RAW格式支持+EXIF元数据查看   | 专业级照片管理       |
| 隐私保护          | 数据完全自托管，不上传云端   | 满足GDPR/隐私需求    |
| 多人共享          | 伙伴共享+共享相册            | 家庭成员互相查看照片 |
| 旅行记录          | 地图视图+时间线+回忆功能     | 回顾旅行足迹         |
| 替代Google Photos | 功能对标Google Photos        | 省去云存储订阅费用   |

---

## 八、社区与生态

- **官方网站**：[https://immich.app](https://immich.app)
- **官方文档**：[https://docs.immich.app](https://docs.immich.app)
- **在线Demo**：[https://demo.immich.app](https://demo.immich.app)（账号：demo@immich.app / demo）
- **安装指南**：[https://docs.immich.app/install/requirements](https://docs.immich.app/install/requirements)
- **功能路线图**：[https://immich.app/roadmap](https://immich.app/roadmap)
- **赞助支持**：[https://buy.immich.app](https://buy.immich.app)
- **周边商店**：[https://immich.store](https://immich.store)

---

## 九、总结

Immich作为GitHub上75K+ Stars的开源自托管照片视频管理平台，凭借其**高性能自动备份、AI智能搜索、人脸识别、地图视图、多用户支持、Google Photos级体验**六大核心优势，正在成为家庭用户和摄影爱好者替代Google Photos的首选开源方案。

无论是希望保护隐私的家庭用户，还是需要管理大量RAW格式照片的专业摄影师，Immich都提供了成熟且功能完善的解决方案。通过简单的Docker Compose部署，你可以在30分钟内拥有一个属于自己的照片视频管理系统。

> **立即体验**：访问 [https://github.com/immich-app/immich](https://github.com/immich-app/immich) 获取源码，或执行 `curl -fsSL https://raw.githubusercontent.com/immich-app/immich/main/install.sh | bash` 一键安装。
