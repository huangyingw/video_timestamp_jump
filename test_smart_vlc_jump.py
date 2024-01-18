import re
from smart_vlc_jump import *


# 单元测试部分
import unittest


class TestVideoPlayerFunctions(unittest.TestCase):
    def test_extract_timestamps(self):
        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.mp4:24:30,:1:11:27,1:40:56,:02:35:52"
        expected_timestamps = ["24:30", "1:11:27", "1:40:56", "02:35:52"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:24:30,1:11:27,:02:35:52"
        expected_timestamps = ["24:30", "1:11:27", "02:35:52"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:1:11:27,:24:30,:02:35:52"
        expected_timestamps = ["24:30", "1:11:27", "02:35:52"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.mp4:02:43,07:34,10:26"
        expected_timestamps = ["02:43", "07:34", "10:26"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.mp4:24:30,:1:11:27,1:40:56,:02:35:52,:02:36:03,:2:39:25,:2:43:06,:2:48:24,:2:53:16,:3:08:41,:3:58:08,:4:00:38,5:12:14,5:24:58,5:36:54,5:41:01,:6:16:21,:6:20:03"
        expected_timestamps = [
            "24:30",
            "1:11:27",
            "1:40:56",
            "02:35:52",
            "02:36:03",
            "2:39:25",
            "2:43:06",
            "2:48:24",
            "2:53:16",
            "3:08:41",
            "3:58:08",
            "4:00:38",
            "5:12:14",
            "5:24:58",
            "5:36:54",
            "5:41:01",
            "6:16:21",
            "6:20:03",
        ]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

    def test_get_video_length():
        # 替换为实际测试视频文件的路径
        test_video_file = (
            "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/"
            "./dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:13:57,:09:56"
        )

        # 预期的视频长度（秒），需要根据实际测试视频的长度进行替换
        expected_length = "23:39"  # 假设测试视频长度为2分钟，即120秒

        # 调用 get_video_length 函数获取视频长度
        actual_length = get_video_length(test_video_file)

        # 检查实际长度是否接近预期长度（可以允许一定的误差，例如±1秒）
        assert (
            abs(actual_length - expected_length) <= 1
        ), f"Expected length: {expected_length}, but got: {actual_length}"

        print("测试通过：视频长度匹配")


# 运行单元测试
if __name__ == "__main__":
    unittest.main()
