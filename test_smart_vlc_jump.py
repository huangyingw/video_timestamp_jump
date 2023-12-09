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


# 运行单元测试
if __name__ == "__main__":
    unittest.main()
