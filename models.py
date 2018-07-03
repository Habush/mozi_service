__author__ = 'Abdulrahman Semrie'
import uuid
import time


class Task(object):
    '''
    A task represents a single instance of a Moses cross-validation run
    '''
    def __init__(self, db, task_id, created_at, status):
        self.task_id = task_id
        self.created_at = created_at
        self.status = status #The current status of the task, -1 = error, 1 = running , 0 = completed
        self.db = db

    def save(self):
        task = {
            'task_id': self.task_id,
            'created_at': self.created_at,
            'status': self.status
        }

        self.db['tasks'].insert_one(task)

    def get_results(self):
        results = []

        for result in self.db['results'].find({'task_id': self.task_id}):
            results.append(Result(self.db, result['task'], result['fold'], result['precision'], result['recall'],
                             result['accuracy'], result['data']))

        return results

    @staticmethod
    def get_task(db,task_id):

        task = db['tasks'].find_one({
            'task_id': task_id
        })

        if task:
            return Task(db, task['task_id'], task['created_at'], task['status'])

        return None

    @staticmethod
    def get_task_status(db, task_id):

        task = db['tasks'].find_one({
            'task_id': task_id
        })

        if task:
            return task['status']

        return -2

    @staticmethod
    def update_status(db, task_id, status):
        db['tasks'].update_one({'task_id':task_id}, {
            '$set': {
                'status': status
            }
        })

class Result(object):
    """
    This model class represents the MOSES task analysis result
    """

    def __init__(self, db, task, fold, precision, recall, accuracy, data, id=None):
        """
        :param db: The PyMongodb client
        :param task: The task id
        :param data: A json data that represents the MOSES models as a tree
        :param id: The id of the result
        """

        self.db = db
        self.task = task
        self.data = data
        self.id = id
        self.fold = fold
        self.precision = precision
        self.recall = recall
        self.accuracy = accuracy

    def save(self):
        """
        Adds a result to the database
        :return:
        """
        result = {
            "task": self.task,
            "data": self.data,
            "fold": self.fold,
            "precision": self.precision,
            "recall": self.recall,
            "accuracy": self.accuracy
        }

        try:
            self.id = str(self.db['results'].insert_one(result).inserted_id)
            return True
        except Exception:
            return False

    def update(self, new_data):
        self.data = new_data
        try:
            self.db['results'].update_one({
                "task": self.task
            }, {
                '$set': {
                    "data": self.data
                }
            }, upsert=True)
            return True
        except Exception:
            return False

    @staticmethod
    def get_result(task_id, db):
        res = db['results'].find({
            'task': task_id
        })
        results = []
        for result in res:
            results.append(Result(db, result['task'], result['fold'], result['precision'], result['recall'],
                         result['accuracy'], result['data']))

        return results

