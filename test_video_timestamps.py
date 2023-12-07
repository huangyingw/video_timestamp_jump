import re
from smart_vlc_jump import *


# 单元测试部分
import unittest


class TestVideoPlayerFunctions(unittest.TestCase):
    def test_extract_timestamps(self):
        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:24:30,:1:11:27,:02:35:52"
        expected_timestamps = ["24:30", "1:11:27", "02:35:52"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:24:30,1:11:27,:02:35:52"
        expected_timestamps = ["24:30", "1:11:27", "02:35:52"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:1:11:27,:24:30,:02:35:52"
        expected_timestamps = ["24:30", "1:11:27", "02:35:52"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)


# 运行单元测试
if __name__ == "__main__":
    unittest.main()
