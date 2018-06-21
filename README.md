# camera_problem

assuming all endpoints will return json as content.

assuming 200 is the only vaild status code which we expected.

## currently solution:
main function is the `app.domain.api_handlers.camera_stats()`, it take a big list of camera_id, async call the API and merge all result into another big list, process it and give analysis result.

## steps to make it work on prod:
1. need to add auth in API call. `fetch_data_async()` may need include auth info from internal lib.
2. replace `domain.com/camera/{}/` to real endpoint.
3. call `app.domain.api_handlers.camera_stats()` and pass `camera_id` list in.
4. setup on the wire tests if we have any.

## still existed problem:
when image and camera list getting huge, it will have bottleneck on memory.
do not have retry system yet.

## some possible improvement if have more time:

- use two queue system, **retriever**( include camera_id) and **analyser**( include raw_response_data) 
  - grequest will consume retriever queue, push data to analyser queue (need to modify all helper functions, take reference of two queues instead of taking big list itself)
  - grequest will push url item back to retriever queue if cannot fetch anything, and +1 on retry times. discard item if retry times over limit.
  - `analysis_camera_data()` will consume analyser queue, update data, and when the queue is empty return result.
  - only have exprience implementing this kind of structure in golang. not sure what we can use in python side. may need a 1 day spike to find out if needed.

- use `requests.session` to add retry. but it may not work for current `imap`. need further verification. 