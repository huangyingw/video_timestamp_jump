#!/usr/bin/env python3
import os
from threading import Lock
import sys
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

# VLC的路径
vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"


# 提取时间戳的函数
def extract_timestamps(filename):
    # 匹配冒号或逗号后的 MM:SS 或 H:MM:SS 格式的时间戳
    pattern = r"[:,](\d{1,2}:\d{2}(?::\d{2})?)"
    timestamps = re.findall(pattern, filename)
    # 将时间戳转换为秒并排序
    return sorted(timestamps, key=timestamp_to_seconds)


def timestamp_to_seconds(timestamp):
    parts = timestamp.split(":")
    if len(parts) == 2:  # 只有分钟和秒
        minutes, seconds = map(int, parts)
        total_seconds = minutes * 60 + seconds
    elif len(parts) == 3:  # 包含小时、分钟和秒
        hours, minutes, seconds = map(int, parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"无效的时间戳格式: {timestamp}")

    return total_seconds


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


class VLCController:
    def __init__(self, file_path):
        self.load_file(file_path)

    def load_file(self, file_path):
        self.file_path = file_path
        self.timestamps = extract_timestamps(file_path)
        self.current_index = 0
        self.file_path = file_path
        self.timestamps = extract_timestamps(file_path)
        self.current_index = 0
        self.index_lock = Lock()

        # 准备 VLC 的启动参数
        vlc_args = [
            vlc_path,
            "--sub-language",
            "Chinese",
            "--sub-autodetect-file",
            "-f",  # 全屏播放
            "--macosx-continue-playback=2",
            "--rate=2.0",  # 两倍速播放
            file_path,
        ]

        # 使用 subprocess.Popen 在后台启动 VLC
        self.vlc_process = subprocess.Popen(
            vlc_args,
            stdout=subprocess.DEVNULL,  # 将标准输出重定向到 DEVNULL
            stderr=subprocess.DEVNULL,  # 将标准错误重定向到 DEVNULL
        )

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == "h":
                with self.index_lock:  # 使用锁来保护对 self.current_index 的访问
                    self.current_index = (self.current_index + 1) % len(
                        self.timestamps
                    )
                    timestamp = self.timestamps[self.current_index]

                print("Jumping to timestamp:", timestamp)
                timestamp_in_second = int(timestamp_to_seconds(timestamp))
                send_command_to_vlc(f"seek&val={timestamp_in_second}")
            elif key.char == "n":
                self.vlc_process.kill()
                self.listener.stop()
                return False
        except AttributeError:
            pass


def main(file_path):
    controller = VLCController(file_path)
    try:
        controller.listener.join()  # 等待监听器结束
    except KeyboardInterrupt:
        controller.vlc_process.kill()
        controller.listener.stop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python smart_vlc_jump.py [dir_path] [line]")
        sys.exit(1)

    dir_path = sys.argv[1]
    line = sys.argv[2]

    # 移除可能的引号
    line = line.strip('"')

    # 检查并处理可能存在的文件大小数字
    if re.match(r"^\d+,", line):
        line = line.split(",", 1)[1]

    # 构建完整的文件路径
    file_path = os.path.join(dir_path, line)

    main(file_path)
