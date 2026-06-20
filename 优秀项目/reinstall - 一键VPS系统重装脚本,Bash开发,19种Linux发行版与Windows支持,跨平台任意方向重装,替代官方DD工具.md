---
title: reinstall开源项目详解：一键VPS系统重装脚本部署教程与跨平台DD工具实战指南
id: reinstall-vps-reinstall-script-guide
date: 2026-06-20
auther: loveos
cover: /upload/reinstall-cover.png
excerpt: 开源协议：MIT GitHub Stars：10K+ 核心定位：一键 VPS 系统重装脚本，支持 19 种 Linux 发行版与 Windows 官方 ISO 重装，跨平台任意方向重装
permalink: /2026/reinstall---yi-jian-vps-xi-tong-zhong-zhuang-jiao-ben-19-chong-linux-fa-xing-ban-yu-windows-zhi-chi
categories:
 - Github
tags:
 - Project.Recommendation
 - github
 - bash
 - vps
 - dd
 - system-reinstall
 - linux
 - windows
---

> **开源协议**：MIT
> **GitHub Stars**：10K+
> **核心定位**：一键 VPS 系统重装脚本，支持 19 种 Linux 发行版与 Windows 官方 ISO 重装，跨平台任意方向重装

---

<hyperlink-card href="https://github.com/bin456789/reinstall" target="_blank" theme="regular"></hyperlink-card>


## 一、项目概述

**reinstall** 是一款专为 VPS 服务器设计的一键系统重装脚本，由开发者 bin456789 维护，是目前 GitHub 上最成熟、功能最完善的跨平台 DD/重装工具之一。它彻底解决了传统 VPS 重装依赖商家后台、系统选择有限、无法自定义镜像等痛点。

该脚本使用纯 Bash（Linux 端）和 Batch（Windows 端）编写，无任何第三方依赖，单文件即可运行。它支持从任意系统重装到任意系统——无论是 Linux → Linux、Linux → Windows、Windows → Windows，还是 Windows → Linux，都能一键完成。

reinstall 的核心设计理念是 **"最小化资源占用 + 最大化兼容性"**：

- **内存友好**：Alpine/Debian 仅需 256MB 内存即可完成重装，比官方 netboot 方案要求更低
- **智能网络**：自动检测并配置静态/动态 IP，支持 /32、/128、网关不在子网范围、纯 IPv6、IPv4/IPv6 在不同网卡等复杂网络环境
- **安全识别**：全程使用分区表 ID 识别硬盘，从根本上避免写错硬盘的风险
- **广泛兼容**：支持 BIOS 和 EFI 双引导模式，支持 ARM 服务器（aarch64）
- **纯净透明**：不含任何自制软件包，所有资源均实时从官方镜像源获取，确保系统纯净可信

---

## 二、核心特性解读

### 2.1 支持 19 种 Linux 发行版

| 发行版 | 版本 | 内存要求 | 硬盘要求 | 安装方式 |
| ------ | ---- | -------- | -------- | -------- |
| Alpine | 3.21, 3.22, 3.23, 3.24 | 256 MB | 1 GB | 网络安装 |
| Debian | 9, 10, 11, 12, 13 | 256 MB | 1 ~ 1.5 GB | 网络安装/云镜像 |
| Kali | 滚动版 | 256 MB | 1 ~ 1.5 GB | 网络安装 |
| Ubuntu | 18.04 LTS ~ 26.04 LTS | 512 MB | 2 GB | 云镜像 |
| Anolis | 7, 8, 23 | 512 MB | 5 GB | 云镜像 |
| RHEL / AlmaLinux / Rocky / Oracle | 8, 9, 10 | 512 MB | 5 GB | 云镜像 |
| OpenCloudOS | 8, 9, Stream 23 | 512 MB | 5 GB | 云镜像 |
| CentOS Stream | 9, 10 | 512 MB | 5 GB | 云镜像 |
| Fedora | 43, 44 | 512 MB | 5 GB | 云镜像 |
| openEuler | 20.03 LTS ~ 24.03 LTS | 512 MB | 5 GB | 云镜像 |
| openSUSE | Leap 16.0, Tumbleweed | 512 MB | 5 GB | 云镜像 |
| NixOS | 26.05 | 512 MB | 5 GB | 云镜像 |
| Arch Linux | 滚动版 | 512 MB | 5 GB | 云镜像 |
| Gentoo | 滚动版 | 512 MB | 5 GB | 云镜像 |
| 安同 OS (AOSC) | 滚动版 | 512 MB | 5 GB | 云镜像 |
| 飞牛 fnOS / FygoOS | 1 | 512 MB | 8 GB | 云镜像 |

