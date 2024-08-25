import redis
import json
import os
from django.conf import settings

redis_connection = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def enqueue_task(language, code, test_cases, user_id, problem_id):
    task = {
        "language": language,
        "code": code,
        "test_cases": test_cases,
        "user_id": user_id,
        "problem_id": problem_id
    }

    redis_connection.rpush("code_queue", json.dumps(task))

def get_task_results(user_id):
    channel = f"code_result_{user_id}"
    result = redis_connection.get(channel)
    if result:
        redis_connection.delete(channel)
        return json.loads(result)
    
    return "Pending"