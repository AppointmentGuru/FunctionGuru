from celery import Celery
from time import sleep
import os, docker
rabbit_user = os.environ.get('RABBITMQ_DEFAULT_USER')
rabbit_pass = os.environ.get('RABBITMQ_DEFAULT_PASS')
connection = 'amqp://{}:{}@broker:5672//'.format(rabbit_user, rabbit_pass)
app = Celery('tasks', broker=connection, backend='amqp')

@app.task
def add(x, y):
    sleep(1)
    return x + y

@app.task
def run_in_container(image, command):
    client = docker.from_env()
    # pull the image:
    client.images.pull(image, auth_config={"username": os.environ(DOCKER_USERNAME), "password": "budry0kibri"}
    return client.containers.run(image, command)