### 2.2 Windows 官方 ISO 重装

- **原版镜像**：使用微软官方 ISO 而非自制镜像，确保系统安全可信
- **自动查找**：脚本自动从微软服务器查找对应版本的 ISO 下载链接
- **驱动自动注入**：自动安装 VirtIO、KVM、VMware、Xen、Hyper-V 等公有云驱动
- **版本支持**：
  - Vista / 7 / 8.x / Server 2008 ~ 2012 R2（需 512MB 内存 + 25GB 硬盘）
  - Windows 10 / 11 / Server 2016 ~ 2025（需 1GB 内存 + 25GB 硬盘）

### 2.3 五大核心功能

| 功能 | 说明 |
| ---- | ---- |
| **一键重装 Linux** | 指定发行版和版本号，自动下载内核/镜像并完成重装 |
| **一键 DD Raw 镜像** | 支持将任意 raw/dd 格式镜像直接写入硬盘 |
| **一键引导到 Alpine Live OS** | 重启后进入内存中的 Alpine 系统，用于救砖/调试 |
| **一键引导到 netboot.xyz** | 重启后进入 netboot.xyz 引导界面，可选择更多系统 |
| **一键重装 Windows** | 使用官方 ISO 完成 Windows 系统自动安装 |

### 2.4 智能网络配置

- **自动识别 IP 类型**：动态 DHCP / 静态 IP 自动检测
- **特殊网络支持**：
  - /32 掩码 IP（常见于部分商家）
  - /128 掩码 IPv6
  - 网关不在子网范围内（非常规网络配置）
  - 纯 IPv6 环境
  - IPv4/IPv6 分散在不同网卡
- **国内镜像源优化**：自动检测是否位于中国，自动切换至清华/南大等国内镜像源加速下载

### 2.5 国内优化支持

脚本内置 `is_in_china` 检测，根据服务器位置自动选择镜像源：

- **Alpine**：清华 TUNA 镜像 (`mirrors.tuna.tsinghua.edu.cn`)
- **Debian**：ftp.cn.debian.org / 南大镜像
- **Ubuntu**：清华 TUNA 镜像
- **Arch Linux**：清华 TUNA 镜像
- **openSUSE**：中科大 USTC 镜像
- **CentOS/RHEL 系**：南大镜像

### 2.6 安全与可靠性

- **分区表 ID 识别**：不依赖 `/dev/sda` 等易变的设备名，使用 GPT/MBR 分区 ID 识别硬盘
- **取消重装机制**：重启前可随时通过 `reset` 命令取消重装操作
- **SSH 救砖支持**：即使安装过程出错，也能通过 SSH 手动连接修复
- **双重查看方式**：支持 SSH、HTTP 80 端口、商家后台 VNC、串行控制台等多种方式查看安装进度

---

## 三、系统架构与工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    当前系统（Linux/Windows）                │
│                    执行 reinstall.sh / reinstall.bat         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    下载内核/initramfs/镜像
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    修改 Bootloader 配置                     │
│  (GRUB / syslinux / Windows BCD)                           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                         重启服务器
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    网络引导/内存系统启动                    │
│  (Alpine Live OS / Debian Installer / Cloud Image)         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    自动执行预配置的安装脚本
                  ┌────────────┼────────────┐
                  │            │            │
         ┌────────▼───┐ ┌──────▼─────┐ ┌────▼────────┐
         │ 传统网络安装 │ │ 云镜像写入   │ │ ISO 自动安装 │
         │ (Debian网络) │ │ (直接dd)     │ │ (Windows)   │
         └─────────────┘ └────────────┘ └─────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    新系统启动，配置完成                      │
│                    SSH 账户信息通过日志输出                  │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 Linux 重装流程（以 Debian 为例）

1. **下载阶段**：从 Debian 官方镜像站下载 linux（内核）和 initrd.gz（初始化内存盘）
2. **配置阶段**：生成 preseed 自动应答文件，预设语言、时区、root 密码、分区方案
3. **引导阶段**：临时添加 GRUB 启动项，指向下载的内核和 initrd
4. **重启阶段**：服务器重启后进入 Debian 安装程序，全自动完成安装
5. **完成阶段**：新系统启动，SSH 可用，使用预设的 root 密码登录

### 3.2 云镜像重装流程（以 Ubuntu 为例）

