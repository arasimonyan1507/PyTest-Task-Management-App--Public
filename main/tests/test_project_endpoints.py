def test_create_task(create_task):
    # Create a task with randomized data. Extract task data, status code and response body.
    task_data, status_code, response_body = create_task

    # Assert the status code
    assert status_code == 200, f"Task creation failed with status code: {status_code}"

    # Assert the task properties
    keys_to_assert = ['user_id', 'task_id', 'content']
    for key in keys_to_assert:
        assert task_data[key] == response_body[
            key], f"{key}s don't match: input`{task_data[key]}, output`{response_body[key]} "

    # Assert that the expiration duration is 86400 seconds.
    expiration_duration = response_body['ttl'] - response_body['created_time']
    assert expiration_duration == 86400, (f"Expiration duration does not match the expected value: expected`86400, "
                                          f"actual`{expiration_duration}")


def test_update_task(update_task):
    # Update a task by task id. Extract data before update, updated task data, status code, and response body.
    data_before_update, updated_task_data, status_code, response_body = update_task

    # Assert the status code
    assert status_code == 200, f"Task update failed with status code: {status_code}"

    # Assert that the response body contains the updated task id.
    assert response_body['updated_task_id'] == updated_task_data['task_id']


def test_get_task_by_id(get_task_by_id):
    # Get task by id. Extract the status code and body from the response, along with the updated task data.
    updated_task_data, status_code, response_body = get_task_by_id

    # Assert the status code
    assert status_code == 200, f"Task retrieval failed with status code: {status_code}"

    # Assert response body properties following the update of task data.
    keys_to_assert = ['task_id', 'content', 'is_done']
    for key in keys_to_assert:
        assert updated_task_data[key] == response_body[key], (f"{key}s don't match between updated task data and "
                                                              f"response body")


def test_create_multiple_tasks_for_the_same_user(create_multiple_tasks_for_the_same_user, get_tasks_list):
    # Create multiple tasks for the same user
    list_of_tasks = create_multiple_tasks_for_the_same_user

    # Get list of tasks by user id
    status_code, response_body = get_tasks_list

    # Extract task ids from response body
    response_body_ids = [task['task_id'] for task in response_body]

    # Assert the status code
    assert status_code == 200, f"Task retrieval failed with status code: {status_code} for getting list of tasks"

    # Assert task id exists in the list received from response body
    for task_id in list_of_tasks:
        assert task_id in response_body_ids, 'Task creation failed'


def test_delete_all_created_tasks(delete_all_created_tasks, get_tasks_list):
    # Delete all created tasks by task id and extract list of task ids
    tasks_ids_to_delete = delete_all_created_tasks

    # Get list of tasks by user id
    status_code, response_body = get_tasks_list

    # Extract task ids from response body
    response_body_ids = [task['task_id'] for task in response_body]

    # Assert the status code
    assert status_code == 200, f"Task retrieval failed with status code: {status_code} for getting list of tasks"

    # Assert deleted task's id doesn't exist in the list received from response body
    for task_id in tasks_ids_to_delete:
        assert task_id not in response_body_ids, "Task is not deleted successfully"
