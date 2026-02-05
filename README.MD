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

#### 2.3 离线 Docker 部署（适用于网络受限环境）

1. **在可访问网络的环境中下载镜像：**
   ```bash
   # 拉取 Python 基础镜像
   docker pull python:3.10-slim
   
   # 保存镜像到本地文件
   docker save python:3.10-slim -o python-3.10-slim.tar
   ```

2. **将镜像文件传输到目标服务器**（使用 USB 或其他方法）

3. **在目标服务器上加载镜像：**
   ```bash
   docker load -i python-3.10-slim.tar
   ```

4. **构建并运行：**
   ```bash
   # 构建项目镜像
   docker build -t sap-mcp .
   
   # 运行容器
   docker run -d -p 8000:8000 -p 8080:8080 sap-mcp
   ```

### 4. Docker 部署重要注意事项

#### 4.1 Docker 的主机配置

在 Docker 容器中运行时，必须将 MCP 服务器配置为监听所有网络接口（0.0.0.0），而不仅仅是本地主机（127.0.0.1）。默认配置文件中已经正确设置，但如果您修改了它，请确保：

```python
# MCP 服务器配置
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",  # 重要：Docker 部署必须为 0.0.0.0
    "port": 8000,
    "path": "/mcp"
}
```

如果您将 `host` 设置为 `127.0.0.1`，MCP 服务将只能在容器内部访问，而无法从外部访问。

#### 4.2 端口映射

确保 Web 界面端口（8080）和 MCP 服务端口（8000）在 Docker 配置中正确映射：

```yaml
# 在 docker-compose.yml 中
ports:
  - "8080:8080"  # Web 管理界面
  - "8000:8000"  # MCP 服务
```

### 5. 访问应用

- **Web 管理界面**：打开浏览器并导航至 `http://server-ip:8080`
- **MCP 服务器**：服务器在 `http://server-ip:8000/mcp` 可用于客户端连接

### 6. 常见问题

#### 6.1 端口冲突

如果端口被占用，请修改 `config.py` 中的端口号：

```python
# 修改 MCP 服务器端口
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8001,  # 更改为其他端口
    "path": "/mcp"
}
```

#### 6.2 依赖安装失败

如果依赖安装失败，请尝试使用国内镜像源：

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

#### 6.3 服务启动失败

查看日志文件 `log/sap_api.log` 获取详细错误信息：

```bash
# 查看日志文件
cat log/sap_api.log
```

#### 6.4 MCP 服务无法从 Docker 容器外部访问

**问题**：通过 Web 管理界面启动 MCP 服务后，服务无法从 Docker 容器外部访问。

**解决方案**：
1. 确保 MCP 服务配置为监听所有网络接口（`0.0.0.0`）：
   ```python
   # 在 config.py 中
   MCP_SERVER_CONFIG = {
       "host": "0.0.0.0",  # Docker 部署必须为 0.0.0.0
       "port": 8000,
       "path": "/mcp"
   }
   ```
2. 确保端口在 `docker-compose.yml` 中正确映射：
   ```yaml
   # 在 docker-compose.yml 中
   ports:
     - "8000:8000"  # 映射 MCP 服务端口
   ```
3. 修改后重启 Docker 服务

**根本原因**：如果服务仅监听 `127.0.0.1`，则只能在容器内部访问，无法从外部访问。

### 7. 服务管理

#### 7.1 停止服务

- **按 Ctrl+C** 停止运行中的服务
- 或使用 `kill` 命令终止进程

#### 7.2 重启服务

只需重新执行启动命令即可。

### 8. 监控和维护

- 定期检查日志文件：`log/sap_api.log`
- 定期更新依赖：`pip install -r requirements.txt --upgrade`
- 定期备份配置文件：`config.py`

## 开发者

- **产品设计**：Mark（吴让宇）
- **开发者**：Mark（吴让宇）
- **电话**：18685095797
- **QQ**：121980331
- **邮箱**：121980331@qq.com

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
