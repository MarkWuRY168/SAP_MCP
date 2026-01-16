import json as json_module
import logging
import os
import re
import sys
import time

import httpx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SAP_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sap_api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('SAPHttpClient')

class SAPHttpClient:
    """SAP接口HTTP客户端"""
    
    def __init__(self):
        self.base_url = SAP_CONFIG["base_url"]
        self.client_id = SAP_CONFIG["client_id"]
        self.timeout = SAP_CONFIG["timeout"]
        self.sap_user = SAP_CONFIG["sap-user"]
        self.sap_password = SAP_CONFIG["sap-password"]
        
    async def _send_request(self, method: str, endpoint: str = "", params: dict = None, json: dict = None) -> dict:
        """发送HTTP请求到SAP接口
        
        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE)
            endpoint: 接口端点
            params: URL查询参数
            json: 请求体JSON数据
            
        Returns:
            dict: 响应数据
        """
        start_time = time.time()
        
        try:
            # 构建完整URL
            url = f"{self.base_url}{endpoint}"
            
            # 添加SAP客户端ID到查询参数
            if params is None:
                params = {}
            params["sap-client"] = self.client_id
            
            # 记录请求日志
            logger.info(f"请求开始 - 方法: {method}, URL: {url}")
            logger.info(f"请求参数: {params}")
            if json:
                logger.info(f"请求数据: {json_module.dumps(json, ensure_ascii=False)}")
            
            # 发送请求（使用HTTP Basic Auth）
            auth = (self.sap_user, self.sap_password)
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    auth=auth,
                    headers=headers
                )
                
                # 计算响应时间
                response_time = time.time() - start_time
                
                # 记录响应日志
                logger.info(f"响应成功 - 状态码: {response.status_code}, 响应时间: {response_time:.3f}秒")
                logger.info(f"响应内容类型: {response.headers.get('content-type', 'unknown')}")
                
                # 检查响应状态
                response.raise_for_status()
                
                # 获取响应内容
                content = response.text
                content_type = response.headers.get("content-type", "")
                
                # 首先检查内容是否为HTML，无论content-type是什么
                if content.strip().startswith("<!DOCTYPE html") or content.strip().startswith("<html"):
                    logger.error(f"响应错误: 返回HTML内容")
                    raise Exception("SAP接口返回HTML内容，可能需要重新认证")
                
                # 处理Server-Sent Events (SSE)响应
                if "text/event-stream" in content_type:
                    # 解析SSE响应，提取data字段
                    lines = content.splitlines()
                    data_lines = []
                    for line in lines:
                        line = line.strip()
                        if line.startswith("data:"):
                            data_lines.append(line[5:].strip())
                    
                    if data_lines:
                        json_data = "\n".join(data_lines)
                        result = json_module.loads(json_data)
                        logger.info(f"响应数据: {json_module.dumps(result, ensure_ascii=False)[:500]}...")
                        return result
                    else:
                        logger.error(f"响应错误: 无法从SSE响应中提取数据")
                        raise Exception("无法从SSE响应中提取数据")
                
                # 处理HTML响应（可能是登录页面）
                if "text/html" in content_type:
                    logger.error(f"响应错误: 返回HTML内容")
                    raise Exception("SAP接口返回HTML内容，可能需要重新认证")
                
                # 尝试返回普通JSON响应
                try:
                    result = response.json()
                    logger.info(f"响应数据: {json_module.dumps(result, ensure_ascii=False)[:500]}...")
                    return result
                except json_module.JSONDecodeError:
                    logger.error(f"响应错误: 无法解析JSON响应")
                    raise Exception("SAP接口返回非JSON响应")
                
        except httpx.HTTPStatusError as e:
            # 处理HTTP错误
            response_time = time.time() - start_time
            error_msg = f"HTTP请求错误: {e.response.status_code} - {e.response.text}"
            logger.error(f"{error_msg}, 响应时间: {response_time:.3f}秒")
            raise Exception(error_msg) from e
        
        except httpx.RequestError as e:
            # 处理请求错误
            response_time = time.time() - start_time
            error_msg = f"请求发送失败: {str(e)}"
            logger.error(f"{error_msg}, 响应时间: {response_time:.3f}秒")
            raise Exception(error_msg) from e
        
        except Exception as e:
            # 处理其他错误
            response_time = time.time() - start_time
            error_msg = f"请求处理失败: {str(e)}"
            logger.error(f"{error_msg}, 响应时间: {response_time:.3f}秒")
            raise Exception(error_msg) from e
    
    async def get(self, endpoint: str = "", params: dict = None) -> dict:
        """发送GET请求
        
        Args:
            endpoint: 接口端点
            params: URL查询参数
            
        Returns:
            dict: 响应数据
        """
        return await self._send_request(method="GET", endpoint=endpoint, params=params)
    
    async def post(self, endpoint: str = "", params: dict = None, json: dict = None) -> dict:
        """发送POST请求
        
        Args:
            endpoint: 接口端点
            params: URL查询参数
            json: 请求体JSON数据
            
        Returns:
            dict: 响应数据
        """
        return await self._send_request(method="POST", endpoint=endpoint, params=params, json=json)