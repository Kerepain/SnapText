# SnapText - 截图文字处理工具

![Build Status](https://github.com/kltions/SnapText/actions/workflows/build.yml/badge.svg)

一个用于在截图上添加文字的工具，支持批量处理。

## 功能特点

- 支持截图和导入图片
- 支持拖放导入图片和CSV文件
- 支持批量添加文字
- 支持自定义文字位置
- 支持Windows系统截图功能

## 安装说明

1. 确保已安装 Python 3.9 或更高版本
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

### Windows系统截图
1. 点击"选择截图区域"按钮
2. 使用鼠标拖动选择要截图的区域
3. 释放鼠标完成截图
4. 按ESC键可以取消截图

### 导入数据
1. 点击"导入文本数据"按钮或拖放CSV文件
2. CSV文件格式要求：
   - 使用UTF-8编码
   - 每行代表一组数据
   - 数据之间用逗号分隔

### 设置文字位置
1. 点击"选择所有文字位置"按钮
2. 在图片上点击设置每个文字的位置
3. 可以调整字体、大小和颜色

### 生成图片
1. 点击"生成带文字截图"按钮
2. 等待处理完成
3. 生成的图片会保存在output目录下

## 系统要求

- Windows 10/11
- Python 3.9+
- 至少4GB内存

## 注意事项

- 截图功能仅在Windows系统上测试通过
- 确保有足够的磁盘空间存储生成的图片
- 建议使用高分辨率显示器以获得更好的效果

## 技术栈

- Python 3.9
- PyQt6
- Pillow
- pyautogui
- PyInstaller

## 版权和许可

Copyright (c) 2025 Kerepain

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交问题和改进建议！如果您想贡献代码，请遵循以下步骤：

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 联系方式

如有任何问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：kltion@qq.com