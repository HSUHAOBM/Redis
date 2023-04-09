from datetime import timedelta,datetime
from flask import Flask, session, request
from redis import Redis
from flask_session import RedisSessionInterface

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# 儲存方式為 Redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379)

# 設置 session 過期時間
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=20)

# 設置 Flask-Session 的 RedisSessionInterface
redis = Redis(host='localhost', port=6379)
app.session_interface = RedisSessionInterface(redis=redis, key_prefix='session:')

@app.route('/')
def index():
    if 'username' in session:
        return 'Hello, {}!'.format(session['username'])
    else:
        return 'Hello, guest!'

@app.route('/login')
def login():
    # 模擬登錄，設置用戶名為 'John' 的會話信息
    session.permanent = True
    session['username'] = 'John'
    return 'Logged in successfully!'

@app.route('/logout')
def logout():
    # 刪除用戶名為 'John' 的會話信息
    session.pop('username', None)
    return 'Logged out successfully!'

@app.before_request
def update_session_expiration():

    print(request.remote_addr)
    print(request.headers.get('User-Agent'))
    print(request.cookies)
    print(request.method)

    if 'username' in session:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(seconds=60)
        new_expiration = datetime.now() + app.permanent_session_lifetime

        session['expiration'] = new_expiration
        print(f"{session['username']}的過期時間：{new_expiration}")

        session_id = session.sid
        print("Session ID:", session_id)
app.run(debug=True)