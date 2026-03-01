# SAP MCP Server

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg)](https://fastapi.tiangolo.com)

Publish SAP system tools as MCP services, providing solutions for integrating AI capabilities into SAP systems

**Languages:** [中文](/DOC/README_ZH.MD) | [日本語](/DOC/README_JA.MD)

</div>

---

## 🚀 Project Features

### Core Features
- **AI-Driven Tool Management**: Utilize AI technology to retrieve and manage SAP_MCP tool list data, enabling intelligent tool discovery and categorization
- **Intelligent Tool Detail Query**: Leverage AI capabilities to obtain comprehensive tool details through tool IDs, including structured input/output parameters and usage patterns
- **AI-Enhanced Tool Execution**: Apply AI-driven data transformation to convert inputs into SAP-recognizable formats, calling SAP_MCP tools to provide optimized execution results

### Project Advantages
- Deploy once, use long-term. Manage tool lists through configuration tables in SAP system without needing to update code each time

### Enhanced Features
- This service enables integration with multiple AI tools:
  - Chat tools (e.g., ChatGPT, Cherry Studio)
  - Programming tools (e.g., Cursor, Claude Code)
  - Platform tools (e.g., LangChain, Dify)

## 🎨 Web Management Interface

### Service Status Management
- Real-time view of MCP service running status
- One-click start/stop MCP service
- Real-time view of service logs
- Port occupancy detection and conflict handling

### Configuration Management
- SAP system configuration (Base URL, Client ID, username, password, timeout)
- MCP server configuration (host, port, path)
- Web management interface configuration (port, path)
- Real-time configuration file saving
- Interface connection testing functionality

### Tool Management
- Browse and search SAP MCP tools
- View tool details and parameters
- Execute tools through interactive forms
- Intelligent parameter parsing and display

### Log Management
- View logs with filtering options
- Clear logs after confirmation
- Real-time log updates

### Deployment

For detailed installation, configuration, and usage steps, please refer to: [User Guide](/Doc/USAGE/USAGE_EN.md)

## 🔗 Access Addresses

- **Web Management Interface**: http://localhost:6680
- **MCP Server**: http://localhost:6688/mcp
- **API Documentation (Swagger UI)**: http://localhost:6680/docs
- **API Documentation (ReDoc)**: http://localhost:6680/redoc
- **Health Check**: http://localhost:6680/api/health

## 🛡️ Security

- Configuration files added to `.gitignore`, will not be committed to version control
- Support configuring sensitive information through environment variables
- Provide configuration example file `utils/config.example.py`

## 👥 Developer

- **Product Designer**: Mark (Wu Rangyu)
- **Developer**: Mark (Wu Rangyu)
- **Phone**: 18685095797
- **QQ**: 121980331
- **Email**: 121980331@qq.com

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>If this project helps you, please give us a ⭐️ star!</sub>
</div>