1. **下载阶段**：下载 Ubuntu 官方 cloud image（qcow2/img 格式）
2. **写入阶段**：将镜像直接 dd 到系统盘
3. **配置阶段**：cloud-init 自动完成首次启动配置，包括网络设置、SSH 密钥、用户账户
4. **完成阶段**：系统首次启动后即可 SSH 登录

### 3.3 Windows 重装流程

1. **准备阶段**：下载 Windows 官方 ISO 和 VirtIO 驱动 ISO
2. **配置阶段**：生成 autounattend.xml 自动应答文件，预设语言、版本、许可、账户、驱动注入
3. **引导阶段**：使用 memdisk/grub 引导 ISO，或提取 install.wim 直接应用
4. **安装阶段**：Windows 自动完成安装、驱动注入、系统配置
5. **完成阶段**：系统启动，使用预设密码通过 RDP/SSH 登录

---

## 四、部署指南

### 4.1 系统要求

| 项目 | 要求 |
| ---- | ---- |
| **原系统** | Linux（任意发行版）或 Windows（Vista/7/8/10/11, Server 2008-2025） |
| **虚拟化** | KVM / VMware / Xen / Hyper-V / VirtualBox / 独服均支持 |
| **不支持** | ❌ OpenVZ / LXC 容器（请改用 OsMutation） |
| **内存** | 256 MB（Linux）/ 512 MB ~ 1 GB（Windows） |
| **硬盘** | 1 GB ~ 25 GB，视目标系统而定 |
| **网络** | 服务器需能访问外网以下载镜像 |
| **引导方式** | BIOS / EFI 均可，支持 ARM64 |

> ⚠️ **注意**：本脚本理论上支持独服和 PC，但如果能使用 IPMI 或 U 盘重装，则不建议使用本脚本（IPMI 方式更可靠）。

### 4.2 Linux 端：下载脚本

**国外服务器**：

```bash
curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh
# 或使用 wget
wget -O reinstall.sh https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh
```

**国内服务器（加速下载）**：

```bash
curl -O https://cnb.cool/bin456789/reinstall/-/git/raw/main/reinstall.sh
# 或使用 wget
wget -O reinstall.sh https://cnb.cool/bin456789/reinstall/-/git/raw/main/reinstall.sh
```

### 4.3 Windows 端：下载脚本

> ❗ **重要提示**：请先关闭 `Windows Defender` 的 **实时保护** 功能，该功能会阻止 `certutil` 下载任何文件。

**国外服务器**：

```batch
certutil -urlcache -f -split https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.bat
```

**国内服务器（加速下载）**：

```batch
certutil -urlcache -f -split https://cnb.cool/bin456789/reinstall/-/git/raw/main/reinstall.bat
```

> 💡 **Windows 7 特殊说明**：由于 Windows 7 默认不支持 TLS 1.2、SHA-256，且根证书可能过期，Vista / 7 / Server 2008 (R2) 可能无法自动下载脚本。需要手动通过 IE（先在 IE 高级设置中启用 TLS 1.2）或远程桌面，将以下两个文件保存到同一目录：
>
> - https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.bat
> - https://www.cygwin.com/setup-x86.exe
>
> 使用时运行下载的 `reinstall.bat`

---

## 五、功能一：一键重装 Linux

### 5.1 基本用法

> ⚠️ **警告**：此功能会清除当前系统**整个硬盘**的全部数据（包含其它分区）！如果不小心运行了脚本，可以在**重启前**运行 `bash reinstall.sh reset` 取消重装。

```bash
bash reinstall.sh [发行版] [版本号] [可选参数]
```

**示例：重装为 Debian 12**

```bash
bash reinstall.sh debian 12
```

**示例：重装为 Ubuntu 24.04 LTS**

```bash
bash reinstall.sh ubuntu 24.04
```

**示例：重装为 Alpine 3.24**

```bash
bash reinstall.sh alpine 3.24
```

**示例：重装为 Arch Linux（滚动版）**

```bash
bash reinstall.sh arch
```

**示例：重装为 Windows 11**

```bash
bash reinstall.sh windows 11
```

### 5.2 完整发行版命令速查

```bash
bash reinstall.sh anolis      7|8|23
                  rocky       8|9|10
                  oracle      8|9|10
                  almalinux   8|9|10
                  opencloudos 8|9|23
                  centos      9|10
                  fnos        1
                  fygoos      1
                  nixos       26.05
                  fedora      43|44
                  debian      9|10|11|12|13
                  opensuse    16.0|tumbleweed
                  openeuler   20.03|22.03|24.03
                  alpine      3.21|3.22|3.23|3.24
                  ubuntu      18.04|20.04|22.04|24.04|26.04 [--minimal]
                  kali
                  arch
                  gentoo
                  aosc
                  redhat      --img="http://access.cdn.redhat.com/xxx.qcow2"
```

