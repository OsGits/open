# Jellyfin开源项目详解：自托管媒体服务器部署教程与Emby分叉版Netflix私有化实战指南

## 一、项目概述

**Jellyfin** 是一款免费的开源媒体服务器，用于组织和管理用户的电影、电视剧、音乐、照片和其他媒体内容，并将它们流式传输到各种客户端设备。它是 Emby 项目的社区分支（Fork），在 Emby 3.6 版本闭源后由志愿者团队接手并继续开发。Jellyfin 采用 .NET/C# 编写后端，采用 HTML/JavaScript 编写前端，支持 Docker、Windows、macOS、Linux 多种部署方式，并且完全免费、无广告、无订阅，是替代 Plex、Emby、Kodi 的最佳开源媒体服务器之一。

与 Plex 相比，Jellyfin 没有任何高级功能付费墙：硬件转码、多用户、插件系统、Live TV 等核心功能均可免费使用。项目目前在 GitHub 上拥有超过 34K Stars，最新稳定版本为 10.10.x，配套客户端覆盖 Web、Android、iOS、Android TV、Fire TV、Kodi 等主流设备，是目前自托管媒体服务器领域最受欢迎的开源项目。

- **GitHub 地址**：https://github.com/jellyfin/jellyfin
- **官方网站**：https://jellyfin.org
- **开源协议**：GPL-2.0
- **开发语言**：C# / .NET 8 / JavaScript
- **核心定位**：免费、无广告、自托管的媒体服务器与流媒体平台

### 1.1 与同类产品对比

| 特性 | Jellyfin | Plex | Emby | Kodi |
|------|----------|------|------|------|
| 开源免费 | ✅ | ❌（高级功能收费） | ❌（部分功能订阅） | ✅ |
| 服务端模式 | C/S | C/S | C/S | 本地应用 |
| 硬件转码 | ✅（免费） | ✅（Plex Pass 收费） | ✅（Emby Premiere 收费） | ❌ |
| 多用户 | ✅ | ✅ | ✅ | ❌ |
| 移动端支持 | ✅ | ✅ | ✅ | 有限 |
| 元数据刮削 | ✅ | ✅ | ✅ | ✅ |
| DVR 录像 | ✅（免费） | ✅（Plex Pass） | ✅（Emby Premiere） | ❌ |
| 插件系统 | ✅ | ✅ | ✅ | ✅ |
| 典型适用场景 | 家庭媒体中心、电影库 | 易用家庭影院 | 商业媒体服务 | HTPC 本地播放 |

---

## 二、核心功能模块详解

### 2.1 媒体库管理

Jellyfin 支持多种媒体类型，每种都能自动归类并生成封面、海报、简介：

| 媒体类型 | 文件结构示例 |
|----------|-------------|
| 电影 | `Movies/星际穿越 (2014)/星际穿越 (2014).mp4 |
| 电视剧 | `TV Shows/绝命毒师/Season 01/绝命毒师 S01E01.mkv |
| 音乐 | `Music/周杰伦/叶惠美/01 以父之名.flac |
| 播客 | 通过 RSS URL 订阅 |
| 书籍 | `Books/三体.epub |
| 照片 | `Photos/2024 全家福/IMG_0001.jpg |

### 2.2 元数据刮削（Metadata Scraping）

| 数据源 | 说明 |
|--------|------|
| TheMovieDB（TMDB） | 电影、电视剧的封面、简介、评分 |
| TheTVDB | 电视剧剧集信息 |
| MusicBrainz | 音乐专辑和艺术家 |
| Fanart.tv | 海报、粉丝艺术图、横幅 |
| OpenSubtitles | 字幕自动搜索下载 |
| 本地 NFO | 用户自定义元数据文件 |

### 2.3 硬件转码（Hardware Transcoding）

Jellyfin 支持多种硬件加速方案，可将不兼容的原始格式实时转码为适合播放器的格式：

| 技术 | 厂商 | 环境 |
|------|------|------|
| VA-API | Intel / AMD | Linux |
| NVENC/NVDEC | NVIDIA | Linux / Windows |
| QSV | Intel | Linux / Windows |
| VCE / AMF | AMD | Linux / Windows |
| VideoToolbox | Apple | macOS |

### 2.4 用户与权限

- **多用户**：每位家庭成员可拥有独立账号与观看看好
- **家长控制**：根据内容分级（PG、PG-13、R）屏蔽内容
- **并发流限制**：限制每位用户或全系统并发播放数量
- **播放策略**：禁止下载、禁止远程访问等策略设置

### 2.5 Live TV 与 DVR

Jellyfin 支持 HDHomeRun、SAT>IP、M3U 格式的 IPTV 源，配合 NextPVR、TVHeadend 等后端，可实现：
- 实时电视直播
- 节目表（EPG）
- 定时录像（DVR）

### 2.6 插件系统

| 官方插件 | 用途 |
|----------|------|
| Jellyseerr | 用户请求与管理电影/电视剧（Ombi 替代品） |
| Open Subtitles | 自动搜索并下载字幕 |
| Trakt | 与 Trakt.tv 同步观看进度 |
| Kodi Sync | 与 Kodi 客户端同步 |
| LDAP Auth | LDAP/Active Directory 认证 |
| TMDb Box Sets | TMDB 电影合集 |

---

## 三、技术架构与实现原理

### 3.1 整体架构

```
[客户端（Web / Android / iOS / Kodi）]
               │
               │ HTTPS / DLNA / Cast
               ▼
