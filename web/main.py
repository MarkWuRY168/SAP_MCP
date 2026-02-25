from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入现有的SAP MCP服务器功能
from server.http_client import SAPHttpClient
from config import SAP_CONFIG, MCP_SERVER_CONFIG, WEB_CONFIG
from utils.common import handle_http_error, format_jsonrpc_result
from utils.logging_config import get_logger
import subprocess
import time

# 获取logger实例
logger = get_logger(__name__)

# SAP API端点配置
API_ENDPOINTS = {
    "TOOL_LIST": "TOOL_LIST",
    "TOOL_DETAIL": "TOOL_DETAIL",
    "USE_TOOL": "TOOL_USED"
}

# 创建FastAPI应用
app = FastAPI(
    title="SAP MCP Web Management",
    description="SAP MCP服务器的Web管理界面，提供工具管理、配置管理、服务管理和日志管理等功能",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制为特定域名
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
)

# 创建HTTP客户端实例
http_client = SAPHttpClient()

# 服务状态管理
mcp_server_process = None
mcp_server_status = {"status": "stopped", "host": MCP_SERVER_CONFIG["host"], "port": MCP_SERVER_CONFIG["port"]}

# 统一错误处理函数
async def handle_error(error: Exception, context: str = "") -> None:
    """统一错误处理函数"""
    await handle_http_error(error, context)

# 定义API路由
@app.get("/api/tools", tags=["工具管理"])
async def api_get_tool_list():
    """获取工具清单
    
    Returns:
        dict: 包含工具清单的JSON-RPC响应
    """
    try:
        logger.info("获取工具清单")
        result = await http_client.get(params={"id": API_ENDPOINTS["TOOL_LIST"]})
        return format_jsonrpc_result(result)
    except Exception as e:
        return await handle_error(e, "获取工具清单失败")

@app.post("/api/tools/{tool_id}/details", tags=["工具管理"])
async def api_get_tool_details(tool_id: str, request_data: dict = None):
    """获取工具详情
    
    Args:
        tool_id: 工具ID
        request_data: 请求数据（可选）
    
    Returns:
        dict: 工具参数格式，包含工具的详细参数信息
    """
    try:
        logger.info(f"获取工具详情: {tool_id}")
        result = await http_client.post(
            params={"id": API_ENDPOINTS["TOOL_DETAIL"]},
            json={"TOOL_ID": tool_id}
        )
        
        if result and isinstance(result, dict):
            # 处理新的JSON格式，从param字段获取参数格式
            param_format = result.get("param", {})
            # 同时兼容旧格式，从PARAM字段获取参数格式
            if not param_format:
                param_format = result.get("PARAM", {})
            
            # 确保返回的数据格式符合前端预期
            return {
                "TOOL_ID": tool_id,
                "PARAM": param_format
            }
        
        return result
    except Exception as e:
        return await handle_error(e, "获取工具详情失败")

@app.post("/api/tools/{tool_id}/use", tags=["工具管理"])
async def api_use_tool(tool_id: str, request_data: dict):
    """使用工具
    
    Args:
        tool_id: 工具ID
        request_data: 请求数据，包含工具所需的参数
    
    Returns:
        dict: 工具执行结果
    """
    try:
        logger.info(f"使用工具: {tool_id}")
        
        # 从请求数据中提取PARAM对象
        param_data = request_data.get("PARAM", {})
        
        # 构建发送给SAP接口的数据（保持PARAM结构）
        sap_request_data = {
            "TOOL_ID": tool_id,
            "PARAM": param_data
        }
        
        result = await http_client.post(
            params={"id": API_ENDPOINTS["USE_TOOL"]},
            json=sap_request_data
        )
        return result
    except Exception as e:
        return await handle_error(e, "使用工具失败")

@app.get("/api/config", tags=["配置管理"])
async def api_get_config():
    """获取服务器配置
    
    Returns:
        dict: 包含MCP服务器配置、SAP配置和WEB配置的字典
    """
    return {
        "config": MCP_SERVER_CONFIG,
        "sap_config": SAP_CONFIG,
        "web_config": WEB_CONFIG
    }

