import unittest
from camera_handler import camera_stats

class TestCameraHandler(unittest.TestCase):
    def test_dumb_test(self):
        pass

    def test_return_empty_json_if_camera_ids_are_empty(self):
        stats = camera_stats([])
        self.assertEqual({}, stats)
