# Syncthing开源项目详解：P2P文件同步工具部署教程与去中心化文件分享实战指南

## 一、项目概述

**Syncthing** 是一款开源的对等（P2P）文件同步工具，无需中心服务器即可在多台设备之间保持文件夹同步。它由 Jakob Borg 于 2013 年创建，采用 Go 语言开发，支持 Windows、macOS、Linux、FreeBSD、Solaris、Android 等几乎所有主流平台。Syncthing 的核心设计理念是安全、隐私与去中心化，所有数据传输均采用端到端加密（TLS 1.3），用户数据完全掌握在自己手中，是 Dropbox、Resilio Sync、Nextcloud 等集中式云存储服务的极佳开源替代方案。

与传统云同步不同，Syncthing 不依赖任何中央服务器来存储或转发你的文件。设备之间通过各自的设备 ID 互相发现并建立连接，直接点对点传输数据。项目目前在 GitHub 上拥有超过 62K Stars，最新稳定版本为 v1.27.x，是自托管社区中最受推崇的文件同步工具之一。

- **GitHub 地址**：https://github.com/syncthing/syncthing
- **官方网站**：https://syncthing.net
- **开源协议**：MPL-2.0（Mozilla Public License 2.0）
- **开发语言**：Go
- **核心定位**：去中心化、端到端加密的跨平台 P2P 文件同步引擎

### 1.1 与同类产品对比

| 特性 | Syncthing | Dropbox | Resilio Sync | Nextcloud | rsync |
|------|-----------|---------|--------------|-----------|-------|
| 中心服务器 | 无 | 有 | 可选 | 有 | 无（单向） |
| 端到端加密 | ✅ | 部分（客户端需信任服务端） | ✅ | 部分 | ❌ |
| 跨平台 | ✅ | ✅ | ✅ | ✅ | 类 Unix |
| 文件版本 | ✅ 可配置 | ✅ | ✅ | ✅ | 无 |
| 冲突处理 | ✅ 自动 + 手动 | ✅ | ✅ | ✅ | 覆盖 |
| 选择性同步 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P2P 直连 | ✅ | ❌ | ✅ | ❌ | ❌ |
| 开源免费 | ✅ | ❌ | ❌ 商业版收费 | ✅ | ✅ |
| 典型适用场景 | 跨设备私有同步、多节点备份 | 个人云盘、团队协作 | 企业 P2P 同步 | 自托管网盘 | 脚本化单向同步 |

---

## 二、核心功能模块详解

### 2.1 P2P 点对点同步

Syncthing 实现了自定义的 **Block Exchange Protocol（BEP）**，设备之间通过加密通道交换文件块而非整文件，能够做到：

- **增量同步**：仅传输变化的文件块，节省带宽
- **并行传输**：一个文件可以同时从多个节点获取
- **断点续传**：传输中断后可从上次中断处继续
- **哈希校验**：每块数据 SHA-256 校验，确保传输完整性

### 2.2 设备发现与连接建立

| 发现方式 | 说明 |
|----------|------|
| 本地广播（Local Discovery） | 局域网内通过 UDP 21027 端口广播设备 ID 自动发现 |
| 全局发现（Global Discovery） | 借助公共发现服务器 announce.syncthing.net 帮助设备互相定位 IP |
| 手动指定地址 | 在 GUI 中直接输入 `tcp://192.168.1.100:22000` 等静态地址 |
| Relay 中继 | 当 NAT/防火墙限制时，通过 `relay.syncthing.net` 等中继服务器转发流量 |
| QUIC 协议 | 使用 QUIC（UDP）协议可更好地穿透 NAT，减少对 Relay 的依赖 |

### 2.3 文件夹配置与同步策略

每个文件夹可独立配置：

- **共享对象**：只同步给指定的设备 ID
- **忽略模式**：`.stignore` 文件，支持 `.gitignore` 语法的通配
- **扫描间隔**：`300` 秒或 `60` 秒，按需调节
- **FS Watcher**：基于文件系统事件的增量扫描，性能更高
- **发送-接收 / 仅发送 / 仅接收 / 仅发送加密**：四种同步模式
- **版本管理**：`Simple / Staggered / Trash Can / External` 四种策略

### 2.4 冲突处理与版本管理

