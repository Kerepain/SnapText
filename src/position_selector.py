from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QApplication, 
                           QDialog, QPushButton, QHBoxLayout, QFontDialog,
                           QColorDialog, QSpinBox)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QFont

class PositionSelector(QDialog):
    position_selected = pyqtSignal(list)  # 修改信号类型为list
    
    def __init__(self, image_path, preview_texts, previous_positions=None):
        super().__init__()
        self.setWindowTitle("文字位置预览")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 加载截图
        self.pixmap = QPixmap(image_path)
        if self.pixmap.isNull():
            print(f"无法加载图片: {image_path}")
            return
        
        # 记录原始图片尺寸
        self.original_size = self.pixmap.size()
        
        # 如果截图太大，调整窗口大小
        screen_size = QApplication.primaryScreen().size()
        if self.pixmap.width() > screen_size.width() * 0.8 or \
           self.pixmap.height() > screen_size.height() * 0.8:
            self.pixmap = self.pixmap.scaled(
                screen_size.width() * 0.8,
                screen_size.height() * 0.8,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        
        # 创建图片标签
        self.image_label = QLabel()
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)
        
        # 创建控制布局
        control_layout = QHBoxLayout()
        
        # 添加字体选择按钮
        self.font_button = QPushButton("选择字体")
        self.font_button.clicked.connect(self.select_font)
        control_layout.addWidget(self.font_button)
        
        # 添加颜色选择按钮
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.select_color)
        control_layout.addWidget(self.color_button)
        
        # 添加字体大小选择
        self.size_label = QLabel("字体大小:")
        control_layout.addWidget(self.size_label)
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(16)
        self.size_spin.valueChanged.connect(self.on_size_changed)
        control_layout.addWidget(self.size_spin)
        
        main_layout.addLayout(control_layout)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 添加确定按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        
        # 添加取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
        
        # 初始化变量
        self.click_positions = []  # 存储所有点击位置
        self.preview_texts = preview_texts  # 预览文本列表
        self.font = QFont("Arial", 16)
        self.color = QColor(255, 0, 0)  # 默认红色
        self.previous_positions = previous_positions or []  # 存储之前的位置信息
        self.current_position_index = 0  # 当前正在选择的位置索引
        
        # 设置鼠标追踪
        self.image_label.setMouseTracking(True)
        
        # 设置窗口大小
        self.resize(800, 600)
        
        # 添加提示标签
        self.hint_label = QLabel(f"点击图片选择位置 {self.current_position_index + 1}", self)
        self.hint_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        self.hint_label.adjustSize()
        self.hint_label.move(10, 10)
        
        # 创建一个覆盖层用于绘制文字
        self.overlay = QLabel(self.image_label)
        self.overlay.setGeometry(0, 0, self.image_label.width(), self.image_label.height())
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay.setStyleSheet("background: transparent;")
        
        # 连接图片标签的鼠标事件
        self.image_label.mousePressEvent = self.image_mousePressEvent
        self.image_label.mouseMoveEvent = self.image_mouseMoveEvent
    
    def get_relative_position(self, pos):
        """将屏幕坐标转换为相对于图片的坐标"""
        # 获取图片在标签中的实际显示区域
        label_size = self.image_label.size()
        pixmap_size = self.pixmap.size()
        
        # 计算缩放比例
        scale_x = self.original_size.width() / pixmap_size.width()
        scale_y = self.original_size.height() / pixmap_size.height()
        
        # 计算图片在标签中的偏移
        offset_x = (label_size.width() - pixmap_size.width()) / 2
        offset_y = (label_size.height() - pixmap_size.height()) / 2
        
        # 转换为原始图片坐标
        original_x = (pos.x() - offset_x) * scale_x
        original_y = (pos.y() - offset_y) * scale_y
        
        return QPoint(int(original_x), int(original_y))
    
    def image_mousePressEvent(self, event):
        """图片区域鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 更新点击位置（转换为原始图片坐标）
            pos = self.get_relative_position(event.pos())
            
            # 如果已经选择了这个位置，则跳过
            if pos in self.click_positions:
                return
            
            # 添加新位置
            self.click_positions.append(pos)
            
            # 更新提示
            self.current_position_index += 1
            if self.current_position_index < len(self.preview_texts):
                self.hint_label.setText(f"点击图片选择位置 {self.current_position_index + 1}")
            else:
                self.hint_label.setText("所有位置已选择完成")
            
            self.update_preview()
    
    def image_mouseMoveEvent(self, event):
        """图片区域鼠标移动事件"""
        if self.current_position_index < len(self.preview_texts):
            # 更新当前位置（转换为原始图片坐标）
            self.current_position = self.get_relative_position(event.pos())
            self.update_preview()
    
    def select_font(self):
        """选择字体"""
        font, ok = QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
            self.update_preview()
    
    def select_color(self):
        """选择颜色"""
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.update_preview()
    
    def on_size_changed(self, size):
        """字体大小改变事件"""
        self.font.setPointSize(size)
        self.update_preview()
    
    def update_preview(self):
        """更新预览"""
        # 创建新的图片用于绘制
        overlay_pixmap = QPixmap(self.image_label.width(), self.image_label.height())
        overlay_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(overlay_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # 获取图片在标签中的实际显示区域
        label_size = self.image_label.size()
        pixmap_size = self.pixmap.size()
        
        # 计算缩放比例
        scale_x = pixmap_size.width() / self.original_size.width()
        scale_y = pixmap_size.height() / self.original_size.height()
        
        # 计算图片在标签中的偏移
        offset_x = (label_size.width() - pixmap_size.width()) / 2
        offset_y = (label_size.height() - pixmap_size.height()) / 2
        
        # 绘制之前的位置
        for pos_info in self.previous_positions:
            painter.setFont(pos_info['font'])
            painter.setPen(pos_info['color'])
            
            # 计算文字位置（转换为显示坐标）
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(pos_info['text'])
            text_height = metrics.height()
            
            # 转换为显示坐标
            display_x = pos_info['position'].x() * scale_x + offset_x
            display_y = pos_info['position'].y() * scale_y + offset_y
            
            # 调整位置，使文字居中
            x = display_x - text_width / 2
            y = display_y + text_height / 4
            
            # 确保使用整数坐标
            x = int(x)
            y = int(y)
            
            # 绘制文字
            painter.drawText(x, y, pos_info['text'])
        
        # 绘制已选择的位置
        for i, pos in enumerate(self.click_positions):
            if i < len(self.preview_texts):
                painter.setFont(self.font)
                painter.setPen(self.color)
                
                # 计算文字位置（转换为显示坐标）
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(self.preview_texts[i])
                text_height = metrics.height()
                
                # 转换为显示坐标
                display_x = pos.x() * scale_x + offset_x
                display_y = pos.y() * scale_y + offset_y
                
                # 调整位置，使文字居中
                x = display_x - text_width / 2
                y = display_y + text_height / 4
                
                # 确保使用整数坐标
                x = int(x)
                y = int(y)
                
                # 绘制文字
                painter.drawText(x, y, self.preview_texts[i])
        
        # 绘制当前位置（如果还有位置要选择）
        if hasattr(self, 'current_position') and self.current_position_index < len(self.preview_texts):
            painter.setFont(self.font)
            painter.setPen(self.color)
            
            # 计算文字位置（转换为显示坐标）
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(self.preview_texts[self.current_position_index])
            text_height = metrics.height()
            
            # 转换为显示坐标
            display_x = self.current_position.x() * scale_x + offset_x
            display_y = self.current_position.y() * scale_y + offset_y
            
            # 调整位置，使文字居中
            x = display_x - text_width / 2
            y = display_y + text_height / 4
            
            # 确保使用整数坐标
            x = int(x)
            y = int(y)
            
            # 绘制文字
            painter.drawText(x, y, self.preview_texts[self.current_position_index])
        
        painter.end()
        self.overlay.setPixmap(overlay_pixmap)
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        self.overlay.setGeometry(0, 0, self.image_label.width(), self.image_label.height())
        self.update_preview()
    
    def accept(self):
        """确定按钮点击事件"""
        if len(self.click_positions) == len(self.preview_texts):
            # 保存所有位置设置
            positions = []
            
            # 添加调试输出
            print("\n保存位置信息:")
            print(f"原始图片尺寸: {self.original_size.width()} x {self.original_size.height()}")
            print(f"显示图片尺寸: {self.pixmap.width()} x {self.pixmap.height()}")
            
            for i, pos in enumerate(self.click_positions):
                # 获取文字测量信息
                painter = QPainter()
                painter.begin(self.pixmap)
                painter.setFont(self.font)
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(self.preview_texts[i])
                text_height = metrics.height()
                painter.end()
                
                # 计算绘制位置
                draw_x = pos.x() - text_width / 2
                draw_y = pos.y() + text_height / 4
                
                # 确保整数坐标
                draw_x = int(draw_x)
                draw_y = int(draw_y)
                
                # 计算相对坐标(百分比)
                relative_x = pos.x() / self.original_size.width()
                relative_y = pos.y() / self.original_size.height()
                
                # 计算相对字体大小
                relative_font_size = self.font.pointSize() / self.original_size.height()
                
                print(f"位置 {i+1}:")
                print(f"  原始点击坐标: ({pos.x()}, {pos.y()})")
                print(f"  相对坐标: ({relative_x:.6f}, {relative_y:.6f})")
                print(f"  相对字体大小: {relative_font_size:.6f}")
                print(f"  文字宽度: {text_width}, 高度: {text_height}")
                print(f"  计算后绘制坐标: ({draw_x}, {draw_y})")
                
                # 保存所有位置相关信息
                positions.append({
                    'position': pos,
                    'text': self.preview_texts[i],
                    'font': self.font,
                    'color': self.color,
                    'index': i,  # 添加索引信息
                    'text_width': text_width,  # 保存文字宽度
                    'text_height': text_height,  # 保存文字高度
                    'draw_x': draw_x,  # 保存计算后的绘制x坐标
                    'draw_y': draw_y,   # 保存计算后的绘制y坐标
                    'relative_x': relative_x,  # 相对横坐标(百分比)
                    'relative_y': relative_y,  # 相对纵坐标(百分比)
                    'relative_font_size': relative_font_size  # 相对字体大小
                })
            
            self.position_selected.emit(positions)
        
        super().accept() 