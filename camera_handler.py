"""methods use to fetch camera images and analysis result"""

import grequests


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

    urls = build_endpoint_url(camera_ids)

    return {}

def build_endpoint_url(camera_ids):
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

def endpoint_caller(urls, timeout=30):
    """
    make async call to get response of endpoints.
    timeout: the maxmium timeout we can wait
    exception_handler: the handler we use if status code is not 200 
    """
    filtered_urls = urls
    result = []
    # # if we have any cache system, we will try to get result from cache system first.
    # for url in urls:
    #     cache_result = memcache(url)
    #     if cache_result:
    #         responses.append(cache_result)
    #         filtered_urls.remove(url)

    rs = (grequests.get(u, timeout=timeout) for u in filtered_urls)
    new_responses = grequests.map(rs, exception_handler=exception_handler)

    # # do not have real endpoint to test so not sure how to really handle non-200
    # # but if we need to handle it, we will do it here, like this:
    # for response in new_responses:
    #     if response.status_code != 200:
    #         # do something here.

    result += [new_response.text for new_response in new_responses if (new_response and new_response.status_code == 200)]
    # # if we have any cache system, add new results into cache system to avoid extra endpoint call
    # for response in new_responses:
    #     memcache.add(response)
    return result

def exception_handler(request, exception):
    # put all error handle code here.
    print "Request failed"