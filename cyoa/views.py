import cgi
from flask import render_template, abort, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, \
                            current_user
from jinja2 import TemplateNotFound
from twilio import twiml
from twilio.rest import TwilioRestClient

from .config import TWILIO_NUMBER
from .forms import LoginForm, PresentationForm
from .models import User, Presentation, Choice

from . import app, redis_db, socketio, db, login_manager

client = TwilioRestClient()

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/', methods=['GET'])
def list_public_presentations():
    presentations = Presentation.query.filter_by(is_active=True)
    return render_template('list_presentations.html', 
                           presentations=presentations)


@app.route('/<presentation_name>/', methods=['GET'])
def presentation(presentation_name):
    try:
        return render_template('/presentations/' + presentation_name + '.html')
    except TemplateNotFound:
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
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('wizard_list_presentations'))
    return render_template('wizard/sign_in.html', form=form, no_nav=True)


@app.route('/sign-out/', methods=['GET'])
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('list_public_presentations'))


@app.route('/wizard/presentations/', methods=['GET'])
@login_required
def wizard_list_presentations():
    presentations = Presentation.query.all()
    return render_template('wizard/presentations.html',
                           presentations=presentations)

@app.route('/wizard/presentation/', methods=['GET', 'POST'])
@login_required
def wizard_new_presentation():
    form = PresentationForm()
    if form.validate_on_submit():
        p = Presentation(name=form.name.data, filename=form.filename.data)
        if form.is_active.data:
            p.is_active = form.is_active.data
        if form.number.data:
            p.choices_number = form.number.data
        if form.email.data:
            p.choices_email = form.choices_email.data
        if form.url_slug.data:
            p.url_slug = form.url_slug.data
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('wizard_list_presentations'))
    return render_template('wizard/presentation.html', form=form, is_new=True)


@app.route('/wizard/presentation/<int:id>/', methods=['GET', 'POST'])
@login_required
def wizard_edit_presentation(id):
    form = PresentationForm()
    p = Presentation.query.get_or_404(id)
    if form.validate_on_submit():
        p.name = form.name.data
        p.filename = form.filename.data
        print form.url_slug.data
        p.url_slug = form.url_slug.data
        # todo: save rest of fields
        db.session.merge(p)
        db.session.commit()
        db.session.refresh(p)
        print p.url_slug
    else:
        form.name.data = p.name
        form.filename.data = p.filename
        # todo: fill in rest of fields
    return render_template('wizard/presentation.html', form=form,
                           presentation=p)



