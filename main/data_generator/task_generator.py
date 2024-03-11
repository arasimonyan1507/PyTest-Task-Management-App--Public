import random

from main.data.data import Task, UpdatedTask
from faker import Faker
import json

fake = Faker()


def generate_task_data(user_id=None):
    yield Task(
        content=fake.sentence(nb_words=5, variable_nb_words=True),
        task_id=str(fake.random_int()),
        user_id=user_id or str(fake.random_int()),
        is_done=False
    )


def update_task_data():
    with open('main/data/json/created_task_data.json', 'r') as created_task_file:
        created_task_id = json.load(created_task_file)['task_id']
        yield UpdatedTask(
            content=fake.sentence(nb_words=5, variable_nb_words=True),
            user_id=str(fake.random_int()),
            task_id=created_task_id,
            is_done=False
        )

