import sys
import os
import logging
from typing import Dict, Any, Optional, List

# 添加父目录到Python路径，解决相对导入问题
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP

# 尝试相对导入，如果失败则使用绝对导入
try:
    from .http_client import SAPHttpClient
except ImportError:
    from server.http_client import SAPHttpClient

# 导入配置文件
try:
    from config import MCP_SERVER_CONFIG
except ImportError:
    from ..config import MCP_SERVER_CONFIG

# 导入工具函数
try:
    from utils.common import handle_error, format_jsonrpc_result, convert_user_params_to_sap_format
except ImportError:
    from ..utils.common import handle_error, format_jsonrpc_result, convert_user_params_to_sap_format

# 导入日志配置
try:
    from utils.logging_config import get_logger
except ImportError:
    from ..utils.logging_config import get_logger

# 获取logger实例
logger = get_logger(__name__)

API_ENDPOINTS = {
    "TOOL_LIST": "TOOL_LIST",
    "TOOL_DETAIL": "TOOL_DETAIL",
    "USE_TOOL": "TOOL_USED"
}

mcp = FastMCP("SAP_MCP_Server")
http_client = SAPHttpClient()

# 工具参数格式缓存（内存存储，无需数据库）
TOOL_PARAMS_CACHE: Dict[str, Dict[str, Any]] = {}


async def get_tool_params_format(tool_id: str) -> Optional[Dict[str, Any]]:
    """从内存缓存获取工具参数格式
    
    Args:
        tool_id: 工具ID
        
    Returns:
        工具参数格式字典，如果不存在返回None
    """
    return TOOL_PARAMS_CACHE.get(tool_id)


@mcp.tool(name="get_tool_list")
async def get_tool_list() -> Dict[str, Any]:
    """获取工具清单
    
    Returns:
        dict: 包含工具清单的JSON-RPC响应，格式为:
            {
                "JSONRPC": "2.0",
                "RESULT": [工具列表],
                "ID": ""
            }
            或包含错误信息的字典
    """
    try:
        logger.info("获取工具清单")
        result = await http_client.get(params={"id": API_ENDPOINTS["TOOL_LIST"]})
        return format_jsonrpc_result(result)
    except Exception as e:
        return handle_error(e, "获取工具清单失败")


@mcp.tool(name="get_tool_details")
async def get_tool_details(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """根据工具信息获取工具使用说明，并保存到内存缓存
    
    Args:
        json_data: JSON格式数据，必须包含TOOL_ID字段
            {
                "TOOL_ID": "工具ID"
            }
        
    Returns:
        dict: 工具参数格式，包含工具的详细参数信息
            或包含错误信息的字典
    """
    try:
        tool_id = json_data.get("TOOL_ID")
        if not tool_id:
            return handle_error(ValueError("TOOL_ID不能为空"), "获取工具详情")
        
        logger.info(f"获取工具详情: {tool_id}")
        
        result = await http_client.post(
            params={"id": API_ENDPOINTS["TOOL_DETAIL"]},
            json=json_data
        )
        
        if result and isinstance(result, dict):
            # 处理新的JSON格式，从param字段获取参数格式
            param_format = result.get("param", {})
            # 同时兼容旧格式，从PARAM字段获取参数格式
            if not param_format:
                param_format = result.get("PARAM", {})
            # 将工具参数格式保存到内存缓存
            TOOL_PARAMS_CACHE[tool_id] = param_format
            logger.info(f"工具参数格式已保存到内存缓存: {tool_id}")
            
            # 确保返回的数据格式符合前端预期
            return {
                "TOOL_ID": tool_id,
                "PARAM": param_format
            }
        
        return result
    except Exception as e:
        return handle_error(e, "获取工具详情失败")


@mcp.tool(name="use_tool")
async def use_tool(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """使用工具执行操作
    
    使用工具前，请先调用get_tool_details获取工具使用说明
    
    Args:
        json_data: JSON格式数据，必须包含TOOL_ID和参数
            {
                "TOOL_ID": "工具ID",
                "参数名1": "值1",
                "参数名2": "值2",
                ...
            }
        
    Returns:
        dict: 工具执行结果
            或包含错误信息的字典
    """
    try:
        tool_id = json_data.get("TOOL_ID")
        if not tool_id:
            return handle_error(ValueError("TOOL_ID不能为空"), "使用工具")
        
        logger.info(f"使用工具: {tool_id}")
        
        # 从内存缓存获取工具参数格式
        param_format = await get_tool_params_format(tool_id)
        
        # 提取用户传入的参数（除了 TOOL_ID 之外的所有字段）
        user_params = {
            key: value 
            for key, value in json_data.items() 
            if key != "TOOL_ID"
        }
        
        # 如果缓存中没有参数格式，尝试直接使用用户参数
        if param_format is None:
            logger.warning(f"工具 {tool_id} 未在缓存中找到，尝试直接使用用户参数")
            # 直接使用用户参数，不进行格式转换
            sap_params = {
                "IMPORT": {
                    "IMPORTING_DATA": user_params
                }
            }
        else:
            # 将用户参数转换为SAP接口要求的格式
            sap_params = convert_user_params_to_sap_format(user_params, param_format)
        
        # 构造SAP请求数据
        sap_request_data = {
            "TOOL_ID": tool_id,
            "PARAM": sap_params
        }
        
        logger.info(f"参数转换完成，调用SAP接口: {tool_id}")
        result = await http_client.post(
            params={"id": API_ENDPOINTS["USE_TOOL"]},
            json=sap_request_data
        )
        
        return result
    except Exception as e:
        return handle_error(e, "使用工具失败")


def main():
    """主函数，用于启动MCP服务器
    
    这个函数被sap-mcp-server命令调用，用于启动MCP服务器。
    """
    logger.info("启动MCP服务器")
    mcp.run(
        transport="http",
        host=MCP_SERVER_CONFIG["host"],
        port=MCP_SERVER_CONFIG["port"],
        path=MCP_SERVER_CONFIG["path"]
    )

if __name__ == "__main__":
    main()
