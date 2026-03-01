# SAP MCP 服务器

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg)](https://fastapi.tiangolo.com)

将 SAP 系统工具发布为 MCP 服务，为 AI 能力集成到 SAP 系统提供解决方案

**Languages:** [English](README_EN.MD) | [日本語](README_JA.MD)

</div>

---

## 🚀 项目特点

### 核心功能

- **AI 驱动的工具管理**：利用 AI 技术检索和管理 SAP_MCP 工具列表数据，实现智能工具发现和分类
- **智能工具详情查询**：借助 AI 能力通过工具 ID 获取全面的工具详情，包括结构化的输入/输出参数和使用模式
- **AI 增强的工具执行**：应用 AI 驱动的数据转换将输入转换为 SAP 可识别的格式，调用 SAP_MCP 工具提供优化的执行结果

### 项目优势
- 一次部署，长期使用。通过在SAP系统中配置表管理工具列表，无需每次更新代码
  
### 增强功能
- 本服务可以使多种AI工具集成：
  - 聊天工具（如ChatGPT,Cheery Studio）
  - 编程工具（如Curse,Claude Code）
  - 平台工具（如Langchain,Dify）

## 🎨 Web 管理界面

### 服务状态管理
- 实时查看 MCP 服务运行状态
- 一键启动/停止 MCP 服务
- 实时查看服务日志
- 端口占用检测和冲突处理

### 配置管理
- SAP 系统配置（Base URL、Client ID、用户名、密码、超时）
- MCP 服务器配置（主机、端口、路径）
- WEB 管理界面配置（端口、路径）
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

### 部署方式

详细的安装、配置和使用步骤请参考：[操作指南](/Doc/USAGE/USAGE_ZH.md)

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
