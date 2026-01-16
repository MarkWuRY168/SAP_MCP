import os
import sys
import ast
import subprocess
import time
from typing import Dict, Any, Optional

class Utils:
    """工具类，提供常用的辅助功能"""
    
    @staticmethod
    def read_config_file(config_file_path: str) -> Dict[str, Any]:
        """读取配置文件
        
        Args:
            config_file_path: 配置文件路径
            
        Returns:
            配置字典
        """
        config = {}
        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用ast模块安全解析配置文件
            tree = ast.parse(content)
            
            # 提取配置字典
            for node in tree.body:
                if isinstance(node, ast.Assign) and len(node.targets) == 1:
                    target = node.targets[0]
                    if isinstance(target, ast.Name):
                        config_name = target.id
                        if isinstance(node.value, (ast.Dict, ast.Call)):
                            # 执行配置文件内容，获取配置值
                            exec(content, globals())
                            if config_name in globals():
                                config_value = globals()[config_name]
                                config[config_name] = config_value
            
        except Exception as e:
            print(f"读取配置文件失败: {str(e)}")
        
        return config
    
    @staticmethod
    def write_config_file(config_file_path: str, config: Dict[str, Any]) -> bool:
        """写入配置文件
        
        Args:
            config_file_path: 配置文件路径
            config: 配置字典
            
        Returns:
            是否写入成功
        """
        try:
            # 读取原始配置文件内容
            with open(config_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 更新配置文件内容
            new_lines = []
            in_dict = False
            current_dict = None
            dict_indent = 0
            
            for line in lines:
                stripped_line = line.strip()
                
                if in_dict:
                    # 检查是否结束字典
                    if stripped_line == '}' and line.startswith(' ' * dict_indent):
                        in_dict = False
                        current_dict = None
                    new_lines.append(line)
                else:
                    # 检查是否开始新字典
                    if '=' in line and any(config_name in line for config_name in config):
                        parts = line.split('=', 1)
                        config_name = parts[0].strip()
                        if config_name in config:
                            # 更新配置值
                            config_value = config[config_name]
                            # 生成新的配置行
                            indent = line[:len(line) - len(line.lstrip())]
                            new_line = f"{indent}{config_name} = {Utils.format_dict(config_value)}\n"
                            new_lines.append(new_line)
                            
                            # 检查是否是字典
                            if isinstance(config_value, dict):
                                in_dict = True
                                current_dict = config_name
                                dict_indent = len(indent) + 4
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
            
            # 写入更新后的配置文件
            with open(config_file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            return True
            
        except Exception as e:
            print(f"写入配置文件失败: {str(e)}")
            return False
    
    @staticmethod
    def format_dict(config_dict: Any) -> str:
        """格式化字典为字符串
        
        Args:
            config_dict: 配置字典
            
        Returns:
            格式化后的字符串
        """
        if not isinstance(config_dict, dict):
            return str(config_dict)
        
        lines = ['{']
        for key, value in config_dict.items():
            if isinstance(value, str):
                formatted_value = f'"{value}"'
            else:
                formatted_value = str(value)
            lines.append(f'    "{key}": {formatted_value},')
        lines.append('}')
        
        return '\n'.join(lines)
    
    @staticmethod
    def check_service_status(process: Optional[subprocess.Popen]) -> bool:
        """检查服务状态
        
        Args:
            process: 服务进程对象
            
        Returns:
            服务是否正在运行
        """
        if not process:
            return False
        
        return_code = process.poll()
        return return_code is None
    
    @staticmethod
    def start_service(script_path: str, cwd: Optional[str] = None) -> Optional[subprocess.Popen]:
        """启动服务
        
        Args:
            script_path: 服务脚本路径
            cwd: 工作目录
            
        Returns:
            服务进程对象
        """
        try:
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd
            )
            return process
        except Exception as e:
            print(f"启动服务失败: {str(e)}")
            return None
    
    @staticmethod
    def stop_service(process: Optional[subprocess.Popen]) -> bool:
        """停止服务
        
        Args:
            process: 服务进程对象
            
        Returns:
            是否停止成功
        """
        if not process:
            return True
        
        try:
            # 终止服务进程
            process.terminate()
            time.sleep(1)  # 等待进程终止
            
            if process.poll() is None:
                # 如果进程仍在运行，强制终止
                process.kill()
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"停止服务失败: {str(e)}")
            return False
    
    @staticmethod
    def get_current_time() -> str:
        """获取当前时间
        
        Returns:
            当前时间字符串，格式为YYYY-MM-DD HH:MM:SS
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def validate_port(port: str) -> bool:
        """验证端口号是否有效
        
        Args:
            port: 端口号字符串
            
        Returns:
            端口号是否有效
        """
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except ValueError:
            return False
    
    @staticmethod
    def validate_timeout(timeout: str) -> bool:
        """验证超时时间是否有效
        
        Args:
            timeout: 超时时间字符串
            
        Returns:
            超时时间是否有效
        """
        try:
            timeout_num = int(timeout)
            return timeout_num > 0
        except ValueError:
            return False
