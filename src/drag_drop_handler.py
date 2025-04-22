from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import os

class DragDropHandler:
    """处理拖放功能的类"""
    
    def __init__(self, parent: QWidget):
        self.parent = parent
        self.supported_image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
        self.supported_csv_extensions = ['.csv', '.txt']
    
    def setup_drag_drop(self, widget: QWidget, is_image: bool = True):
        """设置拖放功能
        
        Args:
            widget: 要启用拖放的部件
            is_image: 是否为图片拖放(True为图片,False为CSV)
        """
        widget.setAcceptDrops(True)
        widget.dragEnterEvent = lambda event: self.drag_enter_event(event, is_image)
        widget.dropEvent = lambda event: self.drop_event(event, is_image)
    
    def drag_enter_event(self, event: QDragEnterEvent, is_image: bool):
        """处理拖入事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                ext = os.path.splitext(file_path)[1].lower()
                
                if is_image and ext in self.supported_image_extensions:
                    event.acceptProposedAction()
                elif not is_image and ext in self.supported_csv_extensions:
                    event.acceptProposedAction()
    
    def drop_event(self, event: QDropEvent, is_image: bool):
        """处理放下事件"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            ext = os.path.splitext(file_path)[1].lower()
            
            if is_image and ext in self.supported_image_extensions:
                self.parent.on_image_dropped(file_path)
            elif not is_image and ext in self.supported_csv_extensions:
                self.parent.on_csv_dropped(file_path)

class DragDropLabel(QLabel):
    """支持拖放的标签类"""
    
    def __init__(self, parent: QWidget, is_image: bool = True):
        super().__init__(parent)
        self.drag_handler = DragDropHandler(parent)
        self.drag_handler.setup_drag_drop(self, is_image)
        
        # 设置默认文本和样式
        self.setText("拖放文件到这里" + ("\n(支持PNG/JPG/BMP)" if is_image else "\n(支持CSV/TXT)"))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QLabel:hover {
                border-color: #4a90e2;
                background-color: rgba(74, 144, 226, 0.1);
            }
        """) 