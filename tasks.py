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

    env = [
        'MAILGUN_TOKEN={}'.format(os.environ.get('MAILGUN_TOKEN')),
        'MAILGUN_DOMAIN={}'.format(os.environ.get('MAILGUN_DOMAIN'))
    ]

    # pull the image:
    auth = {
        "username": os.environ.get('DOCKER_USERNAME'),
        "password": os.environ.get('DOCKER_PASSWORD')
    }
    client.images.pull(image, auth_config=auth)
    result = client.containers.run(image, command, environment=env)
    return result.decode("utf-8")
