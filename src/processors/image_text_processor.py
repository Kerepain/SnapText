"""
图像文字处理器
"""
import os
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor
from src.utils.file_utils import ensure_dir_exists
from src.utils.logger import logger

class ImageTextProcessor(QObject):
    """图像文本处理类"""
    
    # 定义信号
    progress_updated = pyqtSignal(int)  # 进度更新信号
    generation_completed = pyqtSignal(str)  # 生成完成信号
    error_occurred = pyqtSignal(str)  # 错误信号
    
    def __init__(self):
        super().__init__()
        self.output_dir = ""  # 输出目录
    
    def generate_screenshots(self, image_path, data, text_positions):
        """
        生成带文字的截图
        
        Args:
            image_path: 图片路径
            data: 要添加的文本数据列表
            text_positions: 文字位置信息列表
        """
        try:
            # 选择保存目录
            self.output_dir = QFileDialog.getExistingDirectory(
                None, 
                "选择保存目录", 
                os.path.join(os.path.expanduser("~"), "Desktop")
            )
            
            if not self.output_dir:
                return
            
            # 确保输出目录存在
            ensure_dir_exists(self.output_dir)
            
            # 加载原始图片
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise ValueError(f"无法加载图片: {image_path}")
            
            # 输出图片信息
            image_width = pixmap.width()
            image_height = pixmap.height()
            logger.debug(f"输出图片尺寸: {image_width} x {image_height}")
            
            # 开始处理每组数据
            total_count = len(data)
            for i, row in enumerate(data):
                try:
                    # 创建新的图片
                    new_pixmap = pixmap.copy()
                    painter = QPainter(new_pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
                    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
                    
                    # 在指定位置绘制文字
                    for pos_info in text_positions:
                        try:
                            # 确保索引在数据范围内
                            index = min(pos_info.get('index', 0), len(row) - 1)
                            text = str(row[index])  # 确保转换为字符串

                            # 使用 PositionSelector 传来的原始 QFont (包含绝对点数)
                            font = QFont(pos_info['font'])
                            painter.setFont(font)
                            painter.setPen(QColor(pos_info['color']))

                            # 使用 PositionSelector 传来的绝对坐标
                            position = pos_info['position']

                            # 计算文字尺寸用于居中
                            metrics = painter.fontMetrics()
                            text_width = metrics.horizontalAdvance(text)
                            text_height = metrics.height()
                            baseline_offset = metrics.descent() # 用于垂直对齐的基线偏移

                            # 计算绘制文字所需的左上角坐标 (x, y)，使文字块在 position 处居中
                            x = position.x() - text_width / 2
                            # 垂直居中: 目标中心y + 文字高度一半 - 基线偏移 (drawText从基线开始绘制)
                            y = position.y() + text_height / 2 - baseline_offset

                            # 确保为整数坐标
                            x = int(x)
                            y = int(y)

                            # 记录调试信息
                            logger.debug(f"绘制文字: '{text}' at ({x}, {y}) Font: {font.family()} {font.pointSize()}pt")
                            logger.debug(f"  目标中心点 (绝对): ({position.x()}, {position.y()})")
                            logger.debug(f"  文本度量: 宽={text_width}, 高={text_height}, 基线偏移={baseline_offset}")

                            # 绘制文字
                            painter.drawText(x, y, text)

                        except Exception as e:
                            logger.error(f"绘制单个文字时出错: {str(e)}")
                            continue
                    
                    painter.end()
                    
                    # 生成文件名
                    # 使用第一列数据作为文件名的一部分
                    filename = f"{row[0] if row else i+1}.png"
                    safe_filename = self._get_safe_filename(filename)
                    
                    # 保存图片
                    output_path = os.path.join(self.output_dir, safe_filename)
                    success = new_pixmap.save(output_path)
                    if success:
                        logger.debug(f"已保存: {output_path}")
                    else:
                        logger.error(f"保存失败: {output_path}")
                    
                    # 更新进度
                    progress = int((i + 1) / total_count * 100)
                    self.progress_updated.emit(progress)
                    
                except Exception as e:
                    logger.error(f"处理数据行 {i+1} 时出错: {str(e)}")
            
            # 完成处理
            message = f"已生成 {total_count} 张图片，保存在 {self.output_dir}"
            self.generation_completed.emit(message)
            logger.info(message)
            
        except Exception as e:
            error_message = f"生成截图失败: {str(e)}"
            self.error_occurred.emit(error_message)
            logger.error(error_message)
    
    def _get_safe_filename(self, filename):
        """获取安全的文件名"""
        # 替换不安全的字符
        unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        
        # 确保文件名不超过255个字符
        base_name, ext = os.path.splitext(filename)
        if len(filename) > 255:
            base_name = base_name[:255 - len(ext) - 1]
            filename = base_name + ext
        
        return filename 