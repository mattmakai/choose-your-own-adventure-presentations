import cgi
from flask import render_template, abort, request
from flask import redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, \
                            current_user
from jinja2 import TemplateNotFound
from twilio import twiml
from twilio.rest import TwilioRestClient

from .config import TWILIO_NUMBER
from .forms import LoginForm
from .models import Wizard, Decision

from . import app, redis_db, socketio, login_manager
from .models import Presentation

client = TwilioRestClient()

@login_manager.user_loader
def load_user(userid):
    return Wizard.query.get(int(userid))


@app.route('/', methods=['GET'])
def list_public_presentations():
    presentations = Presentation.query.filter_by(is_visible=True)
    return render_template('list_presentations.html',
                           presentations=presentations)


@app.route('/<slug>/', methods=['GET'])
def presentation(slug):
    presentation = Presentation.query.filter_by(is_visible=True,
                                                slug=slug).first()
    if presentation:
        return render_template('/presentations/' + presentation.filename)
    abort(404)


@app.route('/cyoa/twilio/webhook/', methods=['POST'])
def twilio_callback():
    to = request.form.get('To', '')
    from_ = request.form.get('From', '')
    message = request.form.get('Body', '').lower()
    if to == TWILIO_NUMBER:
        redis_db.incr(cgi.escape(message))
        socketio.emit('msg', {'div': cgi.escape(message),
                              'val': redis_db.get(message)},
                      namespace='/cyoa')
    resp = twiml.Response()
    resp.message("Thanks for your vote!")
    return str(resp)


@app.route('/wizard/', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        wizard = Wizard.query.filter_by(wizard_name=
                                        form.wizard_name.data).first()
        if wizard is not None and wizard.verify_password(form.password.data):
            login_user(wizard)
            return redirect(url_for('wizard_list_presentations'))
    return render_template('wizard/sign_in.html', form=form, no_nav=True)


@app.route('/sign-out/')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('sign_in'))


@app.route('/<presentation_slug>/vote/<decision_slug>/', methods=['GET'])
def decision(presentation_slug, decision_slug):
    presentations = Presentation.query.filter_by(slug=presentation_slug)
    if presentations.count() > 0:
        presentation = presentations.first()
        decision = Decision.query.filter_by(presentation=presentation.id,
                                            slug=decision_slug).first()
        return render_template('decision.html', presentation=presentation,
                               decision=decision)
    return render_template("404.html"), 404


@app.route('/<presentation_slug>/vote/<decision_slug>/<choice_slug>/',
           methods=['GET'])
def web_vote(presentation_slug, decision_slug, choice_slug):
    presentations = Presentation.query.filter_by(slug=presentation_slug)
    if presentations.count() > 0:
        presentation = presentations.first()
        decision = Decision.query.filter_by(presentation=presentation.id,
                                            slug=decision_slug).first()
        if decision:
            votes = redis_db.get(choice_slug)
            return render_template('web_vote.html', decision=decision,
                                   presentation=presentation, votes=votes,
                                   choice=choice_slug)
    return render_template("404.html"), 404


def broadcast_vote_count(key):
    total_votes = 0
    if redis_db.get(key):
        total_votes += int(redis_db.get(key))
    total_votes += len(socketio.rooms['/cyoa'][key])
    socketio.emit('msg', {'div': key, 'val': total_votes},
                  namespace='/cyoa')
