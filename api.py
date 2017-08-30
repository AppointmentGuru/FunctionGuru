"""Trigger functions inside docker containers"""
import hug

@hug.cli()
@hug.local()
def trigger(image: hug.types.text, command: hug.types.text, tag='latest'):
    """Runs command inside image:tag"""
    import docker, os
    client = docker.from_env()
    volumes = { '/code/': { 'bind': '/downloads/' } }
    return client.containers.run("{}:{}".format(image, tag), command, volumes=volumes)
