import cgi
import twilio.twiml
from flask import request, render_template, jsonify, abort
from twilio.rest import TwilioRestClient
from jinja2 import TemplateNotFound

from .config import TWILIO_NUMBER
from . import app, redis_db, socketio


client = TwilioRestClient()


@app.route('/<presentation_name>/', methods=['GET'])
def landing(presentation_name):
    try:
        return render_template(presentation_name + '.html')
    except TemplateNotFound:
        abort(404)


@app.route('/twilio/callback/343595/', methods=['POST'])
def twilio_callback():
    to = request.form.get('To', '')
    from_ = request.form.get('From', '')
    message = request.form.get('Body', '').lower()
    if to == TWILIO_NUMBER: 
        redis_db.incr(message)
        socketio.emit('msg', {'div': cgi.escape(message), 
            'val': redis_db.get(message)}, 
            namespace='/djangocon-2014-deployment')
    resp = twilio.twiml.Response()
    resp.message("Thanks for your vote!")
    return str(resp)
