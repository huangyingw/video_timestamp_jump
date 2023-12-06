import re
import vlc
from datetime import timedelta
from pynput.keyboard import Listener, Key


# 提取时间戳的函数
def extract_timestamps(filename):
    # 匹配冒号或逗号后的 HH:MM 或 H:MM:SS 格式的时间戳
    pattern = r"[:,](\d{1,2}:\d{2}(?::\d{2})?)"
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


def timestamp_to_seconds(timestamp):
    parts = timestamp.split(":")
    if len(parts) == 2:  # 只有分钟和秒
        minutes, seconds = map(int, parts)
        hours = 0
    elif len(parts) == 3:  # 包含小时、分钟和秒
        hours, minutes, seconds = map(int, parts)
    else:
        raise ValueError(f"无效的时间戳格式: {timestamp}")

    return timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()


# 主函数
def main():
    video_filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:13:57,:09:56"
    timestamps = extract_timestamps(video_filename)
    if not timestamps:
        print("未找到时间戳")
        return
    # 将时间戳转换为秒数并排序
    timestamps_in_seconds = sorted(
        [timestamp_to_seconds(ts) for ts in timestamps]
    )

    print(timestamps_in_seconds)  # 输出排序后的时间戳（秒数）

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
