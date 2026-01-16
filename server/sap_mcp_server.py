import sys
import os
import logging
from typing import Dict, Any, Optional, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
from http_client import SAPHttpClient
from config import MCP_SERVER_CONFIG
from db_handler import get_db_handler

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
db = get_db_handler()


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


async def get_tool_description(tool_id: str) -> str:
    """从工具列表获取工具描述
    
    Args:
        tool_id: 工具ID
        
    Returns:
        工具描述文本，如果获取失败返回空字符串
    """
    try:
        tool_list_result = await http_client.get(params={"id": API_ENDPOINTS["TOOL_LIST"]})
        if isinstance(tool_list_result, list):
            for tool in tool_list_result:
                if tool.get("TOOL_ID") == tool_id:
                    return tool.get("DESCRIPTION", "")
    except Exception as e:
        logger.warning(f"获取工具描述失败: {e}")
    return ""


def convert_user_params_to_sap_format(user_params: Dict[str, Any], param_format: Dict[str, Any]) -> Dict[str, Any]:
    """将用户传入的参数转换为SAP接口要求的格式
    
    Args:
        user_params: 用户传入的原始参数（扁平格式）
        param_format: 从数据库获取的参数格式模板（嵌套格式）
        
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
    """从数据库获取工具参数格式
    
    Args:
        tool_id: 工具ID
        
    Returns:
        工具参数格式字典，如果获取失败返回None
    """
    try:
        tool_info = db.get_tool(tool_id)
        if tool_info and tool_info.get("parameters"):
            import json
            return json.loads(tool_info["parameters"])
        return None
    except Exception as e:
        logger.error(f"从数据库获取工具参数格式失败: {e}")
        return None


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
    """根据工具信息获取工具使用说明，并保存到数据库
    
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
            description = await get_tool_description(tool_id)
            
            logger.info(f"准备保存工具到数据库: {tool_id}, 描述: {description}")
            try:
                save_result = db.save_tool(result, description)
                if save_result:
                    logger.info(f"工具详情已成功保存到数据库: {tool_id}")
                else:
                    logger.warning(f"工具详情保存到数据库失败: {tool_id}")
            except Exception as e:
                logger.error(f"保存工具详情到数据库时发生异常: {e}", exc_info=True)
        
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
        
        # 从数据库获取工具参数格式
        param_format = await get_tool_params_format(tool_id)
        
        if param_format is None:
            logger.warning(f"工具 {tool_id} 未在数据库中找到，请先调用 get_tool_details 获取工具详情")
            return handle_error(
                ValueError(f"工具 {tool_id} 未在数据库中找到，请先调用 get_tool_details 获取工具详情"),
                "使用工具"
            )
        
        # 提取用户传入的参数（除了 TOOL_ID 之外的所有字段）
        user_params = {
            key: value 
            for key, value in json_data.items() 
            if key != "TOOL_ID"
        }
        
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
