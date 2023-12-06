import subprocess
import threading
from pynput import keyboard

# VLC的路径和要播放的文件路径
vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
file_path = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠110.rmvb"

# 从文件名解析时间戳数组
timestamps = [10, 20, 30]  # 示例时间戳，单位为秒
current_index = 0

# 启动VLC
vlc_process = subprocess.Popen([vlc_path, file_path])


def on_press(key):
    global current_index
    try:
        # 检测按键是否为'j'
        if key.char == "h":
            current_index = (current_index + 1) % len(timestamps)
            # 构建跳转命令
            command = f"seek {timestamps[current_index]}"
            # 发送命令到VLC
            vlc_process.communicate(input=command.encode())
    except AttributeError:
        pass


# 监听键盘事件
listener = keyboard.Listener(on_press=on_press)
listener.start()

# 让主线程继续运行
try:
    while True:
        pass
except KeyboardInterrupt:
    # 关闭VLC和监听器
    vlc_process.kill()
    listener.stop()
