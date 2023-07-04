from flask import Flask , request , jsonify , make_response , render_template , session
import jwt
from datetime import datetime , timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '6bb14f2e41bb41209aae287dc1a9f063'

def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!':'Token is missing'})
        try:
            payload =jwt.decode(token, app.config ['SECRET_KEY'])
        except:
            return jsonify({'Alert!':'Invalid Token'})

    return decorated

#home
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return'Logged in currently!'

#for public
@app.route('/public')
def public():
    return 'For Public'
#Authentificated
@app.route('/auth')
@token_required
@token_required
def auth():
    try:
        token = request.args.get('token')
        payload = jwt.decode(token, app.config['SECRET_KEY'])
        return 'JWT is verified. Welcome to your dashboard!'
    except jwt.ExpiredSignatureError:
        return 'Token has expired. Please obtain a new token.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Authentication failed.'

#login
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm:"Authentication Failed!"'})


@app.route('/refresh-token', methods=['POST'])
@token_required
def refresh_token():
    try:
        token = request.args.get('token')
        payload = jwt.decode(token, app.config['SECRET_KEY'])

        # Generate a new token with refreshed expiration time
        refreshed_token = jwt.encode({
            'user': payload['user'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        }, app.config['SECRET_KEY'])

        return jsonify({'token': refreshed_token.decode('utf-8')})

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired. Please login again.'}), 401

    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token. Authentication failed.'}), 401



if __name__ == "__main__" :
    app.run(debug=True)
