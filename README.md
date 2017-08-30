## Run commands inside containers

**Getting started:**

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