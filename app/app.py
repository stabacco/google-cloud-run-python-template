import os, urllib.request, json

from flask import Flask, send_from_directory, jsonify
from flask.helpers import get_load_dotenv, send_file

get_load_dotenv()

def render_template(template_name: str, render_kwargs: "Dict[Any, Any]"):
    import jinja2

    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
    templateEnv = jinja2.Environment(
        loader=templateLoader, extensions=["jinja2.ext.i18n"]
    )

    send_file('firebase-messaging-sw.js')
    template = templateEnv.get_template(template_name)
    return template.render(render_kwargs)

app = Flask(__name__, static_url_path='')

@app.route('/')
def hello_world():
    return render_template("index.html", {})

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/confirm-received/<target_id>')
def confirm_received(target_id):
    return f"yes baby i received the notification about {target_id}"

@app.route('/send-notifications')
def send_notification():
    from pyfcm import FCMNotification
    client = FCMNotification(api_key=os.getenv('FCM_KEY'))
    data_message = {
    "Nick" : "Mario",
    "body" : "great match!",
    "Room" : "PortugalVSDenmark"
    }

    registration_id = 'frx2IAlOhBPPpo4x7uHfOX:APA91bFuet5ldR5E49QU8A8htwwb8izD4yDqL-_LmqdZW9sspMY9ymq6n8W72XNJK0snF4JoDa2qA6j7OzYHZrbDnEEsG_eBAZ9Jw-_ueVk9UlcyX6TSTSUMB0ndb3jfXcP5kGtghvRJ'
    message_title = "Johnny likes your comment"
    message_body = "Hi john, someone likes your comment"
    result = client.notify_single_device(registration_id=registration_id, 
    badge='https://skodel.com/static/logo-093f845aca56eaa157a5dbc5f8179f02.png', low_priority=True, 
    click_action='/confirm-received/message-id',message_title=message_title, message_body=message_body, data_message=data_message)
    return jsonify(result)
   
@app.route('/send-task', methods = ['GET'])
def send_task():
    from google.cloud import tasks_v2
    from google.protobuf import timestamp_pb2
    import datetime

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    project = 'kubernetes-test-302803'
    queue = 'yfinance-update-queue'
    location = 'australia-southeast1'
    url = 'https://google-cloud-run-python-template-o6yadma6ta-ew.a.run.app/task-run'
    service_account_email = 'cloud-tasker@kubernetes-test-302803.iam.gserviceaccount.com';
    payload = 'hello'
    schedule_time = datetime.datetime.now() + datetime.timedelta(hours=2)

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,  # The full url path that the task will be sent to.
            "oidc_token": {"service_account_email": service_account_email},
        }
    }

    if payload is not None:
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task["http_request"]["body"] = converted_payload

    if schedule_time:
        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(schedule_time)

        # Add the timestamp to the tasks.
        task["schedule_time"] = timestamp
    # Use the client to build and send the task.
    response = client.create_task(request={"parent": parent, "task": task})

    print("Created task {}".format(response.name))
    return ("Created task {}".format(response.name))


from functools import wraps
from flask import request
from google.oauth2 import id_token
from google.auth.transport import requests

def verify_service_account_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        try:
            token = request.headers.get('Authorization')
            if not token:
                return {"error": "not authenticated"}, 401

            token = token.replace('Bearer ', '')
            t = id_token.verify_oauth2_token(token, requests.Request(), )
            raise RuntimeError(t)
        except ValueError:
            return {"error": "not authenticated"}, 401
        
        return func(*args, **kwargs)
    return wrapper

@app.route('/task-run', methods=['GET', 'POST'])
@verify_service_account_token
def task_run():
    import logging
    logging.warning("all good, no worry")
    return {"all": "good"}

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
