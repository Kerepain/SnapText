import csv
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal

class TextProcessor(QObject):
    data_loaded = pyqtSignal(list)  # 数据加载完成信号
    error_occurred = pyqtSignal(str)  # 错误信号
    
    def __init__(self):
        super().__init__()
        self.data = []
        self.headers = []
    
    def import_text(self, file_path=None, parent=None):
        """导入文本数据
        
        Args:
            file_path: 文件路径，如果为None则打开文件选择对话框
            parent: 父窗口，用于显示对话框
        """
        try:
            if file_path is None:
                file_path, _ = QFileDialog.getOpenFileName(
                    parent,
                    "选择文本文件",
                    "",
                    "CSV文件 (*.csv);;文本文件 (*.txt);;所有文件 (*.*)"
                )
            
            if not file_path:
                return
            
            if file_path.endswith('.csv'):
                self._import_csv(file_path)
            else:
                self._import_txt(file_path)
            
            # 验证数据格式
            is_valid, message = self.validate_data()
            if not is_valid:
                self.error_occurred.emit(message)
                return
            
            self.data_loaded.emit(self.data)
            
        except Exception as e:
            self.error_occurred.emit(f"导入失败: {str(e)}")
    
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