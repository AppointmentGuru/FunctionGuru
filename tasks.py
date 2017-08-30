from celery import Celery
from time import sleep
import os
rabbit_user = os.environ.get('RABBITMQ_DEFAULT_USER')
rabbit_pass = os.environ.get('RABBITMQ_DEFAULT_PASS')
connection = 'amqp://{}:{}@broker:5672//'.format(rabbit_user, rabbit_pass)
print (connection)
app = Celery('tasks', broker=connection)

@app.task
def add(x, y):
    sleep(1)
    return x + y

@app.task
def run_in_container(image, command):
    import docker, os
    client = docker.from_env()
    volumes = { '/code/': { 'bind': '/downloads/' } }
    return client.containers.run(image, command, volumes=volumes)
