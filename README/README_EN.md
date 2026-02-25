# SAP MCP Server

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg)](https://fastapi.tiangolo.com)

Publish SAP system tools as MCP services, providing solutions for integrating AI capabilities into SAP systems

**Languages:** [中文](README_ZH.MD) | [日本語](README_JA.MD)

</div>

---**Languages:** [中文](README_ZH.MD) | [日本語](README_JA.MD)

</div>

---

## 🚀 Project Features

### Core Features
- **AI-Driven Tool Management**: Utilize AI technology to retrieve and manage SAP_MCP tool list data, enabling intelligent tool discovery and categorization
- **Intelligent Tool Detail Query**: Leverage AI capabilities to obtain comprehensive tool details through tool IDs, including structured input/output parameters and usage patterns
- **AI-Enhanced Tool Execution**: Apply AI-driven data transformation to convert inputs into SAP-recognizable formats, calling SAP_MCP tools to provide optimized execution results

### Enhanced Features
- **Health Check**: Added health check endpoints to monitor service status and SAP interface connection status
- **Environment Variable Support**: Support configuring sensitive information through environment variables for improved security
- **Log Rotation**: Implemented automatic log file rotation to prevent log files from becoming too large
- **Performance Optimization**:
  - Added caching mechanisms to reduce duplicate requests
  - Improved HTTP client with connection pooling and retry mechanisms
  - Implemented exponential backoff strategy to improve request success rates
- **API Documentation**: Integrated FastAPI's automatic documentation generation feature, accessible via `/docs` and `/redoc`
- **Code Structure Optimization**: Refactored code structure, removed duplicate code, added utility function modules

## 🎨 Web Management Interface

### Service Status Management
- Real-time view of MCP service running status
- One-click start/stop MCP service
- Real-time view of service logs
- Port occupancy detection and conflict handling

### Configuration Management
- SAP system configuration (Base URL, Client ID, username, password, timeout)
- MCP server configuration (host, port, path)
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

## 🛠️ Quick Start

### Prerequisites

- Python 3.8 or higher
- SAP system administrator privileges

### Deployment

```bash
# Clone project
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure project
cp utils/config.example.py utils/config.py
# Edit configuration file...

# Start service
python web/main.py
```

Access Web Management Interface: http://localhost:6680 (default port)

## 📖 Detailed Documentation

For detailed installation, configuration, and usage steps, please refer to: [User Guide](Doc/USAGE.md)

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
