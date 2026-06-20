---
title: reinstall开源项目详解：一键安装飞牛NAS系统与VPS跨平台重装工具实战指南
id: reinstall-fnOS-vps-reinstall-guide
date: 2026-06-20
auther: loveos
cover: /upload/reinstall-cover.png
excerpt: 开源协议：MIT GitHub Stars：10K+ 核心定位：一键安装飞牛NAS系统，支持19种Linux发行版与Windows，VPS跨平台任意方向重装
permalink: /2026/reinstall---yi-jian-an-zhuang-fei-niu-nas-xi-tong-yu-vps-kua-ping-tai-zhong-zhuang-gong-ju-shi-zhan
categories:
 - Github
tags:
 - Project.Recommendation
 - github
 - bash
 - fnOS
 - 飞牛NAS
 - vps
 - dd
 - system-reinstall
 - linux
 - windows
---

> **开源协议**：MIT
> **GitHub Stars**：10K+
> **核心定位**：一键安装飞牛NAS系统，支持19种Linux发行版与Windows官方ISO，VPS跨平台任意方向重装

---

<hyperlink-card href="https://github.com/bin456789/reinstall" target="_blank" theme="regular"></hyperlink-card>


## 一、项目概述

**reinstall** 是一款专为 VPS 服务器设计的一键系统重装脚本，支持一键安装 **飞牛NAS (fnOS)** 系统到 VPS 或物理服务器上。同时还支持 19 种 Linux 发行版与 Windows 官方 ISO 重装，跨平台任意方向重装。

该脚本使用纯 Bash（Linux 端）和 Batch（Windows 端）编写，无任何第三方依赖，单文件即可运行。它支持从任意系统重装到任意系统——无论是 Linux → fnOS、Linux → Windows、Windows → Windows，还是 Windows → Linux，都能一键完成。

### 1.1 核心应用场景：飞牛NAS一键安装

飞牛NAS (fnOS) 是一款国产开源的 NAS 操作系统，支持 x86_64 和 ARM64 架构，界面美观、功能强大。但官方只提供物理机镜像，对于使用 VPS 的用户来说，如何安装 fnOS 一直是个难题。reinstall 脚本完美解决了这个问题，只需一条命令即可将任意 Linux VPS 重装为飞牛NAS系统。

**飞牛NAS最低系统要求**：

| 项目 | 要求 |
| ---- | ---- |
| CPU | 2核+ |
| 内存 | 512 MB（推荐 1GB+） |
| 硬盘 | 8 GB+ 系统盘 |
| 网络 | 可访问外网 |

### 1.2 支持的系统列表

| 类型 | 系统 | 版本 | 内存要求 |
| ---- | ---- | ---- | -------- |
| **NAS** | **飞牛NAS (fnOS)** | **1** | **512 MB** |
| **NAS** | **FygoOS** | **1** | **512 MB** |
| Linux | Alpine | 3.21 ~ 3.24 | 256 MB |
| Linux | Debian | 9 ~ 13 | 256 MB |
| Linux | Kali | 滚动版 | 256 MB |
| Linux | Ubuntu | 18.04 ~ 26.04 LTS | 512 MB |
| Linux | Anolis | 7, 8, 23 | 512 MB |
| Linux | RHEL / AlmaLinux / Rocky / Oracle | 8, 9, 10 | 512 MB |
| Linux | CentOS Stream | 9, 10 | 512 MB |
| Linux | Fedora | 43, 44 | 512 MB |
| Linux | openEuler | 20.03 LTS ~ 24.03 LTS | 512 MB |
| Linux | openSUSE | Leap 16.0, Tumbleweed | 512 MB |
| Linux | NixOS | 26.05 | 512 MB |
| Linux | Arch Linux | 滚动版 | 512 MB |
| Linux | Gentoo | 滚动版 | 512 MB |
| Linux | 安同 OS (AOSC) | 滚动版 | 512 MB |
| Windows | Windows (DD) | 任何 | 512 MB |
| Windows | Windows (ISO) | Vista ~ 11 / Server 2008 ~ 2025 | 512 MB ~ 1 GB |

---

## 二、快速开始：安装飞牛NAS (fnOS)

### 2.1 一键安装命令

**国外服务器**：

```bash
curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh
bash reinstall.sh fnos
```

**国内服务器（加速下载）**：

```bash
curl -O https://cnb.cool/bin456789/reinstall/-/git/raw/main/reinstall.sh
bash reinstall.sh fnos
```

