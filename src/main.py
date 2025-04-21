import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QProgressBar, QMessageBox,
                           QHBoxLayout, QSpinBox, QFileDialog)
from PyQt6.QtCore import Qt, QPoint
from screenshot import ScreenshotWidget
from text_processor import TextProcessor
from document_generator import DocumentGenerator
from position_selector import PositionSelector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapText - 批量截图文字处理工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化模块
        self.text_processor = TextProcessor()
        self.document_generator = DocumentGenerator()
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # 添加标题
        title = QLabel("SnapText - 批量截图文字处理工具")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 创建截图和导入按钮的水平布局
        screenshot_layout = QHBoxLayout()
        
        # 添加截图按钮
        self.screenshot_btn = QPushButton("选择截图区域")
        screenshot_layout.addWidget(self.screenshot_btn)
        
        # 添加导入图片按钮
        self.import_image_btn = QPushButton("导入已有图片")
        screenshot_layout.addWidget(self.import_image_btn)
        
        layout.addLayout(screenshot_layout)
        
        # 添加位置数量选择
        position_count_layout = QHBoxLayout()
        position_count_layout.addWidget(QLabel("文字位置数量:"))
        self.position_count_spin = QSpinBox()
        self.position_count_spin.setRange(1, 10)  # 最多支持10个位置
        self.position_count_spin.setValue(3)  # 默认3个位置
        position_count_layout.addWidget(self.position_count_spin)
        layout.addLayout(position_count_layout)
        
        # 添加文字位置选择按钮
        self.select_positions_btn = QPushButton("选择所有文字位置")
        layout.addWidget(self.select_positions_btn)
        
        # 添加数据组数选择
        data_count_layout = QHBoxLayout()
        data_count_layout.addWidget(QLabel("数据组数:"))
        self.data_count_spin = QSpinBox()
        self.data_count_spin.setRange(1, 40)
        self.data_count_spin.setValue(1)
        data_count_layout.addWidget(self.data_count_spin)
        layout.addLayout(data_count_layout)
        
        # 添加导入和生成按钮
        self.import_btn = QPushButton("导入文本数据")
        self.generate_btn = QPushButton("生成带文字截图")
        layout.addWidget(self.import_btn)
        layout.addWidget(self.generate_btn)
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 添加状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 连接信号
        self.screenshot_btn.clicked.connect(self.select_screenshot_area)
        self.import_image_btn.clicked.connect(self.import_image)
        self.select_positions_btn.clicked.connect(self.select_all_positions)
        self.import_btn.clicked.connect(self.import_text_data)
        self.generate_btn.clicked.connect(self.generate_screenshots)
        
        # 连接模块信号
        self.text_processor.data_loaded.connect(self.on_data_loaded)
        self.text_processor.error_occurred.connect(self.show_error)
        self.document_generator.progress_updated.connect(self.update_progress)
        self.document_generator.generation_completed.connect(self.on_generation_completed)
        self.document_generator.error_occurred.connect(self.show_error)
        
        # 初始化变量
        self.screenshot_path = None
        self.data = None
        self.text_positions = []  # 存储所有文字位置信息
    
    def select_screenshot_area(self):
        """选择截图区域"""
        self.status_label.setText("请选择截图区域...")
        screenshot_widget = ScreenshotWidget()
        screenshot_widget.show()
        screenshot_widget.finished.connect(self.on_screenshot_finished)
    
    def on_screenshot_finished(self, screenshot):
        """截图完成回调"""
        if screenshot:
            # 保存截图
            self.screenshot_path = "temp_screenshot.png"
            screenshot.save(self.screenshot_path)
            self.status_label.setText("截图已保存")
        else:
            self.status_label.setText("截图已取消")
    
    def select_all_positions(self):
        """一次性选择所有文字位置"""
        if not self.screenshot_path:
            QMessageBox.warning(self, "警告", "请先选择截图区域或导入图片")
            return
        
        if not os.path.exists(self.screenshot_path):
            QMessageBox.warning(self, "警告", "找不到图片文件，请重新截图或导入图片")
            return
        
        if not self.data:
            QMessageBox.warning(self, "警告", "请先导入数据")
            return
        
        # 获取需要的位置数量
        position_count = self.position_count_spin.value()
        
        # 使用第一组数据作为预览文本
        preview_texts = []
        for i in range(position_count):
            if i < len(self.data[0]):
                preview_texts.append(str(self.data[0][i]))
            else:
                preview_texts.append(f"位置 {i+1}")
        
        # 创建位置选择器对话框
        selector = PositionSelector(self.screenshot_path, preview_texts, self.text_positions)
        selector.position_selected.connect(self.on_positions_selected)
        selector.exec()
    
    def on_positions_selected(self, positions):
        """处理所有位置选择完成"""
        self.text_positions = positions
        self.status_label.setText(f"已设置 {len(positions)} 个文字位置")
        
        # 打印调试信息
        for i, pos_info in enumerate(positions):
            print(f"位置 {i+1} 设置:")
            print(f"  位置: ({pos_info['position'].x()}, {pos_info['position'].y()})")
            print(f"  文字: {pos_info['text']}")
            print(f"  字体: {pos_info['font'].family()}, {pos_info['font'].pointSize()}pt")
            print(f"  颜色: ({pos_info['color'].red()}, {pos_info['color'].green()}, {pos_info['color'].blue()})")
    
    def import_text_data(self):
        """导入文本数据"""
        self.status_label.setText("正在导入数据...")
        self.text_processor.import_text(self)
    
    def on_data_loaded(self, data):
        """数据加载完成回调"""
        self.data = data
        self.status_label.setText(f"已导入 {len(data)} 条数据")
        # 更新数据组数选择框的最大值
        self.data_count_spin.setMaximum(min(len(data), 40))
    
    def generate_screenshots(self):
        """生成带文字的截图"""
        if not self.data:
            QMessageBox.warning(self, "警告", "请先导入数据")
            return
        
        if not self.screenshot_path:
            QMessageBox.warning(self, "警告", "请先选择截图区域")
            return
        
        if not self.text_positions:
            QMessageBox.warning(self, "警告", "请选择所有文字位置")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("正在生成截图...")
        
        # 生成截图
        self.document_generator.generate_screenshots(
            self.screenshot_path,
            self.data[:self.data_count_spin.value()],
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
    
    def show_error(self, message):
        """显示错误信息"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("发生错误")
        QMessageBox.critical(self, "错误", message)

    def import_image(self):
        """导入已有图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                # 复制图片到临时文件
                import shutil
                self.screenshot_path = os.path.abspath("temp_screenshot.png")
                if os.path.exists(self.screenshot_path):
                    os.remove(self.screenshot_path)
                shutil.copy2(file_path, self.screenshot_path)
                self.status_label.setText("图片已导入")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入图片失败: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 