[Jellyfin Server（.NET 8 / ASP.NET Core）]
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
[SQLite]   [FFmpeg]   [插件 Host]
```

### 3.2 核心组件

| 组件 | 说明 |
|------|------|
| Jellyfin Server | .NET 8 / ASP.NET Core 编写，核心服务，默认 8096 端口 |
| Jellyfin Web | 内置 Web 客户端，随服务端同进程提供 |
| FFmpeg | 处理转码、解码、编码，所有流媒体处理引擎 |
| SQLite | 默认数据库，存储用户、媒体、插件配置 |
| 插件 Host | 承载 C# 插件，独立进程 |

### 3.3 FFmpeg 转码流程

1. 客户端请求播放指定音视频文件
2. Server 检查客户端能力（编码/分辨率/码率）
3. Server 调用 FFmpeg 进行转码
4. FFmpeg 使用硬件编码器（如 h264_nvenc / h264_vaapi）
5. Server 将转码后的流分段通过 HTTP/HTTPS 发送到客户端

### 3.4 文件扫描与数据库

- Jellyfin 会定时扫描媒体库目录
- 为每个文件匹配 TMDB 数据并提取元数据
- 元数据和播放状态写入 SQLite（路径：`/var/lib/jellyfin/data/jellyfin.db`）

---

## 四、快速上手：Docker 部署实战

### 4.1 官方镜像选择

| 镜像 | 适用场景 |
|------|----------|
| `jellyfin/jellyfin:latest | 官方标准镜像 |
| `lscr.io/linuxserver/jellyfin` | Linuxserver.io，含权限管理（推荐） |
| `nyanmisaka/jellyfin` | 第三方，含第三方补丁与 FFmpeg |

### 4.2 Docker CLI 基础部署

```bash
docker run -d \
  --name=jellyfin \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Shanghai \
  -p 8096:8096 \
  -p 8920:8920 \
  -p 7359:7359/udp \
  -p 1900:1900/udp \
  -v ./jellyfin-config:/config \
  -v ./jellyfin-cache:/cache \
  -v /data/media/movies:/data/movies \
  -v /data/media/tvshows:/data/tvshows \
  -v /data/media/music:/data/music \
  --restart=unless-stopped \
  lscr.io/linuxserver/jellyfin:latest
```

访问 `http://<主机IP>:8096` 进入初始化界面。

### 4.3 Docker Compose + NVIDIA GPU 加速（推荐生产环境）

```yaml
version: "3.8"

services:
  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      - JELLYFIN_PublishedServerUrl=https://jellyfin.example.com
      # NVIDIA 驱动相关（可选）
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,video,utility
    volumes:
      - ./config:/config
      - ./cache:/cache
      - /data/media/movies:/data/movies:ro
      - /data/media/tvshows:/data/tvshows:ro
      - /data/media/music:/data/music:ro
      - /data/media/photos:/data/photos:ro
    ports:
      - "8096:8096"        # HTTP Web UI
      - "8920:8920"      # HTTPS Web UI
      - "7359:7359/udp"  # 客户端自动发现
      - "1900:1900/udp"   # SSDP/DLNA
    devices:
      # Intel VA-API 显卡直通（如果是 Intel 核显）
      - /dev/dri/renderD128:/dev/dri/renderD128
      - /dev/dri/card0:/dev/dri/card0
    runtime: nvidia          # NVIDIA GPU 加速（可选）
    restart: unless-stopped
```

### 4.4 初始化向导

1. 创建管理员账户
2. 添加媒体库（电影、电视剧、音乐等）
3. 设置首选语言为 `zh-CN`，选择 `TheMovieDB` / `TheTVDB` 作为元数据源
4. 勾选 "启用远程访问"
5. 完成后进入主界面

