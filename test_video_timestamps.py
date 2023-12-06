import unittest
from video_timestamp_navigator import extract_timestamps, timestamp_to_seconds

class TestVideoPlayerFunctions(unittest.TestCase):

    def test_extract_timestamps(self):
        # 测试 extract_timestamps 函数
        filename = "example_video.mp4:01:23:45,:02:34:56"
        expected_timestamps = ["01:23:45", "02:34:56"]
        self.assertEqual(extract_timestamps(filename), expected_timestamps)

    def test_timestamp_to_seconds(self):
        # 测试 timestamp_to_seconds 函数
        timestamp = "01:23:45"
        expected_seconds = 1*3600 + 23*60 + 45
        self.assertEqual(timestamp_to_seconds(timestamp), expected_seconds)

if __name__ == '__main__':
    unittest.main()
