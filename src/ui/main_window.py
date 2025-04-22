"""
主窗口模块
"""
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QProgressBar, QMessageBox,
                           QHBoxLayout, QSpinBox, QFileDialog, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

from src.ui.components import CardFrame, CSVFormatDialog
from src.ui.styles import Style
from src.ui.drag_drop_label import DragDropLabel
from src.config.constants import (APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, 
                               WINDOW_MARGIN, WINDOW_SPACING, DEFAULT_POSITION_COUNT, 
                               DEFAULT_DATA_COUNT, MAX_DATA_COUNT, 
                               SUPPORTED_IMAGE_FORMATS, SUPPORTED_DATA_FORMATS)
from src.processors.text_processor import TextProcessor
from src.processors.image_text_processor import ImageTextProcessor
from src.processors.position_selector import PositionSelector
from src.utils.file_utils import get_resource_path, copy_to_temp
from src.utils.theme_utils import is_system_dark_mode
from src.utils.logger import logger

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 设置主题
        self.isDarkMode = is_system_dark_mode()
        
        # 创建主窗口部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(WINDOW_SPACING)
        layout.setContentsMargins(WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN)
        
        # 添加标题和主题切换
        header_layout = QHBoxLayout()
        
        # 添加logo
        logo_label = QLabel()
        logo_path = get_resource_path("assets/logo.svg")
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            # 设置应用图标
            self.setWindowIcon(QIcon(logo_path))
        header_layout.addWidget(logo_label)
        
        title = QLabel(APP_TITLE)
        title.setObjectName("title")  # 设置对象名称以便样式表识别
        title.setStyleSheet(Style.get_title_style(self.isDarkMode))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(title)
        
        # 添加主题切换复选框
        self.theme_checkbox = QCheckBox("暗色模式")
        self.theme_checkbox.setChecked(self.isDarkMode)
        self.theme_checkbox.stateChanged.connect(self.toggleTheme)
        header_layout.addWidget(self.theme_checkbox, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(header_layout)
        
        # 初始化处理器
        self.text_processor = TextProcessor()
        self.image_processor = ImageTextProcessor()
        
        # 图片设置卡片
        image_card = CardFrame("图片设置")
        screenshot_layout = QHBoxLayout()
        screenshot_layout.setSpacing(10)
        
        self.import_image_btn = QPushButton("导入图片")
        self.import_image_btn.setIcon(QIcon.fromTheme("folder-open"))
        screenshot_layout.addWidget(self.import_image_btn)
        
        image_card.layout.addLayout(screenshot_layout)
        
        # 创建拖放区域
        self.image_drop_label = DragDropLabel(self, is_image=True)
        image_card.layout.addWidget(self.image_drop_label)
        
        layout.addWidget(image_card)
        
        # 数据设置卡片
        data_card = CardFrame("数据设置")
        data_layout = QVBoxLayout()
        
        # 数据组数选择
        data_count_layout = QHBoxLayout()
        data_count_layout.addWidget(QLabel("数据组数:"))
        self.data_count_spin = QSpinBox()
        self.data_count_spin.setRange(1, MAX_DATA_COUNT)
        self.data_count_spin.setValue(DEFAULT_DATA_COUNT)
        data_count_layout.addWidget(self.data_count_spin)
        
        # 添加帮助按钮
        help_btn = QPushButton("?")
        help_btn.setFixedSize(20, 20)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        help_btn.setToolTip("点击查看CSV格式说明")
        help_btn.clicked.connect(self.show_csv_format_help)
        data_count_layout.addWidget(help_btn)
        
        data_count_layout.addStretch()
        data_layout.addLayout(data_count_layout)
        
        # 导入数据按钮
        self.import_btn = QPushButton("导入文本数据")
        self.import_btn.setIcon(QIcon.fromTheme("document-open"))
        data_layout.addWidget(self.import_btn)
        
        # 创建拖放区域（放在按钮下方）
        self.csv_drop_label = DragDropLabel(self, is_image=False)
        data_layout.addWidget(self.csv_drop_label)
        
        data_card.layout.addLayout(data_layout)
        layout.addWidget(data_card)
        
        # 文字位置设置卡片
        position_card = CardFrame("文字位置设置")
        position_layout = QVBoxLayout()
        
        # 位置数量选择
        position_count_layout = QHBoxLayout()
        position_count_layout.addWidget(QLabel("文字位置数量:"))
        self.position_count_spin = QSpinBox()
        self.position_count_spin.setRange(1, 10)
        self.position_count_spin.setValue(DEFAULT_POSITION_COUNT)
        position_count_layout.addWidget(self.position_count_spin)
        position_count_layout.addStretch()
        position_layout.addLayout(position_count_layout)
        
        # 选择位置按钮
        self.select_positions_btn = QPushButton("选择所有文字位置")
        self.select_positions_btn.setIcon(QIcon.fromTheme("edit"))
        position_layout.addWidget(self.select_positions_btn)
        
        position_card.layout.addLayout(position_layout)
        layout.addWidget(position_card)
        
        # 生成按钮和进度条卡片
        generate_card = CardFrame()
        generate_layout = QVBoxLayout()
        
        self.generate_btn = QPushButton("生成带文字截图")
        self.generate_btn.setIcon(QIcon.fromTheme("document-save"))
        generate_layout.addWidget(self.generate_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        generate_layout.addWidget(self.progress_bar)
        
        generate_card.layout.addLayout(generate_layout)
        layout.addWidget(generate_card)
        
        # 添加状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 连接信号
        self.import_image_btn.clicked.connect(self.import_image)
        self.select_positions_btn.clicked.connect(self.select_all_positions)
        self.import_btn.clicked.connect(self.import_text)
        self.generate_btn.clicked.connect(self.generate_screenshots)
        
        # 连接模块信号
        self.text_processor.data_loaded.connect(self.on_data_loaded)
        self.text_processor.error_occurred.connect(self.show_error)
        self.image_processor.progress_updated.connect(self.update_progress)
        self.image_processor.generation_completed.connect(self.on_generation_completed)
        self.image_processor.error_occurred.connect(self.show_error)
        
        # 初始化变量
        self.image_path = None
        self.data = None
        self.text_positions = []  # 存储所有文字位置信息
        
        # 更新全局样式
        self.updateStyle()
        
        # 记录启动日志
        logger.info("应用程序已启动")
    
    def updateStyle(self):
        """更新全局样式"""
        # 设置窗口背景色
        self.setStyleSheet(Style.get_main_style(self.isDarkMode))
        
        # 更新所有卡片的样式
        for widget in self.findChildren(CardFrame):
            widget.updateStyle()
        
        # 更新标题样式
        title = self.findChild(QLabel, "title")
        if title:
            title.setStyleSheet(Style.get_title_style(self.isDarkMode))
        
        # 更新特殊按钮样式
        self.import_image_btn.setStyleSheet(Style.get_primary_button_style(self.isDarkMode))
        self.select_positions_btn.setStyleSheet(Style.get_primary_button_style(self.isDarkMode))
        self.generate_btn.setStyleSheet(Style.get_success_button_style(self.isDarkMode))
        
        # 记录主题切换日志
        logger.debug(f"主题已更新为: {'暗色' if self.isDarkMode else '亮色'}")

    def select_all_positions(self):
        """一次性选择所有文字位置"""
        if not self.image_path:
            QMessageBox.warning(self, "警告", "请先选择图片或导入图片")
            return
        
        if not os.path.exists(self.image_path):
            QMessageBox.warning(self, "警告", "找不到图片文件，请重新截图或导入图片")
            return
        
        position_count = self.position_count_spin.value()
        
        # 使用第一组数据作为预览文本(如果有的话)
        preview_texts = []
        if self.data and len(self.data) > 0:
            for i in range(position_count):
                if i < len(self.data[0]):
                    preview_texts.append(str(self.data[0][i]))
                else:
                    preview_texts.append(f"位置 {i+1}")
        else:
            for i in range(position_count):
                preview_texts.append(f"位置 {i+1}")
        
        # 创建位置选择器对话框
        selector = PositionSelector(self.image_path, preview_texts, self.text_positions)
        selector.position_selected.connect(self.on_positions_selected)
        selector.exec()
    
    def on_positions_selected(self, positions):
        """处理所有位置选择完成"""
        self.text_positions = positions
        self.status_label.setText(f"已设置 {len(positions)} 个文字位置")
        
        # 记录位置设置日志
        logger.info(f"已设置 {len(positions)} 个文字位置")
        
        # 打印调试信息
        for i, pos_info in enumerate(positions):
            logger.debug(f"位置 {i+1} 设置:")
            logger.debug(f"  位置: ({pos_info['position'].x()}, {pos_info['position'].y()})")
            logger.debug(f"  文字: {pos_info['text']}")
            logger.debug(f"  字体: {pos_info['font'].family()}, {pos_info['font'].pointSize()}pt")
            logger.debug(f"  颜色: ({pos_info['color'].red()}, {pos_info['color'].green()}, {pos_info['color'].blue()})")
    
    def import_text(self):
        """导入文本数据"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文本数据文件",
            "",
            SUPPORTED_DATA_FORMATS
        )
        
        if file_path:
            self.status_label.setText("正在导入数据...")
            try:
                # 导入数据
                self.text_processor.import_text(file_path=file_path)
                self.csv_drop_label.setText(f"已导入数据:\n{os.path.basename(file_path)}")
                logger.info(f"已导入数据文件: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入数据失败: {str(e)}")
                self.status_label.setText("导入数据失败")
                logger.error(f"导入数据失败: {str(e)}")
        else:
            self.status_label.setText("未选择文件")
    
    def on_data_loaded(self, data):
        """数据加载完成回调"""
        self.data = data
        self.status_label.setText(f"已导入 {len(data)} 条数据")
        # 更新数据组数选择框的最大值
        self.data_count_spin.setMaximum(min(len(data), MAX_DATA_COUNT))
        logger.info(f"数据加载完成，共 {len(data)} 条记录")
    
    def generate_screenshots(self):
        """生成带文字的截图"""
        if not self.data:
            QMessageBox.warning(self, "警告", "请先导入数据")
            return
        
        if not self.image_path:
            QMessageBox.warning(self, "警告", "请先选择图片")
            return
        
        if not self.text_positions:
            QMessageBox.warning(self, "警告", "请选择所有文字位置")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("正在生成截图...")
        
        # 生成截图
        data_count = self.data_count_spin.value()
        logger.info(f"开始生成截图，数据组数: {data_count}")
        
        self.image_processor.generate_screenshots(
            self.image_path,
            self.data[:data_count],
            self.text_positions
        )
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def on_generation_completed(self, message):
        """生成完成回调"""
        self.progress_bar.setVisible(False)
        self.status_label.setText(message)
        QMessageBox.information(self, "完成", "截图生成完成！")
        logger.info("截图生成完成")
    
    def show_error(self, message):
        """显示错误信息"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("发生错误")
        QMessageBox.critical(self, "错误", message)
        logger.error(f"错误: {message}")

    def import_image(self):
        """导入图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            SUPPORTED_IMAGE_FORMATS
        )
        
        if file_path:
            try:
                # 复制图片到临时文件
                self.image_path = copy_to_temp(file_path, "snaptext_image.png")
                self.status_label.setText("图片已导入")
                logger.info(f"图片已导入: {file_path}")
                
                # 更新拖放标签显示
                self.image_drop_label.setText(f"已导入图片:\n{os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入图片失败: {str(e)}")
                logger.error(f"导入图片失败: {str(e)}")
                self.status_label.setText("导入图片失败")

    def show_csv_format_help(self):
        """显示CSV格式说明对话框"""
        dialog = CSVFormatDialog(self)
        dialog.exec()
        logger.debug("显示CSV格式说明对话框")
    
    def on_image_dropped(self, file_path):
        """处理图片拖放"""
        try:
            # 复制图片到临时文件
            self.image_path = copy_to_temp(file_path, "snaptext_image.png")
            self.status_label.setText("图片已导入")
            logger.info(f"拖放导入图片: {file_path}")
            
            # 更新拖放标签显示
            self.image_drop_label.setText(f"已导入图片:\n{os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入图片失败: {str(e)}")
            logger.error(f"拖放导入图片失败: {str(e)}")
            self.status_label.setText("导入图片失败")
    
    def on_csv_dropped(self, file_path):
        """处理CSV拖放"""
        try:
            # 复制CSV文件到临时文件并导入
            temp_file = copy_to_temp(file_path, "snaptext_data.csv")
            self.text_processor.import_text(file_path=temp_file)
            self.status_label.setText("数据已导入")
            logger.info(f"拖放导入数据: {file_path}")
            
            # 更新拖放标签显示
            self.csv_drop_label.setText(f"已导入数据:\n{os.path.basename(file_path)}")
            
            # 删除临时文件
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入数据失败: {str(e)}")
            logger.error(f"拖放导入数据失败: {str(e)}")
            self.status_label.setText("导入数据失败")

    def toggleTheme(self, state):
        """切换主题"""
        self.isDarkMode = bool(state)
        self.updateStyle()
    
    def closeEvent(self, event):
        """处理窗口关闭事件"""
        logger.info("应用程序关闭")
        event.accept() 