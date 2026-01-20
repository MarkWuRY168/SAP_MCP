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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ENDPOINTS = {
    "TOOL_LIST": "MCP_TOOL_LIST",
    "TOOL_DETAIL": "MCP_TOOL_DETAIL",
    "USE_TOOL": "USE_MCP_TOOL"
}

JSONRPC_VERSION = "2.0"

mcp = FastMCP("SAP_MCP_Server")
http_client = SAPHttpClient()

# 工具参数格式缓存（内存存储，无需数据库）
TOOL_PARAMS_CACHE: Dict[str, Dict[str, Any]] = {}


def handle_error(error: Exception, context: str = "") -> Dict[str, Any]:
    """统一错误处理函数
    
    Args:
        error: 捕获的异常对象
        context: 错误发生的上下文信息
        
    Returns:
        包含错误信息的字典
    """
    error_msg = f"{context}: {str(error)}" if context else str(error)
    logger.error(error_msg, exc_info=True)
    return {"error": error_msg}


def format_jsonrpc_result(result: Any) -> Dict[str, Any]:
    """格式化JSON-RPC响应
    
    Args:
        result: 原始结果数据
        
    Returns:
        格式化后的JSON-RPC响应
    """
    if isinstance(result, list):
        return {
            "JSONRPC": JSONRPC_VERSION,
            "RESULT": result,
            "ID": ""
        }
    elif isinstance(result, dict) and "RESULT" in result:
        return result
    else:
        return {
            "JSONRPC": JSONRPC_VERSION,
            "RESULT": result if isinstance(result, list) else [result],
            "ID": ""
        }


def convert_user_params_to_sap_format(user_params: Dict[str, Any], param_format: Dict[str, Any]) -> Dict[str, Any]:
    """将用户传入的参数转换为SAP接口要求的格式
    
    Args:
        user_params: 用户传入的原始参数（扁平格式）
        param_format: 从内存缓存获取的参数格式模板（嵌套格式）
        
    Returns:
        转换后的符合SAP接口格式的参数
    """
    if not param_format:
        return user_params
    
    def fill_params(template: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
        """递归填充参数值到模板中"""
        result = {}
        for key, template_value in template.items():
            if isinstance(template_value, dict):
                if key in values:
                    user_value = values[key]
                    if isinstance(user_value, dict):
                        result[key] = fill_params(template_value, user_value)
                    else:
                        result[key] = user_value
                else:
                    result[key] = fill_params(template_value, values)
            else:
                if key in values:
                    result[key] = values[key]
                else:
                    result[key] = template_value
        return result
    
    return fill_params(param_format, user_params)


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
            # 将工具参数格式保存到内存缓存
            TOOL_PARAMS_CACHE[tool_id] = result.get("PARAM", {})
            logger.info(f"工具参数格式已保存到内存缓存: {tool_id}")
        
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


if __name__ == "__main__":
    logger.info("启动MCP服务器")
    mcp.run(
        transport="http",
        host=MCP_SERVER_CONFIG["host"],
        port=MCP_SERVER_CONFIG["port"],
        path=MCP_SERVER_CONFIG["path"]
    )
