import os, urllib.request, json

from flask import Flask, send_from_directory, jsonify
from flask.helpers import send_file


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


@app.route('/confirm-received')
def confirm_received():
    return "yes baby"

@app.route('/send-notifications')
def send_notification():
    from pyfcm import FCMNotification
    client = FCMNotification(api_key='AAAApNL_Spc:APA91bFiPwQpZOpODWg08WuaA0qcA9jknHagr5ZxPvmR7lf3upwDXCH_LUP0rJ5L2FN3If11GRTKgIh1dvzW3gKXO2WmuFiQLaPV0jO7Ohdmjegllpk5FjXYwRGepoTJAFRiNcWF-Cx4')
    data_message = {
    "Nick" : "Mario",
    "body" : "great match!",
    "Room" : "PortugalVSDenmark"
    }

    registration_id = 'fQGho5eSP2oAaNMFBB41o7:APA91bH3Pf6w8c2h70EDjvU1hYnw9wVm_ZiFfD1zHnoaVtxH0Vswc9K8sADimLk0KVBMmTkm0XeBubB1-k4Lg-44Yx8m_YUFlYbd-RqceFF7Fo0prSGQCyVX_pSj7KS0WJUS2eyS10Nf'
    message_title = "Johnny likes your comment"
    message_body = "Hi john, someone likes your comment"
    result = client.notify_single_device(registration_id=registration_id, low_priority=True, click_action='/confirm-received',message_title=message_title, message_body=message_body, data_message=data_message)
    return jsonify(result)
   

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