> 💡 **提示**：
> - 不输入版本号则自动安装最新版本
> - 脚本会提示输入用户名和密码，不输入则使用 `root` 和随机密码
> - 最大化利用磁盘空间：不含 boot 和 swap 分区
> - 自动根据机器类型和商家安装优化内核
> - 安装 Red Hat 时需填写从 https://access.redhat.com/downloads/content/rhel 得到的 qcow2 镜像链接，也可以安装其它类 RHEL 系统的 qcow2，例如 Alibaba Cloud Linux 和 TencentOS Server
> - 重装后如需修改 SSH 端口或者改成密钥登录，注意还要修改 `/etc/ssh/sshd_config.d/` 里面的文件
> - 为了快速安装，重装时不会对新系统进行更新，请在重装后自行更新

### 5.3 可选参数详解

| 参数 | 说明 |
| ---- | ---- |
| `--username USERNAME` | 设置新系统的用户名 |
| `--password PASSWORD` | 设置新系统的登录密码 |
| `--ssh-key KEY` | 设置 SSH 登录公钥。使用公钥时，密码将为空 |
| `--ssh-port PORT` | 修改新系统的 SSH 端口 |
| `--web-port PORT` | 修改安装日志查看的 Web 端口 |
| `--frpc-config PATH` | 添加 frpc 内网穿透，参数填配置文件的本地路径或 HTTP 链接 |
| `--hold 1` | 仅重启到安装环境，不运行安装，用于 SSH 登录验证网络连通性 |
| `--hold 2` | 安装结束后不重启，用于 SSH 登录修改系统内容（Debian/Kali 会挂载在 `/target`，其它系统会挂载在 `/os`） |

**示例：重装为 Debian 12，预设 root 密码和 SSH 公钥**

```bash
bash reinstall.sh debian 12 \
  --username root \
  --password "MySecureP@ss123" \
  --ssh-key "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAA... your_email@example.com"
```

**示例：重装为 Ubuntu 24.04，指定 SSH 端口为 2222**

```bash
bash reinstall.sh ubuntu 24.04 \
  --username root \
  --password "MySecureP@ss123" \
  --ssh-port 2222
```

**示例：测试网络连通性（hold 1 模式）**

```bash
bash reinstall.sh debian 12 --hold 1
# 重启后会进入 Alpine Live OS，可 SSH 登录检查网络
# 确认无误后再执行正式安装
```

### 5.4 查看安装进度

重装过程中，可通过以下方式查看安装日志：

| 方式 | 说明 |
| ---- | ---- |
| **SSH** | 部分安装环境支持 SSH 连接查看实时日志 |
| **HTTP 80 端口** | 脚本会启动简易 Web 服务，通过 `http://服务器IP` 查看日志 |
| **商家后台 VNC** | 通过 VPS 商家提供的 VNC 控制台查看安装过程（最推荐） |
| **串行控制台** | 支持串行 console 的服务器可通过串口查看 |

> 💡 **救砖提示**：即使安装过程出错，也能连接 SSH 手动修复。目标系统非 Debian/Kali 时，可以运行 `/trans.sh alpine` 自动救砖成 Alpine 系统（轻量系统，便于重新部署）。

### 5.5 取消重装

如果在执行脚本后、重启前发现选错了发行版或改变了主意，可以取消重装：

```bash
bash reinstall.sh reset
```

此命令会恢复 bootloader 的原始配置，服务器重启后仍为原系统。

---

## 六、功能二：一键 DD Raw 镜像到硬盘

### 6.1 使用场景

- 安装自定义制作的系统镜像（.img / .raw / .gz / .xz 等格式）
- 快速部署已配置好的生产环境镜像
- 恢复备份的系统快照
- 使用第三方提供的 DD 包

### 6.2 命令格式

```bash
bash reinstall.sh dd --img="镜像URL"
```

**示例：DD 一个自定义系统镜像**

```bash
bash reinstall.sh dd --img="https://example.com/my-custom-system.img.gz"
```

**示例：DD 一个 OpenWrt 镜像**

```bash
bash reinstall.sh dd --img="https://downloads.openwrt.org/releases/23.05.0/targets/x86/64/openwrt-23.05.0-x86-64-generic-ext4-combined.img.gz"
```

