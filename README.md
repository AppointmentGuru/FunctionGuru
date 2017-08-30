## Run commands inside containers

Exposes an API and cli for executing commands inside containers.



**Getting started:**

**API**

```
docker-compose up -d

# docker run ubuntu:latest echo "hi"
# by default this will run in the background and return the result id of the celery task
curl -i -XPOST http://localhost:8002/trigger/ --data image=ubuntu --data command='echo "hi"'
>> {"result": "6fe9a204-450f-4d8c-a237-50569e5858d1"}

# or run the command as a blocking request by specifying: --data background=false
# will return the response directly from the command
curl -i -XPOST http://localhost:8002/trigger/ --data image=ubuntu --data command='echo "hi"' --data background=false
>> "hi\n"
```

**cli usgage:**

Simply check out the repo, then run: `docker-compose run --rm web hug -f api.py -c trigger ubuntu "echo 'hello'"`

### Examples:

(to run them inside docker, simply prepend with: `docker-compose run --rm web`)

**CLI:**

**Hello world**

Run `echo "hello"` inside an ubuntu container

```
hug -f api.py -c trigger ubuntu "echo 'hello'"
```


```
>>> from api import trigger
>>> trigger('ubuntu', 'echo "hello"')
b'hello\n'
```

<!--
**Generate a PDF**

```
>>> from api import trigger
>>> trigger('aquavitae/weasyprint', 'weasyprint https://invoiceguru.appointmentguru.co/invoice/1/ /downloads/vumatel.pdf')
b'hello\n'
```
-->