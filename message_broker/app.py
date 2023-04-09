from flask import Flask, render_template, Response
from redis import Redis
import json

app = Flask(__name__)
redis = Redis(host='localhost', port=6379)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message')
def send_message():
    message = {'text': 'New message received!'}
    redis.publish('notification', json.dumps(message))
    return 'Message sent!'

def event_stream():
    pubsub = redis.pubsub()
    pubsub.subscribe('notification')

    for message in pubsub.listen():
        yield 'data: {}\n\n'.format(str(message['data']).encode())

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)