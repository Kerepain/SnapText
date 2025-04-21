class Style:
    @staticmethod
    def get_theme_colors(is_dark):
        """获取主题颜色"""
        return {
            'background': '#1e1e1e' if is_dark else '#f5f5f5',
            'card_bg': '#2d2d2d' if is_dark else '#ffffff',
            'text': '#ffffff' if is_dark else '#333333',
            'border': '#404040' if is_dark else '#ddd',
            'button': '#404040' if is_dark else '#e0e0e0',
            'button_hover': '#505050' if is_dark else '#d0d0d0',
            'button_disabled': '#303030' if is_dark else '#cccccc',
            'button_disabled_text': '#808080' if is_dark else '#666666',
            'primary_button': '#4a90e2',
            'primary_button_hover': '#357abd',
            'success_button': '#28a745',
            'success_button_hover': '#218838',
            'title': '#ffffff' if is_dark else '#000000',
        }
    
    @staticmethod
    def get_main_style(is_dark):
        """获取主窗口样式"""
        colors = Style.get_theme_colors(is_dark)
        return f"""
            QMainWindow {{
                background-color: {colors['background']};
            }}
            QWidget {{
                background-color: {colors['background']};
            }}
            QPushButton {{
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 120px;
                background-color: {colors['button']};
                color: {colors['text']};
                border: none;
            }}
            QPushButton:hover {{
                background-color: {colors['button_hover']};
            }}
            QPushButton:disabled {{
                background-color: {colors['button_disabled']};
                color: {colors['button_disabled_text']};
            }}
            QLabel {{
                color: {colors['text']};
                font-size: 13px;
            }}
            QSpinBox {{
                padding: 5px;
                border: 1px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['card_bg']};
                color: {colors['text']};
            }}
            QProgressBar {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                text-align: center;
                background-color: {colors['card_bg']};
            }}
            QProgressBar::chunk {{
                background-color: {colors['primary_button']};
            }}
            QCheckBox {{
                color: {colors['text']};
            }}
        """
    
    @staticmethod
    def get_card_style(is_dark):
        """获取卡片样式"""
        colors = Style.get_theme_colors(is_dark)
        return f"""
            CardFrame {{
                background-color: {colors['card_bg']};
                border-radius: 8px;
                border: 1px solid {colors['border']};
            }}
            QLabel {{
                color: {colors['text']};
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
            }}
        """
    
    @staticmethod
    def get_title_style(is_dark):
        """获取标题样式"""
        colors = Style.get_theme_colors(is_dark)
        return f"""
            font-size: 24px;
            font-weight: bold;
            color: {colors['title']};
            margin-bottom: 10px;
        """
    
    @staticmethod
    def get_primary_button_style(is_dark):
        """获取主要按钮样式"""
        colors = Style.get_theme_colors(is_dark)
        return f"""
            QPushButton {{
                background-color: {colors['primary_button']};
                color: white;
            }}
            QPushButton:hover {{
                background-color: {colors['primary_button_hover']};
            }}
        """
    
    @staticmethod
    def get_success_button_style(is_dark):
        """获取成功按钮样式"""
        colors = Style.get_theme_colors(is_dark)
        return f"""
            QPushButton {{
                background-color: {colors['success_button']};
                color: white;
                font-size: 14px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {colors['success_button_hover']};
            }}
        """ 