"""
主题处理工具类
"""
import sys
import subprocess

def is_system_dark_mode():
    """检测系统是否为暗色模式"""
    if sys.platform == "darwin":  # macOS
        try:
            from subprocess import run, PIPE
            result = run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                        stdout=PIPE, stderr=PIPE)
            return result.returncode == 0
        except Exception:
            return False
    elif sys.platform == "win32":  # Windows
        # Windows的暗色模式检测需要读取注册表
        # 这里提供一个简化版实现
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except Exception:
            return False
    elif sys.platform.startswith("linux"):  # Linux
        # Linux下检测暗色模式较复杂，依赖具体桌面环境
        # 这里提供GNOME的检测方法
        try:
            result = subprocess.run(
                ['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
                capture_output=True, text=True
            )
            return 'dark' in result.stdout.lower()
        except Exception:
            return False
    
    return False 