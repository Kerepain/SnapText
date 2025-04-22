"""
文字位置选择器
"""
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                          QSpinBox, QCheckBox, QApplication, QWidget, QFontDialog, QColorDialog, QSlider, QSizePolicy)
from PyQt6.QtGui import QPixmap, QPainter, QPen, QFont, QColor, QFontMetrics, QImage
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QSize, QSizeF
from src.utils.logger import logger

class PositionSelector(QDialog):
    """
    位置选择器对话框，用于在图片上选择文本位置
    """
    position_selected = pyqtSignal(list)  # 修改信号类型为list
    
    def __init__(self, image_path, preview_texts, previous_positions=None):
        """
        初始化位置选择器
        
        Args:
            image_path: 图片路径
            preview_texts: 预览文本列表
            previous_positions: 之前选择的位置(可选)
        """
        super().__init__()
        
        logger.info("初始化位置选择器")
        
        self.setWindowTitle("选择文本位置")
        self.resize(800, 600)
        
        # 保存图片路径和预览文本
        self.image_path = image_path
        self.preview_texts = preview_texts
        self.previous_positions = previous_positions
        
        # 初始化字体和颜色 - 默认设置为红色和大小60
        self.font = QFont("Arial", 60)
        self.font.setBold(True)  # 默认加粗
        self.color = QColor(255, 0, 0)  # 默认红色
        
        # 点击位置列表
        self.click_positions = []
        if previous_positions:
            logger.info(f"使用之前的位置配置: {len(previous_positions)}个位置")
            # 从之前保存的位置恢复
            for pos_data in previous_positions:
                relative_x = pos_data.get('relative_x', 0.5)
                relative_y = pos_data.get('relative_y', 0.5)
                
                # 字体配置
                if 'font' in pos_data:
                    self.font = pos_data['font']
                if 'color' in pos_data:
                    self.color = pos_data['color']
                
                # 等待图片加载后再计算实际像素位置
                self.click_positions.append(QPoint(-1, -1))  # 临时点位，稍后更新
        
        self.current_position_index = 0
        
        # 设置布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 图片显示
        image_layout = QVBoxLayout()
        
        # 图片标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setMouseTracking(True)  # 启用鼠标跟踪
        self.image_label.mousePressEvent = self.image_mousePressEvent
        self.image_label.mouseMoveEvent = self.image_mouseMoveEvent
        
        # 创建叠加层用于绘制选择点和预览文本
        self.overlay = QLabel(self.image_label)
        self.overlay.setMouseTracking(True)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        image_layout.addWidget(self.image_label)
        
        # 加载图片
        self.pixmap = QPixmap(self.image_path)
        if self.pixmap.isNull():
            logger.error(f"无法加载图片: {self.image_path}")
            self.image_label.setText("无法加载图片")
        else:
            logger.info(f"已加载图片: {self.image_path}")
            self.original_size = QSize(self.pixmap.width(), self.pixmap.height())
            
            # 调整图片大小以适应窗口
            if self.pixmap.width() > 700 or self.pixmap.height() > 500:
                self.pixmap = self.pixmap.scaled(700, 500, Qt.AspectRatioMode.KeepAspectRatio)
            
            self.image_label.setPixmap(self.pixmap)
            self.overlay.setGeometry(0, 0, self.image_label.width(), self.image_label.height())
            
            # 更新之前选择的位置的实际像素坐标
            if previous_positions:
                for i, pos_data in enumerate(previous_positions):
                    if i < len(self.click_positions):
                        relative_x = pos_data.get('relative_x', 0.5)
                        relative_y = pos_data.get('relative_y', 0.5)
                        
                        # 计算实际像素位置
                        pixel_x = int(relative_x * self.original_size.width())
                        pixel_y = int(relative_y * self.original_size.height())
                        
                        self.click_positions[i] = QPoint(pixel_x, pixel_y)
        
        # 提示标签
        instruction_label = QLabel()
        instruction_label.setText(f"请在图片上点击选择文本位置，共需选择{len(self.preview_texts)}个位置")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 文本样式设置
        style_layout = QHBoxLayout()
        
        font_button = QPushButton("选择字体")
        font_button.clicked.connect(self.select_font)
        
        color_button = QPushButton("选择颜色")
        color_button.clicked.connect(self.select_color)
        
        # 扩大字体大小范围
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(8)
        self.size_slider.setMaximum(120)  # 增大最大字体大小
        self.size_slider.setValue(self.font.pointSize())
        self.size_slider.valueChanged.connect(self.on_size_changed)
        
        self.bold_checkbox = QCheckBox("粗体")
        self.bold_checkbox.setChecked(self.font.bold())
        self.bold_checkbox.stateChanged.connect(self.on_bold_changed)
        
        style_layout.addWidget(font_button)
        style_layout.addWidget(color_button)
        style_layout.addWidget(QLabel("大小:"))
        style_layout.addWidget(self.size_slider)
        style_layout.addWidget(self.bold_checkbox)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        # 添加所有布局
        layout.addLayout(image_layout)
        layout.addWidget(instruction_label)
        layout.addLayout(style_layout)
        layout.addLayout(button_layout)
        
        # 更新预览
        self.update_preview()
        
    def get_relative_position(self, pos):
        """
        获取相对于原始图片的位置比例
        
        Args:
            pos: 点击位置
        
        Returns:
            相对位置坐标(QPoint)
        """
        if self.pixmap and not self.pixmap.isNull():
            # 计算相对于当前显示图片的位置
            image_rect = self.image_label.pixmap().rect()
            image_pos = self.image_label.pos()
            
            # 调整位置以考虑图片在标签中的居中显示
            offset_x = (self.image_label.width() - image_rect.width()) / 2
            offset_y = (self.image_label.height() - image_rect.height()) / 2
            
            # 计算相对于图片的实际点击位置
            relative_pos = QPoint(
                pos.x() - offset_x,
                pos.y() - offset_y
            )
            
            # 检查点击是否在图片范围内
            if (0 <= relative_pos.x() <= image_rect.width() and
                0 <= relative_pos.y() <= image_rect.height()):
                
                # 计算相对于原始图片尺寸的坐标
                original_x = relative_pos.x() * self.original_size.width() / image_rect.width()
                original_y = relative_pos.y() * self.original_size.height() / image_rect.height()
                
                return QPoint(int(original_x), int(original_y))
        
        return QPoint(-1, -1)
    
    def image_mousePressEvent(self, event):
        """
        图片鼠标点击事件处理
        
        Args:
            event: 鼠标事件
        """
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.get_relative_position(event.pos())
            
            if pos.x() != -1 and self.current_position_index < len(self.preview_texts):
                logger.info(f"选择位置 {self.current_position_index+1}/{len(self.preview_texts)}: ({pos.x()}, {pos.y()})")
                
                # 如果已经选择了足够的位置，则替换最后一个
                if len(self.click_positions) > self.current_position_index:
                    self.click_positions[self.current_position_index] = pos
                else:
                    self.click_positions.append(pos)
                
                self.current_position_index += 1
                self.update_preview()
    
    def image_mouseMoveEvent(self, event):
        """
        图片鼠标移动事件处理
        
        Args:
            event: 鼠标事件
        """
        if self.current_position_index < len(self.preview_texts):
            self.current_position = self.get_relative_position(event.pos())
            self.update_preview()
    
    def select_font(self):
        """字体选择对话框"""
        font, ok = QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
            self.size_slider.setValue(font.pointSize())
            self.bold_checkbox.setChecked(font.bold())
            logger.info(f"字体已更改: {font.family()}, 大小: {font.pointSize()}")
            self.update_preview()
    
    def select_color(self):
        """颜色选择对话框"""
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            logger.info(f"颜色已更改: RGB({color.red()}, {color.green()}, {color.blue()})")
            self.update_preview()
    
    def on_size_changed(self, size):
        """字体大小更改事件"""
        self.font.setPointSize(size)
        self.update_preview()
    
    def on_bold_changed(self, state):
        """字体粗细更改事件"""
        self.font.setBold(state == Qt.CheckState.Checked)
        self.update_preview()
    
    def update_preview(self):
        """更新预览图像，显示所有选择的位置和预览文本"""
        if self.pixmap.isNull():
            return
        
        # 创建透明叠加层
        overlay_pixmap = QPixmap(self.image_label.size())
        overlay_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter()
        painter.begin(overlay_pixmap)
        
        # 获取图片在标签中的显示区域
        image_rect = self.image_label.pixmap().rect()
        label_size = self.image_label.size()
        
        # 计算图片在标签中的偏移和缩放比例
        offset_x = (label_size.width() - image_rect.width()) / 2
        offset_y = (label_size.height() - image_rect.height()) / 2
        
        scale_x = image_rect.width() / self.original_size.width()
        scale_y = image_rect.height() / self.original_size.height()
        
        # 计算预览缩放后的字体大小
        preview_point_size_f = self.font.pointSizeF() * scale_y
        
        preview_font = QFont(self.font) # 复制其他字体属性
        preview_font.setPointSizeF(preview_point_size_f) # 设置缩放后的预览点数

        # --- 使用缩放后的字体绘制预览 --- 
        painter.setFont(preview_font)
        painter.setPen(self.color)

        # --- 绘制已选择的位置 ---
        for i, pos in enumerate(self.click_positions):
            if i < len(self.preview_texts):
                text_to_draw = self.preview_texts[i]
                
                # 计算文字在显示区域的中心点坐标 (display_x, display_y)
                display_x = pos.x() * scale_x + offset_x
                display_y = pos.y() * scale_y + offset_y
                
                # 使用缩放后的字体计算度量
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(text_to_draw)
                text_height = metrics.height()
                # 使用基线偏移进行更精确的垂直居中
                baseline_offset = metrics.descent()
                
                # 计算绘制的左上角坐标 (x, y)，使文字居中于 (display_x, display_y)
                x = display_x - text_width / 2
                y = display_y + text_height / 2 - baseline_offset
                
                painter.drawText(int(x), int(y), text_to_draw)
        
        # --- 绘制当前鼠标悬停位置的预览 (如果还在选择中) ---
        if hasattr(self, 'current_position') and self.current_position_index < len(self.preview_texts):
            current_text = self.preview_texts[self.current_position_index]
            
            # 计算当前鼠标位置对应的显示中心点坐标
            cursor_display_x = self.current_position.x() * scale_x + offset_x
            cursor_display_y = self.current_position.y() * scale_y + offset_y
            
            # 使用缩放后的字体计算度量 (如果上面设置了，这里无需重复设置 font)
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(current_text)
            text_height = metrics.height()
            baseline_offset = metrics.descent()
            
            # 计算绘制的左上角坐标
            x = cursor_display_x - text_width / 2
            y = cursor_display_y + text_height / 2 - baseline_offset

            painter.drawText(int(x), int(y), current_text)

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
            logger.info("\n保存位置信息:")
            logger.info(f"原始图片尺寸: {self.original_size.width()} x {self.original_size.height()}")
            logger.info(f"显示图片尺寸: {self.pixmap.width()} x {self.pixmap.height()}")
            
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
                
                logger.info(f"位置 {i+1}:")
                logger.info(f"  原始点击坐标: ({pos.x()}, {pos.y()})")
                logger.info(f"  相对坐标: ({relative_x:.6f}, {relative_y:.6f})")
                logger.info(f"  相对字体大小: {relative_font_size:.6f}")
                logger.info(f"  文字宽度: {text_width}, 高度: {text_height}")
                logger.info(f"  计算后绘制坐标: ({draw_x}, {draw_y})")
                
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