from flask import Flask, request, json, Response, redirect
from flask_script import Manager, Server
from flask_cache import Cache
import time
app = Flask(__name__)
manager = Manager(app)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})


# Flask Classics

@app.route('/')
def api_root():
    """ Root """
    return 'simple Web API with Python & Flask'

@app.route('/hi')
def hello():
    """ hi """
    return 'hi\n'

@app.route('/hello/<name>')
def hello_people(name):
    """ hello people """
    return 'hello ' + name + '\n'

@app.route('/hello', methods=['GET'])
@cache.cached(timeout=60)
def api_hello():
    """ Response """
    data = {
        'hello'  : 'world',
    }
    message = json.dumps(data)
    resp = Response(message, status=200, mimetype='application/json')
    resp.cache_control.max_age = 60
    return resp

# Methods

@app.route('/request', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    """ Request Methods """
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE\n"

@app.route('/messages', methods=['POST'])
def api_message():
    """ POST text or json """
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)
    return "415 Unsupported Media Type ;)"

# HTTP Code

@app.route('/redirect/<redirect_url>')
def api_redirect(redirect_url):
    """ redirect """
    return redirect(redirect_url, code=302)

@app.errorhandler(404)
def not_found(error=None):
    """ 404 """
    message = {
        'error': str(error),
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = json.jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/code/<code>')
def api_http_code(code):
    """ return HTTP status code you want!"""
    try:
        http_code = int(code)
        if (http_code > 300 and http_code < 304) or http_code == 305 or http_code == 307:
            return redirect('/', code=http_code)
        elif http_code >= 100 and http_code < 400:
            return Response('success\n', status=http_code, mimetype='application/json')
        elif http_code >= 400 and http_code < 500:
            return Response('fail\n', status=http_code, mimetype='application/json')
        return Response('what do you want ?\n', status=200, mimetype='application/json')
    except ValueError:
        return Response('what do you want ?\n', status=200, mimetype='application/json')

# file

from flask import send_file
@app.route('/png')
def png():
    return send_file('1.png', mimetype='image/png', cache_timeout=60)

@app.route('/jpg')
def jpg():
    return send_file('1.jpg', mimetype='image/jpg', cache_timeout=30)

# request log
@app.before_request
def log_request():
    app.logger.info(time.asctime(time.localtime(time.time())) + ' ' + request.url)

from werkzeug import secure_filename
import os
from flask import url_for

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jepeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """filename:string"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """ upload file """
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    manager.add_command("runserver", Server(use_debugger=True, host='0.0.0.0', port=5000))
    manager.run()