# SAP MCP 配置文件示例
# 复制此文件为 config.py 并根据实际情况修改配置

# SAP接口配置
SAP_CONFIG = {
    "base_url": "http://sap-s4d-app.example.com:8000/sap/zmcp",
    "client_id": "300",
    "sap-user": "YOUR_SAP_USER",
    "sap-password": "YOUR_SAP_PASSWORD",
    "timeout": 30,
}

# MCP服务器配置
MCP_SERVER_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
    "path": "/mcp"
}
