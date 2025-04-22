"""
文本数据处理器
"""
import csv
import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from src.utils.logger import logger

class TextProcessor(QObject):
    """文本数据处理类"""
    
    # 定义信号
    data_loaded = pyqtSignal(list)  # 数据加载完成信号，传递数据列表
    error_occurred = pyqtSignal(str)  # 错误信号，传递错误信息
    
    def __init__(self):
        super().__init__()
        self.data = []  # 存储加载的数据
        self.headers = []
    
    def import_text(self, file_path=None, text_content=None):
        """导入文本数据"""
        try:
            if file_path and os.path.exists(file_path):
                # 从文件导入
                self._import_from_file(file_path)
            elif text_content:
                # 从文本内容导入
                self._import_from_content(text_content)
            else:
                raise ValueError("必须提供文件路径或文本内容之一")
            
            # 验证数据格式
            is_valid, message = self.validate_data()
            if not is_valid:
                self.error_occurred.emit(message)
                return
            
            # 发出数据加载完成信号
            self.data_loaded.emit(self.data)
            logger.info(f"成功导入 {len(self.data)} 条数据")
            return self.data
        except Exception as e:
            logger.error(f"导入数据失败: {str(e)}")
            self.error_occurred.emit(f"导入数据失败: {str(e)}")
            raise
    
    def _import_from_file(self, file_path):
        """从文件导入数据"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.csv':
            self._import_csv(file_path)
        elif ext == '.txt':
            self._import_txt(file_path)
        else:
            self._import_as_csv(file_path)  # 尝试作为CSV导入
        
        logger.debug(f"从文件导入了 {len(self.data)} 条数据")
    
    def _import_from_content(self, text_content):
        """从文本内容导入数据"""
        # 分割文本内容为行
        lines = text_content.strip().split('\n')
        
        # 尝试作为CSV处理
        try:
            reader = csv.reader(lines)
            self.data = [row for row in reader]
            logger.debug(f"从文本内容导入了 {len(self.data)} 条数据")
        except Exception as e:
            logger.error(f"从文本内容导入失败: {str(e)}")
            raise ValueError(f"解析文本内容失败: {str(e)}")
    
    def _import_csv(self, file_path):
        """导入CSV文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.headers = next(reader)  # 获取表头
            self.data = [row for row in reader]
    
    def _import_txt(self, file_path):
        """导入TXT文件
        格式要求：
        1. 每行代表一组数据
        2. 每组数据包含三个字段，用制表符分隔
        3. 例如：姓名\t学号\t班级
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = []
            for line in f:
                line = line.strip()
                if line:  # 忽略空行
                    fields = line.split('\t')
                    if len(fields) != 3:
                        raise ValueError("每行数据必须包含3个字段，用制表符分隔")
                    self.data.append(fields)
            
            if self.data:
                self.headers = ["姓名", "学号", "班级"]
    
    def _import_as_csv(self, file_path):
        """尝试作为CSV导入文件"""
        try:
            self._import_csv(file_path)
        except Exception as e:
            logger.error(f"作为CSV导入失败: {str(e)}")
            raise ValueError(f"无法导入文件: {str(e)}")
    
    def get_headers(self):
        """获取表头"""
        return self.headers
    
    def get_data(self):
        """获取数据"""
        return self.data
    
    def validate_data(self):
        """验证数据格式"""
        if not self.data:
            return False, "没有数据"
        
        # 检查数据组数
        if len(self.data) > 40:
            return False, "数据组数不能超过40组"
        
        # 检查每行数据长度是否一致
        row_length = len(self.data[0])
        for i, row in enumerate(self.data):
            if len(row) != row_length:
                return False, f"第{i+1}行数据格式不正确"
        
        return True, "数据验证通过"
    
    def process_data(self, template):
        """处理数据，根据模板生成最终数据"""
        processed_data = []
        for row in self.data:
            processed_row = {}
            for i, header in enumerate(self.headers):
                processed_row[header] = row[i]
            processed_data.append(processed_row)
        return processed_data
    
    def clear_data(self):
        """清除数据"""
        self.data = []
        logger.debug("数据已清除") 