def save_config_to_file():
    """将配置保存到文件中"""
    try:
        # 保存到 utils/config.py
        utils_config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils", "config.py")
        
        # 重写整个配置文件
        config_content = f'''from pydantic_settings import BaseSettings
from typing import Optional


class SAPConfig(BaseSettings):
    """SAP接口配置模型"""
    base_url: str = "{SAP_CONFIG["base_url"]}"
    client_id: int = {SAP_CONFIG["client_id"]}
    sap_user: str = "{SAP_CONFIG["sap-user"]}"
    sap_password: str = "{SAP_CONFIG["sap-password"]}"
    timeout: int = {SAP_CONFIG["timeout"]}
    
    class Config:
        env_prefix = "SAP_"
        env_file = ".env"
        case_sensitive = False


class MCPConfig(BaseSettings):
    """MCP服务器配置模型"""
    host: str = "{MCP_SERVER_CONFIG["host"]}"
    port: int = {MCP_SERVER_CONFIG["port"]}
    path: str = "{MCP_SERVER_CONFIG["path"]}"
    
    class Config:
        env_prefix = "MCP_"
        env_file = ".env"
        case_sensitive = False


class WebConfig(BaseSettings):
    """Web服务器配置模型"""
    host: str = "{WEB_CONFIG["host"]}"
    port: int = {WEB_CONFIG["port"]}
    reload: bool = {str(WEB_CONFIG["reload"])}
    
    class Config:
        env_prefix = "WEB_"
        env_file = ".env"
        case_sensitive = False


# 创建配置实例
sap_config = SAPConfig()
mcp_config = MCPConfig()
web_config = WebConfig()

# 转换为字典格式，保持向后兼容
SAP_CONFIG = {{
    "base_url": sap_config.base_url,
    "client_id": sap_config.client_id,
    "sap-user": sap_config.sap_user,
    "sap-password": sap_config.sap_password,
    "timeout": sap_config.timeout,
}}

MCP_SERVER_CONFIG = {{
    "host": mcp_config.host,
    "port": mcp_config.port,
    "path": mcp_config.path,
}}

WEB_CONFIG = {{
    "host": web_config.host,
    "port": web_config.port,
    "reload": web_config.reload,
}}
'''
        
        # 写入文件
        with open(utils_config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        
        logger.info(f"配置已保存到文件: {utils_config_path}")
        return True
    except Exception as e:
        logger.error(f"保存配置到文件失败: {str(e)}")
        return False

@app.post("/api/config", tags=["配置管理"])
async def api_save_config(config_data: dict):
    """保存服务器配置
    
    Args:
        config_data: 包含配置数据的字典，可包含sap、mcp和web三个键
    
    Returns:
        dict: 包含保存结果和更新后配置的字典
    """
    try:
        logger.info(f"保存配置请求: {json.dumps(config_data, ensure_ascii=False)}")
        
        # 更新内存中的配置
        if "sap" in config_data:
            SAP_CONFIG.update(config_data["sap"])
        if "mcp" in config_data:
            MCP_SERVER_CONFIG.update(config_data["mcp"])
        if "web" in config_data:
            WEB_CONFIG.update(config_data["web"])
        
        # 保存配置到文件
        save_config_to_file()
        
        logger.info("配置保存成功")
        return {
            "message": "配置保存成功",
            "config": MCP_SERVER_CONFIG,
            "sap_config": SAP_CONFIG,
            "web_config": WEB_CONFIG
        }
    except Exception as e:
        return await handle_error(e, "保存配置失败")

@app.post("/api/test-api", tags=["配置管理"])
async def api_test_api():
    """测试SAP接口连接
    
    Returns:
        dict: 包含测试结果的字典
    """
    try:
        logger.info("测试SAP接口连接")
        
        # 使用当前配置创建新的HTTP客户端实例
        test_client = SAPHttpClient()
        
        # 调用id=TOOL_LIST的接口
        result = await test_client.get(params={"id": "TOOL_LIST"})
        
        logger.info(f"SAP接口测试成功: {json.dumps(result, ensure_ascii=False)}")
        return {
            "message": "SAP接口测试成功",
            "success": True,
            "result": result
        }
    except Exception as e:
        logger.error(f"SAP接口测试失败: {str(e)}")
        return {
            "message": f"SAP接口测试失败: {str(e)}",
            "success": False,
            "error": str(e)
        }

@app.get("/api/service/status", tags=["服务管理"])
async def api_get_service_status():
    """获取服务状态"""
    global mcp_server_process, mcp_server_status
    
    # 检查进程是否还在运行
    if mcp_server_process is not None:
        if mcp_server_process.poll() is None:
            # 进程还在运行，确保状态为running
            if mcp_server_status["status"] != "running":
                mcp_server_status = {
                    "status": "running",
                    "host": MCP_SERVER_CONFIG["host"],
                    "port": MCP_SERVER_CONFIG["port"],
                    "pid": mcp_server_process.pid
                }
        else:
            # 进程已经终止，更新状态为stopped
            mcp_server_status = {
                "status": "stopped",
                "host": MCP_SERVER_CONFIG["host"],
                "port": MCP_SERVER_CONFIG["port"]
            }
    
    return mcp_server_status

@app.post("/api/service/start", tags=["服务管理"])
async def api_start_service():
    """启动MCP服务器"""
    global mcp_server_process, mcp_server_status
    
    try:
        if mcp_server_process is not None and mcp_server_process.poll() is None:
            return {"message": "服务已经在运行中", "status": mcp_server_status}
        
        # 启动MCP服务器进程
        logger.info("启动MCP服务器进程")
        
        # 获取项目根目录
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 构建启动命令
        cmd = [
            sys.executable,  # 使用当前Python解释器
            os.path.join("server", "sap_mcp_server.py")
        ]
        
        # 启动进程，捕获输出到日志文件
        log_file_path = os.path.join(project_root, "log", "mcp_server.log")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            mcp_server_process = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=log_file,
                cwd=project_root  # 在项目根目录执行
            )
        
        logger.info(f"MCP服务器进程启动，PID: {mcp_server_process.pid}")
        logger.info(f"启动命令: {' '.join(cmd)}")
        logger.info(f"日志文件: {log_file_path}")
        
        # 等待服务启动
        time.sleep(3)
        
        # 检查进程是否还在运行
        if mcp_server_process.poll() is None:
            mcp_server_status = {
                "status": "running",
                "host": MCP_SERVER_CONFIG["host"],
                "port": MCP_SERVER_CONFIG["port"],
                "pid": mcp_server_process.pid,
                "log_file": log_file_path
            }
            logger.info(f"MCP服务器启动成功，进程ID: {mcp_server_process.pid}")
            return {"message": "服务启动成功", "status": mcp_server_status}
        else:
            # 获取完整的错误信息
            try:
                with open(log_file_path, "r", encoding="utf-8") as log_file:
                    log_content = log_file.read()
            except Exception:
                log_content = "无法读取日志文件"
            
            logger.error(f"MCP服务器启动失败，退出码: {mcp_server_process.returncode}")
            logger.error(f"日志内容: {log_content}")
            
            mcp_server_status = {
                "status": "stopped",
                "host": MCP_SERVER_CONFIG["host"],
                "port": MCP_SERVER_CONFIG["port"],
                "error": log_content[:500] if log_content else "启动失败"
            }
            return {"message": "服务启动失败", "status": mcp_server_status}
            
    except Exception as e:
        logger.error(f"启动服务失败: {str(e)}")
        mcp_server_status = {
            "status": "stopped",
            "host": MCP_SERVER_CONFIG["host"],
            "port": MCP_SERVER_CONFIG["port"],
            "error": str(e)
        }
        return {"message": "服务启动失败", "status": mcp_server_status}

