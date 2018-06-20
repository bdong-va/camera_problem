"""methods use to fetch camera images and analysis result"""

import grequests


def camera_stats(camera_ids):
    """
    get camera image data from API calls, analysize it and return stats in json.
    camera_ids: list of string, camera_id.
    Return: json include stats info, example:
    {
        "camera_ids":{
            "most_data_use": "camera_id_one",
            "highest_image_num":"camera_id_two",
        },
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

    urls = build_endpoint_url(camera_ids)
    camera_content_gen_list = fetch_data_async(urls)
    return analysis_camera_data(camera_content_gen_list)

def build_endpoint_url(camera_ids):
    """
    take camera_ids list, return list of API endpoint list for these cameras.
    """
    if not isinstance(camera_ids, list):
        return []
    
    urls = [ "domain.com/camera/{}/".format(camera_id) for camera_id in camera_ids]
    return urls

def fetch_data_async(urls, timeout=30):
    """
    make async call to get response of endpoints.
    timeout: the maxmium timeout we can wait
    exception_handler: the handler we use if status code is not 200 

    return: list of response generators.
    """
    filtered_urls = urls

    rs = (grequests.get(u, timeout=timeout) for u in filtered_urls)
    response_gens = grequests.imap(rs, exception_handler=exception_handler)
    return response_gens


def analysis_camera_data(response_gen_list):
    """
    analysis data and return result
    response_gen_list: list of response generator, each object include one camera's api response
    return: json result. example:
    {
        "camera_ids":{
            "most_data_use": "camera_id_one",
            "highest_image_num":"camera_id_two",
        },
        "largest_image_list":[
            {
            "camera_id": 1,
            "image": {
                "file_size": 42048,
                },
            }
        ]
    }

    """
    most_data_use_id = None
    most_data_use = 0
    highest_image_id = None
    highest_image_num = 0
    largest_image_list = []
    for response in response_gen_list:
        # # do not have real endpoint to test so not sure how to really handle non-200
        # # but if we need to handle it, we will do it here, like:
        # if response.status_code != 200:
        #     # do something here.
        camera_content = response.json() if (response and response.status_code == 200) else None
        if isValid(camera_content):
            camera_id = camera_content.get("camera_id")
            image_list = camera_content.get("images")
            # highest image number camera
            if len(image_list)>highest_image_num:
                highest_image_id = camera_id
                highest_image_num = len(image_list)
            # most data use camera
            max_image, total_size = images_data(image_list)
            if total_size > most_data_use:
                most_data_use_id = camera_id
                most_data_use = total_size
            # list of the largest image of each camera  
            largest_image_list.append({
                "camera_id": camera_id,
                "image": max_image,
                })

    result = {
        "camera_ids":{
            "most_data_use": most_data_use_id,
            "highest_image_num": highest_image_id,
        },
        "largest_image_list":largest_image_list
    }

    return result


def exception_handler(request, exception):
    # put all error handle code here.
    print "Request failed"

def isValid(camera_content):
    """
    return true if camera_content is valid, otherwise false
    """
    return camera_content and "camera_id" in camera_content and "images" in camera_content and isinstance(camera_content["images"], list)

def images_data(image_list):
    """
    return maxinuim size image and total size of image list
    """
    max_size = 0
    max_size_image = None
    total_size = 0
    for image in image_list:
        if image and "file_size" in image:
            file_size = image.get("file_size")
            total_size += file_size
            if file_size > max_size:
                max_size = file_size
                max_size_image = image
    return (max_size_image, total_size)
