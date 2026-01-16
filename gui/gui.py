import sys
import os

from PyQt5.QtWidgets import QApplication, QVBoxLayout

from main_window import MainWindow
from service_status import ServiceStatusWidget
from config_manager import ConfigManagerWidget
from project_info import ProjectInfoWidget

class SAPMCPGUI:
    """SAP MCP GUI应用"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.init_tabs()
    
    def init_tabs(self):
        """初始化标签页"""
        # 服务状态标签页
        self.service_status_widget = ServiceStatusWidget(self.window)
        service_status_layout = QVBoxLayout()
        service_status_layout.addWidget(self.service_status_widget)
        self.window.service_status_tab.setLayout(service_status_layout)
        # 保存service_status_widget到window对象中，以便在退出时访问
        self.window.service_status_widget = self.service_status_widget
        
        # 配置管理标签页
        self.config_manager_widget = ConfigManagerWidget()
        config_manager_layout = QVBoxLayout()
        config_manager_layout.addWidget(self.config_manager_widget)
        self.window.config_manager_tab.setLayout(config_manager_layout)
        
        # 项目信息标签页
        self.project_info_widget = ProjectInfoWidget()
        project_info_layout = QVBoxLayout()
        project_info_layout.addWidget(self.project_info_widget)
        self.window.project_info_tab.setLayout(project_info_layout)
    
    def run(self):
        """运行应用"""
        self.window.show()
        return self.app.exec_()

if __name__ == "__main__":
    gui = SAPMCPGUI()
    sys.exit(gui.run())
