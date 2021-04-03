import os, urllib.request, json

from flask import Flask, send_from_directory
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


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
