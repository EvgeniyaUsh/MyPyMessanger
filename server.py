from flask import Flask, request, abort
import datetime
import time

db = []

app = Flask(__name__)


# чтобы возвращал общее кол-во пользователей и сообщений на сервере
@app.route("/status")
@app.route("/")
def status():
    dt = datetime.datetime.now()
    return {
        'status': True,
        'name': 'MyPyMess',
        'time': dt
    }


@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json.get('name')
    text = request.json.get('text')

    if not (isinstance(name, str) and isinstance(text, str)
            and name and text):
        return abort(400)

    new_message = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    db.append(new_message)
    return {
        'ok': True
    }


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args.get('after', 0))
    except ValueError:
        return abort(400)

    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)
    return {'messages': messages}


app.run()
