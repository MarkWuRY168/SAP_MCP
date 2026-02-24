# SAP MCP 服务器

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg)](https://fastapi.tiangolo.com)

将 SAP 系统工具发布为 MCP 服务，为 AI 能力集成到 SAP 系统提供解决方案

</div>

---

## 🚀 项目特点

### 核心功能

- **AI 驱动的工具管理**：利用 AI 技术检索和管理 SAP_MCP 工具列表数据，实现智能工具发现和分类
- **智能工具详情查询**：借助 AI 能力通过工具 ID 获取全面的工具详情，包括结构化的输入/输出参数和使用模式
- **AI 增强的工具执行**：应用 AI 驱动的数据转换将输入转换为 SAP 可识别的格式，调用 SAP_MCP 工具提供优化的执行结果

### 增强功能

- **健康检查**：添加了健康检查端点，可监控服务状态和 SAP 接口连接状态
- **环境变量支持**：支持通过环境变量配置敏感信息，提高安全性
- **日志轮转**：实现了日志文件自动轮转，避免日志文件过大
- **性能优化**：
  - 添加了缓存机制，减少重复请求
  - 改进了 HTTP 客户端，使用连接池和重试机制
  - 实现了指数退避策略，提高请求成功率
- **API 文档**：集成了 FastAPI 的自动文档生成功能，可通过 `/docs` 和 `/redoc` 访问
- **代码结构优化**：重构了代码结构，移除了重复代码，添加了工具函数模块

## 🎨 Web 管理界面

### 服务状态管理
- 实时查看 MCP 服务运行状态
- 一键启动/停止 MCP 服务
- 实时查看服务日志
- 端口占用检测和冲突处理

### 配置管理
- SAP 系统配置（Base URL、Client ID、用户名、密码、超时）
- MCP 服务器配置（主机、端口、路径）
- 实时配置文件保存
- 接口连接测试功能

### 工具管理
- 浏览和搜索 SAP MCP 工具
- 查看工具详情和参数
- 通过交互式表单执行工具
- 智能参数解析和展示

### 日志管理
- 查看带有过滤选项的日志
- 确认后清除日志
- 实时日志更新

## 🛠️ 快速开始

### 前置条件

- Python 3.8 或更高版本
- Docker（可选，用于容器化部署）
- 拥有 SAP 系统管理员权限

### 方式一：Docker 部署（推荐）

```bash
# 进入 Docker 文件夹
cd Docker

# 构建并运行所有服务
docker-compose up -d
```

访问 Web 管理界面：http://localhost:6680（默认端口）

### 方式二：手动部署

```bash
# 克隆项目
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置项目
cp utils/config.example.py utils/config.py
# 编辑配置文件...

# 启动服务
python web/main.py
```

访问 Web 管理界面：http://localhost:6680（默认端口）

## 📖 详细文档

详细的安装、配置和使用步骤请参考：[操作指南](Doc/USAGE.md)

## 🔗 访问地址

- **Web 管理界面**: http://localhost:6680
- **MCP 服务器**: http://localhost:6688/mcp
- **API 文档 (Swagger UI)**: http://localhost:6680/docs
- **API 文档 (ReDoc)**: http://localhost:6680/redoc
- **健康检查**: http://localhost:6680/api/health  

## 🛡️ 安全性

- 配置文件已添加到 `.gitignore`，不会被提交到版本控制
- 支持通过环境变量配置敏感信息
- 提供配置示例文件 `utils/config.example.py`

## 👥 开发者

- **产品设计**: Mark (Wu Rangyu)
- **开发者**: Mark (Wu Rangyu)
- **电话**: 18685095797
- **QQ**: 121980331
- **邮箱**: 121980331@qq.com

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

<div align="center">
  <sub>如果这个项目对你有帮助，请给我们一个 ⭐️ 星标！</sub>
</div>
