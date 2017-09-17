"""Trigger functions inside docker containers"""
import hug, yaml, docker, uuid, pytz, datetime
from dateutil import parser
from tasks import run_in_container

DOCKER = docker.from_env()

@hug.cli()
@hug.post(examples='image=ubuntu&command=echo "hi"&async=0')
@hug.local()
def trigger(
    image: hug.types.text,
    command: hug.types.text,
    background: hug.types.smart_boolean=True,
    tag='latest'):
    """
    Runs command inside image:tag

    `curl -X POST http://localhost:8002/trigger/ --data image=appointmentguru/urltopdfandemail --data command="hug -f api.py -c handle info@38.co.za http://yahoo.com"`

    """

    image_tag = "{}:{}".format(image, tag)
    if background:
        result = run_in_container.delay(image_tag, command)
        return {"result": result.id}
    else:
        return run_in_container(image_tag, command)

def get_secrets(list_of_secrets):
    required_secrets = []
    for secret_name in list_of_secrets:
        secret_object = DOCKER.secrets.get(secret_name)
        secret_ref = docker.types.SecretReference(secret_object.id, secret_object.name)
        required_secrets.append(secret_ref)
    return required_secrets

def short_id():
    return str(uuid.uuid4()).split('-')[0]

@hug.cli()
@hug.post(examples='image=ubuntu&command=echo "hi"&async=0')
@hug.local()
def service(slug: hug.types.text):
    '''Run a service from the registry'''
    yml = open('registry.yml').read()
    registry = yaml.load(yml)
    config = registry.get('functions', {}).get(slug, None)

    if config is not None:
        command = config.get('command')
        secrets = get_secrets(config.get('secrets'))
        image = config.get('container')
        name = '{}_functionguru_{}'.format(slug, short_id())
        return DOCKER.services.create(
            image,
            command,
            name=name,
            secrets=secrets)
    else:
        print('{} is not in the registry'.format(slug))

@hug.cli()
def gc(seconds: hug.types.number=60):
    '''Garbage collection'''

    for service in DOCKER.services.list():

        created = parser.parse(service.attrs.get('CreatedAt'))
        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.utc)
        delete_before = datetime.timedelta(seconds=seconds)

        if created < (now - delete_before):
            service.remove()
            print ('removed {}'.format(service.name))



