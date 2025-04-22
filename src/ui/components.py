"""
UI通用组件
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QDialog, QTextEdit
from PyQt6.QtCore import Qt
from src.ui.styles import Style

class CardFrame(QFrame):
    """卡片样式框架组件"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.updateStyle()
        self.layout = QVBoxLayout(self)
        if title:
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(title_label)
    
    def updateStyle(self):
        """更新样式"""
        isDark = self.window().isDarkMode if hasattr(self.window(), 'isDarkMode') else False
        self.setStyleSheet(Style.get_card_style(isDark))

class CSVFormatDialog(QDialog):
    """CSV格式说明对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CSV格式说明")
        self.setMinimumWidth(500)
        
        # 获取当前主题模式
        isDark = self.window().isDarkMode if hasattr(self.window(), 'isDarkMode') else False
        
        layout = QVBoxLayout()
        
        # 添加说明文本
        text = QTextEdit()
        text.setReadOnly(True)
        # 根据主题设置文本颜色
        text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {'#2d2d2d' if isDark else '#ffffff'};
                color: {'#ffffff' if isDark else '#000000'};
                border: 1px solid {'#404040' if isDark else '#ddd'};
                border-radius: 4px;
                padding: 10px;
            }}
        """)
        text.setHtml("""
            <h3>CSV文件格式说明</h3>
            <p>请按照以下格式准备CSV文件：</p>
            <ol>
                <li>使用UTF-8编码保存文件</li>
                <li>每行代表一组数据</li>
                <li>数据之间用逗号分隔</li>
                <li>数据顺序要与文字位置一一对应</li>
            </ol>
            <p><b>示例：</b></p>
            <pre>张三,25,男
李四,30,女
王五,28,男</pre>
            <p><b>说明：</b></p>
            <ul>
                <li>第一列对应第一个文字位置</li>
                <li>第二列对应第二个文字位置</li>
                <li>第三列对应第三个文字位置</li>
                <li>以此类推...</li>
            </ul>
            <p><b>注意事项：</b></p>
            <ul>
                <li>确保CSV文件中的数据列数与设置的文字位置数量相同</li>
                <li>如果数据中包含逗号，请用双引号将整个字段括起来</li>
                <li>建议使用Excel或Numbers等软件编辑后导出为CSV格式</li>
            </ul>
        """)
        layout.addWidget(text)
        
        # 添加确定按钮
        ok_button = QPushButton("我知道了")
        ok_button.setStyleSheet(Style.get_primary_button_style(isDark))
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout) 