import re
import vlc
from pynput.keyboard import Listener, Key


# 提取时间戳的函数
def extract_timestamps(filename):
    pattern = r"\d{2}-\d{2}-\d{2}"  # HH-MM-SS格式
    return re.findall(pattern, filename)


# 跳转至下一个时间戳的函数
def jump_to_next_timestamp(player, timestamps, current_index):
    if current_index[0] < len(timestamps) - 1:
        current_index[0] += 1
        ts = timestamps[current_index[0]]
        hours, minutes, seconds = map(int, ts.split("-"))
        time_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000
        player.set_time(time_milliseconds)
        print(f"跳转至: {ts}")


# 主函数
def main():
    video_filename = "example_video_00-10-20_00-20-30.mp4"  # 假设的文件名
    timestamps = extract_timestamps(video_filename)
    if not timestamps:
        print("未找到时间戳")
        return

    # 初始化VLC播放器
    player = vlc.MediaPlayer(video_filename)
    player.play()

    current_index = [0]  # 当前时间戳索引

    # 定义按键事件处理函数
    def on_press(key):
        if key == Key.space:  # 假设空格键用于跳转
            jump_to_next_timestamp(player, timestamps, current_index)

    # 监听键盘事件
    with Listener(on_press=on_press) as listener:
        listener.join()


# 执行主函数
if __name__ == "__main__":
    main()