### 2.2 安装步骤详解

**步骤1：连接服务器 SSH**

使用 SSH 客户端连接您的 VPS 服务器。

**步骤2：下载并执行脚本**

```bash
# 下载脚本
curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh

# 执行安装飞牛NAS
bash reinstall.sh fnos
```

**步骤3：设置密码**

脚本会提示输入 root 密码（用于后续 SSH 登录和管理后台）。不输入则使用随机密码。

**步骤4：设置系统盘大小**

- 默认系统盘大小为 8GB
- 如果您的硬盘空间充足，建议设置 16GB 或更大
- 系统盘用于安装 fnOS 和基础应用，数据应存储在数据盘中

**步骤5：等待安装完成**

脚本会自动完成以下操作：
1. 下载 fnOS 镜像
2. 分区和格式化系统盘
3. 写入 fnOS 系统
4. 配置引导程序

**步骤6：重启并访问**

安装完成后，通过 `reboot` 命令重启服务器。等待 3-5 分钟后，访问：

```
http://服务器IP:5666
```

进入飞牛NAS初始化界面，设置管理员账户即可开始使用。

### 2.3 初始化配置

1. 访问 `http://服务器IP:5666`
2. 点击"开始 NAS 之旅"
3. 设置设备名称和管理员账户密码
4. 完成初始化

### 2.4 后续配置

**开启 SSH 服务**：

飞牛NAS默认关闭SSH权限，需要手动开启：
1. 登录 fnOS Web 管理界面
2. 进入"设置" → "终端"
3. 开启 SSH 服务
4. 设置 SSH 端口（默认22）

**创建存储池**：

1. 进入"存储" → "硬盘"
2. 初始化数据硬盘
3. 创建存储池（RAID 类型可选）
4. 创建共享文件夹

---

## 三、系统架构与工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    当前系统（Linux/Windows）                │
│                    执行 reinstall.sh                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    下载 fnOS / Linux / Windows 镜像
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    修改 Bootloader 配置                     │
│  (GRUB / syslinux / Windows BCD)                           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                         重启服务器
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    飞牛NAS安装程序启动                     │
│  (Cloud Image 写入 / Debian Installer / Windows Setup)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    自动完成系统安装与配置
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    飞牛NAS启动完成                          │
│                    Web管理界面: http://IP:5666              │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、功能二：安装 FygoOS

FygoOS 是另一款国产 NAS 系统，与 fnOS 类似。

```bash
bash reinstall.sh fygoos
```

安装步骤与 fnOS 相同。

---

## 五、功能三：安装其他 Linux 发行版

### 5.1 常用发行版命令

```bash
# Debian 12
bash reinstall.sh debian 12

# Ubuntu 24.04 LTS
bash reinstall.sh ubuntu 24.04

# Alpine Linux 3.24（轻量级，最小配置仅需 256MB 内存）
bash reinstall.sh alpine 3.24

# CentOS Stream 9
bash reinstall.sh centos 9

# Rocky Linux 9
bash reinstall.sh rocky 9

# Arch Linux（滚动版）
bash reinstall.sh arch

# Fedora 44
bash reinstall.sh fedora 44
```

### 5.2 可选参数

| 参数 | 说明 |
| ---- | ---- |
| `--username USERNAME` | 设置用户名 |
| `--password PASSWORD` | 设置密码 |
| `--ssh-key KEY` | 设置 SSH 公钥 |
| `--ssh-port PORT` | 修改 SSH 端口 |
| `--hold 1` | 仅重启到安装环境，不运行安装（用于测试网络） |
| `--hold 2` | 安装结束后不重启 |

**示例：安装 Debian 12，预设密码和 SSH 密钥**

```bash
bash reinstall.sh debian 12 \
  --password "MySecureP@ss123" \
  --ssh-key "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAA... user@example.com"
```

---

## 六、功能四：安装 Windows

### 6.1 一键安装 Windows

```bash
# Windows Server 2025
bash reinstall.sh windows 2025

# Windows 11
bash reinstall.sh windows 11

# Windows Server 2022
bash reinstall.sh windows 2022
```

### 6.2 支持的 Windows 版本

| 类型 | 版本 | 内存要求 | 硬盘要求 |
| ---- | ---- | -------- | -------- |
| 桌面版 | Windows Vista / 7 / 8.x / 10 / 11 | 512 MB ~ 1 GB | 25 GB |
| 服务器版 | Server 2008 ~ 2025 | 512 MB ~ 1 GB | 25 GB |

