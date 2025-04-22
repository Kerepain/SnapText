## SnapText - 批量图片文字处理工具

SnapText 是一个用于批量处理图片文本的工具，可以将多组数据应用到图片上的指定位置，生成含有不同文字的图片。

### 功能特点

- 支持导入和拖放图片
- 支持导入和拖放数据文件（CSV，TXT）
- 支持定义多个文字位置，包括位置、字体、大小和颜色
- 支持批量生成包含不同文字的图片
- 支持亮色/暗色主题切换
- 界面简洁易用

### 安装方法

#### 从源码运行

1. 确保已安装 Python 3.6+ 和 pip
2. 克隆项目仓库：

```
git clone https://github.com/yourusername/SnapText.git
cd SnapText
```

3. 安装依赖：

```
pip install -r requirements.txt
```

4. 运行程序：

```
python src/app.py
```

#### 使用可执行文件

- Windows：下载并运行 `SnapText.exe`
- macOS：下载并运行 `SnapText.app`

### 使用方法

1. 导入图片（支持直接拖放）
2. 导入文本数据（支持CSV文件，直接拖放）
3. 设置文字位置数量
4. 点击"选择所有文字位置"按钮，在图片上设置文字位置、字体和颜色
5. 设置要生成的数据组数
6. 点击"生成带文字截图"按钮，等待生成完成

### 项目结构

模块化设计，清晰的代码组织结构：

```
SnapText/
├── assets/            # 资源文件（图标、图片等）
├── src/               # 源代码目录
│   ├── config/        # 配置文件
│   │   └── constants.py  # 常量定义
│   ├── processors/    # 数据和图像处理器
│   │   ├── image_text_processor.py  # 图像文字处理器
│   │   ├── position_selector.py     # 位置选择器
│   │   └── text_processor.py        # 文本处理器
│   ├── ui/            # 用户界面组件
│   │   ├── components.py      # UI通用组件
│   │   ├── drag_drop_label.py # 拖放标签
│   │   ├── main_window.py     # 主窗口
│   │   └── styles.py          # 样式定义
│   ├── utils/         # 工具类
│   │   ├── file_utils.py  # 文件工具
│   │   ├── logger.py      # 日志工具
│   │   └── theme_utils.py # 主题工具
│   └── app.py         # 程序入口
├── output/            # 输出目录
├── requirements.txt   # 依赖项
└── README.md          # 说明文档
```

### 许可证

[LICENSE](./LICENSE)