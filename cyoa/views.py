from flask import render_template, abort
from jinja2 import TemplateNotFound

from . import app

@app.route('/<presentation_name>/', methods=['GET'])
def landing(presentation_name):
    try:
        return render_template(presentation_name + '.html')
    except TemplateNotFound:
        abort(404)
