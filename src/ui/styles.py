"""
应用样式定义
"""

class Style:
    """样式类，定义应用的各种样式"""
    
    @staticmethod
    def get_main_style(isDark=False):
        """获取主窗口样式"""
        bg_color = "#2d2d2d" if isDark else "#f5f5f5"
        text_color = "#eeeeee" if isDark else "#333333"
        
        return f"""
            QMainWindow {{
                background-color: {bg_color};
                color: {text_color};
            }}
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
            }}
            QLabel {{
                color: {text_color};
            }}
            QPushButton {{
                background-color: {"#3d3d3d" if isDark else "#e0e0e0"};
                color: {text_color};
                border-radius: 4px;
                padding: 6px 12px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {"#4d4d4d" if isDark else "#d0d0d0"};
            }}
            QPushButton:pressed {{
                background-color: {"#5d5d5d" if isDark else "#c0c0c0"};
            }}
            QSpinBox {{
                background-color: {"#3d3d3d" if isDark else "#ffffff"};
                color: {text_color};
                border: 1px solid {"#5d5d5d" if isDark else "#c0c0c0"};
                border-radius: 4px;
                padding: 2px;
            }}
            QProgressBar {{
                border: 1px solid {"#5d5d5d" if isDark else "#c0c0c0"};
                border-radius: 4px;
                background-color: {"#3d3d3d" if isDark else "#f0f0f0"};
                text-align: center;
                color: {"#eeeeee" if isDark else "#333333"};
            }}
            QProgressBar::chunk {{
                background-color: #4a90e2;
                width: 10px;
                margin: 0.5px;
            }}
            QCheckBox {{
                color: {text_color};
            }}
        """
    
    @staticmethod
    def get_title_style(isDark=False):
        """获取标题样式"""
        title_color = "#ffffff" if isDark else "#333333"
        
        return f"""
            QLabel {{
                color: {title_color};
                font-size: 18px;
                font-weight: bold;
                margin-left: 5px;
            }}
        """
    
    @staticmethod
    def get_card_style(isDark=False):
        """获取卡片样式"""
        bg_color = "#3d3d3d" if isDark else "#ffffff"
        border_color = "#5d5d5d" if isDark else "#dddddd"
        
        return f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 15px;
            }}
        """
    
    @staticmethod
    def get_primary_button_style(isDark=False):
        """获取主要按钮样式"""
        text_color = "#ffffff"
        
        return f"""
            QPushButton {{
                background-color: #4a90e2;
                color: {text_color};
                border-radius: 4px;
                padding: 6px 12px;
                min-height: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #357abd;
            }}
            QPushButton:pressed {{
                background-color: #2a5d9c;
            }}
        """
    
    @staticmethod
    def get_success_button_style(isDark=False):
        """获取成功按钮样式"""
        text_color = "#ffffff"
        
        return f"""
            QPushButton {{
                background-color: #4caf50;
                color: {text_color};
                border-radius: 4px;
                padding: 6px 12px;
                min-height: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #3d8b40;
            }}
            QPushButton:pressed {{
                background-color: #2d682f;
            }}
        """
    
    @staticmethod
    def get_github_button_style(isDark=False):
        """获取GitHub按钮样式"""
        if isDark:
            return """
                QPushButton {
                    background-color: #2b3137;
                    color: white;
                    border: 1px solid #444d56;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3f464e;
                }
                QPushButton:pressed {
                    background-color: #24292e;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #fafbfc;
                    color: #24292e;
                    border: 1px solid #e1e4e8;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #f3f4f6;
                }
                QPushButton:pressed {
                    background-color: #e1e4e8;
                }
            """ 