### 6.3 支持的镜像格式

- 原始 raw 镜像（.img / .raw）
- Gzip 压缩镜像（.img.gz / .raw.gz）
- XZ 压缩镜像（.img.xz / .raw.xz）
- Bzip2 压缩镜像
- Zstd 压缩镜像

> 💡 **提示**：DD 模式下，脚本会自动检测镜像的压缩格式并解包后写入硬盘。确保镜像的磁盘分区与目标服务器的引导方式（BIOS/EFI）兼容。

---

## 七、功能三：一键引导到 Alpine Live OS（内存系统）

### 7.1 使用场景

- **系统救砖**：原系统无法启动，但需要进入一个可用的 Linux 环境进行修复
- **数据备份**：在重装前，先进入 Live OS 备份重要数据
- **磁盘操作**：需要对磁盘进行分区、格式化、数据迁移等操作
- **网络诊断**：测试服务器网络配置，为后续重装做准备
- **手动安装**：需要完全手动控制安装过程

### 7.2 命令格式

```bash
bash reinstall.sh alpine [版本号]
```

**示例**：

```bash
# 重启后进入 Alpine 3.24 Live OS
bash reinstall.sh alpine 3.24
```

重启后，服务器将进入一个完全运行在内存中的 Alpine Linux 环境，不修改任何磁盘数据。默认登录信息：

- **用户名**：root（或脚本执行时指定的用户名）
- **密码**：脚本执行时指定的密码（或生成的随机密码）

进入后可进行以下操作：

```bash
# 查看当前磁盘分区
fdisk -l

# 挂载原系统分区进行数据备份
mount /dev/sda1 /mnt
ls /mnt/

# 手动下载并 dd 镜像
wget https://example.com/system.img
dd if=system.img of=/dev/sda bs=4M status=progress

# 完成后重启
reboot
```

---

## 八、功能四：一键引导到 netboot.xyz

### 8.1 netboot.xyz 简介

netboot.xyz 是一个开源的网络引导工具，提供了一个菜单式的界面，可以从网络启动并安装数十种不同的 Linux 发行版和实用工具。它的优势在于：

- **系统选择极其丰富**：远超 reinstall 脚本本身支持的范围
- **交互式安装**：可以手动选择分区方案、软件包、时区等
- **包含实用工具**：如 Clonezilla（系统克隆）、GParted（分区工具）、SystemRescue 等

### 8.2 命令格式

```bash
bash reinstall.sh netbootxyz
```

执行后重启服务器，将进入 netboot.xyz 的菜单界面。通过 VNC/控制台可以：

1. 选择 **Linux Network Installs** 查看所有支持的 Linux 发行版
2. 选择 **Utilities** 进入系统维护工具
3. 选择 **iPXE Shell** 手动输入引导命令

> 💡 **适用场景**：当 reinstall 脚本不支持某个特定发行版或版本时，netboot.xyz 是一个很好的备选方案。

---

## 九、功能五：一键重装 Windows

### 9.1 使用场景

- 将 Linux VPS 改为 Windows 系统
- 升级 Windows 版本（如 Server 2019 → 2025）
- 更换 Windows 发行版（如 Windows Server → Windows 11）
- 系统崩溃后重装纯净 Windows

### 9.2 命令格式

```bash
bash reinstall.sh windows [版本]
```

**常用示例**：

```bash
# 重装为 Windows Server 2025
bash reinstall.sh windows 2025

# 重装为 Windows Server 2022
bash reinstall.sh windows 2022

# 重装为 Windows 11
bash reinstall.sh windows 11

# 重装为 Windows 10
bash reinstall.sh windows 10

# 使用自定义 ISO
bash reinstall.sh windows --iso="https://example.com/custom-win.iso" --image-name="Windows 11 Pro"
```

### 9.3 支持的 Windows 版本

| 类型 | 版本 | 内存要求 | 硬盘要求 |
| ---- | ---- | -------- | -------- |
| 桌面版 | Windows Vista / 7 / 8.x / 10 / 11 | 512 MB ~ 1 GB | 25 GB |
| 服务器版 | Windows Server 2008 / 2008 R2 / 2012 / 2012 R2 / 2016 / 2019 / 2022 / 2025 | 512 MB ~ 1 GB | 25 GB |

### 9.4 自动驱动注入

脚本会自动检测虚拟化平台并注入对应驱动：

