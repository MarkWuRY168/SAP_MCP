# SAP MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 项目概述

SAP MCP（Model Context Protocol）Server是一个用于管理和控制SAP系统的平台，提供了一系列工具和接口，方便用户与SAP系统进行交互。

## 功能特性

### 核心功能

1. **工具清单管理**：获取SAP_MCP工具清单数据
2. **工具明细查询**：根据工具号获取工具明细，包括传入传出参数
3. **工具执行**：根据工具明细，将数据转换为可识别的格式，调用SAP_MCP工具获取执行结果

### Web管理界面

1. **服务状态管理**：
   - 查看MCP服务运行状态
   - 启动/停止MCP服务
   - 实时查看服务日志
   - 端口占用检测和冲突处理

2. **配置管理**：
   - SAP系统配置（Base URL、Client ID、用户名、密码、超时时间）
   - MCP服务器配置（主机、端口、路径）
   - 配置文件实时保存

3. **工具管理**：
   - 浏览和搜索SAP MCP工具
   - 查看工具详情和参数
   - 通过交互式表单执行工具
   - 查看工具执行结果

4. **日志管理**：
   - 查看带过滤选项的服务日志
   - 带确认的日志清空
   - 实时日志更新

## 项目结构

```
SAP_MCP/
├── .gitignore                  # Git忽略文件
├── LICENSE                     # MIT许可证
├── README.md                   # 项目说明文档
├── CHANGELOG.md                # 变更日志
├── pyproject.toml            # 项目配置文件
├── requirements.txt           # 项目依赖
├── config.py                 # 配置文件（不提交到版本控制）
├── config.example.py         # 配置文件示例
├── server/                   # 服务器模块
│   ├── __init__.py          # 包初始化文件
│   ├── sap_mcp_server.py   # MCP服务器
│   ├── sap_mcp_client.py   # MCP客户端
│   └── http_client.py      # HTTP客户端
├── web/                      # Web管理模块
│   ├── static/               # 静态文件（CSS、JS）
│   ├── templates/            # HTML模板
│   └── main.py              # Web服务器入口文件
├── log/                      # 日志文件目录
└── mcpDemo/                 # MCP示例代码
    ├── my_server.py        # 示例服务器
    └── my_client.py        # 示例客户端
```

## 技术栈

- **Python**：>= 3.8
- **FastMCP**：MCP协议实现
- **httpx**：HTTP客户端
- **pydantic**：数据验证和设置管理
- **FastAPI**：Web管理界面框架
- **Uvicorn**：ASGI服务器
- **Bootstrap 5**：前端CSS框架

## 安装说明

### 环境要求

- Python 3.8 或更高版本
- SAP系统访问权限

### 安装步骤

1. **克隆项目**：
   ```bash
   git clone https://github.com/example/sap-mcp.git
   cd SAP_MCP
   ```

2. **创建虚拟环境**（推荐）：
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

4. **配置应用**：
   ```bash
   cp config.example.py config.py
   # 编辑 config.py，填入实际配置信息
   ```

## 配置说明

### SAP接口配置

在 `config.py` 文件中配置SAP接口信息：

```python
SAP_CONFIG = {
    "base_url": "http://sap-s4d-app.example.com:8000/sap/zmcp",
    "client_id": "300",
    "sap-user": "YOUR_SAP_USER",
    "sap-password": "YOUR_SAP_PASSWORD",
    "timeout": 30
}
```

### MCP服务器配置

```python
MCP_SERVER_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
    "path": "/mcp"
}
```

## 使用说明

### 启动服务

#### 方式一：使用Web管理界面

1. 启动Web管理界面：
   ```bash
   python -m uvicorn web.main:app --reload --host 0.0.0.0 --port 8080
   ```

2. 打开Web浏览器，导航到 `http://localhost:8080`

3. 在Web界面中点击"启动服务"按钮

#### 方式二：命令行启动

1. 启动MCP服务器：
   ```bash
   python server/sap_mcp_server.py
   ```

2. 服务器将在 `http://127.0.0.1:8000/mcp` 上运行

### 使用Web管理界面

1. **服务管理页面**：
   - 查看服务运行状态
   - 启动/停止服务
   - 检查服务配置

2. **工具管理页面**：
   - 浏览和搜索SAP MCP工具
   - 查看工具详情和参数
   - 通过交互式表单执行工具
   - 查看工具执行结果

3. **配置页面**：
   - 修改SAP接口配置
   - 修改MCP服务器配置
   - 保存配置更改

4. **日志页面**：
   - 查看带过滤选项的服务日志
   - 带确认的日志清空
   - 实时日志更新

### 客户端连接示例

```python
import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8000/mcp")
    async with client:
        # 获取工具清单
        result = await client.call_tool("get_tool_list", {})
        print(result)

asyncio.run(main())
```

### 调用工具示例

1. **获取工具清单**：
   ```python
   result = await client.call_tool("get_tool_list", {})
   ```

2. **获取工具明细**：
   ```python
   result = await client.call_tool("get_tool_details", {"TOOL_ID": "工具ID"})
   ```

3. **使用工具**：
   ```python
   result = await client.call_tool("use_tool", {
       "TOOL_ID": "工具ID",
       "参数名1": "值1",
       "参数名2": "值2"
   })
   ```

## 开发指南

### 代码风格

项目遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格规范。

使用以下工具进行代码格式化和检查：

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy .
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=server --cov-report=html
```

### 构建和发布

```bash
# 构建分发包
python -m build

# 发布到PyPI
python -m twine upload dist/*
```

## 故障排除

### 常见问题

1. **端口占用错误**：
   - 检查端口8000是否被其他程序占用
   - 修改 `config.py` 中的端口号

2. **SAP接口连接失败**：
   - 确认SAP服务器地址正确
   - 检查网络连接
   - 验证用户名和密码

3. **Web界面无响应**：
   - 检查Web服务器是否正在运行
   - 验证服务器日志中的错误
   - 重启Web服务器应用程序

## 开发人员

- **产品设计**：Mark（吴让宇）
- **开发人员**：Mark（吴让宇）
- **联系电话**：18685095797
- **QQ**：121980331
- **邮箱**：121980331@qq.com

## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 变更日志

详细的变更日志请查看 [CHANGELOG.md](CHANGELOG.md)。

## 支持

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/example/sap-mcp/issues)
- 发送邮件至：121980331@qq.com

## 致谢

感谢所有为本项目做出贡献的开发者！

---

**注意**：请勿将包含敏感信息的配置文件提交到版本控制系统。