### 6.3 Windows 安装后配置

安装完成后通过 RDP 连接：

- **地址**：`服务器IP:3389`
- **用户名**：`Administrator`
- **密码**：安装时设置的密码

> 💡 **提示**：首次登录后建议：
> 1. 修改默认 Administrator 密码
> 2. 开启 Windows Update
> 3. 配置防火墙

---

## 七、功能五：DD Raw 镜像

如果官方不支持您需要的系统，可以使用 DD 模式安装任意 raw 镜像：

```bash
bash reinstall.sh dd --img="https://example.com/custom-image.img.gz"
```

支持的镜像格式：.img、.img.gz、.img.xz、.raw、.raw.gz

---

## 八、常见问题与解决方案

### 8.1 飞牛NAS安装后无法访问 Web 界面

| 检查项 | 解决方案 |
| ------ | -------- |
| 服务未启动 | 等待 3-5 分钟让系统完全启动 |
| 端口被防火墙拦截 | 在商家控制台开放 5666 端口 |
| IP 地址错误 | 检查服务器当前 IP 地址 |
| 服务故障 | 通过 VNC 重启服务器 |

### 8.2 SSH 无法连接

1. 确认 fnOS 中已开启 SSH 服务
2. 检查 SSH 端口是否为默认 22
3. 通过 VNC 登录检查 SSH 服务状态
4. 确认密码正确（区分大小写）

### 8.3 内存不足

fnOS 最低要求 512MB 内存，但如果运行 Docker 等应用，建议：

| 场景 | 最低内存 |
| ---- | -------- |
| 纯 fnOS 基本功能 | 512 MB |
| 运行 1-2 个 Docker 应用 | 1 GB |
| 运行 5+ Docker 应用 | 2 GB+ |
| 媒体服务器等重载应用 | 4 GB+ |

### 8.4 硬盘空间不足

fnOS 系统盘默认 8GB，如果提示空间不足：

1. 重新执行安装脚本，设置更大的系统盘大小
2. 或将数据存储在独立的数据硬盘上

### 8.5 OpenVZ / LXC 容器

❌ **不支持**：本脚本需要直接操作硬盘和引导程序，不支持 OpenVZ、LXC 等容器环境。

**解决方案**：
- 联系商家开通 KVM/VMware 类型的 VPS
- 或使用 OsMutation（仅支持系统切换，不支持完整安装）：https://github.com/LloydAsp/OsMutation

### 8.6 国内服务器下载速度慢

使用国内镜像加速：

```bash
curl -O https://cnb.cool/bin456789/reinstall/-/git/raw/main/reinstall.sh
bash reinstall.sh fnos
```

---

## 九、安全建议

| 建议 | 说明 |
| ---- | ---- |
| **修改默认密码** | 立即修改 root 和管理员账户密码 |
| **开启 SSH 密钥登录** | 禁用密码登录，使用 SSH 公钥 |
| **修改 SSH 端口** | 将默认 22 端口改为其他端口 |
| **配置防火墙** | 仅开放必要端口（5666、22等） |
| **开启自动更新** | 保持系统和应用更新 |
| **定期备份** | 重要数据定期备份 |

---

## 十、社区与生态

- **项目仓库**：[https://github.com/bin456789/reinstall](https://github.com/bin456789/reinstall)
- **问题反馈**：[GitHub Issues](https://github.com/bin456789/reinstall/issues)
- **飞牛NAS官网**：[https://www.fnnas.com](https://www.fnnas.com)
- **飞牛NAS论坛**：[https://club.fnnas.com](https://club.fnnas.com)

---

## 十一、总结

reinstall 脚本是 VPS 用户安装飞牛NAS的利器，只需一条命令即可将任意 Linux VPS 转换为功能完善的私有 NAS 系统。相比传统的物理机安装方式，它具有以下优势：

- **零门槛**：无需制作启动盘，无需进入 BIOS 设置，一行命令完成安装
- **速度快**：3-5 分钟即可完成安装并访问 Web 界面
- **资源占用低**：512MB 内存即可运行，适合低配 VPS
- **灵活切换**：支持在 fnOS、Debian、Ubuntu、Windows 等系统间任意切换
- **可视化运维**：安装完成后通过 Web 界面管理，无需命令行操作

> **立即体验**：执行 `curl -O https://raw.githubusercontent.com/bin456789/reinstall/main/reinstall.sh && bash reinstall.sh fnos` 即可在一台 Linux VPS 上安装飞牛NAS系统。
