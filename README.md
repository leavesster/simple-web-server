# StatusCodeServer

simple Web API with Python &amp; Flask, which return http status code you want

## Requirement

python3 flask

```shell
brew install python3
pip3 install flask
```

## Example Usage

```shell
cd path # server.py document path
python3 server.py
```

open a new terminal window.

```shell
curl -i http://127.0.0.1:5000/code/{code} # replace http code
curl -X {Method} http://127.0.0.1:5000/request # replace Request Method
```
