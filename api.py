"""Trigger functions inside docker containers"""
import hug

@hug.cli()
@hug.local()
def trigger(image: hug.types.text, command: hug.types.text, tag='latest'):
    """Runs command inside image:tag"""
    from .tasks import run_in_container
    run_in_container("{}:{}".format(image, tag), command)
    return 'queued'
