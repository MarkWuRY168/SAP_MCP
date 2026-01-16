from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QMenuBar, QMenu, QAction, QStatusBar, QLabel,
                             QSystemTrayIcon, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
import sys
import os

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_status_bar()
        self.init_timer()
        self.init_system_tray()
    
    def init_ui(self):
        """初始化UI"""
        # 设置窗口标题和大小
        self.setWindowTitle("SAP MCP管理平台")
        self.setGeometry(100, 100, 1000, 700)
        
        # 设置字体
        font = QFont("Microsoft YaHei", 9)
        self.setFont(font)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 添加标签页（后续会实现具体内容）
        self.service_status_tab = QWidget()
        self.config_manager_tab = QWidget()
        self.project_info_tab = QWidget()
        
        self.tabs.addTab(self.service_status_tab, "服务状态")
        self.tabs.addTab(self.config_manager_tab, "配置管理")
        self.tabs.addTab(self.project_info_tab, "项目信息")
        
        # 设置标签页样式
        self.set_tab_style()
        
        # 设置窗口样式
        self.set_window_style()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 关闭窗口动作（最小化到托盘）
        close_action = QAction("关闭窗口", self)
        close_action.setShortcut("Ctrl+W")
        close_action.triggered.connect(self.close_window)
        file_menu.addAction(close_action)
        
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_application)
        file_menu.addAction(exit_action)
        
        # 设置菜单
        setting_menu = menu_bar.addMenu("设置")
        
        # 主题设置动作
        theme_action = QAction("主题设置", self)
        setting_menu.addAction(theme_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 关于动作
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
    
    def init_status_bar(self):
        """初始化状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # 添加状态栏标签
        self.status_label = QLabel("就绪")
        status_bar.addWidget(self.status_label)
        
        # 添加时间标签
        self.time_label = QLabel()
        status_bar.addPermanentWidget(self.time_label)
    
    def init_timer(self):
        """初始化定时器"""
        # 用于更新时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        # 初始更新时间
        self.update_time()
    
    def update_time(self):
        """更新时间显示"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)
    
    def set_tab_style(self):
        """设置标签页样式"""
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-bottom-color: #FFFFFF;
                padding: 8px 20px;
                margin-right: 2px;
                font-size: 10pt;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                border-color: #CCCCCC;
                border-bottom-color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background-color: #E8E8E8;
            }
        """)
    
    def set_window_style(self):
        """设置窗口样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F2F5;
            }
            QMenuBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E0E0E0;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #E8E8E8;
            }
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3498DB;
                color: #FFFFFF;
            }
            QStatusBar {
                background-color: #FFFFFF;
                border-top: 1px solid #E0E0E0;
            }
        """)
    
    def update_service_status(self, status):
        """更新服务状态显示"""
        self.status_label.setText(f"服务状态: {status}")
    
    def init_system_tray(self):
        """初始化系统托盘"""
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        
        # 创建托盘图标（使用内置图标）
        icon = self.create_tray_icon()
        self.tray_icon.setIcon(icon)
        
        # 设置托盘图标名称
        self.tray_icon.setToolTip("SAP_MCP")
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 显示/隐藏窗口
        self.show_hide_action = QAction("显示窗口", self)
        self.show_hide_action.triggered.connect(self.toggle_window)
        tray_menu.addAction(self.show_hide_action)
        
        # 退出应用
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.exit_application)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        
        # 双击托盘图标显示/隐藏窗口
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # 显示托盘图标
        self.tray_icon.show()
    
    def create_tray_icon(self):
        """创建托盘图标"""
        # 使用内置图标
        from PyQt5.QtWidgets import QStyle
        style = self.style()
        icon = style.standardIcon(QStyle.SP_ComputerIcon)
        return icon
    
    def tray_icon_activated(self, reason):
        """托盘图标被激活"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window()
    
    def toggle_window(self):
        """切换窗口显示/隐藏"""
        if self.isVisible():
            self.hide()
            self.show_hide_action.setText("显示窗口")
        else:
            self.show()
            self.show_hide_action.setText("隐藏窗口")
            self.activateWindow()
            self.raise_()
    
    def close_window(self):
        """关闭窗口（最小化到托盘）"""
        self.hide()
        self.show_hide_action.setText("显示窗口")
    
    def exit_application(self):
        """退出应用程序"""
        reply = QMessageBox.question(
            self,
            '确认退出',
            '确定要退出应用程序吗？这将停止所有服务。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 停止服务
            if hasattr(self, 'service_status_widget') and self.service_status_widget:
                self.service_status_widget.stop_service()
            
            # 隐藏托盘图标
            self.tray_icon.hide()
            
            # 退出应用
            QApplication.instance().quit()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 阻止窗口关闭，改为最小化到托盘
        event.ignore()
        self.close_window()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
