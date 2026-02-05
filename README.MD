# SAP MCP 服务器

## 功能特性

### 核心功能

1. **AI 驱动的工具管理**：利用 AI 技术检索和管理 SAP_MCP 工具列表数据，实现智能工具发现和分类
2. **智能工具详情查询**：借助 AI 能力通过工具 ID 获取全面的工具详情，包括结构化的输入/输出参数和使用模式
3. **AI 增强的工具执行**：应用 AI 驱动的数据转换将输入转换为 SAP 可识别的格式，调用 SAP_MCP 工具提供优化的执行结果

该项目利用 AI 技术将 SAP 系统工具发布为 MCP 服务，为将前沿 AI 能力集成到 SAP 系统中提供了可行的解决方案。

### Web 管理界面

1. **服务状态管理**：
   - 查看 MCP 服务运行状态
   - 启动/停止 MCP 服务
   - 实时查看服务日志
   - 端口占用检测和冲突处理

2. **配置管理**：
   - SAP 系统配置（Base URL、Client ID、用户名、密码、超时）
   - MCP 服务器配置（主机、端口、路径）
   - 实时配置文件保存

3. **工具管理**：
   - 浏览和搜索 SAP MCP 工具
   - 查看工具详情和参数
   - 通过交互式表单执行工具

4. **日志管理**：
   - 查看带有过滤选项的日志
   - 确认后清除日志
   - 实时日志更新

## 部署

### 前置条件

- Python 3.8 或更高版本
- Git（可选，用于克隆仓库）
- 网络连接（用于安装依赖）

### 1. 手动部署

#### 1.1 获取项目代码

**方法 1：从 Git 仓库克隆**
```bash
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP
```

**方法 2：直接复制文件**
- 将整个项目文件夹复制到您的服务器

#### 1.2 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 1.3 安装依赖

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

#### 1.4 配置项目

```bash
# 复制配置示例文件
cp config.example.py config.py

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

#### 1.5 启动服务

##### 方法 1：仅启动 MCP 服务器

```bash
# 启动 MCP 服务器
python server/sap_mcp_server.py
```

##### 方法 2：启动 Web 管理界面

```bash
# 启动 Web 管理界面
python -m uvicorn web.main:app --host 0.0.0.0 --port 8080
```

### 2. Docker 部署

#### 2.1 前置条件

- 系统已安装 Docker
- 系统已安装 Docker Compose

#### 2.2 使用 Docker Compose 构建和运行

```bash
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

### Services

- **sap-mcp-server**: SAP MCP Server running on port 8000
- **sap-mcp-web**: Web management interface running on port 8080

### Access the Application

1. **Web Management Interface**: Open your browser and navigate to `http://localhost:8080`
2. **MCP Server**: The server is available at `http://localhost:8000/mcp` for client connections

### Configuration

The `config.py` file is mounted as a volume in both containers, so you can modify it on the host machine and the changes will be reflected in the containers.

### Logs

Logs are stored in a Docker volume named `log_volume` and can be accessed from within the containers at `/app/log/sap_api.log`.

### Customization

You can customize the Docker configuration by modifying the following files:

- `Dockerfile`: For customizing the base image and build process
- `docker-compose.yml`: For customizing services, ports, volumes, and environment variables
- `.dockerignore`: For excluding files from the Docker build context

## Developers

- **Product Design**: Mark (Wu Rangyu)
- **Developer**: Mark (Wu Rangyu)
- **Phone**: 18685095797
- **QQ**: 121980331
- **Email**: 121980331@qq.com

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