### 4.5 硬件加速配置

进入 **控制台 → 播放 → 硬件加速**：

| 显卡类型 | 加速方式 |
|----------|----------|
| Intel 核显（10/11/12代） | 选择 "Video Acceleration API（VA-API） |
| NVIDIA GTX/RTX 显卡 | 选择 "NVIDIA NVENC" |
| AMD APU / Radeon | 选择 "AMD AMF" 或 "VA-API" |

勾选后保存并重启容器生效。

---

## 五、从源码编译与开发环境

### 5.1 Linux 环境构建

```bash
# 1. 安装 .NET 8 SDK
wget https://dot.net/v1/dotnet-install.sh
bash dotnet-install.sh --channel 8.0
export PATH="$HOME/.dotnet:$PATH"

# 2. 安装 Node.js 18+ 和 FFmpeg
sudo apt install -y nodejs npm ffmpeg

# 3. 克隆仓库
git clone https://github.com/jellyfin/jellyfin.git
cd jellyfin
git submodule update --init --recursive

# 4. 构建
dotnet publish Jellyfin.Server --configuration Release
./.build/jellyfin --version
```

### 5.2 构建 Docker 镜像

```bash
docker build -f Dockerfile -t jellyfin:local .
docker run -d -p 8096:8096 jellyfin:local
```

### 5.3 插件开发

```bash
# 克隆插件模板
dotnet new -i MediaBrowser.Plugin.Templates
dotnet new jellyfinplugin -n MyPlugin
cd MyPlugin
dotnet build -c Release
# 将输出的 DLL 放入 Jellyfin 的 plugins 目录
```

---

## 六、API 接口与自动化集成

### 6.1 REST API 调用

Jellyfin 提供完整 REST API，Web UI 本身就是通过 API 驱动的：

```bash
# 登录获取 token
curl -X POST http://127.0.0.1:8096/Users/authenticatebyname \
  -H "Content-Type: application/json" \
  -d '{"Username":"admin","Pw":"your-password"}'

# 获取所有电影
curl -H "X-Emby-Token: <YOUR-API-TOKEN>" \
  "http://127.0.0.1:8096/Items?Recursive=true&IncludeItemTypes=Movie"

# 刷新媒体库
curl -X POST -H "X-Emby-Token: <YOUR-API-TOKEN>" \
  "http://127.0.0.1:8096/Library/Refresh"
```

### 6.2 与 Jellyseerr 集成（用户请求管理）

```yaml
services:
  jellyseerr:
    image: fallenbagel/jellyseerr:latest
    container_name: jellyseerr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
    ports:
      - "5055:5055"
    volumes:
      - ./jellyseerr:/app/config
    restart: unless-stopped
```

在 Jellyseerr 中配置 Jellyfin 服务器地址 + API Key，用户可登录请求新的电影和电视剧。

### 6.3 常用 API 端点速查

| 端点 | 说明 |
|------|------|
| `/Users/authenticatebyname` | POST：用户名密码登录 |
| `/Items` | GET：浏览媒体库 |
| `/Items/{id}/PlaybackInfo` | GET：获取播放信息 |
| `/Items/{id}/ThemeSong` | GET：获取主题曲 |
| `/ScheduledTasks` | GET：获取任务列表 |
| `/Library/Refresh` | POST：刷新媒体库 |

---

## 七、性能优化与大规模部署

### 7.1 转码性能调优

| 设置项 | 推荐值 | 说明 |
|--------|--------|------|
| 硬件加速 | 启用 GPU 加速 | 显著降低 CPU 占用 |
| 转码线程数 | `0`（自动） 或 CPU 核心数 | 限制并发转码任务 |
| 转码临时目录 | 使用 SSD 或 RAM Disk | 提升 I/O 性能 |
| 缓存策略 | `EnableThrottling = true` | 限制非活动流的转码 |

### 7.2 媒体库性能

- **分离 `/cache` 目录到独立 SSD 分区或 tmpfs**
- **使用网络存储时用 NFS v4.2 / SMB 3.0**
- **启用媒体库扫描节流**：控制台 → Scheduled Tasks 调整扫描频率
- **启用实时监控**：对大目录关闭 "实时监控"，改用定时扫描

### 7.3 并发流限制

进入 **控制台 → 用户 → 编辑用户 → 媒体播放**：
- `最大并发流数`：设置为 `0` 不限或根据硬件性能设定（如 3-5）
- `最大比特率`：根据上行带宽设定

