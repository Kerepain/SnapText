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

class ImageTextProcessor(QObject):
    progress_updated = pyqtSignal(int)  # 进度更新信号
    generation_completed = pyqtSignal(str)  # 生成完成信号
    error_occurred = pyqtSignal(str)  # 错误信号
    
    def __init__(self):
        super().__init__()
        self.output_dir = None
        # 创建输出目录
        if not os.path.exists('output'):
            os.makedirs('output')
    
    def set_output_dir(self, output_dir):
        """设置图片输出目录"""
        self.output_dir = output_dir
    
    def generate_screenshots(self, image_path, data, positions, output_dir="output"):
        """在图片上添加文字并生成新的图片"""
        try:
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 加载原始图片
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise ValueError(f"无法加载图片: {image_path}")
            
            # 输出图片信息
            image_width = pixmap.width()
            image_height = pixmap.height()
            print(f"输出图片尺寸: {image_width} x {image_height}")
            
            # 处理每组数据
            for i, row in enumerate(data):
                try:
                    # 创建新的图片
                    new_pixmap = pixmap.copy()
                    painter = QPainter(new_pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
                    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
                    
                    # 在指定位置绘制文字
                    for pos_info in positions:
                        try:
                            # 确保索引在数据范围内
                            index = min(pos_info.get('index', 0), len(row) - 1)
                            text = str(row[index])  # 确保转换为字符串
                            
                            # 使用相对坐标和大小来计算实际绘制位置
                            if 'relative_x' in pos_info and 'relative_y' in pos_info:
                                # 使用相对坐标计算实际点击位置
                                abs_x = int(pos_info['relative_x'] * image_width)
                                abs_y = int(pos_info['relative_y'] * image_height)
                                
                                # 使用相对字体大小计算实际字体大小
                                font = QFont(pos_info['font'])
                                if 'relative_font_size' in pos_info:
                                    actual_font_size = int(pos_info['relative_font_size'] * image_height)
                                    font.setPointSize(actual_font_size)
                                
                                # 设置字体和颜色
                                painter.setFont(font)
                                painter.setPen(QColor(pos_info['color']))
                                
                                # 计算文字尺寸
                                metrics = painter.fontMetrics()
                                text_width = metrics.horizontalAdvance(text)
                                text_height = metrics.height()
                                
                                # 计算最终绘制位置(完全居中)
                                # 水平居中: 将坐标点减去文字宽度的一半
                                # 垂直居中: 将坐标点加上文字高度的一半减去基线偏移
                                # 基线偏移约为文字高度的1/3到1/4
                                baseline_offset = metrics.descent()  # 获取基线偏移
                                
                                x = abs_x - text_width / 2
                                # 使文字垂直居中
                                y = abs_y + text_height / 2 - baseline_offset
                                
                                # 确保为整数坐标
                                x = int(x)
                                y = int(y)
                                
                                print(f"绘制文字: '{text}'")
                                print(f"  相对坐标: ({pos_info['relative_x']:.6f}, {pos_info['relative_y']:.6f})")
                                print(f"  实际坐标: ({abs_x}, {abs_y})")
                                print(f"  文字尺寸: 宽={text_width}, 高={text_height}, 基线偏移={baseline_offset}")
                                print(f"  最终绘制坐标: ({x}, {y})")
                                print(f"  字体大小: {font.pointSize()}pt")
                                
                                # 绘制文字
                                painter.drawText(x, y, text)
                            else:
                                # 回退到旧方法
                                print("警告: 未找到相对坐标,使用旧方法")
                                font = QFont(pos_info['font'])
                                position = pos_info['position']
                                painter.setFont(font)
                                painter.setPen(QColor(pos_info['color']))
                                
                                # 使用绝对坐标计算
                                metrics = painter.fontMetrics()
                                text_width = metrics.horizontalAdvance(text)
                                text_height = metrics.height()
                                baseline_offset = metrics.descent()  # 获取基线偏移
                                
                                # 计算最终绘制位置(完全居中)
                                x = position.x() - text_width / 2
                                y = position.y() + text_height / 2 - baseline_offset
                                
                                # 确保为整数坐标
                                x = int(x)
                                y = int(y)
                                
                                # 绘制文字
                                painter.drawText(x, y, text)
                        except Exception as e:
                            print(f"绘制单个文字时出错: {str(e)}")
                            import traceback
                            traceback.print_exc()
                            continue
                    
                    painter.end()
                    
                    # 使用第一列数据作为文件名
                    filename = str(row[0]) if row else f"output_{i+1}"
                    # 清理文件名中的非法字符
                    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_'))
                    if not filename:  # 如果清理后文件名为空
                        filename = f"output_{i+1}"
                    
                    # 保存图片
                    output_path = os.path.join(output_dir, f"{filename}.png")
                    success = new_pixmap.save(output_path)
                    if success:
                        print(f"已保存: {output_path}")
                    else:
                        print(f"保存失败: {output_path}")
                    
                    # 更新进度
                    progress = int((i + 1) / len(data) * 100)
                    self.progress_updated.emit(progress)
                
                except Exception as e:
                    print(f"处理数据行出错: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            self.generation_completed.emit(f"已生成 {len(data)} 张图片到 {output_dir} 目录")
            
        except Exception as e:
            print(f"生成异常: {str(e)}")
            import traceback
            traceback.print_exc()
            self.error_occurred.emit(f"生成图片时出错: {str(e)}")
    
    def select_text_position(self, image_path):
        """选择图片上的文字位置"""
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