- **冲突文件**：当两个节点同时修改同一文件时，后修改的版本以 `filename.sync-conflict-YYYYMMDD-HHMMSS.deviceID.ext` 命名保留
- **Trash Can**：被删除的文件保留在 `.stversions` 目录一段时间
- **Simple**：只保留最近 N 个版本
- **Staggered**：按时间间隔分层保留（类似 borg backup 的渐进策略）

### 2.5 .stignore 忽略规则示例

```
# 忽略所有隐藏文件
.*

# 忽略 node_modules 目录
node_modules/

# 忽略 .iso 和 .zip
*.iso
*.zip

# 忽略 temp 目录及其所有内容
temp/

# 不忽略 temp 目录下的 keep.txt
!temp/keep.txt

# 包含子目录的忽略规则
(?d).DS_Store
```

### 2.6 安全与加密

- **设备认证**：基于 TLS 证书 + 设备 ID（指纹）
- **传输加密**：TLS 1.3，采用 AEAD 密码套件
- **本地加密密码库**：可选加密密码库，文件块在离开发送端前已加密，接收端不解密不能读取
- **Web GUI 认证**：HTTPS + 用户名密码（建议配置 HTTPS 证书）

---

## 三、技术架构与实现原理

### 3.1 Block Exchange Protocol（BEP）

Syncthing 的核心协议 BEP 是一个基于 TLS 的二进制协议，主要消息类型包括：

| 消息类型 | 作用 |
|----------|------|
| ClusterConfig | 交换设备支持的文件夹及能力 |
| Index / IndexUpdate | 发布本地文件索引信息 |
| Request / Response | 请求和响应具体的文件块 |
| Ping / Pong | 保持连接和检测链路 |

### 3.2 文件夹索引数据库

Syncthing 维护一个 LevelDB 本地数据库，记录：

- 每个文件的路径、大小、修改时间、权限
- 每个文件的块列表（SHA-256 哈希 + 偏移 + 大小）
- 同步失败或冲突的文件列表
- 同步版本号（Vector Clock）

### 3.3 Web GUI 与 REST API

- Web GUI 使用本地构建的 HTML/JS，通过 8384 端口访问
- 全部配置保存在 `~/.config/syncthing/config.xml`
- 提供完整 REST API，可通过 `apikey` 调用

### 3.4 Relay 与 NAT 穿透

| 端口 | 协议 | 用途 |
|------|------|------|
| 22000/TCP | TCP | 默认文件传输端口 |
| 22000/UDP | QUIC | 默认 QUIC 文件传输端口（推荐开启） |
| 21027/UDP | UDP | 局域网设备发现广播 |
| 8384/TCP | TCP | Web GUI/REST API 端口 |

---

## 四、快速上手：Docker 部署实战

### 4.1 Docker CLI 启动（最简洁）

```bash
docker run -d \
  --name=syncthing \
  --hostname=my-syncthing \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Shanghai \
  -p 8384:8384 \
  -p 22000:22000/tcp \
  -p 22000:22000/udp \
  -p 21027:21027/udp \
  -v ./syncthing-config:/var/syncthing/config \
  -v ./sync-data:/var/syncthing \
  --restart=unless-stopped \
  syncthing/syncthing:latest
```

访问 `http://<主机IP>:8384` 进入 Web GUI。

### 4.2 Docker Compose 部署（推荐）

```yaml
version: "3.8"

services:
  syncthing:
    image: syncthing/syncthing:latest
    container_name: syncthing
    hostname: syncthing-docker
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
    volumes:
      - ./config:/var/syncthing/config
      - /data/sync:/var/syncthing/Data
      - /data/docs:/var/syncthing/Docs
    ports:
      - "8384:8384"
      - "22000:22000/tcp"
      - "22000:22000/udp"
      - "21027:21027/udp"
    restart: unless-stopped
```

启动：

```bash
docker compose up -d
docker compose logs -f
```

### 4.3 Linuxserver 镜像（含权限管理）

```yaml
services:
  syncthing:
    image: lscr.io/linuxserver/syncthing:latest
    container_name: syncthing
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
    volumes:
      - ./config:/config
      - ./data1:/data1
    ports:
      - "8384:8384"
      - "22000:22000/tcp"
      - "22000:22000/udp"
    restart: unless-stopped
```

