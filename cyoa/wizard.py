from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user

from .forms import LoginForm, PresentationForm, ChoicesForm
from .models import User, Presentation, Choice

from . import app, db


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
        p = Presentation()
        form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('wizard_list_presentations'))
    return render_template('wizard/presentation.html', form=form, is_new=True)


@app.route('/wizard/presentation/<int:id>/', methods=['GET', 'POST'])
@login_required
def wizard_edit_presentation(id):
    p = Presentation.query.get_or_404(id)
    form = PresentationForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.merge(p)
        db.session.commit()
        db.session.refresh(p)
    return render_template('wizard/presentation.html', form=form,
                           presentation=p)


@app.route('/wizard/presentation/<int:id>/choices/', methods=['GET'])
@login_required
def wizard_list_presentation_choices(id):
    p = Presentation.query.get_or_404(id)
    return render_template('wizard/choices.html', presentation=p,
                           choices=p.choices_list.all())