| 虚拟化平台 | 自动注入的驱动 |
| ---------- | -------------- |
| **KVM / Proxmox** | VirtIO 网络、磁盘、显卡驱动 |
| **VMware** | VMXNET3 / pvscsi 驱动 |
| **Xen** | Xen PV 驱动 |
| **Hyper-V** | Hyper-V 集成服务 |
| **物理服务器** | 无特殊驱动注入 |

### 9.5 登录信息

Windows 安装完成后，默认账户信息：

- **用户名**：`Administrator`（或通过 `--username` 指定）
- **密码**：执行脚本时设置的密码（或生成的随机密码）
- **登录方式**：通过 RDP（远程桌面）连接 `服务器IP:3389`

> 💡 **提示**：首次登录 Windows 后，建议：
> 1. 修改默认的 Administrator 密码
> 2. 开启 Windows Update 安装最新安全更新
> 3. 配置防火墙规则，仅放行必要端口
> 4. 安装杀毒软件

---

## 十、实战案例指南

### 10.1 案例一：Debian 11 → Debian 12 升级

**场景**：服务器当前运行 Debian 11，希望在不丢失数据盘的前提下升级到 Debian 12。

```bash
# 1. 首先备份重要数据！
# 数据盘通常是 /dev/sdb / /dev/vdb 等，重装只会影响系统盘 /dev/sda / /dev/vda
tar -czf /backup/etc-backup.tar.gz /etc

# 2. 下载脚本
curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh

# 3. 执行重装（设置密码和 SSH 密钥）
bash reinstall.sh debian 12 \
  --password "MyStrongP@ss" \
  --ssh-key "ssh-rsa AAAA... user@home"

# 4. 确认后输入 Y 重启
# 等待 5-10 分钟

# 5. 重装完成后 SSH 登录
ssh root@服务器IP

# 6. 重新挂载数据盘（如 /dev/vdb1）
mkdir -p /data
mount /dev/vdb1 /data
echo "/dev/vdb1 /data ext4 defaults 0 0" >> /etc/fstab
```

### 10.2 案例二：CentOS 7 → Ubuntu 24.04 跨发行版迁移

**场景**：CentOS 7 已于 2024 年 EOL，需要将服务器迁移到 Ubuntu 24.04 LTS。

```bash
# 1. 备份所有重要配置和数据
# /etc 下的配置文件、网站数据、数据库等
# 建议先将数据备份到远程或数据盘

# 2. 下载脚本
curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh

# 3. 重装为 Ubuntu 24.04
bash reinstall.sh ubuntu 24.04 \
  --username root \
  --password "Ubuntu2404!" \
  --ssh-port 22

# 4. 重启等待安装完成
# （Ubuntu 使用云镜像方式，通常 2-3 分钟即可完成）

# 5. 重新部署应用
# - 安装 Docker/Nginx/MySQL 等
# - 恢复数据和配置
```

### 10.3 案例三：Linux → Windows（安装 Windows Server 2025）

**场景**：需要在 Linux VPS 上安装 Windows 系统，用于运行特定 Windows 应用。

```bash
# 1. 检查服务器是否满足要求
# - 内存 >= 1 GB
# - 系统盘 >= 25 GB
# - CPU 支持虚拟化（通常 VPS 都满足）

# 2. 下载脚本
curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh

# 3. 执行 Windows 重装
bash reinstall.sh windows 2025 \
  --password "Win2025Admin!"

# 4. 输入 Y 确认重启
# 安装时间较长，通常 15-30 分钟
# 建议通过 VNC 观察进度

# 5. 安装完成后通过 RDP 连接
# 服务器IP:3389
# 用户：Administrator
# 密码：Win2025Admin!
```

### 10.4 案例四：低配小鸡装 Alpine（256MB 内存）

**场景**：购买了一个 256MB 内存的超便宜 VPS，原系统选择有限。

```bash
# 1. 下载脚本
curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh

# 2. 安装 Alpine Linux 3.24（内存和磁盘占用最小）
bash reinstall.sh alpine 3.24 \
  --username root \
  --password "alpine2026"

# 3. 重启后即可使用
# Alpine 安装仅需约 1 GB 磁盘空间
# 非常适合作为反向代理、VPN、监控节点等轻量级用途
```

### 10.5 案例五：救砖操作（系统无法启动时）

**场景**：服务器配置错误导致系统无法启动，但可以通过 VNC 进入。

