import pyautogui
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap

class ScreenshotWidget(QWidget):
    finished = pyqtSignal(object)  # 截图完成信号
    position_selected = pyqtSignal(QPoint)  # 位置选择信号
    
    def __init__(self, mode="screenshot"):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        self.start_pos = None
        self.end_pos = None
        self.selection_rect = None
        self.mode = mode  # "screenshot" 或 "position"
        self.click_pos = None
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 绘制半透明背景
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        # 如果有选择区域，绘制白色边框
        if self.selection_rect:
            painter.setPen(QPen(Qt.GlobalColor.white, 2))
            painter.drawRect(self.selection_rect)
        
        # 如果已选择位置，绘制标记
        if self.click_pos:
            painter.setPen(QPen(Qt.GlobalColor.red, 2))
            painter.drawEllipse(self.click_pos, 5, 5)
    
    def mousePressEvent(self, event):
        if self.mode == "screenshot":
            self.start_pos = event.pos()
            self.selection_rect = None
        else:
            self.click_pos = event.pos()
            self.position_selected.emit(self.click_pos)
            self.close()
        self.update()
    
    def mouseMoveEvent(self, event):
        if self.mode == "screenshot" and self.start_pos:
            self.end_pos = event.pos()
            self.selection_rect = QRect(self.start_pos, self.end_pos).normalized()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if self.mode == "screenshot" and self.selection_rect:
            # 获取截图
            screenshot = pyautogui.screenshot(region=(
                self.selection_rect.x(),
                self.selection_rect.y(),
                self.selection_rect.width(),
                self.selection_rect.height()
            ))
            self.close()
            self.finished.emit(screenshot)
        return None

class PositionSelector(QWidget):
    position_selected = pyqtSignal(QPoint)
    
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("选择文字位置")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # 加载图片
        pixmap = QPixmap(image_path)
        self.setFixedSize(pixmap.size())
        
        # 创建标签显示图片
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)
    
    def mousePressEvent(self, event):
        self.position_selected.emit(event.pos())
        self.close()

def take_screenshot():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    
    widget = ScreenshotWidget(mode="screenshot")
    widget.show()
    app.exec()
    
    return widget.selection_rect

def select_position(image_path):
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    
    widget = PositionSelector(image_path)
    widget.show()
    app.exec()
    
    return widget.position_selected 