import json
import os
import sys
from typing import Any, Dict, Optional

import pymysql

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATABASE_CONFIG

class DatabaseHandler:
    """数据库操作类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=DATABASE_CONFIG["host"],
                port=DATABASE_CONFIG["port"],
                user=DATABASE_CONFIG["user"],
                password=DATABASE_CONFIG["password"],
                database=DATABASE_CONFIG["database"],
                charset=DATABASE_CONFIG["charset"],
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            print(f"数据库连接失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
    
    def save_tool(self, tool_data: Dict[str, Any], description: str = "") -> bool:
        """保存工具信息到数据库
        
        Args:
            tool_data: 工具数据，包含 TOOL_ID, PARAM 等
            description: 工具描述
            
        Returns:
            bool: 是否保存成功
        """
        try:
            with self.connection.cursor() as cursor:
                tool_id = tool_data.get("TOOL_ID", "")
                params = tool_data.get("PARAM", {})
                
                if not tool_id:
                    print(f"[DB] 保存失败: TOOL_ID为空")
                    return False
                
                params_json = json.dumps(params, ensure_ascii=False, indent=2)
                
                print(f"[DB] 准备保存工具: {tool_id}")
                print(f"[DB] 描述: {description}")
                print(f"[DB] 参数JSON长度: {len(params_json)}")
                
                sql = """
                INSERT INTO tool_server 
                (name, description, parameters)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                description = VALUES(description),
                parameters = VALUES(parameters),
                updated_at = CURRENT_TIMESTAMP
                """
                
                cursor.execute(sql, (
                    tool_id,
                    description,
                    params_json
                ))
                
                affected_rows = cursor.rowcount
                self.connection.commit()
                print(f"[DB] 保存成功: {tool_id}, 影响行数: {affected_rows}")
                return True
                
        except Exception as e:
            print(f"[DB] 保存失败: {tool_id}, 错误: {e}")
            import traceback
            traceback.print_exc()
            self.connection.rollback()
            return False
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """根据工具名称获取工具信息
        
        Args:
            name: 工具名称
            
        Returns:
            dict: 工具信息，如果不存在返回 None
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM tool_server WHERE name = %s"
                cursor.execute(sql, (name,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            return None
    
    def list_tools(self) -> list:
        """获取工具列表
        
        Returns:
            list: 工具列表
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM tool_server"
                cursor.execute(sql)
                
                results = cursor.fetchall()
                return results
        except Exception as e:
            return []
    
    def delete_tool(self, name: str) -> bool:
        """删除工具（软删除，设置 is_active = 0）
        
        Args:
            name: 工具名称
            
        Returns:
            bool: 是否删除成功
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE tool_server SET is_active = 0 WHERE name = %s"
                cursor.execute(sql, (name,))
                self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            return False

# 全局数据库处理器实例
db_handler = None

def get_db_handler():
    """获取数据库处理器实例"""
    global db_handler
    if db_handler is None:
        db_handler = DatabaseHandler()
    return db_handler