### 7.4 Nginx 反代 + HTTPS

```nginx
server {
    listen 443 ssl http2;
    server_name jellyfin.example.com;

    ssl_certificate     /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    client_max_body_size 0;

    location / {
        proxy_pass http://127.0.0.1:8096;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 转码临时文件需要更大的缓冲区
    location /Videos {
        proxy_pass http://127.0.0.1:8096;
        proxy_buffering off;
    }
}
```

---

## 八、常见问题与故障排查

### 8.1 无法识别电影或海报缺失

- 检查文件名是否符合命名规范 `电影名 (年份)`
- 进入电影详情 → "识别" → 手动搜索 TMDB
- 查看 `/config/log` 目录下日志确认 TMDB 访问是否失败
- 如无法访问 TMDB，需配置代理或使用镜像站点

### 8.2 硬件加速不生效

```bash
# 检查 NVIDIA 显卡
nvidia-smi

# 检查 Intel VA-API 设备
ls -la /dev/dri/
vainfo --display drm --device /dev/dri/renderD128
```

- 确保容器内 `/dev/dri` 已映射
- 确保 PUID/PGID 用户在 `render` 组：`sudo usermod -aG render 1000`

### 8.3 转码失败 / 播放卡顿

- 检查 `/cache/transcodes` 目录磁盘空间
- 检查 FFmpeg 日志：`tail -f /config/log/log_*.log | grep ffmpeg`
- 降低码率 / 分辨率或增加并发限制

### 8.4 元数据刮削失败（国内网络问题）

- 在 **控制台 → 插件** 安装 "Chinese Subtitles" 插件
- 手动指定 TMDB 镜像站点：https://api.themoviedb.org
- 使用代理服务器访问国外站点

### 8.5 数据库迁移与备份

```bash
# 备份数据库与配置
cp -r /path/to/jellyfin/config /mnt/backup/jellyfin-$(date +%Y%m%d)

# 备份用户观看进度（watchdata.db）
sqlite3 /config/data/jellyfin.db ".backup /backup/watchdata-$(date +%Y%m%d).db"
```

---

## 九、社区生态与学习资源

| 项目 | 用途 | 地址 |
|------|------|------|
| 官方文档 | 完整部署与配置手册 | https://jellyfin.org/docs/ |
| Jellyfin Forum | 官方论坛 | https://forum.jellyfin.org/ |
| Jellyfin Reddit | Reddit 社区 | https://reddit.com/r/jellyfin |
| 客户端下载 | 各平台客户端 | https://jellyfin.org/clients/ |
| Jellyfin Media Player | 桌面客户端（基于 mpv） | https://github.com/jellyfin/jellyfin-media-player |
| Jellyfin Android TV | TV 客户端 | Google Play |
| Infuse | iOS/Apple TV 推荐客户端 | https://firecore.com/infuse |
| Jellyseerr | 用户请求系统 | https://github.com/Fallenbagel/jellyseerr |
| Jellyfin Plugin Repository | 第三方插件库 | https://repo.jellyfin.org/ |

---

## 十、使用场景与案例参考

### 10.1 家庭影院

在 NAS 上部署 Jellyfin + 本地千兆局域网 + Apple TV 4K（Infuse 客户端），全家人均可 4K HDR 流畅播放。

### 10.2 远程访问家庭媒体

通过公网访问：`https://jellyfin.家庭域名`，出差在外也能看家里的电影。

### 10.3 多人共享媒体库

多位用户各有观看进度和收藏，互不干扰。

### 10.4 与 Plex / Emby / Kodi 的选择

| 工具 | 推荐场景 |
|------|----------|
| Jellyfin | 免费自托管、无订阅、社区驱动 |
| Plex | 追求极致易用、有付费高级功能 |
| Emby | 愿意订阅、商业支持 |
| Kodi | 本地 HTPC 单设备播放 |

---

## 总结

Jellyfin 作为 Emby 的开源分叉，凭借完全免费、功能完善的媒体服务器方案，在自托管社区获得了极高人气。它拥有 Plex/Emby 商业产品的绝大多数核心功能，且无任何订阅费用。对于拥有本地媒体库的用户而言，搭配 Docker 能够在几分钟内部署一套完整的家庭媒体中心；配合硬件加速和多客户端，4K HDR、多用户并发观看都可以流畅实现。推荐生产部署使用 Linuxserver.io 镜像 + NVENC/VA-API 硬件加速 + Nginx 反代 + Jellyseerr 管理用户请求，即可构建一个真正媲美 Netflix 的私有化流媒体平台。
