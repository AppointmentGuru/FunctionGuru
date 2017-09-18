"""Trigger functions inside docker containers"""
import hug, yaml, docker, uuid, pytz, datetime
from dateutil import parser
from tasks import run_in_container

DOCKER = docker.from_env()

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
@hug.post(examples='slug=debug&payload={}')
@hug.local()
def service(slug: hug.types.text, command: hug.types.text):
    '''Run a service from the registry'''
    yml = open('registry.yml').read()
    registry = yaml.load(yml)
    config = registry.get('functions', {}).get(slug, None)

    if config is not None:
        restart_policy = docker.types.RestartPolicy(condition='none', max_attempts=1)
        secrets = get_secrets(config.get('secrets'))
        image = config.get('container')
        name = '{}_functionguru_{}'.format(slug, short_id())
        print(command)
        result = DOCKER.services.create(
            image,
            command,
            name=name,
            secrets=secrets,
            restart_policy=restart_policy
        )
        # print(result)
        return {
            "image": image,
            "name": name,
            "command": command,
        }
    else:
        message = '{} is not in the registry'.format(slug)
        print(message)
        return json.dumps({
            "error": message
        })

@hug.cli()
def gc(seconds: hug.types.number=60):
    '''Garbage collection'''
    while True:
        for service in DOCKER.services.list():

            if '_functionguru_' in service.name:
                created = parser.parse(service.attrs.get('CreatedAt'))
                now = datetime.datetime.utcnow()
                now = now.replace(tzinfo=pytz.utc)
                delete_before = datetime.timedelta(seconds=seconds)

                if created < (now - delete_before):
                    service.remove()
                    print ('removed {}'.format(service.name))