### 4.4 首次使用：Web GUI 初始化

1. 打开 Web GUI，进入 "设置 → GUI"，设置 **用户名** 和 **密码**
2. 进入 "设置 → 连接"，勾选：
   - 使用 NAT 穿透（UPnP）
   - 启用 QUIC 监听（可显著提升连接成功率）
   - 使用全局发现 + 本地发现
3. 进入 "操作 → 显示 ID"，复制自己的 Device ID
4. 在其他设备添加此 ID 并勾选共享文件夹
5. 新增文件夹 → 选择目录 → 共享给目标设备 → 保存

---

## 五、从源码编译与开发环境

### 5.1 依赖与构建

Syncthing 完全使用 Go 编写，依赖较少：

```bash
# 1. 安装 Go 1.21+
wget https://go.dev/dl/go1.22.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.4.linux-amd64.tar.gz

# 2. 克隆仓库
git clone https://github.com/syncthing/syncthing.git
cd syncthing

# 3. 编译
go run build.go
./bin/syncthing --version
```

### 5.2 交叉编译其他平台

```bash
# Linux AMD64
GOOS=linux GOARCH=amd64 go build -o syncthing ./cmd/syncthing

# Windows
GOOS=windows GOARCH=amd64 go build -o syncthing.exe ./cmd/syncthing

# FreeBSD
GOOS=freebsd GOARCH=amd64 go build -o syncthing ./cmd/syncthing

# Android（需配合 NDK 构建）
./build.sh -goos android -goarch arm64
```

### 5.3 开发调试

```bash
# 启用调试模式
syncthing --verbose

# 查看 Web UI 日志中的调试信息
syncthing -reset-database   # 重置索引数据库
```

---

## 六、API 接口与自动化集成

Syncthing 提供完整 REST API，通过 `Actions → Settings → API Key` 获取密钥后可进行自动化配置。

### 6.1 查询设备状态

```bash
APIKEY="your-api-key"
curl -H "X-API-Key: $APIKEY" http://127.0.0.1:8384/rest/system/status | jq
```

### 6.2 强制立即扫描某个文件夹

```bash
curl -X POST -H "X-API-Key: $APIKEY" \
  "http://127.0.0.1:8384/rest/db/scan?folder=default"
```

### 6.3 查询同步失败文件

```bash
curl -H "X-API-Key: $APIKEY" \
  "http://127.0.0.1:8384/rest/db/completion?folder=default&device=XXXX-XXXX"
```

### 6.4 常用 API 端点速查

| 路径 | 方法 | 说明 |
|------|------|------|
| `/rest/system/config` | GET/PUT | 获取/修改完整配置 |
| `/rest/system/connections` | GET | 查看所有对等连接状态 |
| `/rest/system/ping` | GET | 健康检查 |
| `/rest/system/shutdown` | POST | 停止 Syncthing |
| `/rest/db/browse?folder=X` | GET | 浏览文件夹 |
| `/rest/db/ignores?folder=X` | GET/PUT | 获取/修改忽略规则 |

---

## 七、性能优化与大规模部署

### 7.1 连接慢 / 同步慢优化

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 设备间无法直连 | NAT/防火墙阻挡 | 启用 UPnP、开启 QUIC、手动指定 `tcp://IP:22000` |
| 一直依赖 Relay | 公网端口不通 | 在路由器上开放 22000 TCP/UDP 转发到本机 |
| 首次扫描慢 | 大文件数量多 | 降低 `fsync`、启用 FS Watcher，将扫描间隔改为 `3600` 秒 |
| 版本目录占空间大 | 版本保留过多 | 选用 Staggered 策略而非 Simple |

### 7.2 使用私有 Relay / 发现服务器

```bash
# 部署私有发现服务器
docker run -d --name stdiscosrv -p 8443:8443 syncthing/discosrv

# 部署私有 Relay
docker run -d --name strelaysrv -p 22067:22067 -p 22070:22070 \
  syncthing/relaysrv
```

在 Syncthing GUI 设置中，将发现服务器地址改为 `https://<你的IP>:8443/`，将 Relay 列表添加 `relay://<你的IP>:22067/`。

### 7.3 通过 Nginx 反代 Web GUI

