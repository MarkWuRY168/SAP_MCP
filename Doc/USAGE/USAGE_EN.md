# SAP MCP User Guide

This document provides detailed installation, configuration, and usage steps for the SAP MCP project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [SAP Http Interface Service Activation](#sap-http-interface-service-activation)
3. [Manual Deployment](#manual-deployment)
4. [Usage Guide](#usage-guide)
5. [Common Issues](#common-issues)

---

## Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning repository)
- Network connection (for installing dependencies)
- SAP system administrator privileges

---

## SAP Http Interface Service Activation

Before installing this project, you need to activate the Http interface service in the SAP system. Follow these steps:

### Step 1: SAP System Program Code Import

Refer to the SAP request import program documentation at: `Request\SAP Request\Y_UPLOAD_TRANSPORT_REQUEST.md`

### Step 2: Execute SAP Request Import Program

Execute the SAP request import program to import the development package.

![SAP Request Import](/Doc/Picture/image-1.png)

### Step 3: Activate ZMCP Service via SICF

Use transaction code SICF to activate the ZMCP service and test that the service is working properly.

![SICF Service Activation](/Doc/Picture/image-2.png)

### Step 4: Configure SAP Tool List via Transaction Code ZMCP_CONFIG

Use transaction code ZMCP_CONFIG to configure the SAP tool list.

![Tool Configuration](/Doc/Picture/image-3.png)

SAP Tool Sample Data:
|MCP Tool ID|Active Flag|MCP Name|Tool Description|Version|Timeout (Seconds)|Retry Count|Priority|Category|Tag|Type|Name|Indicator|Indicator|Created By|Created Date|Created Time|Modified By|Modified Date|Modified Time|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|CHECK_MATNR|X|Check Material Number|Enter the material number and return the|0|10|0|2|MM|MM|FUNC|BAPI_MATERIAL_EXISTENCECHECK|||||0:00:00|||0:00:00|
|GET_MATNR_DETAILS|X|Get Material Details|Enter the material number to obtain the|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_DETAILS|||||0:00:00|||0:00:00|
|GET_MATNR_FROM_DES|X|Get Material Number|Enter material description and language|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_FROM_DES|||||0:00:00|||0:00:00|
|GET_MATNR_WERKS_LIST|X|Get Plant Material List|Enter the factory number to obtain all m|0|10|0|2|MM|MM|FUNC|ZMCP_GET_WERKS_MATNR_LIST|||||0:00:00|||0:00:00|
|GET_MATNR_WERKS_STOC|X|Get Plant Warehouse List|Enter the material number and factory nu|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_WERKS_STOCK|||||0:00:00|||0:00:00|
|GET_PERNR_FROM_DES|X|Get Employee ID|Enter name to obtain employee ID|0|10|0|2|PA|PA|FUNC|ZMCP_GET_PERNR_FROM_DES|||||0:00:00|||0:00:00|
|GET_PERNR_ORG|X|Get Organization Info|Enter the employee ID and query date to|0|10|0|2|PA|PA|FUNC|ZMCP_GET_PERNR_ORG|||||0:00:00|||0:00:00|
|GET_PERNR_WORK_PLAN|X|Get Work Plan|Enter the employee ID and year/month to|0|10|0|2|PT|PT|FUNC|ZMCP_GET_PERNR_WORK_PLAN|||||0:00:00|||0:00:00|
|GET_WERKS_FROM_DES|X|Get Plant Number|Enter factory description to obtain fact|0|10|0|2|MM|MM|FUNC|ZMCP_GET_WERKS_FROM_DES|||||0:00:00|||0:00:00|
|REVERSE_MATERIAL|X|Reverse Material Document|Enter material voucher information to re|0|10|0|2|MM|MM|FUNC|BAPI_GOODSMVT_CANCEL|||||0:00:00|||0:00:00|
|TOOL_DETAIL|X|Tool Detail|Tool detail|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_DETAIL|X|X|ADMIN||0:00:00|||0:00:00|
|TOOL_LIST|X|Tool List|Tool list|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_LIST|X|X|ADMIN||0:00:00|||0:00:00|
|TOOL_USED|X|Tool Used|Use tool|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_USED|X|X|ADMIN||0:00:00|||0:00:00|

---

## Manual Deployment

### 1.1 Get Project Code

**Method 1: Clone from Git Repository**
```bash
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP
```

**Method 2: Direct File Copy**
- Copy the entire project folder to your server

### 1.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 1.3 Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install project
pip install -e .
```

### 1.4 Configure Project

```bash
# Copy configuration example file
cp utils/config.example.py utils/config.py

# Edit configuration file (modify according to your environment)
# You can use any text editor, for example
# notepad config.py      # Windows
# vim config.py          # Linux/Mac
```

**Configuration File Example:**
```python
# SAP Interface Configuration
SAP_CONFIG = {
    "base_url": "http://your-sap-server:port/sap/zmcp",
    "client_id": "your-client-id",
    "sap-user": "your-sap-username",
    "sap-password": "your-sap-password",
    "timeout": 30
}

# MCP Server Configuration
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 6688,
    "path": "/mcp"
}

# WEB Server Configuration
WEB_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 6680,
    "reload": False
}
```

**Environment Variable Configuration:**

The project supports configuring sensitive information through environment variables to avoid hardcoding. Here are the supported environment variables:

| Environment Variable | Description | Default Value |
|---------------------|-------------|---------------|
| MCP_HOST | MCP server host | 0.0.0.0 |
| MCP_PORT | MCP server port | 6688 |
| MCP_PATH | MCP server path | /mcp |
| WEB_HOST | Web server host | 0.0.0.0 |
| WEB_PORT | Web server port | 6680 |
| WEB_RELOAD | Web server auto reload (development environment) | True |
| SAP_BASE_URL | SAP interface base URL | - |
| SAP_CLIENT_ID | SAP client ID | - |
| SAP_SAP_USER | SAP username | - |
| SAP_SAP_PASSWORD | SAP password | - |
| SAP_TIMEOUT | SAP request timeout (seconds) | 30 |

You can set these environment variables before starting the service, or create a `.env` file to store them.

### 1.5 Start Service

#### Method 1: Start MCP Server Only

```bash
# Start MCP server
python server/sap_mcp_server.py
```

#### Method 2: Start Web Management Interface

```bash
# Start Web management interface
python web/main.py
```

Or use uvicorn to start directly:

```bash
# Start Web management interface
python -m uvicorn web.main:app --host 0.0.0.0 --port 8080
```

---

## Usage Guide

### Access Web Management Interface

After starting the service, open in your browser: `http://localhost:6680`

### Service Management Page

1. **View Service Status**: Displays the current running status of the MCP service
2. **Start Service**: Click the "Start Service" button to start the MCP server
3. **Stop Service**: Click the "Stop Service" button to stop the MCP server
4. **View Logs**: View service running logs in real-time

### Tool Management Page

1. **View Tool List**: All available SAP tools are displayed on the left
2. **Search Tools**: Use the search box to quickly find tools
3. **View Tool Details**: Click a tool in the tool list to display tool details and parameters on the right
4. **Execute Tool**:
   - Fill in parameter values in the parameter form
   - Click the "Execute Tool" button
   - View execution results

### Server Configuration Page

1. **SAP Interface Configuration**:
   - Base URL
   - Client ID
   - SAP Username
   - SAP Password
   - Timeout

2. **MCP Server Configuration**:
   - Host Address
   - Port
   - Path

3. **Interface Test**: Click the "Interface Test" button to verify SAP interface connection

4. **Save Configuration**: Click the "Save Configuration" button to save all configurations

### Log Viewing Page

1. **Refresh Logs**: Click the "Refresh Logs" button to view the latest logs
2. **Log Level Filter**: Select log level for filtering
3. **Clear Logs**: Click the "Clear Logs" button to clear all logs

---

## Configure AI Tools

### Supported AI Tool Types

This service can be integrated into various AI tools, including:
- **Chat Tools**: Such as ChatGPT, Cherry Studio
- **Programming Tools**: Such as Cursor, Claude Code
- **Platform Tools**: Such as LangChain, Dify

### Configure MCP Service Address

Configure the MCP service address in your AI tools as:

```json 
{
  "mcpServers": {
    "SAP_MCP": {
      "type": "streamable_http",
      "url": "http://localhost:6688/mcp"
    }
  }
}
```

---

## Common Issues

### MCP Service Cannot Be Accessed

**Problem**: After starting the MCP service through the Web management interface, it cannot be accessed from outside.

**Solutions**:

1. Ensure the host configured for the MCP server is `0.0.0.0` (not `127.0.0.1`)
2. Ensure port mapping is configured correctly
3. Check firewall settings

### Configuration File Changes Not Taking Effect

**Problem**: After modifying the configuration file, the service is not using the new configuration.

**Solutions**:

1. Restart the Web management interface service
2. Stop and restart the MCP service

---

## Technical Support

If you have any questions, please contact:

- **Product Designer**: Mark (Wu Rangyu)
- **Developer**: Mark (Wu Rangyu)
- **Phone**: 18685095797
- **QQ**: 121980331
- **Email**: 121980331@qq.com
