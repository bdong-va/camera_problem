import unittest
from mock import patch, Mock, MagicMock
from app.domain.api_handlers.camera_handler import camera_stats, build_endpoint_url, fetch_data_async, exception_handler, analysis_camera_data, isValid

class TestCameraHandler(unittest.TestCase):
    def test_return_empty_json_if_camera_ids_are_empty(self):
        stats = camera_stats([])
        self.assertEqual({}, stats)

    def test_return_empty_json_if_camera_ids_is_not_list(self):
        stats = camera_stats("not_list")
        self.assertEqual({}, stats)
        
    

class TestBuildEndpointUrl(unittest.TestCase):
    def test_return_empty_list_if_camera_ids_are_empty(self):
        urls = build_endpoint_url([])
        self.assertEqual([], urls)
    
    def test_return_empty_json_if_camera_ids_is_not_list(self):
        urls = build_endpoint_url("not_list")
        self.assertEqual([], urls)

    def test_return_url_list_with_correct_camera_ids(self):
        urls = build_endpoint_url(["id_one", "id_two","id_three"])
        expected = [
            "domain.com/camera/id_one/",
            "domain.com/camera/id_two/",
            "domain.com/camera/id_three/",
        ]
        self.assertEqual(expected, urls)

class TestFetchDataAsync(unittest.TestCase):

    def test_return_empty_list_if_url_list_is_empty(self):
        responses = fetch_data_async([])
        result = []
        for r in responses:
            result.append(r)
        self.assertEqual([], result)

    @patch('app.domain.api_handlers.camera_handler.grequests.get')
    def test_url_be_called(self, get_mock):
        responses = fetch_data_async(["http://www.google.com", "http://facebook.com"])
        for r in responses:
            pass
        get_mock.assert_any_call("http://www.google.com", timeout=30)
        get_mock.assert_any_call("http://facebook.com", timeout=30)

class TestAnalysisCameraData(unittest.TestCase):
    camera_one = MagicMock(status_code=200)
    camera_one.json.return_value={
        "camera_id": 1,
        "images": [
            {
            "file_size": 42048,
            },
            {
            "file_size": 1024,
            },
        ]
    }
    camera_two = MagicMock(status_code=200)
    camera_two.json.return_value= {
        "camera_id": 2,
        "images": [
            {
            "file_size": 25000,
            },
            {
            "file_size": 1024,
            },
            {
            "file_size": 1024,
            },
            {
            "file_size": 1024,
            },
        ]
    }
    camera_three = MagicMock(status_code=200)
    camera_three.json.return_value= {
        "camera_id": 3,
        "images": [
            {
            "file_size": 1024,
            },
            {
            "file_size": 1024,
            },
            {
            "file_size": 1024,
            },
        ]
    }
    missing_camera_id = MagicMock(status_code=200)
    missing_camera_id.json.return_value= {
         "images": [
            {
            "file_size": 1024,
            },
            {
            "file_size": 1024,
            },
            {
            "file_size": 1024,
            },
        ]
    }
    
    def test_return_empty_result_if_response_is_empty(self):
        expected= {
            "camera_ids":{
                "most_data_use": None,
                "highest_image_num": None,
            },
            "largest_image_list":[]
        }
        result = analysis_camera_data([])
        self.assertEqual(expected, result)

    def test_skip_bad_data(self):
        expected= {
            "camera_ids":{
                "most_data_use": 1,
                "highest_image_num": 1,
            },
            "largest_image_list":[
                {
                "camera_id": 1,
                "image": {
                    "file_size": 42048,
                    },
                },
            ]
        }
        result = analysis_camera_data([self.camera_one, self.missing_camera_id])
        self.assertEqual(expected, result)

    def test_good_path(self):
        expected= {
            "camera_ids":{
                "most_data_use": 1,
                "highest_image_num": 2,
            },
            "largest_image_list":[
                {
                "camera_id": 1,
                "image": {
                    "file_size": 42048,
                    },
                },
                {
                "camera_id": 2,
                "image": {
                    "file_size": 25000,
                    },
                },
                {
                "camera_id": 3,
                "image": {
                    "file_size": 1024,
                    },
                },
            ]
        }
        result = analysis_camera_data([self.camera_one, self.camera_two, self.camera_three])
        self.assertEqual(expected, result)

class TestIsVaild(unittest.TestCase):

    def test_return_false_if_dict_empty(self):
        self.assertFalse(isValid({}))

    def test_return_false_if_dict_do_not_have_camera_id(self):
        self.assertFalse(isValid({"images":[]}))

    def test_return_false_if_dict_do_not_have_images(self):
        self.assertFalse(isValid({"camera_id":1}))

    def test_return_true_for_good_data(self):
        self.assertTrue(isValid({"camera_id":1, "images":[]}))