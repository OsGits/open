# OpenDataV - 纯前端拖拽式数据可视化平台

> 纯前端拖拽式数据可视化平台，无需后端即可快速搭建炫酷大屏

---

## 📖 项目介绍

**OpenDataV** 是一款纯前端的拖拽式数据可视化平台，基于 Vue3 + TypeScript 构建。它支持图层编辑、组件定制、数据接入与接口管理，适合快速搭建酷炫大屏和低代码场景下的可视化应用。

### About

OpenDataV is a pure frontend drag-and-drop data visualization platform built with Vue3 + TypeScript. It supports layer editing, component customization, data integration and API management, perfect for quickly building visual dashboards in low-code scenarios.

---

## 🔑 核心特点

> 💡 开源地址：https://gitee.com/small_bud_star/OpenDataV

### 主要功能

- 🎨 **拖拽编辑**：可视化拖拽组件，无需编码
- 📊 **丰富组件**：多种数据可视化组件可选
- 🔌 **数据接入**：支持API、静态JSON等多种数据源
- 🎭 **主题定制**：灵活的主题和样式配置
- 📱 **响应式设计**：适配多种屏幕尺寸
- 🛠️ **组件扩展**：支持自定义组件开发

### 技术栈

- Vue3
- TypeScript
- Element Plus
- ECharts / AntV

---

## 🛠️ 安装方法

### 前置要求

- Node.js 16+ （推荐 Node.js 18）
- npm 或 yarn 或 pnpm
- Git

### 方式一：直接下载（推荐）

```bash
# 克隆项目
git clone https://gitee.com/small_bud_star/OpenDataV.git

# 进入项目目录
cd OpenDataV

# 安装依赖
npm install

# 或使用yarn
yarn install

# 或使用pnpm
pnpm install
```

### 方式二：使用Docker

```bash
# 拉取镜像
docker pull smallbudstar/opendatav

# 运行容器
docker run -d -p 8080:80 --name opendatav smallbudstar/opendatav

# 访问 http://localhost:8080
```

### 步骤3：启动开发服务器

```bash
# 开发模式启动
npm run dev

# 访问 http://localhost:5173
```

### 步骤4：构建生产版本

```bash
# 构建生产版本
npm run build

# 构建产物在 dist 目录下
```

---

## 📝 快速开始

### 创建自定义组件

```typescript
// src/components/custom/MyChart.vue
<template>
  <div class="my-chart">
    <div ref="chartRef" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps<{
  data: any
  config: any
}>()

const chartRef = ref<HTMLElement>()

onMounted(() => {
  initChart()
})

function initChart() {
  if (!chartRef.value) return
  const chart = echarts.init(chartRef.value)
  chart.setOption({
    title: { text: props.config?.title || '图表' },
    series: [{ data: props.data || [] }]
  })
}
</script>
```

### 接入API数据

```typescript
// 在组件中请求API
import { request } from '@/utils/request'

const fetchData = async () => {
  const res = await request.get('/api/your-data-source')
  console.log(res.data)
}

// 或使用配置式数据源
const dataSource = {
  type: 'fetch',
  url: 'https://api.example.com/data',
  method: 'GET',
  interval: 5000  // 5秒刷新一次
}
```

---

## 🎨 组件开发

### 创建新组件

```bash
# 在 src/components 目录下创建组件
mkdir -p src/components/custom/YourComponent

# 创建组件文件
touch src/components/custom/YourComponent/index.vue
```

### 注册组件

```typescript
// src/config/components.ts
import YourComponent from './custom/YourComponent/index.vue'

export default {
  yourComponent: {
    component: YourComponent,
    name: '自定义组件',
    icon: 'chart',
    props: {
      title: { type: 'string', default: '标题' },
      data: { type: 'array', default: [] }
    }
  }
}
```

---

## 🔧 Nginx部署

### 生产环境配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/OpenDataV/dist;
    index index.html;

    # SPA路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API代理（如需要）
    location /api/ {
        proxy_pass http://backend-server:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 重载Nginx配置
nginx -s reload
```

---

## 📊 项目信息

| 项目 | 信息 |
|------|------|
| 开源协议 | Apache-2.0 |
| 语言 | Vue3 + TypeScript |
| 平台 | Gitee |
| 类型 | 前端工具 |

---

## 🔗 相关链接

- Gitee: https://gitee.com/small_bud_star/OpenDataV
- GitHub: https://github.com/smallbudstar/OpenDataV
- 前后端均开源，持续迭代中

---

#### 🔗 方向

[← 返回项目首页](README.md)

---
