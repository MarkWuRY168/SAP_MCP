from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
                             QTextEdit, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import os

class ProjectInfoWidget(QWidget):
    """项目信息标签页"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 项目基本信息
        basic_info_group = QGroupBox("项目基本信息")
        basic_info_layout = QGridLayout()
        basic_info_layout.setVerticalSpacing(15)
        basic_info_group.setLayout(basic_info_layout)
        
        # 项目名称
        basic_info_layout.addWidget(QLabel("项目名称:"), 0, 0, Qt.AlignRight | Qt.AlignVCenter)
        project_name_label = QLabel("SAP MCP 管理平台")
        project_name_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        basic_info_layout.addWidget(project_name_label, 0, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        # 项目描述
        basic_info_layout.addWidget(QLabel("项目描述:"), 1, 0, Qt.AlignRight | Qt.AlignTop)
        project_desc_text = QTextEdit()
        project_desc_text.setReadOnly(True)
        project_desc_text.setFixedHeight(60)
        project_desc_text.setPlainText("SAP MCP（Management Control Platform）是一个用于管理和控制SAP系统的平台，提供了一系列工具和接口，方便用户与SAP系统进行交互。")
        project_desc_text.setStyleSheet(self.get_text_edit_style())
        basic_info_layout.addWidget(project_desc_text, 1, 1)
        
        # 技术栈
        basic_info_layout.addWidget(QLabel("技术栈:"), 2, 0, Qt.AlignRight | Qt.AlignTop)
        tech_stack_text = QTextEdit()
        tech_stack_text.setReadOnly(True)
        tech_stack_text.setFixedHeight(80)
        tech_stack_text.setPlainText("- Python：主要开发语言\n- FastMCP：用于创建MCP服务器\n- httpx：用于发送HTTP请求\n- PyQt5：用于GUI界面开发")
        tech_stack_text.setStyleSheet(self.get_text_edit_style())
        basic_info_layout.addWidget(tech_stack_text, 2, 1)
        
        main_layout.addWidget(basic_info_group)
        
        # 开发人员信息
        dev_info_group = QGroupBox("开发人员信息")
        dev_info_layout = QGridLayout()
        dev_info_layout.setVerticalSpacing(15)
        dev_info_group.setLayout(dev_info_layout)
        
        # 产品设计
        dev_info_layout.addWidget(QLabel("产品设计:"), 0, 0, Qt.AlignRight | Qt.AlignVCenter)
        dev_info_layout.addWidget(QLabel("Mark（吴让宇）"), 0, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        # 开发人员
        dev_info_layout.addWidget(QLabel("开发人员:"), 1, 0, Qt.AlignRight | Qt.AlignVCenter)
        dev_info_layout.addWidget(QLabel("Mark（吴让宇）"), 1, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        # 联系电话
        dev_info_layout.addWidget(QLabel("联系电话:"), 2, 0, Qt.AlignRight | Qt.AlignVCenter)
        dev_info_layout.addWidget(QLabel("18685095797"), 2, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        # QQ
        dev_info_layout.addWidget(QLabel("QQ:"), 3, 0, Qt.AlignRight | Qt.AlignVCenter)
        dev_info_layout.addWidget(QLabel("121980331"), 3, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        # 邮箱
        dev_info_layout.addWidget(QLabel("邮箱:"), 4, 0, Qt.AlignRight | Qt.AlignVCenter)
        dev_info_layout.addWidget(QLabel("121980331@qq.com"), 4, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        main_layout.addWidget(dev_info_group)
        
        # 产品功能
        product_func_group = QGroupBox("产品功能")
        product_func_layout = QVBoxLayout()
        product_func_group.setLayout(product_func_layout)
        
        func_list = [
            "1. 取得工具清单：调用SAP接口返回工具清单数据",
            "2. 根据工具号取得工具明细：调用SAP接口返回工具明细，包括传入传出参数",
            "3. 使用工具：根据工具明细，将数据转换为可识别的格式，调用SAP接口返回执行结果",
            "4. 服务状态监控：实时显示MCP服务运行状态",
            "5. 配置管理：方便用户修改和管理系统配置",
            "6. 日志管理：查看和管理服务运行日志"
        ]
        
        func_text = QTextEdit()
        func_text.setReadOnly(True)
        func_text.setPlainText("\n".join(func_list))
        func_text.setStyleSheet(self.get_text_edit_style())
        product_func_layout.addWidget(func_text)
        
        main_layout.addWidget(product_func_group)
        
        # 产品推广
        promote_group = QGroupBox("产品推广")
        promote_layout = QVBoxLayout()
        promote_group.setLayout(promote_layout)
        
        promote_text = QTextEdit()
        promote_text.setReadOnly(True)
        promote_text.setPlainText("SAP MCP管理平台是一款功能强大、易于使用的SAP系统管理工具。它提供了直观的图形界面，让用户能够轻松地管理和控制SAP系统，提高工作效率，降低操作风险。\n\n产品优势：\n- 简约商务风格的界面设计，易于使用\n- 实时监控服务状态，确保系统稳定运行\n- 灵活的配置管理，适应不同的业务需求\n- 完整的日志记录，便于故障排查和分析\n- 强大的工具支持，方便与SAP系统进行交互\n\n应用场景：\n- SAP系统管理员日常管理和维护\n- 开发人员调试和测试SAP接口\n- 业务人员快速访问SAP系统功能\n- 企业级SAP系统集成和扩展")
        promote_text.setStyleSheet(self.get_text_edit_style())
        promote_layout.addWidget(promote_text)
        
        main_layout.addWidget(promote_group)
        
        # 版本信息
        version_frame = QFrame()
        version_frame.setStyleSheet("""
            QFrame {
                border-top: 1px solid #E0E0E0;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        version_layout = QHBoxLayout()
        version_frame.setLayout(version_layout)
        
        version_label = QLabel("版本信息：v1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #7F8C8D; font-size: 9pt;")
        version_layout.addWidget(version_label)
        
        main_layout.addWidget(version_frame)
        
        self.setLayout(main_layout)
        
        # 设置样式
        self.set_style()
    
    def get_text_edit_style(self):
        """获取文本框样式"""
        return """
            QTextEdit {
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                border-radius: 4px;
                font-size: 10pt;
                font-family: Microsoft YaHei;
            }
            QTextEdit:focus {
                border-color: #3498DB;
                outline: none;
            }
        """
    
    def set_style(self):
        """设置组件样式"""
        self.setStyleSheet("""
            QGroupBox {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 15px;
                margin-bottom: 10px;
                font-size: 11pt;
                font-weight: bold;
            }
            QLabel {
                font-size: 10pt;
                color: #333333;
                font-family: Microsoft YaHei;
            }
            QGridLayout {
                background-color: #FFFFFF;
            }
        """)
