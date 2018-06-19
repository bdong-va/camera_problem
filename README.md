# camera_problem

assuming all endpoints will return json as content.

assuming 200 is the only vaild status code which we expected.

## currently solution:
main function is the `camera_stats()`, it take a big list of camera_id, async call the API and merge all result into another big list, process it and give analysis result.

## still existed problem:
when image and camera list getting huge, it will have bottleneck on memory.

## some possible improvement if have more time:
- use async and await make it works in better concurrency.

- use two queue system, **retriever**( include camera_id) and **analyser**( include raw_response_data) 
  - grequest will consume retriever queue, push data to analyser queue (need to modify all helper functions, take reference of two queues instead of taking big list itself)
  - `analysis_camera_data()` will consume analyser queue, update data, and when the queue is empty return result.