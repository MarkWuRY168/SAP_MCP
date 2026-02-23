from typing import Dict, Any, Optional
import time


class SimpleCache:
    """简单的内存缓存实现"""
    
    def __init__(self, default_ttl: int = 3600):
        """初始化缓存
        
        Args:
            default_ttl: 默认缓存过期时间（秒）
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            Any: 缓存值，如果不存在或已过期则返回None
        """
        if key not in self._cache:
            return None
        
        item = self._cache[key]
        current_time = time.time()
        if current_time > item["expire_at"]:
            # 缓存已过期，删除
            del self._cache[key]
            return None
        
        return item["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 缓存过期时间（秒），None表示使用默认值
        """
        expire_at = time.time() + (ttl or self.default_ttl)
        self._cache[key] = {
            "value": value,
            "expire_at": expire_at
        }
    
    def delete(self, key: str) -> None:
        """删除缓存值
        
        Args:
            key: 缓存键
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    def size(self) -> int:
        """获取缓存大小
        
        Returns:
            int: 缓存项数量
        """
        # 清理过期项
        now = time.time()
        expired_keys = [key for key, item in self._cache.items() if now > item["expire_at"]]
        for key in expired_keys:
            del self._cache[key]
        
        return len(self._cache)


# 创建全局缓存实例
cache = SimpleCache()


# 缓存装饰器
def cache_decorator(ttl: int = 3600):
    """缓存装饰器
    
    Args:
        ttl: 缓存过期时间（秒）
    
    Returns:
        Callable: 装饰器函数
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = "|".join(key_parts)
            
            # 尝试从缓存获取
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 调用原函数
            result = await func(*args, **kwargs)
            
            # 缓存结果
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
