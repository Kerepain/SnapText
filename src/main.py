#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SnapText - 批量图片文字处理工具
主入口文件 - 为了向后兼容，保留该文件作为入口点
"""

import sys
from src.app import main

if __name__ == "__main__":
    sys.exit(main()) 