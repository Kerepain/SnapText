"""
应用程序常量配置
"""
import os
import tempfile

# 应用信息
APP_NAME = "SnapText"
APP_TITLE = "SnapText - 批量图片文字处理工具"
APP_VERSION = "1.1.0"
GITHUB_REPO_URL = "https://github.com/Kerepain/SnapText"

# 窗口设置
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650
WINDOW_MARGIN = 15
WINDOW_SPACING = 15

# 文件相关
TEMP_DIR = tempfile.gettempdir()
TEMP_IMAGE_FILE = os.path.join(TEMP_DIR, "snaptext_image.png")
TEMP_DATA_FILE = os.path.join(TEMP_DIR, "snaptext_data.csv")

# 默认值
DEFAULT_POSITION_COUNT = 3
DEFAULT_DATA_COUNT = 1
MAX_DATA_COUNT = 40

# 支持的图片格式
SUPPORTED_IMAGE_FORMATS = "图片文件 (*.png *.jpg *.jpeg *.bmp);;所有文件 (*.*)"

# 支持的数据格式
SUPPORTED_DATA_FORMATS = "CSV 文件 (*.csv);;文本文件 (*.txt);;所有文件 (*.*)" 