@app.post("/api/service/stop", tags=["服务管理"])
async def api_stop_service():
    """停止MCP服务器"""
    global mcp_server_process, mcp_server_status
    
    try:
        if mcp_server_process is None or mcp_server_process.poll() is not None:
            return {"message": "服务已经停止", "status": mcp_server_status}
        
        logger.info(f"停止MCP服务器进程，进程ID: {mcp_server_process.pid}")
        
        # 终止进程
        mcp_server_process.terminate()
        
        # 等待进程结束，最多等待5秒
        try:
            exit_code = mcp_server_process.wait(timeout=5)
            logger.info(f"MCP服务器进程正常终止，退出码: {exit_code}")
        except subprocess.TimeoutExpired:
            # 如果进程没有在5秒内结束，就发送kill信号
            logger.warning("MCP服务器进程未能在5秒内正常终止，发送kill信号")
            mcp_server_process.kill()
            try:
                exit_code = mcp_server_process.wait(timeout=2)
                logger.info(f"MCP服务器进程被强制终止，退出码: {exit_code}")
            except subprocess.TimeoutExpired:
                logger.error("MCP服务器进程无法终止")
                return {"message": "服务停止失败: 进程无法终止", "status": mcp_server_status}
        
        # 更新状态
        mcp_server_status = {
            "status": "stopped",
            "host": MCP_SERVER_CONFIG["host"],
            "port": MCP_SERVER_CONFIG["port"]
        }
        
        logger.info("MCP服务器已停止")
        return {"message": "服务停止成功", "status": mcp_server_status}
        
    except Exception as e:
        logger.error(f"停止服务失败: {str(e)}")
        return {"message": f"服务停止失败: {str(e)}", "status": mcp_server_status}

