"""
日志处理工具类
"""
import os
import logging
import tempfile
from datetime import datetime

class Logger:
    """日志记录器"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """初始化日志记录器"""
        # 创建日志目录
        log_dir = os.path.join(tempfile.gettempdir(), "snaptext_logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建日志文件名
        log_file = os.path.join(log_dir, f"snaptext_{datetime.now().strftime('%Y%m%d')}.log")
        
        # 配置日志记录器
        self.logger = logging.getLogger("SnapText")
        self.logger.setLevel(logging.DEBUG)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)
    
    def info(self, message):
        """记录一般信息"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)
    
    def error(self, message, exc_info=False):
        """记录错误信息
        
        Args:
            message: 错误信息
            exc_info: 是否包含异常详情
        """
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message):
        """记录严重错误信息"""
        self.logger.critical(message)

# 创建全局日志记录器
logger = Logger.get_instance() 