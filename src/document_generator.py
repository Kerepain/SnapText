from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QImage, QPainter, QFont, QColor, QPixmap
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import os
from PIL import Image as PILImage, ImageDraw, ImageFont
import numpy as np

class DocumentGenerator(QObject):
    progress_updated = pyqtSignal(int)  # 进度更新信号
    generation_completed = pyqtSignal(str)  # 生成完成信号
    error_occurred = pyqtSignal(str)  # 错误信号
    
    def __init__(self):
        super().__init__()
        self.template = None
        self.output_dir = None
        # 创建输出目录
        if not os.path.exists('output'):
            os.makedirs('output')
    
    def set_template(self, template):
        """设置文档模板"""
        self.template = template
    
    def set_output_dir(self, output_dir):
        """设置输出目录"""
        self.output_dir = output_dir
    
    def generate_screenshots(self, image_path, data, positions, output_dir="output"):
        """生成带文字的截图"""
        try:
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 加载原始图片
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise ValueError(f"无法加载图片: {image_path}")
            
            # 记录原始图片尺寸
            original_size = pixmap.size()
            
            # 计算缩放比例
            scale_x = pixmap.width() / original_size.width()
            scale_y = pixmap.height() / original_size.height()
            
            # 处理每组数据
            for i, row in enumerate(data):
                # 创建新的图片
                new_pixmap = pixmap.copy()
                painter = QPainter(new_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
                
                # 在指定位置绘制文字
                for pos_info in positions:
                    try:
                        # 获取位置信息
                        position = pos_info['position']
                        # 确保索引在数据范围内
                        index = min(pos_info.get('index', 0), len(row) - 1)
                        text = str(row[index])  # 确保转换为字符串
                        font = pos_info['font']
                        color = pos_info['color']
                        
                        # 根据缩放比例调整字体大小
                        scaled_font = QFont(font)
                        # 使用相同的缩放比例计算字体大小
                        font_size = int(font.pointSize() * min(scale_x, scale_y))
                        scaled_font.setPointSize(font_size)
                        
                        # 设置字体和颜色
                        painter.setFont(scaled_font)
                        painter.setPen(color)
                        
                        # 计算文字位置（考虑缩放）
                        metrics = painter.fontMetrics()
                        text_width = metrics.horizontalAdvance(text)
                        text_height = metrics.height()
                        
                        # 调整位置，使文字居中
                        x = position.x() * scale_x - text_width / 2
                        y = position.y() * scale_y + text_height / 4
                        
                        # 确保使用整数坐标，避免模糊
                        x = int(x)
                        y = int(y)
                        
                        # 绘制文字
                        painter.drawText(x, y, text)
                    except Exception as e:
                        print(f"绘制文字时出错: {str(e)}")
                        continue
                
                painter.end()
                
                # 保存图片
                output_path = os.path.join(output_dir, f"output_{i+1}.png")
                new_pixmap.save(output_path)
                
                # 更新进度
                progress = int((i + 1) / len(data) * 100)
                self.progress_updated.emit(progress)
            
            self.generation_completed.emit(f"已生成 {len(data)} 张图片到 {output_dir} 目录")
            
        except Exception as e:
            self.error_occurred.emit(f"生成图片时出错: {str(e)}")
    
    def select_text_position(self, image_path):
        """选择文字位置"""
        try:
            # 显示图片并让用户点击选择位置
            image = PILImage.open(image_path)
            # TODO: 实现位置选择功能
            return None
        except Exception as e:
            self.error_occurred.emit(f"选择位置失败: {str(e)}")
            return None
    
    def generate_document(self, data, screenshot_path):
        """生成文档"""
        try:
            if not self.output_dir:
                self.output_dir = QFileDialog.getExistingDirectory(
                    None,
                    "选择输出目录",
                    os.path.expanduser("~")
                )
                if not self.output_dir:
                    return
            
            # 创建PDF文档
            doc = SimpleDocTemplate(
                os.path.join(self.output_dir, "output.pdf"),
                pagesize=letter
            )
            
            # 准备文档内容
            elements = []
            
            # 添加截图
            if screenshot_path and os.path.exists(screenshot_path):
                img = Image(screenshot_path)
                img.drawHeight = 200
                img.drawWidth = 400
                elements.append(img)
            
            # 添加数据表格
            if data:
                table_data = [data[0].keys()]  # 表头
                table_data.extend([row.values() for row in data])
                
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 12),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table)
            
            # 生成文档
            doc.build(elements)
            
            self.generation_completed.emit(os.path.join(self.output_dir, "output.pdf"))
            
        except Exception as e:
            self.error_occurred.emit(f"文档生成失败: {str(e)}")
    
    def generate_batch(self, data_list, screenshot_paths):
        """批量生成文档"""
        try:
            total = len(data_list)
            for i, (data, screenshot_path) in enumerate(zip(data_list, screenshot_paths)):
                self.generate_document(data, screenshot_path)
                self.progress_updated.emit(int((i + 1) / total * 100))
            
            self.generation_completed.emit("批量生成完成")
            
        except Exception as e:
            self.error_occurred.emit(f"批量生成失败: {str(e)}") 