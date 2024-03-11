import pytest
import requests
import json
from main.data_generator.task_generator import generate_task_data, update_task_data
import random
import main.api.tasks as endpoint
from main.data.data import Task, UpdatedTask

@pytest.fixture()
def create_task():
    task_data = next(generate_task_data()).to_dict_and_write()
    response = requests.put(endpoint.CREATE_TASK, json.dumps(task_data))
    response_status_code = response.status_code
    response_body = json.loads(response.content)['task']
    task_data['task_id'] = response_body['task_id']
    return task_data, response_status_code, response_body


@pytest.fixture()
def update_task():
    updated_task_data = next(update_task_data()).to_dict_and_write()
    with open('main/data/json/created_task_data.json', 'r') as data_before:
        data_before_update = json.load(data_before)
    response = requests.put(endpoint.UPDATE_TASK, json.dumps(updated_task_data))
    response_status_code = response.status_code
    response_body = json.loads(response.content)
    return data_before_update, updated_task_data, response_status_code, response_body


@pytest.fixture()
def get_task_by_id():
    with open('main/data/json/updated_task_data.json', 'r') as data_after:
        data_after_update = json.load(data_after)
    response = requests.get(endpoint.GET_TASK_BY_TASK_ID(data_after_update['task_id']))
    response_status_code = response.status_code
    response_body = json.loads(response.content)
    return data_after_update, response_status_code, response_body


@pytest.fixture()
def create_multiple_tasks_for_the_same_user():
    with open('main/data/json/updated_task_data.json', "r") as updated_data_file:
        user_id = json.load(updated_data_file)['user_id']
    task_amount = random.randint(5, 10)
    array_of_tasks = []
    array_of_tasks_ids = []
    for task in range(task_amount):
        task_data = next(generate_task_data(user_id)).to_dict()
        response = requests.put(endpoint.CREATE_TASK, json.dumps(task_data))
        response_body = json.loads(response.content)['task']
        task_data['task_id'] = response_body['task_id']
        array_of_tasks_ids.append(task_data['task_id'])
        array_of_tasks.append(task_data)
    with open('main/data/json/created_task_data.json','w') as created_tasks_file:
        created_tasks_file.write(json.dumps(array_of_tasks))
    return array_of_tasks_ids


@pytest.fixture()
def get_tasks_list():
    with open('main/data/json/updated_task_data.json', "r") as updated_data_file:
        user_id = json.load(updated_data_file)['user_id']
    response = requests.get(endpoint.LIST_TASKS_BY_USER_ID(user_id))
    response_status_code = response.status_code
    response_body = json.loads(response.content)['tasks']
    return response_status_code, response_body


@pytest.fixture()
def delete_all_created_tasks():
    with open("main/data/json/created_task_data.json") as created_tasks_file:
        tasks_to_delete = json.load(created_tasks_file)
    tasks_ids_to_delete = [task['task_id'] for task in tasks_to_delete]
    for task_id in tasks_ids_to_delete:
        response = requests.delete(endpoint.DELETE_TASK_BY_TASK_ID(task_id))
        assert response.status_code == 200, "Task is not deleted"
    return tasks_ids_to_delete
