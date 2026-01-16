from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTextEdit, QComboBox, QGroupBox, QLineEdit, QFormLayout,
                             QGridLayout, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import subprocess
import os
import sys
import time
import socket
import re

class LogReaderThread(QThread):
    """日志读取线程"""
    log_received = pyqtSignal(str)
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True
    
    def run(self):
        """读取日志"""
        while self.running and self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.log_received.emit(line.strip())
                else:
                    # 没有数据时短暂休眠
                    time.sleep(0.1)
            except Exception as e:
                self.log_received.emit(f"读取日志错误: {str(e)}")
                break
    
    def stop(self):
        """停止读取"""
        self.running = False

class ServiceStatusWidget(QWidget):
    """服务状态标签页"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.service_process = None
        self.is_service_running = False
        self.log_reader_thread = None
        self.init_ui()
        self.init_timer()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 服务状态区域
        status_group = QGroupBox("服务状态")
        status_layout = QGridLayout()
        status_group.setLayout(status_layout)
        
        # 状态指示灯和文字
        status_layout.addWidget(QLabel("服务状态:"), 0, 0, Qt.AlignRight | Qt.AlignVCenter)
        
        status_layout.addLayout(self.create_status_indicator(), 0, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        # 服务地址
        status_layout.addWidget(QLabel("服务地址:"), 1, 0, Qt.AlignRight | Qt.AlignVCenter)
        self.service_address_edit = QLineEdit("http://localhost:8000/mcp")
        self.service_address_edit.setReadOnly(True)
        status_layout.addWidget(self.service_address_edit, 1, 1, 1, 2)
        
        # 启动/停止按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.start_button = QPushButton("启动服务")
        self.start_button.setMinimumHeight(30)
        self.start_button.setStyleSheet(self.get_button_style("#27AE60"))
        self.start_button.clicked.connect(self.start_service)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("停止服务")
        self.stop_button.setMinimumHeight(30)
        self.stop_button.setStyleSheet(self.get_button_style("#E74C3C"))
        self.stop_button.clicked.connect(self.stop_service)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        status_layout.addLayout(button_layout, 2, 0, 1, 3)
        
        main_layout.addWidget(status_group)
        
        # 日志显示区域
        log_group = QGroupBox("服务日志")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        # 日志控制栏
        log_control_layout = QHBoxLayout()
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["全部", "INFO", "WARNING", "ERROR"])
        log_control_layout.addWidget(QLabel("日志级别:"))
        log_control_layout.addWidget(self.log_level_combo)
        
        log_control_layout.addStretch()
        
        log_layout.addLayout(log_control_layout)
        
        # 日志文本框
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                font-family: Consolas, monospace;
                font-size: 9pt;
            }
        """)
        log_layout.addWidget(self.log_text_edit)
        
        main_layout.addWidget(log_group, 1)
        
        self.setLayout(main_layout)
        
        # 设置组件样式
        self.set_style()
    
    def create_status_indicator(self):
        """创建状态指示灯"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # 状态指示灯
        self.status_indicator = QFrame()
        self.status_indicator.setFixedSize(20, 20)
        self.status_indicator.setStyleSheet("""
            QFrame {
                border-radius: 10px;
                background-color: #E74C3C;
            }
        """)
        layout.addWidget(self.status_indicator)
        
        # 状态文字
        self.status_label = QLabel("已停止")
        self.status_label.setFont(QFont("Microsoft YaHei", 10))
        layout.addWidget(self.status_label)
        
        return layout
    
    def init_timer(self):
        """初始化定时器"""
        # 用于检查服务状态
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_service_status)
        self.check_timer.start(2000)
    
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
    
    def check_port_available(self, port):
        """检查端口是否可用
        
        Args:
            port: 端口号
            
        Returns:
            端口是否可用
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', port))
                return result != 0
        except Exception as e:
            return False
    
    def get_port_from_config(self):
        """从配置文件获取端口号
        
        Returns:
            端口号
        """
        try:
            config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "server", "config.py")
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单解析端口号
            match = re.search(r'"port":\s*(\d+)', content)
            if match:
                return int(match.group(1))
        except Exception as e:
            pass
        return 8000  # 默认端口
    
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
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #DDDDDD;
                border-radius: 4px;
                font-size: 10pt;
                background-color: #F8F9FA;
            }
            QComboBox {
                padding: 6px;
                border: 1px solid #DDDDDD;
                border-radius: 4px;
                font-size: 10pt;
            }
        """)
    
    def start_service(self):
        """启动服务"""
        try:
            # 检查端口是否可用
            port = self.get_port_from_config()
            if not self.check_port_available(port):
                # 端口被占用
                reply = QMessageBox.question(
                    self, 
                    '端口占用', 
                    f'端口 {port} 已被占用，是否要终止占用端口的进程？',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    # 终止占用端口的进程
                    try:
                        # 查找占用端口的进程
                        result = subprocess.run(
                            ['netstat', '-ano'],
                            capture_output=True,
                            text=True
                        )
                        for line in result.stdout.split('\n'):
                            if f':{port}' in line:
                                parts = line.split()
                                if len(parts) >= 5:
                                    pid = parts[-1]
                                    if pid.isdigit():
                                        subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                                        self.log_text_edit.append(f"已终止占用端口 {port} 的进程: {pid}")
                    except Exception as e:
                        self.log_text_edit.append(f"终止进程失败: {str(e)}")
                        return
                else:
                    self.log_text_edit.append(f"端口 {port} 被占用，请修改配置文件中的端口号或关闭占用端口的应用")
                    return
            
            # 构建服务启动命令
            server_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "server", "sap_mcp_server.py")
            
            # 启动服务进程
            self.service_process = subprocess.Popen(
                [sys.executable, server_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.path.dirname(os.path.dirname(__file__)))
            
            # 启动日志读取线程
            self.log_reader_thread = LogReaderThread(self.service_process)
            self.log_reader_thread.log_received.connect(self.append_log)
            self.log_reader_thread.start()
            
            # 更新UI状态
            self.update_service_indicator(True)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.log_text_edit.append("正在启动MCP服务...")
            
            # 通知主窗口更新状态栏
            self.main_window.update_service_status("运行中")
            
        except Exception as e:
            self.log_text_edit.append(f"启动服务失败: {str(e)}")
    
    def stop_service(self):
        """停止服务"""
        try:
            # 停止日志读取线程（不阻塞）
            if self.log_reader_thread:
                self.log_reader_thread.stop()
                self.log_reader_thread = None
            
            if self.service_process:
                # 终止服务进程
                self.service_process.terminate()
                
                # 不等待进程终止，直接更新UI
                self.service_process = None
            
            # 更新UI状态
            self.update_service_indicator(False)
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.log_text_edit.append("MCP服务已停止")
            
            # 通知主窗口更新状态栏
            self.main_window.update_service_status("已停止")
            
        except Exception as e:
            self.log_text_edit.append(f"停止服务失败: {str(e)}")
    
    def update_service_indicator(self, is_running):
        """更新服务状态指示灯"""
        if is_running:
            self.status_indicator.setStyleSheet("""
                QFrame {
                    border-radius: 10px;
                    background-color: #27AE60;
                }
            """)
            self.status_label.setText("运行中")
            self.is_service_running = True
        else:
            self.status_indicator.setStyleSheet("""
                QFrame {
                    border-radius: 10px;
                    background-color: #E74C3C;
                }
            """)
            self.status_label.setText("已停止")
            self.is_service_running = False
    
    def check_service_status(self):
        """检查服务状态"""
        if self.service_process:
            return_code = self.service_process.poll()
            if return_code is not None:
                # 进程已退出
                self.update_service_indicator(False)
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.log_text_edit.append(f"MCP服务异常退出，返回码: {return_code}")
                
                # 停止日志读取线程
                if self.log_reader_thread:
                    self.log_reader_thread.stop()
                    self.log_reader_thread = None
                
                self.service_process = None
                # 通知主窗口更新状态栏
                self.main_window.update_service_status("已停止")
    
    def append_log(self, log_message):
        """追加日志消息（由日志读取线程调用）"""
        self.log_text_edit.append(log_message)
        # 自动滚动到最新日志
        self.log_text_edit.verticalScrollBar().setValue(
            self.log_text_edit.verticalScrollBar().maximum()
        )
    
    def show_log(self):
        """显示日志（已弃用，现在日志自动显示）"""
        if not self.service_process:
            self.log_text_edit.append("服务未启动")
            return
        
        self.log_text_edit.append("日志已自动显示，无需手动操作")
    
    def refresh_log(self):
        """刷新日志（已弃用，现在日志自动刷新）"""
        if not self.service_process:
            self.log_text_edit.append("服务未启动")
            return
        
        self.log_text_edit.append("日志已自动刷新，无需手动操作")
    
    def update_log(self):
        """更新日志显示（已弃用，改为手动刷新）"""
        pass
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止日志读取线程
        if self.log_reader_thread:
            self.log_reader_thread.stop()
            self.log_reader_thread = None
        
        # 停止服务
        self.stop_service()
        # 停止定时器
        self.check_timer.stop()
        event.accept()
