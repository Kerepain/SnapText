from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import os

def convert_svg_to_ico(svg_path, ico_path, sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]):
    # 将SVG转换为PNG
    drawing = svg2rlg(svg_path)
    png_path = 'temp.png'
    renderPM.drawToFile(drawing, png_path, fmt='PNG', backend='PIL')
    
    # 创建不同尺寸的图标
    images = []
    for size in sizes:
        img = Image.open(png_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        images.append(img)
    
    # 保存为ICO文件
    images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    
    # 删除临时PNG文件
    os.remove(png_path)

if __name__ == '__main__':
    convert_svg_to_ico('assets/logo.svg', 'assets/logo.ico') 