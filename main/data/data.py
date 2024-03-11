from dataclasses import dataclass
import json


@dataclass
class TaskBase:
    content: str = None
    user_id: str = None
    task_id: str = None
    is_done: bool = False

    def to_dict(self):
        return {
            'content': self.content,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'is_done': self.is_done
        }

    def to_dict_and_write(self, filename, mode):
        data = self.to_dict()
        with open(filename, mode) as file:
            file.write(json.dumps(data))
        return data


@dataclass
class Task(TaskBase):
    def to_dict_and_write(self, mode="w"):
        return super().to_dict_and_write('main/data/json/created_task_data.json', mode)


@dataclass
class UpdatedTask(TaskBase):
    def to_dict_and_write(self):
        return super().to_dict_and_write('main/data/json/updated_task_data.json', 'w')

