# SAP MCP 操作指南

本文档提供了 SAP MCP 项目的详细安装、配置和使用步骤。

## 目录

1. [前置条件](#前置条件)
2. [SAP Http接口服务激活](#sap-http接口服务激活)
3. [手动部署](#手动部署)
4. [Docker部署](#docker部署)
5. [使用指南](#使用指南)
6. [常见问题](#常见问题)

---

## 前置条件

- Python 3.8 或更高版本
- Git（可选，用于克隆仓库）
- 网络连接（用于安装依赖）
- 拥有SAP系统管理员权限

---

## SAP Http接口服务激活

在安装本项目前，需要在SAP系统中激活Http接口服务。请按照以下步骤操作：

### 步骤1：SAP系统程序代码导入

查看 SAP 请求导入程序文档，地址：`Request\SAP Request\Y_UPLOAD_TRANSPORT_REQUEST.md`

### 步骤2：执行SAP请求导入程序

执行SAP请求导入程序，导入开发包。

![SAP请求导入](Doc/Picture/image-1.png)

### 步骤3：SICF激活ZMCP服务

使用事务码 SICF 激活 ZMCP 服务，并测试服务正常使用。

![SICF服务激活](Doc/Picture/image-2.png)

### 步骤4：事务码ZMCP_CONFIG配置SAP工具列表

使用事务码 ZMCP_CONFIG 配置 SAP 工具列表。

![工具配置](Doc/Picture/image-3.png)

---

## 手动部署

### 1.1 获取项目代码

**方法 1：从 Git 仓库克隆**
```bash
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP
```

**方法 2：直接复制文件**
- 将整个项目文件夹复制到您的服务器

### 1.2 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 1.3 安装依赖

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

### 1.4 配置项目

```bash
# 复制配置示例文件
cp utils/config.example.py utils/config.py

# 编辑配置文件（根据您的环境修改）
# 您可以使用任何文本编辑器，例如
# notepad config.py      # Windows
# vim config.py          # Linux/Mac
```

**配置文件示例：**
```python
# SAP 接口配置
SAP_CONFIG = {
    "base_url": "http://your-sap-server:port/sap/zmcp",
    "client_id": "your-client-id",
    "sap-user": "your-sap-username",
    "sap-password": "your-sap-password",
    "timeout": 30
}

# MCP 服务器配置
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "path": "/mcp"
}
```

**环境变量配置：**

项目支持通过环境变量配置敏感信息，避免硬编码。以下是支持的环境变量：

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| MCP_HOST | MCP服务器主机 | 0.0.0.0 |
| MCP_PORT | MCP服务器端口 | 8000 |
| MCP_PATH | MCP服务器路径 | /mcp |
| WEB_HOST | Web服务器主机 | 0.0.0.0 |
| WEB_PORT | Web服务器端口 | 8080 |
| WEB_RELOAD | Web服务器自动重载（开发环境） | True |
| SAP_BASE_URL | SAP接口基础URL | - |
| SAP_CLIENT_ID | SAP客户端ID | - |
| SAP_SAP_USER | SAP用户名 | - |
| SAP_SAP_PASSWORD | SAP密码 | - |
| SAP_TIMEOUT | SAP请求超时时间（秒） | 30 |

您可以在启动服务前设置这些环境变量，或者创建一个 `.env` 文件来存储它们。

### 1.5 启动服务

#### 方法 1：仅启动 MCP 服务器

```bash
# 启动 MCP 服务器
python server/sap_mcp_server.py
```

#### 方法 2：启动 Web 管理界面

```bash
# 启动 Web 管理界面
python web/main.py
```

或者使用 uvicorn 直接启动：

```bash
# 启动 Web 管理界面
python -m uvicorn web.main:app --host 0.0.0.0 --port 8080
```

---

## Docker部署

### 2.1 前置条件

- 系统已安装 Docker
- 系统已安装 Docker Compose
- 网络连接正常（需要访问 Docker Hub）

### 2.2 使用 Docker Compose 构建和运行

```bash
# 进入 Docker 文件夹
cd Docker

# 构建并运行所有服务
docker-compose up -d

# 查看所有服务的日志
docker-compose logs -f

# 查看特定服务的日志
docker-compose logs -f sap-mcp-web

# 停止所有服务
docker-compose down

# 停止并移除卷
docker-compose down -v
```

### 2.3 服务说明

- **sap-mcp-server**: SAP MCP 服务器运行在端口 8000
- **sap-mcp-web**: Web 管理界面运行在端口 8080

### 2.4 访问应用

1. **Web 管理界面**: 打开浏览器并导航到 `http://localhost:8080`
2. **MCP 服务器**: 服务器可通过 `http://localhost:8000/mcp` 进行客户端连接
3. **API文档**: 
   - Swagger UI: `http://localhost:8080/docs`
   - ReDoc: `http://localhost:8080/redoc`
4. **健康检查**: `http://localhost:8080/api/health`

### 2.5 配置说明

`config.py` 文件被挂载为两个容器的卷，因此您可以在主机上修改它，更改将反映在容器中。

### 2.6 日志说明

日志存储在名为 `log_volume` 的 Docker 卷中，可从容器内的 `/app/log/sap_api.log` 访问。

### 2.7 自定义配置

您可以通过修改 `Docker` 文件夹中的以下文件来自定义 Docker 配置：

- `Dockerfile`: 用于自定义基础镜像和构建过程
- `docker-compose.yml`: 用于自定义服务、端口、卷和环境变量
- `.dockerignore`: 用于从 Docker 构建上下文中排除文件

---

## 使用指南

### 访问 Web 管理界面

启动服务后，在浏览器中打开：`http://localhost:8080`

### 服务管理页面

1. **查看服务状态**：显示 MCP 服务的当前运行状态
2. **启动服务**：点击"启动服务"按钮启动 MCP 服务器
3. **停止服务**：点击"停止服务"按钮停止 MCP 服务器
4. **查看日志**：实时查看服务运行日志

### 工具管理页面

1. **查看工具列表**：左侧显示所有可用的 SAP 工具
2. **搜索工具**：使用搜索框快速查找工具
3. **查看工具详情**：点击工具列表中的工具，右侧显示工具详情和参数
4. **执行工具**：
   - 在参数表单中填写参数值
   - 点击"执行工具"按钮
   - 查看执行结果

### 服务器配置页面

1. **SAP接口配置**：
   - 基础 URL
   - 客户端 ID
   - SAP 用户名
   - SAP 密码
   - 超时时间

2. **MCP服务器配置**：
   - 主机地址
   - 端口
   - 路径

3. **接口测试**：点击"接口测试"按钮验证 SAP 接口连接

4. **保存配置**：点击"保存配置"按钮保存所有配置

### 日志查看页面

1. **刷新日志**：点击"刷新日志"按钮查看最新日志
2. **日志级别过滤**：选择日志级别进行过滤
3. **清空日志**：点击"清空日志"按钮清空所有日志

---

## 常见问题

### Docker 部署常见问题

#### 问题 1：无法连接到 Docker Hub

如果遇到类似以下的错误：
```
failed to do request: Head "https://registry-1.docker.io/v2/library/ubuntu/manifests/22.04": dial tcp: connectex: A connection attempt failed
```

**解决方案：**

1. **检查网络连接**：确保您的网络可以访问 Docker Hub
2. **配置 Docker 镜像加速器**（推荐）：
   - 打开 Docker Desktop
   - 进入 Settings > Docker Engine
   - 添加以下配置：
   ```json
   {
     "registry-mirrors": [
       "https://docker.mirrors.ustc.edu.cn",
       "https://hub-mirror.c.163.com",
       "https://mirror.baidubce.com"
     ]
   }
   ```
   - 点击 "Apply & Restart"

3. **使用代理**（如果需要）：
   - 打开 Docker Desktop
   - 进入 Settings > Resources > Proxies
   - 配置您的代理服务器

4. **手动拉取镜像**：
   ```bash
   docker pull ubuntu:22.04
   docker-compose up -d
   ```

#### 问题 2：构建失败

如果构建过程中出现错误，可以尝试：

```bash
# 清理之前的构建缓存
docker-compose down
docker system prune -a

# 重新构建
docker-compose up -d --build
```

### MCP 服务无法访问

**问题**：通过 Web 管理界面启动 MCP 服务后，无法从外部访问。

**解决方案**：

1. 确保 MCP 服务器配置的 host 为 `0.0.0.0`（而不是 `127.0.0.1`）
2. 确保端口映射正确配置
3. 检查防火墙设置

### 配置文件修改后不生效

**问题**：修改配置文件后，服务没有使用新配置。

**解决方案**：

1. 重启 Web 管理界面服务
2. 停止并重新启动 MCP 服务

---

## 技术支持

如有问题，请联系：

- **产品设计**: Mark (Wu Rangyu)
- **开发者**: Mark (Wu Rangyu)
- **电话**: 18685095797
- **QQ**: 121980331
- **邮箱**: 121980331@qq.com
