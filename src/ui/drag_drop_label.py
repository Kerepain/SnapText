"""
拖放标签组件
"""
import os
from PyQt6.QtWidgets import QLabel, QMainWindow
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

class DragDropLabel(QLabel):
    """支持拖放的标签"""
    
    # 定义信号
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None, is_image=True):
        super().__init__(parent)
        self.is_image = is_image
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(100)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaaaaa;
                border-radius: 5px;
                padding: 5px;
                background-color: rgba(0, 0, 0, 0.05);
            }
        """)
        
        # 设置提示文字
        if is_image:
            self.setText("拖放图片到这里\n或点击导入图片按钮")
        else:
            self.setText("拖放数据文件到这里\n或点击导入文本数据按钮")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        # 检查是否有URL，通常是文件拖拽
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            
            # 检查文件类型
            if self.is_valid_file(file_path):
                event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        file_path = event.mimeData().urls()[0].toLocalFile()
        
        # 找到主窗口对象
        main_window = self.get_main_window()
        if main_window:
            # 发出信号，传递文件路径
            if self.is_image:
                main_window.on_image_dropped(file_path)
            else:
                main_window.on_csv_dropped(file_path)
    
    def get_main_window(self):
        """获取MainWindow实例"""
        # 递归查找父窗口，直到找到MainWindow对象
        parent = self.parent()
        while parent is not None:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None
    
    def is_valid_file(self, file_path):
        """检查是否为有效文件"""
        if not os.path.isfile(file_path):
            return False
            
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if self.is_image:
            # 检查是否为图片文件
            return ext in ['.png', '.jpg', '.jpeg', '.bmp']
        else:
            # 检查是否为数据文件
            return ext in ['.csv', '.txt'] 