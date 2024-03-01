#!/usr/bin/env python3
import os
from threading import Lock
import sys
import subprocess
import json
import re
import threading
from datetime import timedelta
import requests
from pynput import keyboard
from moviepy.editor import VideoFileClip

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

    # 添加视频开始和结束时间
    timestamps.insert(0, "0:00")
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

    print(f"转换时间戳 '{timestamp}' 为 {total_seconds} 秒")
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


def get_current_vlc_timestamp():
    # 发送请求到 VLC HTTP API
    response = requests.get(
        f"http://{vlc_ip}:{vlc_port}/requests/status.json",
        auth=("", vlc_password),
    )
    if response.status_code == 200:
        data = response.json()
        # 计算当前播放时间（秒）
        current_time = int(data.get("time", 0))
        return str(timedelta(seconds=current_time))
    return "0:00"


def jump_to_timestamp(timestamp_str):
    # 首先，将时间戳字符串转换为秒
    timestamp_seconds = timestamp_to_seconds(timestamp_str)
    print(f"跳转到 {timestamp_seconds} 秒 ({timestamp_str})")
    # 发送跳转命令到 VLC（使用以秒为单位的时间）
    send_command_to_vlc(f"seek&val={timestamp_seconds}")


def find_nearest_timestamp_index(timestamps, current_seconds, direction):
    # 将所有时间戳转换为秒
    timestamp_seconds = [timestamp_to_seconds(ts) for ts in timestamps]
    # 找到当前时间戳的最接近值
    if direction == "left":
        # 找到小于等于当前时间戳的最大值
        nearest_timestamps = [
            ts for ts in timestamp_seconds if ts <= current_seconds
        ]
        if nearest_timestamps:
            return timestamp_seconds.index(max(nearest_timestamps))
    elif direction == "right":
        # 找到大于当前时间戳的最小值
        nearest_timestamps = [
            ts for ts in timestamp_seconds if ts > current_seconds
        ]
        if nearest_timestamps:
            return timestamp_seconds.index(min(nearest_timestamps))
    return None


class VLCController:
    def __init__(self, file_path):
        self.load_file(file_path)

    def load_file(self, file_path):
        self.file_path = file_path
        self.timestamps = extract_timestamps(file_path)
        self.current_index = 0
        self.index_lock = Lock()

        # 终止已有的 VLC 进程
        if hasattr(self, "vlc_process") and self.vlc_process.poll() is None:
            self.vlc_process.kill()

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

        # 重启键盘监听器
        if hasattr(self, "listener"):
            self.listener.stop()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def jump_to_nearest_timestamp(self, current_timestamp, direction="left"):
        # 获取所有时间戳
        timestamps = extract_timestamps(self.file_path)
        # 将当前时间戳转换为秒
        current_seconds = timestamp_to_seconds(current_timestamp)
        # 找到最接近的时间戳
        nearest_timestamp_index = find_nearest_timestamp_index(
            timestamps, current_seconds, direction
        )

        # 如果找到有效的时间戳索引
        if nearest_timestamp_index is not None:
            print(
                f"最近的时间戳索引为 {nearest_timestamp_index}, 时间戳: {timestamps[nearest_timestamp_index]}"
            )
            # 跳转到该时间戳
            jump_to_timestamp(timestamps[nearest_timestamp_index])

    def on_press(self, key):
        print(f"按键被按下: {key}")  # 调试信息
        try:
            if hasattr(key, "char"):
                if key.char == "l":  # 向左跳转
                    current_timestamp = get_current_vlc_timestamp()
                    self.jump_to_nearest_timestamp(
                        current_timestamp, direction="left"
                    )
                elif key.char == "h":  # 向右跳转
                    current_timestamp = get_current_vlc_timestamp()
                    self.jump_to_nearest_timestamp(
                        current_timestamp, direction="right"
                    )
                elif key.char in ["m", "n"]:  # 结束 VLC 进程和监听器
                    self.vlc_process.kill()
                    self.listener.stop()
                    return False
        except AttributeError as e:
            print(f"异常捕获: {e}")  # 调试异常


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
