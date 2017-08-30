"""Trigger functions inside docker containers"""
import hug
from tasks import run_in_container

@hug.cli()
@hug.post(examples='image=ubuntu&command=echo "hi"&async=0')
@hug.local()
def trigger(
    image: hug.types.text,
    command: hug.types.text,
    background: hug.types.smart_boolean=True,
    tag='latest'):
    """Runs command inside image:tag"""

    image_tag = "{}:{}".format(image, tag)
    if background:
        result = run_in_container.delay(image_tag, command)
        return {"result": result.id}
    else:
        return run_in_container(image_tag, command)