```nginx
server {
    listen 443 ssl http2;
    server_name sync.example.com;

    ssl_certificate     /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8384;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 八、常见问题与故障排查

### 8.1 设备无法连接（最常见）

```bash
# 检查本机端口监听
netstat -tulpn | grep -E "22000|8384|21027"

# 检查设备间网络连通性
nc -zv 192.168.1.50 22000
```

**解决方法**：
- 开启 NAT 穿透（UPnP/端口转发）
- 开启 QUIC 协议
- 在 GUI 的 "设备设置 → 地址" 中填写手动地址：`tcp://192.168.1.50:22000`

### 8.2 出现大量 sync-conflict 文件

- 多个设备同时修改同一文件时会产生冲突
- Syncthing 不会自动删除冲突文件，需要人工选择保留哪一个
- 避免策略：将单向同步的设备设为 "仅发送" 或 "仅接收"

### 8.3 .stignore 忽略规则不生效

- `.stignore` 必须放在每个共享文件夹的根目录，不是全局配置目录
- 使用 GUI 的 "文件夹 → 忽略模式 → 已忽略" 验证匹配规则

### 8.4 扫描占用大量 CPU

- 将文件夹扫描间隔改为 `3600`（1 小时）
- 启用 "Watch for Changes"（FS Watcher），减少定期扫描
- 对不需要实时同步的大目录关闭 Watcher

### 8.5 数据库损坏修复

```bash
syncthing --reset-database   # 删除并重建索引
syncthing --reset-deltas     # 重置增量索引
```

---

## 九、社区生态与学习资源

| 项目 | 用途 | 地址 |
|------|------|------|
| Syncthing 官方文档 | 完整使用与配置手册 | https://docs.syncthing.net |
| Syncthing 官方论坛 | 社区交流与问题求助 | https://forum.syncthing.net |
| Syncthing Traefik 示例 | 反向代理配置参考 | https://github.com/syncthing/syncthing |
| Syncthing Android App | Google Play / F-Droid 可下载 | 官网 Apps 页面 |
| Syncthing-GTK | Linux 桌面图形客户端 | https://github.com/syncthing/syncthing-gtk |
| SyncTrayzor | Windows 托盘客户端 | https://github.com/canton7/SyncTrayzor |
| syncthing-inotify | 传统 FS Watcher 替代 | 已合并到主程序 |

---

## 十、使用场景与案例参考

### 10.1 个人多设备文件同步

在家中 PC、笔记本、手机、NAS 四台设备上部署 Syncthing，建立 3 个共享文件夹：

- `~/Photos`：手机拍照自动同步到 PC 与 NAS 做备份
- `~/Docs`：工作文档多端同步
- `~/Notes`：使用 Obsidian 搭配 Syncthing 多端同步笔记

### 10.2 家庭/小团队文件服务器

在 NAS（群晖/Unraid）上部署 Syncthing Docker，作为家庭所有设备的共享文件中枢，不需要购买 Dropbox 空间。

### 10.3 分布式备份集群

使用 3 台异地 VPS，把重要数据在三台之间同步，任一节点故障不会导致数据丢失，配合版本管理防止误删。

### 10.4 与 Nextcloud / rsync / rclone 的选择

| 工具 | 推荐场景 |
|------|----------|
| Syncthing | 多设备对等同步、P2P、完全自托管 |
| Nextcloud | 多人协作、日历/联系人、云盘 UI |
| rsync | 单向脚本同步、服务器备份 |
| rclone | 云盘（S3/OneDrive/Google Drive）挂载与同步 |

---

## 总结

Syncthing 凭借简洁可靠的 P2P 架构与出色的跨平台支持，是目前最值得推荐的开源文件同步方案。它无需维护中心服务器、不产生订阅费用、端到端加密、数据完全私有，完美契合自托管爱好者的核心需求。对于希望摆脱 Dropbox 等商用云服务、追求数据主权的用户而言，Syncthing + NAS 构成的多设备同步方案几乎是 "部署一次、终身使用" 的最佳选择。在实际使用中，建议开启 QUIC、为 NAS 开放 22000 端口，并将大文件文件夹设置为 Staggered 版本管理策略，即可获得最佳的同步体验与数据安全。
