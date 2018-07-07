# StatusCodeServer

simple Web API with Python &amp; Flask, which return http status code you want

## Requirement

python3 flask

```shell
brew install python3

```

## Example Usage

```shell
cd path # server.py document path
python3 server.py runserver
pip3 install -r requirements.txt
```

### website

```
localhost:5000/
localhost:5000/hi
localhost:5000/hello
localhost:5000/hello/{name}
localhost:5000/request # request with your methods
localhost:5000/messsages # post json
localhost:5000/redirect/{url} # which url you want redirect to
localhost:5000/code/{code} # http status code
localhost:5000/png # return png image 
localhost:5000/jpg # return jpg image
```

When you want visit this website by other compute in LAN, replace localhost with ther server compute's LAN IP.

### visit in terminal window.

If you want to see response, call `curl` with `-i`
```shell
curl -i http://127.0.0.1:5000/code/{code} # replace http code
curl -X {Method} http://127.0.0.1:5000/request # replace Request Method
```

## To do

- [ ] cache
    information:    
        1. http://docs.jinkan.org/docs/flask/patterns/caching.html
        2. http://www.bjhee.com/flask-ext6.html
        3. https://pythonhosted.org/Flask-Cache/