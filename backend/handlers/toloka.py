import datetime
import time

import aiohttp.web

import toloka.client as toloka

import requests
import base64

import yadisk as yadisk

disk_token = 'AQAAAAA6X9QEAAcCMWl9KFZcKUYhlvsNrOL_jes'
disk_headers = {"Authorization": "OAuth " + disk_token}
y = yadisk.YaDisk(token=disk_token)

toloka_token = 'AgAAAAA6X9QEAACtpSo1hzCbwkbStjPARSTi9gQ'
headers = {"Authorization": "OAuth " + toloka_token}
toloka_client = toloka.TolokaClient(toloka_token, 'PRODUCTION')


async def handle_sending_to_toloka(request):
    req_json = request.json()
    bytestr = req_json["image"]

    language = req_json["language"]
    if language == 'rus':
        project_id = 49805
        recognition_skill_id = 25594
    elif language == 'eng':
        project_id = 49889
        recognition_skill_id = 25856
    recognition_pool = toloka.pool.Pool(
        project_id=project_id,
        private_name='my new pool',
        may_contain_adult_content=False,
        will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),  # Pool will close after one year
        reward_per_assignment=0.01,  # We set the minimum payment amount for one task page
        auto_accept_solutions=True,
        assignment_max_duration_seconds=60 * 5,  # Give performers 20 minutes to complete one task
        defaults=toloka.pool.Pool.Defaults(
            default_overlap_for_new_task_suites=1,
            default_overlap_for_new_tasks=1,
        ),
    )
    recognition_pool.set_mixer_config(real_tasks_count=1, golden_tasks_count=0, training_tasks_count=0)
    recognition_pool.filter = (
        toloka.filter.Languages.in_(language))  # and (toloka.filter.Skill(recognition_skill_id) == 0))
    recognition_pool = toloka_client.create_pool(recognition_pool)
    pool_id = recognition_pool.id

    imgdata = base64.b64decode(bytestr)
    filename = 'sample.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    y.upload("sample.jpg", "sample.jpg", overwrite=True)
    req_put = requests.put("https://cloud-api.yandex.net/v1/disk/resources/publish?path=%2Fsample.jpg",
                           headers=disk_headers)
    req_get = requests.get('https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2Fsample.jpg',
                           headers=disk_headers)
    url = req_get.json()['public_url']
    tasks = [
        toloka.task.Task(input_values={'image': url, 'breed': f"handwrite recognition in {language}"}, pool_id=pool_id)
    ]
    toloka_client.create_tasks(tasks, toloka.task.CreateTasksParameters(allow_defaults=True))
    recognition_pool = toloka_client.open_pool(pool_id)
    req = requests.get("https://toloka.yandex.ru/api/v1/assignments?pool_id={}".format(pool_id), headers=headers)
    sleep_time = 20
    pool_req = requests.get("https://toloka.yandex.ru/api/v1/pools/{}".format(pool_id), headers=headers)
    status = pool_req.json()['status']
    while not status == 'CLOSED':
        time.sleep(sleep_time)
        pool_req = requests.get("https://toloka.yandex.ru/api/v1/pools/{}".format(pool_id), headers=headers)
        status = pool_req.json()['status']
    data = req.json()
    print(data['items'])
    try:
        answer = data['items'][0]['solutions'][0]['output_values']
        if answer['notext']:
            return aiohttp.web.json_response(
                {"status": "done", "result": "На фотографии не обнаружен текст"}
            )
        else:
            return aiohttp.web.json_response(
                {"status": "done", "result": answer['output']}
            )
    except:
        raise aiohttp.web.HTTPBadRequest()
