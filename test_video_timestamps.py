import re


# 单元测试部分
import unittest


class TestVideoPlayerFunctions(unittest.TestCase):
    def test_extract_timestamps(self):
        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:13:57,:1:14:15,2:25:35,:09:56"
        expected_timestamps = ["13:57", "1:14:15", "2:25:35", "09:56"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)


# 运行单元测试
if __name__ == "__main__":
    unittest.main()