```bash
# 1. 如果还能进入原系统，直接执行
bash reinstall.sh alpine 3.24 --hold 1
# 重启后进入 Alpine Live OS

# 2. 进入 Alpine 后检查数据盘
fdisk -l
mount /dev/vda1 /mnt
ls /mnt/  # 检查是否有可恢复的数据

# 3. 确认无误后重新执行正式重装
# 或者在 Alpine 中手动修复原系统配置
```

---

## 十一、常见问题与解决方案

### 11.1 重装后无法 SSH 登录怎么办？

| 可能原因 | 解决方案 |
| -------- | -------- |
| IP 地址变化 | 在商家后台查看新分配的 IP，或检查 IP 是否通过 DHCP 重新获取 |
| SSH 端口变化 | 如果指定了 `--ssh-port`，使用新端口连接 |
| 密码忘记 | 如果使用了随机密码，通过 VNC 登录后重置；或重新执行重装 |
| 防火墙阻止 | 通过 VNC 登录后检查 iptables/ufw 规则 |
| SSH 未启动 | 通过 VNC 登录后手动启动 sshd 服务 |

### 11.2 网络无法识别（静态 IP 配置）

部分商家使用静态 IP 配置，重装后可能需要手动设置：

```bash
# Debian/Ubuntu 系（查看自动生成的配置）
cat /etc/network/interfaces
cat /etc/netplan/*.yaml

# RHEL/CentOS 系
cat /etc/sysconfig/network-scripts/ifcfg-eth0

# 如果需要手动配置
# 记下重装前的 IP 信息：
ip addr show
ip route show
cat /etc/resolv.conf
```

> 💡 **最佳实践**：重装前执行以下命令保存网络配置，以便重装后核对：
> ```bash
> ip addr show > /backup/network-info.txt
> ip route show >> /backup/network-info.txt
> cat /etc/resolv.conf >> /backup/network-info.txt
> ```

### 11.3 OpenVZ / LXC 服务器无法使用

❌ **错误信息**：`Not Supported OS in Container. Please use https://github.com/LloydAsp/OsMutation`

reinstall 脚本需要操作物理硬盘和 bootloader，而 OpenVZ/LXC 是容器级虚拟化，不暴露底层磁盘操作接口。解决方案：

- **使用 OsMutation**：访问 https://github.com/LloydAsp/OsMutation，这是专为容器环境设计的系统切换工具
- **联系商家**：部分商家提供手动切换系统的后台功能
- **升级 VPS**：如果预算允许，升级到 KVM/VMware 等全虚拟化方案

### 11.4 国内服务器下载速度慢

脚本会自动检测服务器位置，但如果检测不准确，可以手动使用国内镜像：

```bash
# 直接使用国内镜像地址的脚本
curl -O https://cnb.cool/bin456789/reinstall/-/git/raw/main/reinstall.sh
bash reinstall.sh debian 12
```

### 11.5 Windows 下载失败（certutil 被拦截）

**问题**：Windows Defender 实时保护阻止了 certutil 下载。

**解决方案**：
1. 打开 `Windows Security` → `Virus & threat protection` → `Manage settings`
2. 关闭 `Real-time protection`
3. 重新执行下载命令
4. 重装完成后建议重新开启实时保护

### 11.6 Windows 7 无法下载脚本

**问题**：Windows 7 默认不支持 TLS 1.2，且根证书过期。

**解决方案**：
1. 通过远程桌面从本地机器上传 `reinstall.bat`
2. 或使用 IE 浏览器，先在 `Internet Options → Advanced` 中勾选 `Use TLS 1.2`
3. 然后访问 `https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.bat` 下载
4. 同时需要下载 Cygwin 安装程序：`https://www.cygwin.com/setup-x86.exe`

### 11.7 重装后 SSH 密钥登录不生效

**问题**：指定了 `--ssh-key` 但仍需要密码登录。

**解决方案**：
```bash
# 1. 检查 .ssh 目录和 authorized_keys 权限
ls -la ~/.ssh/
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# 2. 检查 sshd_config 配置
grep -E "PubkeyAuthentication|AuthorizedKeysFile|PasswordAuthentication" /etc/ssh/sshd_config

# 3. 注意检查 /etc/ssh/sshd_config.d/ 目录下的配置
ls /etc/ssh/sshd_config.d/
```

### 11.8 ARM 服务器（aarch64）支持

脚本支持 ARM64 架构服务器，但部分发行版的 ARM 版本可能有限制：

