"""
配置模块 - 包含应用程序的常量和配置信息
"""

from src.config.constants import (
    # 应用程序信息
    APP_NAME, APP_TITLE, APP_VERSION,
    
    # 窗口设置
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MARGIN, WINDOW_SPACING,
    
    # 文件相关常量
    TEMP_DIR, TEMP_IMAGE_FILE, TEMP_DATA_FILE,
    
    # 默认值
    DEFAULT_POSITION_COUNT, DEFAULT_DATA_COUNT,
    
    # 支持的格式
    SUPPORTED_IMAGE_FORMATS, SUPPORTED_DATA_FORMATS
)

__all__ = [
    'APP_NAME', 'APP_TITLE', 'APP_VERSION',
    'WINDOW_WIDTH', 'WINDOW_HEIGHT', 'WINDOW_MARGIN', 'WINDOW_SPACING',
    'TEMP_DIR', 'TEMP_IMAGE_FILE', 'TEMP_DATA_FILE',
    'DEFAULT_POSITION_COUNT', 'DEFAULT_DATA_COUNT',
    'SUPPORTED_IMAGE_FORMATS', 'SUPPORTED_DATA_FORMATS'
] 