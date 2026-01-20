from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QFormLayout, QTabWidget, QGroupBox,
                             QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
import os
import sys
import ast
import re

class ConfigManagerWidget(QWidget):
    """配置管理标签页"""
    
    def __init__(self):
        super().__init__()
        self.config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")
        self.original_config = {}
        self.current_config = {}
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建配置子标签页
        self.config_tabs = QTabWidget()
        
        # SAP接口配置
        self.sap_config_widget = QWidget()
        self.init_sap_config_ui()
        self.config_tabs.addTab(self.sap_config_widget, "SAP接口配置")
        
        # MCP服务器配置
        self.mcp_config_widget = QWidget()
        self.init_mcp_config_ui()
        self.config_tabs.addTab(self.mcp_config_widget, "MCP服务器配置")
        
        main_layout.addWidget(self.config_tabs)
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()
        
        self.save_button = QPushButton("保存配置")
        self.save_button.setMinimumHeight(30)
        self.save_button.setStyleSheet(self.get_button_style("#27AE60"))
        self.save_button.clicked.connect(self.save_config)
        button_layout.addWidget(self.save_button)
        
        self.reset_button = QPushButton("重置")
        self.reset_button.setMinimumHeight(30)
        self.reset_button.setStyleSheet(self.get_button_style("#E74C3C"))
        self.reset_button.clicked.connect(self.reset_config)
        button_layout.addWidget(self.reset_button)
        
        self.apply_button = QPushButton("应用")
        self.apply_button.setMinimumHeight(30)
        self.apply_button.setStyleSheet(self.get_button_style("#3498DB"))
        self.apply_button.clicked.connect(self.apply_config)
        button_layout.addWidget(self.apply_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # 设置样式
        self.set_style()
    
    def init_sap_config_ui(self):
        """初始化SAP接口配置UI"""
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # base_url
        self.sap_base_url_edit = QLineEdit()
        form_layout.addRow("Base URL:", self.sap_base_url_edit)
        
        # client_id
        self.sap_client_id_edit = QLineEdit()
        form_layout.addRow("Client ID:", self.sap_client_id_edit)
        
        # sap-user
        self.sap_user_edit = QLineEdit()
        form_layout.addRow("SAP用户:", self.sap_user_edit)
        
        # sap-password
        self.sap_password_edit = QLineEdit()
        self.sap_password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("SAP密码:", self.sap_password_edit)
        
        # timeout
        self.sap_timeout_edit = QLineEdit()
        form_layout.addRow("超时时间(秒):", self.sap_timeout_edit)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        self.sap_config_widget.setLayout(layout)
    
    def init_mcp_config_ui(self):
        """初始化MCP服务器配置UI"""
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # host
        self.mcp_host_edit = QLineEdit()
        form_layout.addRow("主机:", self.mcp_host_edit)
        
        # port
        self.mcp_port_edit = QLineEdit()
        form_layout.addRow("端口:", self.mcp_port_edit)
        
        # path
        self.mcp_path_edit = QLineEdit()
        form_layout.addRow("路径:", self.mcp_path_edit)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        self.mcp_config_widget.setLayout(layout)
    
    def get_button_style(self, color):
        """获取按钮样式"""
        return """
            QPushButton {
                background-color: %s;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 10pt;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
                color: #7F8C8D;
            }
        """ % color
    
    def set_style(self):
        """设置组件样式"""
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
                border-radius: 6px;
            }
            QTabBar::tab {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-bottom-color: #FFFFFF;
                padding: 8px 20px;
                margin-right: 2px;
                font-size: 10pt;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                border-color: #CCCCCC;
                border-bottom-color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background-color: #E8E8E8;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #DDDDDD;
                border-radius: 4px;
                font-size: 10pt;
            }
            QLabel {
                font-size: 10pt;
                color: #333333;
            }
        """)
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
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
                                self.original_config[config_name] = config_value
                                self.current_config[config_name] = config_value.copy() if isinstance(config_value, dict) else config_value
            
            # 填充UI
            self.fill_ui()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载配置文件失败: {str(e)}")
    
    def fill_ui(self):
        """填充UI配置"""
        # SAP接口配置
        sap_config = self.current_config.get("SAP_CONFIG", {})
        self.sap_base_url_edit.setText(sap_config.get("base_url", ""))
        self.sap_client_id_edit.setText(sap_config.get("client_id", ""))
        self.sap_user_edit.setText(sap_config.get("sap-user", ""))
        self.sap_password_edit.setText(sap_config.get("sap-password", ""))
        self.sap_timeout_edit.setText(str(sap_config.get("timeout", 30)))
        
        # MCP服务器配置
        mcp_config = self.current_config.get("MCP_SERVER_CONFIG", {})
        self.mcp_host_edit.setText(mcp_config.get("host", ""))
        self.mcp_port_edit.setText(str(mcp_config.get("port", 8000)))
        self.mcp_path_edit.setText(mcp_config.get("path", ""))
    
    def collect_config(self):
        """从UI收集配置"""
        try:
            # SAP接口配置
            sap_config = {
                "base_url": self.sap_base_url_edit.text().strip(),
                "client_id": self.sap_client_id_edit.text().strip(),
                "sap-user": self.sap_user_edit.text().strip(),
                "sap-password": self.sap_password_edit.text().strip(),
                "timeout": int(self.sap_timeout_edit.text().strip())
            }
            self.current_config["SAP_CONFIG"] = sap_config
            
            # MCP服务器配置
            mcp_config = {
                "host": self.mcp_host_edit.text().strip(),
                "port": int(self.mcp_port_edit.text().strip()),
                "path": self.mcp_path_edit.text().strip()
            }
            self.current_config["MCP_SERVER_CONFIG"] = mcp_config
            
            return True
            
        except ValueError as e:
            QMessageBox.warning(self, "警告", f"配置值格式错误: {str(e)}")
            return False
        except Exception as e:
            QMessageBox.critical(self, "错误", f"收集配置失败: {str(e)}")
            return False
    
    def save_config(self):
        """保存配置到文件"""
        if not self.collect_config():
            return
        
        try:
            # 读取原始配置文件内容
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # 使用正则表达式替换配置
            new_content = original_content
            
            # 替换SAP_CONFIG
            sap_config = self.current_config.get("SAP_CONFIG", {})
            sap_config_str = self.format_config_dict(sap_config)
            # 使用更精确的正则表达式，匹配完整的字典（包括多行）
            new_content = re.sub(
                r'SAP_CONFIG\s*=\s*\{[\s\S]*?\n\}',
                f'SAP_CONFIG = {sap_config_str}',
                new_content
            )
            
            # 替换MCP_SERVER_CONFIG
            mcp_config = self.current_config.get("MCP_SERVER_CONFIG", {})
            mcp_config_str = self.format_config_dict(mcp_config)
            new_content = re.sub(
                r'MCP_SERVER_CONFIG\s*=\s*\{[\s\S]*?\n\}',
                f'MCP_SERVER_CONFIG = {mcp_config_str}',
                new_content
            )
            
            # 写入更新后的配置文件
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            QMessageBox.information(self, "成功", "配置已保存")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置文件失败: {str(e)}")
    
    def format_config_dict(self, config_dict):
        """格式化配置字典为字符串（用于保存到配置文件）"""
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
    
    def format_dict(self, config_dict):
        """格式化字典为字符串（已弃用，保留用于兼容性）"""
        return self.format_config_dict(config_dict)
    
    def reset_config(self):
        """重置配置"""
        # 恢复原始配置
        self.current_config = {}
        for key, value in self.original_config.items():
            self.current_config[key] = value.copy() if isinstance(value, dict) else value
        
        # 重新填充UI
        self.fill_ui()
        
        QMessageBox.information(self, "提示", "配置已重置为原始值")
    
    def apply_config(self):
        """应用配置（仅更新内存中的配置）"""
        if self.collect_config():
            QMessageBox.information(self, "提示", "配置已应用，需要保存才能生效")
