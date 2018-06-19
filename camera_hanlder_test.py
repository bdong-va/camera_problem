import unittest
from mock import patch, Mock, MagicMock
from camera_handler import camera_stats, build_endpoint_url, endpoint_caller, exception_handler, analysis_camera_data

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

class TestEndpointCaller(unittest.TestCase):

    def test_return_empty_list_if_url_list_is_empty(self):
        responses = endpoint_caller([])
        self.assertEqual([], responses)

    @patch('camera_handler.grequests.get')
    def test_url_be_called(self, get_mock):
        responses = endpoint_caller(["http://www.google.com", "http://facebook.com"])
        get_mock.assert_any_call("http://www.google.com", timeout=30)
        get_mock.assert_any_call("http://facebook.com", timeout=30)

    @patch('camera_handler.grequests.map')
    def test_response_returned(self, map_mock):
        response_mock = MagicMock(status_code=200)
        response_mock.json.return_value={"camera_id":"id_one"}
        map_mock.return_value= [response_mock, None]
        responses = endpoint_caller(["http://www.google.com", "http://facebook.com"])
        self.assertEqual([{'camera_id': 'id_one'}], responses)

class TestAnalysisCameraData(unittest.TestCase):

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