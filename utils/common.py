import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)


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


def handle_http_error(error: Exception, context: str = "") -> None:
    """统一HTTP错误处理函数
    
    Args:
        error: 捕获的异常对象
        context: 错误发生的上下文信息
        
    Raises:
        HTTPException: 带有错误信息的HTTP异常
    """
    error_msg = f"{context}: {str(error)}" if context else str(error)
    logger.error(error_msg, exc_info=True)
    raise HTTPException(status_code=500, detail=error_msg)


def format_jsonrpc_result(result: Any) -> Dict[str, Any]:
    """格式化JSON-RPC响应
    
    Args:
        result: 原始结果数据
        
    Returns:
        格式化后的JSON-RPC响应
    """
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
