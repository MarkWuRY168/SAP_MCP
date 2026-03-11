import json as json_module
import logging
import os
import re
import sys
import time
from typing import Optional, Dict, Any

import httpx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SAP_CONFIG
from utils.logging_config import get_logger
from utils.cache import cache_decorator

# 获取logger实例
logger = get_logger('SAPHttpClient')

class SAPHttpClient:
    """SAP接口HTTP客户端"""
    
    def __init__(self):
        # 创建可重用的HTTP客户端
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """获取HTTP客户端实例（使用连接池）
        
        Returns:
            httpx.AsyncClient: HTTP客户端实例
        """
        if self._client is None or self._client.is_closed:
            # 从SAP_CONFIG读取配置
            timeout = SAP_CONFIG["timeout"]
            
            # 创建新的客户端实例
            self._client = httpx.AsyncClient(
                timeout=timeout,
                limits=httpx.Limits(
                    max_connections=100,
                    max_keepalive_connections=20,
                    keepalive_expiry=30.0,
                ),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
        return self._client
    
    async def close(self) -> None:
        """关闭HTTP客户端"""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
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
        retry_count = 0
        max_retries = 3
        retry_delay = 1  # 秒
        
        while retry_count <= max_retries:
            try:
                # 每次请求时都从SAP_CONFIG读取最新配置
                base_url = SAP_CONFIG["base_url"]
                client_id = SAP_CONFIG["client_id"]
                sap_user = SAP_CONFIG["sap-user"]
                sap_password = SAP_CONFIG["sap-password"]
                
                # 构建完整URL
                url = f"{base_url}{endpoint}"
                
                # 添加SAP客户端ID到查询参数
                if params is None:
                    params = {}
                params["sap-client"] = client_id
                
                # 记录请求日志
                logger.info(f"请求开始 - 方法: {method}, URL: {url}")
                logger.info(f"请求参数: {params}")
                if json:
                    logger.info(f"请求数据: {json_module.dumps(json, ensure_ascii=False)}")
                
                # 发送请求（使用HTTP Basic Auth）
                auth = (sap_user, sap_password)
                
                # 获取客户端实例
                client = await self._get_client()
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    auth=auth
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
                except json_module.JSONDecodeError as e:
                    logger.error(f"响应错误: 无法解析JSON响应")
                    logger.error(f"JSON解析错误详情: {str(e)}")
                    logger.error(f"实际响应内容 (前500字符): {content[:500]}")
                    logger.error(f"响应内容长度: {len(content)} 字符")
                    raise Exception("SAP接口返回非JSON响应") from e
                
            except httpx.HTTPStatusError as e:
                # 处理HTTP错误
                response_time = time.time() - start_time
                error_msg = f"HTTP请求错误: {e.response.status_code} - {e.response.text}"
                logger.error(f"{error_msg}, 响应时间: {response_time:.3f}秒")
                
                # 对于4xx错误，不重试
                if 400 <= e.response.status_code < 500:
                    raise Exception(error_msg) from e
                
                # 对于5xx错误，重试
                retry_count += 1
                if retry_count > max_retries:
                    raise Exception(error_msg) from e
                
                logger.warning(f"请求失败，正在重试 ({retry_count}/{max_retries})...")
                time.sleep(retry_delay * (2 ** (retry_count - 1)))  # 指数退避
                
            except httpx.RequestError as e:
                # 处理请求错误
                response_time = time.time() - start_time
                error_msg = f"请求发送失败: {str(e)}"
                logger.error(f"{error_msg}, 响应时间: {response_time:.3f}秒")
                
                # 对于网络错误，重试
                retry_count += 1
                if retry_count > max_retries:
                    # 提供更详细的错误信息
                    if isinstance(e, httpx.ReadTimeout):
                        error_msg = f"连接SAP服务器超时({SAP_CONFIG['timeout']}秒)，请检查：\n1. SAP服务器地址是否正确\n2. 网络连接是否正常\n3. SAP服务器是否正在运行"
                    raise Exception(error_msg) from e
                
                logger.warning(f"请求失败，正在重试 ({retry_count}/{max_retries})...")
                time.sleep(retry_delay * (2 ** (retry_count - 1)))  # 指数退避
                
            except Exception as e:
                # 处理其他错误
                response_time = time.time() - start_time
                error_msg = f"请求处理失败: {str(e)}"
                logger.error(f"{error_msg}, 响应时间: {response_time:.3f}秒")
                raise Exception(error_msg) from e
    
    @cache_decorator(ttl=300)  # 缓存5分钟
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