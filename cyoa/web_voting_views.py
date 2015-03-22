from flask import render_template, abort, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, \
                            current_user
from jinja2 import TemplateNotFound
from twilio import twiml
from twilio.rest import TwilioRestClient

from .config import TWILIO_NUMBER
from .forms import LoginForm
from .models import Wizard, Presentation, Choice

from . import app, redis_db, socketio, db, login_manager


@app.route('/<slug>/vote/<int:decision>/', methods=['GET'])
def decision(slug, decision):
    presentation = _get_presentation_if_web_vote(slug)
    if presentation:
        choices = Choice.query.filter_by(presentation=presentation.id,
                                         decision_point=decision)
        return render_template('decision.html', presentation=presentation,
                               choices=choices)
    return render_template("404.html"), 404


@app.route('/<slug>/vote/<int:decision>/<choice_slug>/', methods=['GET'])
def web_vote(slug, decision, choice_slug):
    presentation = _get_presentation_if_web_vote(slug)
    if presentation:
        choice = Choice.query.filter_by(slug=choice_slug).first()
        votes = redis_db.get(choice.slug)
        return render_template('web_vote.html', choice=choice,
                               presentation=presentation, votes=votes)
    return render_template("404.html"), 404


@socketio.on('vote', namespace='/cyoa')
def vote(vote):
    if vote:
        presentation = _get_presentation_if_web_vote(vote['presentation_slug'])
        if presentation:
            choice = Choice.query.filter_by(slug=vote['choice']).first()
            vote_count = redis_db.incr(choice.slug)
            socketio.emit('msg', {'div': choice.slug, 'val': vote_count},
                          namespace='/cyoa')

@socketio.on('unvote', namespace='/cyoa')
def unvote(vote):
    if vote:
        presentation = _get_presentation_if_web_vote(vote['presentation_slug'])
        if presentation:
            choice = Choice.query.filter_by(slug=vote['choice']).first()
            vote_count = redis_db.decr(choice.slug)
            socketio.emit('msg', {'div': choice.slug, 'val': vote_count},
                          namespace='/cyoa')


def _get_presentation_if_web_vote(slug):
    presentations = Presentation.query.filter_by(slug=slug)
    if presentations.count() > 0:
        presentation = presentations.first()
        if presentation.enable_browser_voting:
            return presentation
    return None
