import re


def extract_timestamps(filename):
    # 匹配冒号或逗号后的 HH:MM 格式的时间戳
    pattern = r"[:,](\d{2}:\d{2})"
    return re.findall(pattern, filename)


# 单元测试部分
import unittest


class TestVideoPlayerFunctions(unittest.TestCase):
    def test_extract_timestamps(self):
        filename = "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:13:57,:09:56"
        expected_timestamps = ["13:57", "09:56"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)


# 运行单元测试
if __name__ == "__main__":
    unittest.main()
