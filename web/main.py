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
from config import SAP_CONFIG, MCP_SERVER_CONFIG
import logging
import subprocess
import os
import sys
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SAP API端点配置
API_ENDPOINTS = {
    "TOOL_LIST": "MCP_TOOL_LIST",
    "TOOL_DETAIL": "MCP_TOOL_DETAIL",
    "USE_TOOL": "USE_MCP_TOOL"
}

# 创建FastAPI应用
app = FastAPI(
    title="SAP MCP Web Management",
    description="SAP MCP服务器的Web管理界面",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建HTTP客户端实例
http_client = SAPHttpClient()

# 服务状态管理
mcp_server_process = None
mcp_server_status = {"status": "stopped", "host": MCP_SERVER_CONFIG["host"], "port": MCP_SERVER_CONFIG["port"]}

# 统一错误处理函数
async def handle_error(error: Exception, context: str = "") -> None:
    """统一错误处理函数"""
    error_msg = f"{context}: {str(error)}" if context else str(error)
    logger.error(error_msg, exc_info=True)
    raise HTTPException(status_code=500, detail=error_msg)

# 格式化JSON-RPC响应
def format_jsonrpc_result(result: any) -> dict:
    """格式化JSON-RPC响应"""
    if isinstance(result, list):
        return {
            "JSONRPC": "2.0",
            "RESULT": result,
            "ID": ""
        }
    elif isinstance(result, dict) and "RESULT" in result:
        return result
    else:
        return {
            "JSONRPC": "2.0",
            "RESULT": result if isinstance(result, list) else [result],
            "ID": ""
        }

# 定义API路由
@app.get("/api/tools", tags=["工具管理"])
async def api_get_tool_list():
    """获取工具清单"""
    try:
        logger.info("获取工具清单")
        result = await http_client.get(params={"id": API_ENDPOINTS["TOOL_LIST"]})
        return format_jsonrpc_result(result)
    except Exception as e:
        return await handle_error(e, "获取工具清单失败")

@app.post("/api/tools/{tool_id}/details", tags=["工具管理"])
async def api_get_tool_details(tool_id: str, request_data: dict = None):
    """获取工具详情"""
    try:
        logger.info(f"获取工具详情: {tool_id}")
        result = await http_client.post(
            params={"id": API_ENDPOINTS["TOOL_DETAIL"]},
            json={"TOOL_ID": tool_id}
        )
        return result
    except Exception as e:
        return await handle_error(e, "获取工具详情失败")

@app.post("/api/tools/{tool_id}/use", tags=["工具管理"])
async def api_use_tool(tool_id: str, request_data: dict):
    """使用工具"""
    try:
        logger.info(f"使用工具: {tool_id}")
        # 添加TOOL_ID到请求数据
        request_data["TOOL_ID"] = tool_id
        result = await http_client.post(
            params={"id": API_ENDPOINTS["USE_TOOL"]},
            json=request_data
        )
        return result
    except Exception as e:
        return await handle_error(e, "使用工具失败")

@app.get("/api/config", tags=["配置管理"])
async def api_get_config():
    """获取服务器配置"""
    return {
        "config": MCP_SERVER_CONFIG,
        "sap_config": SAP_CONFIG
    }

def save_config_to_file():
    """将配置保存到文件中"""
    try:
        config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.py")
        
        with open(config_file_path, "w", encoding="utf-8") as f:
            f.write("# SAP MCP 配置文件\n\n")
            f.write("# SAP接口配置\n")
            f.write("SAP_CONFIG = {\n")
            for key, value in SAP_CONFIG.items():
                if isinstance(value, str):
                    f.write(f"    \"{key}\": \"{value}\",\n")
                else:
                    f.write(f"    \"{key}\": {value},\n")
            f.write("}\n\n")
            
            f.write("# MCP服务器配置\n")
            f.write("MCP_SERVER_CONFIG = {\n")
            for key, value in MCP_SERVER_CONFIG.items():
                if isinstance(value, str):
                    f.write(f"    \"{key}\": \"{value}\",\n")
                else:
                    f.write(f"    \"{key}\": {value},\n")
            f.write("}\n")
        
        logger.info(f"配置已保存到文件: {config_file_path}")
        return True
    except Exception as e:
        logger.error(f"保存配置到文件失败: {str(e)}")
        return False

@app.post("/api/config", tags=["配置管理"])
async def api_save_config(config_data: dict):
    """保存服务器配置"""
    try:
        logger.info(f"保存配置请求: {json.dumps(config_data, ensure_ascii=False)}")
        
        # 更新内存中的配置
        if "sap" in config_data:
            SAP_CONFIG.update(config_data["sap"])
        if "mcp" in config_data:
            MCP_SERVER_CONFIG.update(config_data["mcp"])
        
        # 保存配置到文件
        save_config_to_file()
        
        logger.info("配置保存成功")
        return {
            "message": "配置保存成功",
            "config": MCP_SERVER_CONFIG,
            "sap_config": SAP_CONFIG
        }
    except Exception as e:
        return await handle_error(e, "保存配置失败")

@app.get("/api/service/status", tags=["服务管理"])
async def api_get_service_status():
    """获取服务状态"""
    global mcp_server_status
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
        
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        server_dir = os.path.join(os.path.dirname(current_dir), "server")
        
        # 构建启动命令
        cmd = [
            sys.executable,  # 使用当前Python解释器
            "server/sap_mcp_server.py"
        ]
        
        # 启动进程，不捕获输出，让它直接输出到控制台
        mcp_server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,  # 忽略标准输出
            stderr=subprocess.DEVNULL,  # 忽略标准错误
            cwd=os.path.dirname(current_dir)  # 在项目根目录执行
        )
        
        logger.info(f"MCP服务器进程启动，PID: {mcp_server_process.pid}")
        logger.info(f"启动命令: {' '.join(cmd)}")
        
        # 等待服务启动
        time.sleep(3)
        
        # 检查进程是否还在运行
        if mcp_server_process.poll() is None:
            mcp_server_status = {
                "status": "running",
                "host": MCP_SERVER_CONFIG["host"],
                "port": MCP_SERVER_CONFIG["port"],
                "pid": mcp_server_process.pid
            }
            logger.info(f"MCP服务器启动成功，进程ID: {mcp_server_process.pid}")
            return {"message": "服务启动成功", "status": mcp_server_status}
        else:
            # 获取完整的错误信息
            stdout, stderr = mcp_server_process.communicate()
            full_stderr = stderr_partial + stderr
            full_stdout = stdout_partial + stdout
            logger.error(f"MCP服务器启动失败，退出码: {mcp_server_process.returncode}")
            logger.error(f"完整输出: {full_stdout}")
            logger.error(f"完整错误: {full_stderr}")
            mcp_server_status = {
                "status": "stopped",
                "host": MCP_SERVER_CONFIG["host"],
                "port": MCP_SERVER_CONFIG["port"],
                "error": full_stderr
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
        mcp_server_process.wait(timeout=5)
        
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
        return {"message": "服务停止失败", "status": mcp_server_status}

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

# 静态文件服务
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# 主页面
@app.get("/", response_class=HTMLResponse, tags=["Web界面"])
async def root():
    """Web管理界面主页"""
    with open(os.path.join("web", "templates", "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# 启动服务器
if __name__ == "__main__":
    logger.info("启动SAP MCP Web管理服务器")
    uvicorn.run(
        "web.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True  # 开发环境启用自动重载
    )