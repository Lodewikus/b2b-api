from flask import Flask, request, jsonify, abort
from functools import wraps
from multiprocessing import Process
from jose import jwt, JWTError
import requests

#app = Flask(__name__)

app = Flask('app')
app_ssl = Flask('app_ssl')

# def oauth2_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         # This should be replaced with real OAuth2 token validation
#         if not 'Authorization' in request.headers:
#             return jsonify({"message": "Authorization header missing"}), 403
#         return f(*args, **kwargs)
#     return decorated_function

def oauth2_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        tenant_id = '72250571-2bdd-409c-9171-b48c97ee5d74'
        client_id = '2eaf78be-97f7-44ee-8590-0adf91febc72'
        if not 'Authorization' in request.headers:
            return jsonify({"message": "Authorization header missing"}), 403
        else:
            token = request.headers['Authorization'].split(" ")[1]
            try:
                well_known_endpoint = f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
                jwks_uri = requests.get(well_known_endpoint).json()["jwks_uri"]
                jwks = requests.get(jwks_uri).json()
                header = jwt.get_unverified_header(token)
                rsa_key = {}
                for key in jwks["keys"]:
                    if key["kid"] == header["kid"]:
                        rsa_key = {
                            "kty": key["kty"],
                            "kid": key["kid"],
                            "use": key["use"],
                            "n": key["n"],
                            "e": key["e"]
                        }
                claim = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    #options={"verify_aud": False}
                    audience='api://'+client_id
                )
            except JWTError as error:
                return jsonify({"message": f"Token validation error: {error}"}), 403
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