@app.get("/api/logs", tags=["日志管理"])
async def api_get_logs(level: str = "all", limit: int = 1000):
    """获取日志文件内容
    
    Args:
        level: 日志级别过滤，可选值: all, INFO, WARNING, ERROR, CRITICAL
        limit: 返回日志行数限制，默认1000行
    """
    try:
        log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log", "sap_api.log")
        
        # 读取日志文件
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # 根据日志级别过滤
        if level != "all":
            filtered_lines = []
            for line in lines:
                if f" {level} " in line or line.strip().endswith(f" {level}"):
                    filtered_lines.append(line)
            lines = filtered_lines
        
        # 限制返回行数
        if limit > 0:
            lines = lines[-limit:]
        
        # 连接成字符串并返回
        logs_content = "".join(lines)
        
        return {
            "status": "success",
            "data": logs_content,
            "level": level,
            "total_lines": len(lines)
        }
        
    except Exception as e:
        logger.error(f"读取日志文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"读取日志文件失败: {str(e)}")

@app.delete("/api/logs", tags=["日志管理"])
async def api_clear_logs():
    """清空日志文件
    """
    try:
        log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log", "sap_api.log")
        
        # 清空日志文件（写入空字符串）
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("")
        
        logger.info("日志文件已清空")
        
        return {
            "status": "success",
            "message": "日志文件已成功清空"
        }
        
    except Exception as e:
        logger.error(f"清空日志文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"清空日志文件失败: {str(e)}")


@app.get("/api/health", tags=["健康检查"])
async def api_health_check():
    """健康检查端点
    
    Returns:
        dict: 健康状态信息
    """
    try:
        # 检查服务状态
        service_status = await api_get_service_status()
        
        # 尝试连接SAP接口
        try:
            test_client = SAPHttpClient()
            await test_client.get(params={"id": "TOOL_LIST"})
            sap_status = "healthy"
        except Exception as e:
            sap_status = f"unhealthy: {str(e)}"
        
        return {
            "status": "healthy",
            "service_status": service_status,
            "sap_status": sap_status,
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 静态文件服务
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# 主页面
@app.get("/", response_class=HTMLResponse, tags=["Web界面"])
async def root():
    """Web管理界面主页"""
    with open(os.path.join(current_dir, "templates", "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# 启动服务器
if __name__ == "__main__":
    logger.info("启动SAP MCP Web管理服务器")
    # 从环境变量获取端口配置，如果没有设置则使用配置文件中的值
    web_port = int(os.getenv('WEB_PORT', WEB_CONFIG['port']))
    # 从环境变量获取主机配置
    web_host = os.getenv('WEB_HOST', WEB_CONFIG["host"])
    uvicorn.run(
        "web.main:app",
        host=web_host,
        port=web_port,
        reload=WEB_CONFIG["reload"]
    )