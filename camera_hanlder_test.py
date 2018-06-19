import unittest
from camera_handler import camera_stats, camera_url_maker

class TestCameraHandler(unittest.TestCase):
    def test_return_empty_json_if_camera_ids_are_empty(self):
        stats = camera_stats([])
        self.assertEqual({}, stats)

    def test_return_empty_json_if_camera_ids_is_not_list(self):
        stats = camera_stats("not_list")
        self.assertEqual({}, stats)
        
    

class TestCameraUrlMaker(unittest.TestCase):
    def test_return_empty_list_if_camera_ids_are_empty(self):
        urls = camera_url_maker([])
        self.assertEqual([], urls)
    
    def test_return_empty_json_if_camera_ids_is_not_list(self):
        urls = camera_url_maker("not_list")
        self.assertEqual([], urls)

    def test_return_url_list_with_correct_camera_ids(self):
        urls = camera_url_maker(["id_one", "id_two","id_three"])
        expected = [
            "domain.com/camera/id_one/",
            "domain.com/camera/id_two/",
            "domain.com/camera/id_three/",
        ]
        self.assertEqual(expected, urls)
