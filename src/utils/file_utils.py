"""
文件处理工具类
"""
import os
import sys
import shutil
import tempfile
from PyQt6.QtCore import QFile, QIODevice

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller创建临时文件夹,将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def copy_to_temp(src_path, temp_filename):
    """复制文件到临时目录"""
    temp_dir = tempfile.gettempdir()
    dst_path = os.path.join(temp_dir, temp_filename)
    
    # 确保目标路径不存在
    if os.path.exists(dst_path):
        os.remove(dst_path)
    
    # 复制文件
    shutil.copy2(src_path, dst_path)
    
    return dst_path

def ensure_dir_exists(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def clean_temp_files(temp_files):
    """清理临时文件"""
    for file_path in temp_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass 