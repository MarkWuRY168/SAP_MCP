from pydantic_settings import BaseSettings
from typing import Optional


class SAPConfig(BaseSettings):
    """SAP接口配置模型"""
    base_url: str = "http://sap-s4d-app.example.com:8000/sap/zmcp"
    client_id: int = 300
    sap_user: str = "YOUR_SAP_USER"
    sap_password: str = "YOUR_SAP_PASSWORD"
    timeout: int = 30
    
    class Config:
        env_prefix = "SAP_"
        env_file = ".env"
        case_sensitive = False


class MCPConfig(BaseSettings):
    """MCP服务器配置模型"""
    host: str = "0.0.0.0"
    port: int = 8000
    path: str = "/mcp"
    
    class Config:
        env_prefix = "MCP_"
        env_file = ".env"
        case_sensitive = False


class WebConfig(BaseSettings):
    """Web服务器配置模型"""
    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = True
    
    class Config:
        env_prefix = "WEB_"
        env_file = ".env"
        case_sensitive = False


# 创建配置实例
sap_config = SAPConfig()
mcp_config = MCPConfig()
web_config = WebConfig()

# 转换为字典格式，保持向后兼容
SAP_CONFIG = {
    "base_url": sap_config.base_url,
    "client_id": sap_config.client_id,
    "sap-user": sap_config.sap_user,
    "sap-password": sap_config.sap_password,
    "timeout": sap_config.timeout,
}

MCP_SERVER_CONFIG = {
    "host": mcp_config.host,
    "port": mcp_config.port,
    "path": mcp_config.path,
}

WEB_CONFIG = {
    "host": web_config.host,
    "port": web_config.port,
    "reload": web_config.reload,
}
