def camera_stats(camera_ids):
    """
    get camera image data from API calls, analysize it and return stats in json.
    camera_ids: list of string, camera_id.
    Return: json include stats info, example:
    {
        camera_ids:{
            "most_data_use": "camera_id_one"
            "highest_image":"camera_id_two"
        }
        "largest_image_list":[
            {
            camera_id: 1,
            image: {
                file_size: 42048,
                },
            }
        ]
    }
    """
    if not isinstance(camera_ids, list):
        return {}
    if not camera_ids:
        return {}

    return {}

def camera_url_maker(camera_ids):
    """
    take camera_ids list, return list of API endpoint list for these cameras.
    """
    if not isinstance(camera_ids, list):
        return []
    
    urls = []
    for camera_id in camera_ids:
        url = "domain.com/camera/{}/".format(camera_id)
        urls.append(url)
    return urls

