import pyscreenshot as ImageGrab
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QScreen
import sys
import os
import platform

class ScreenshotTool(QWidget):
    # 定义信号
    screenshot_taken = pyqtSignal(str)
    screenshot_cancelled = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # 获取主屏幕
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        # 设置窗口位置和大小
        self.setGeometry(screen_geometry)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.start_point = None
        self.end_point = None
        self.is_drawing = False
        
        # 设置半透明背景
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 100);
            }
        """)
        
        # Windows特定设置
        if platform.system() == 'Windows':
            import ctypes
            # 设置窗口为最顶层
            ctypes.windll.user32.SetWindowPos(
                self.winId(),
                -1,  # HWND_TOPMOST
                0, 0, 0, 0,
                0x0001 | 0x0002  # SWP_NOMOVE | SWP_NOSIZE
            )
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key.Key_Escape:
            self.screenshot_cancelled.emit()
            self.close()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.position().toPoint()
            self.is_drawing = True
    
    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end_point = event.position().toPoint()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_drawing:
            self.is_drawing = False
            self.end_point = event.position().toPoint()
            
            # 确保坐标是有效的
            if self.start_point and self.end_point:
                # 计算矩形区域
                x = min(self.start_point.x(), self.end_point.x())
                y = min(self.start_point.y(), self.end_point.y())
                width = abs(self.end_point.x() - self.start_point.x())
                height = abs(self.end_point.y() - self.start_point.y())
                
                # 如果选择的区域太小，忽略
                if width < 10 or height < 10:
                    self.screenshot_cancelled.emit()
                    self.close()
                    return
                
                try:
                    # Windows系统使用mss进行截图
                    if platform.system() == 'Windows':
                        from mss import mss
                        with mss() as sct:
                            monitor = sct.monitors[1]  # 主显示器
                            screenshot = sct.grab({
                                'left': int(x),
                                'top': int(y),
                                'width': int(width),
                                'height': int(height)
                            })
                            # 保存截图
                            temp_path = os.path.abspath("temp_screenshot.png")
                            sct.save(screenshot, temp_path)
                    else:
                        # 其他系统使用pyscreenshot
                        screenshot = ImageGrab.grab(bbox=(int(x), int(y), int(x + width), int(y + height)))
                        temp_path = os.path.abspath("temp_screenshot.png")
                        screenshot.save(temp_path)
                    
                    # 发送信号
                    self.screenshot_taken.emit(temp_path)
                except Exception as e:
                    print(f"截图失败: {str(e)}")
                    self.screenshot_cancelled.emit()
                
                # 关闭窗口
                self.close()
    
    def paintEvent(self, event):
        if self.is_drawing and self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 255, 255), 2, Qt.PenStyle.SolidLine))
            
            # 计算矩形区域
            x = min(self.start_point.x(), self.end_point.x())
            y = min(self.start_point.y(), self.end_point.y())
            width = abs(self.end_point.x() - self.start_point.x())
            height = abs(self.end_point.y() - self.start_point.y())
            
            # 绘制矩形
            painter.drawRect(x, y, width, height)
            
            # 显示尺寸信息
            size_text = f"{width}x{height}"
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.drawText(x + 5, y + 20, size_text)

def take_screenshot():
    """创建并显示截图工具"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    tool = ScreenshotTool()
    screenshot_path = [None]  # 使用列表来存储结果
    
    def on_screenshot_taken(path):
        screenshot_path[0] = path
    
    def on_screenshot_cancelled():
        screenshot_path[0] = None
    
    # 连接信号
    tool.screenshot_taken.connect(on_screenshot_taken)
    tool.screenshot_cancelled.connect(on_screenshot_cancelled)
    
    # 显示工具
    tool.show()
    
    # 等待工具关闭
    while tool.isVisible():
        app.processEvents()
    
    return screenshot_path[0] 