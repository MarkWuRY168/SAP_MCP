import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(
    log_dir: str = "log",
    log_file: str = "sap_api.log",
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console_level: Optional[int] = None
) -> logging.Logger:
    """设置日志配置
    
    Args:
        log_dir: 日志目录
        log_file: 日志文件名
        level: 日志级别
        max_bytes: 单个日志文件最大字节数
        backup_count: 日志文件备份数量
        console_level: 控制台日志级别，None表示与level相同
    
    Returns:
        logging.Logger: 配置好的logger实例
    """
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, log_file)
    
    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # 清空现有handler
    for handler in logger.handlers:
        logger.removeHandler(handler)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建文件handler（带轮转）
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 创建控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level or level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# 创建默认logger
default_logger = setup_logging()


# 为不同模块创建logger
def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """获取指定名称的logger
    
    Args:
        name: logger名称
        level: 日志级别，None表示使用默认级别
    
    Returns:
        logging.Logger: logger实例
    """
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger
