BASE_URL = 'https://todo.pixegami.io/'
CREATE_TASK = f"{BASE_URL}create-task"
UPDATE_TASK = f"{BASE_URL}update-task"


def LIST_TASKS_BY_USER_ID(user_id):
    return f"{BASE_URL}list-tasks/{user_id}"


def GET_TASK_BY_TASK_ID(task_id):
    return f"{BASE_URL}get-task/{task_id}"


def DELETE_TASK_BY_TASK_ID(task_id):
    return f"{BASE_URL}delete-task/{task_id}"
