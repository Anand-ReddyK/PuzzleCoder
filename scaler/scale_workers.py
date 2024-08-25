import redis
import docker
import time

REDIS_HOST = "redis"
REDIS_PORT = 6379
QUEUE_NAME = "code_queue"
WORKER_CONTAINER_NAME = "puzzlecoder_worker"

MIN_WORKERS = 1
MAX_WORKERS = 10
SCALE_UP_THRESHOLD = 10
SCALE_DOWN_THRESHOLD = 2
CHECK_INTERVAL = 10

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

client = docker.from_env()

def get_queue_length():
    return r.llen(QUEUE_NAME)


def scale_workers(num_workers):
    try:
        service = client.services.get(WORKER_CONTAINER_NAME)  # Ensure this matches your service name
        service.update(mode={"Replicated": {"Replicas": num_workers}})
        print(f'Scaled worker service to {num_workers} replicas')
    except docker.errors.NotFound as e:
        print(f'Service not found: {e}')


def monitor_and_scale():
    current_worker = MIN_WORKERS
    scale_workers(current_worker)
    while True:
        queue_length = get_queue_length()
        print(f"Queue length: {queue_length}")
        if queue_length > SCALE_UP_THRESHOLD and current_worker < MAX_WORKERS:
            current_worker += 1
            scale_workers(current_worker)
        elif queue_length < SCALE_DOWN_THRESHOLD and current_worker > MIN_WORKERS:
            current_worker -= 1
            scale_workers(current_worker)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_and_scale()