| 发行版 | ARM64 支持 |
| ------ | ---------- |
| Debian | ✅ 9, 10, 11, 12, 13 |
| Ubuntu | ✅ 18.04 ~ 26.04 |
| Alpine | ✅ 3.21 ~ 3.24 |
| Fedora | ✅ |
| Arch Linux | ✅ |
| openSUSE | ✅ |
| 类 RHEL 系 | ✅（AlmaLinux/Rocky 等） |
| Gentoo | ❌ |
| Windows | ⚠️ 仅支持 ARM 版 Windows 镜像 |

---

## 十二、最佳实践与安全建议

### 12.1 重装前准备清单

- ✅ **备份重要数据**：确认所有需要保留的数据已备份到其他位置
- ✅ **记录网络配置**：保存 IP 地址、子网掩码、网关、DNS 信息
- ✅ **记录磁盘分区**：确认系统盘和数据盘分别是哪块磁盘
- ✅ **准备 SSH 密钥**：建议使用密钥登录而非密码登录
- ✅ **检查商家后台**：确认可以通过 VNC/控制台访问（万一重装失败）
- ✅ **记录重要配置**：/etc/fstab、防火墙规则、crontab 等

### 12.2 安全建议

| 建议 | 说明 |
| ---- | ---- |
| **使用强密码** | 至少 12 位，包含大小写字母、数字和特殊字符 |
| **使用 SSH 密钥** | 推荐使用 `--ssh-key` 参数，禁用密码登录 |
| **修改 SSH 端口** | 使用 `--ssh-port` 将 SSH 改为非标准端口（如 22222） |
| **开启防火墙** | 重装后立即配置 iptables/ufw/firewalld |
| **及时更新系统** | 重装后执行系统更新：`apt update && apt upgrade` 或 `yum update` |
| **禁用 root 远程登录** | 生产环境建议创建普通用户，使用 sudo 提权 |
| **定期备份** | 新系统稳定运行后，设置定期备份策略 |

### 12.3 重装后检查清单

- ✅ **SSH 可正常登录**：使用预设的用户名/密码或密钥
- ✅ **网络连接正常**：`ping 8.8.8.8` 和 `curl https://www.google.com`
- ✅ **磁盘空间合理**：`df -h` 确认系统盘空间分配正确
- ✅ **内存识别正确**：`free -h` 确认内存容量
- ✅ **时间同步正常**：`timedatectl` 检查时区和 NTP 同步
- ✅ **数据盘已挂载**：确认 /etc/fstab 中包含数据盘挂载信息
- ✅ **防火墙已开启**：仅放行必要端口
- ✅ **应用服务正常运行**：部署的业务服务可正常访问

---

## 十三、社区与生态

- **项目仓库**：[https://github.com/bin456789/reinstall](https://github.com/bin456789/reinstall)
- **问题反馈**：[GitHub Issues](https://github.com/bin456789/reinstall/issues) — 遇到问题请在此提交
- **交流群组**：[Telegram Group](https://t.me/reinstall_os) — 实时交流和技术支持
- **国内镜像**：[https://cnb.cool/bin456789/reinstall](https://cnb.cool/bin456789/reinstall) — 加速脚本下载
- **替代工具**：
  - [OsMutation](https://github.com/LloydAsp/OsMutation) — OpenVZ/LXC 容器环境专用
  - [netboot.xyz](https://netboot.xyz/) — 网络引导工具，支持数十种系统
  - [VirtIO 驱动](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/) — Windows 虚拟化驱动

---

## 十四、总结

reinstall 脚本以其 **"零依赖、跨平台、智能网络、纯净可信"** 四大核心优势，成为 VPS 运维人员和服务器爱好者必备的工具之一。无论是系统升级、跨发行版迁移、Linux 与 Windows 互转，还是系统救砖，它都能以最简单的方式完成最复杂的操作。

与传统的商家后台重装相比，reinstall 的优势在于：

- **系统选择更自由**：从 19 种 Linux 发行版到多版本 Windows，随心所欲
- **配置更灵活**：自定义用户名、密码、SSH 密钥、端口等参数
- **资源要求更低**：256MB 内存的低配小鸡也能使用
- **过程更可控**：多种方式查看安装日志，支持取消重装，支持 SSH 救砖

对于需要频繁调整服务器系统、管理多台 VPS、或者对商家提供的系统模板不满意的用户，reinstall 是一个值得加入工具箱的优秀工具。

> **立即体验**：访问 [https://github.com/bin456789/reinstall](https://github.com/bin456789/reinstall) 获取源码，或执行 `curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh && bash reinstall.sh debian 12` 一键重装为 Debian 12。
