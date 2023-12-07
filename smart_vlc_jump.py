import subprocess
import threading
import requests
from pynput import keyboard

# VLC HTTP 接口设置
vlc_ip = "localhost"
vlc_port = 8080  # 更改为你的 VLC HTTP 端口
vlc_password = "vlc_password"  # 如果设置了密码，请填写

# VLC的路径和要播放的文件路径
vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
# file_path = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠110.rmvb"
file_path = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:13:57,:09:56"

# 从文件名解析时间戳数组
timestamps = [10, 20, 30]  # 示例时间戳，单位为秒
current_index = 0

# 启动VLC
vlc_process = subprocess.Popen([vlc_path, "--fullscreen", file_path])


# 发送命令到 VLC 的函数
def send_command_to_vlc(command):
    url = f"http://{vlc_ip}:{vlc_port}/requests/status.xml?command={command}"
    requests.get(url, auth=("", vlc_password))


# 监听键盘事件的函数
def on_press(key):
    global current_index
    try:
        if key.char == "h":
            current_index = (current_index + 1) % len(timestamps)
            # 发送跳转命令到 VLC
            send_command_to_vlc(f"seek&val={timestamps[current_index]}")
        elif key.char == "n":
            # 按下 'n' 键时终止 VLC 进程和监听器
            vlc_process.kill()
            listener.stop()
            return False  # 停止监听器
    except AttributeError:
        pass


# 监听键盘事件
listener = keyboard.Listener(on_press=on_press)
listener.start()

# 让主线程继续运行
try:
    listener.join()  # 等待监听器结束
except KeyboardInterrupt:
    # 关闭VLC和监听器
    vlc_process.kill()
    listener.stop()
