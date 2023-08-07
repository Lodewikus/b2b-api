from flask import Flask, request, jsonify, abort
from functools import wraps
from multiprocessing import Process

#app = Flask(__name__)

app = Flask('app')
app_ssl = Flask('app_ssl')

def oauth2_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This should be replaced with real OAuth2 token validation
        if not 'Authorization' in request.headers:
            return jsonify({"message": "Authorization header missing"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app_ssl.route('/api1/')
@oauth2_required
def hello_world():
    if request.path.startswith('/api1') and request.scheme != 'https':
        abort(403)

    return 'Hello, World!'

@app.route('/api2/')
def api_no_auth():
    if request.path.startswith('/api2') and request.scheme != 'http':
        abort(403)
    
    return 'This is API2!'

#if __name__ == '__main__':
#    app.run()
#    app.run(ssl_context=('cert.pem', 'key.pem'))

def run_app_ssl():
    app_ssl.run(port=5000, ssl_context=('cert.pem', 'key.pem'))

def run_app():
    app.run(port=5001)

if __name__ == '__main__':
    p1 = Process(target=run_app)
    p1.start()

    p2 = Process(target=run_app_ssl)
    p2.start()

    p1.join()
    p2.join()