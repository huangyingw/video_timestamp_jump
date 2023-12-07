import subprocess
import re
import threading
from datetime import timedelta
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


# 提取时间戳的函数
def extract_timestamps(filename):
    # 匹配冒号或逗号后的 MM:SS 或 H:MM:SS 格式的时间戳
    pattern = r"[:,](\d{1,2}:\d{2}(?::\d{2})?)"
    return re.findall(pattern, filename)


def timestamp_to_seconds(timestamp):
    parts = timestamp.split(":")
    if len(parts) == 2:  # 只有分钟和秒
        minutes, seconds = map(int, parts)
        hours = 0
    elif len(parts) == 3:  # 包含小时、分钟和秒
        hours, minutes, seconds = map(int, parts)
    else:
        raise ValueError(f"无效的时间戳格式: {timestamp}")

    return timedelta(
        hours=hours, minutes=minutes, seconds=seconds
    ).total_seconds()


# 从文件名解析时间戳数组
timestamps = extract_timestamps(file_path)
current_index = 0

# 启动VLC
vlc_process = subprocess.Popen([vlc_path, "--fullscreen", file_path])


# 发送命令到 VLC 的函数
def send_command_to_vlc(command):
    url = f"http://{vlc_ip}:{vlc_port}/requests/status.xml?command={command}"
    print(f"Sending request to URL: {url}")  # 打印发送的请求URL
    try:
        response = requests.get(url, auth=("", vlc_password))
        print(f"Response Status Code: {response.status_code}")  # 打印响应状态码
        if response.status_code == 200:
            print("Request successful.")
        else:
            print(f"Response Content: {response.text}")  # 打印响应内容（如果有错误）
    except Exception as e:
        print(f"Error sending request: {e}")  # 打印请求错误信息


# 监听键盘事件的函数
def on_press(key):
    global current_index
    try:
        if key.char == "h":
            current_index = (current_index + 1) % len(timestamps)
            # 打印即将跳转到的时间戳
            print("Jumping to timestamp:", timestamps[current_index])
            timestamp_in_second = int(
                timestamp_to_seconds(timestamps[current_index])
            )
            print("Jumping to timestamp_in_second:", timestamp_in_second)
            # 发送跳转命令到 VLC
            send_command_to_vlc(f"seek&val={timestamp_in_second}")
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
