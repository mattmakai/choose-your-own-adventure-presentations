from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user

from .forms import LoginForm, PresentationForm, ChoiceForm
from .models import Wizard, Presentation, Choice

from . import app, db


@app.route('/wizard/presentations/')
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
        presentation = Presentation()
        form.populate_obj(presentation)
        db.session.add(presentation)
        db.session.commit()
        return redirect(url_for('wizard_list_presentations'))
    return render_template('wizard/presentation.html', form=form, is_new=True)


@app.route('/wizard/presentation/<int:id>/', methods=['GET', 'POST'])
@login_required
def wizard_edit_presentation(id):
    presentation = Presentation.query.get_or_404(id)
    form = PresentationForm(obj=presentation)
    if form.validate_on_submit():
        form.populate_obj(presentation)
        db.session.merge(presentation)
        db.session.commit()
        db.session.refresh(presentation)
    return render_template('wizard/presentation.html', form=form,
                           presentation=presentation)


@app.route('/wizard/presentation/<int:pres_id>/choices/')
@login_required
def wizard_list_presentation_choices(pres_id):
    presentation = Presentation.query.get_or_404(pres_id)
    return render_template('wizard/choices.html', presentation=presentation,
                           choices=presentation.choices_list.all())


@app.route('/wizard/presentation/<int:pres_id>/choice/',
           methods=['GET', 'POST'])
@login_required
def wizard_new_choice(pres_id):
    form = ChoiceForm()
    if form.validate_on_submit():
        choice = Choice()
        form.populate_obj(choice)
        choice.presentation = pres_id
        db.session.add(choice)
        db.session.commit()
        return redirect(url_for('wizard_list_presentation_choices',
                                pres_id=pres_id))
    return render_template('wizard/choice.html', form=form, is_new=True,
                           presentation_id=pres_id)


@app.route('/wizard/presentation/<int:pres_id>/choice/<int:choice_id>',
           methods=['GET', 'POST'])
@login_required
def wizard_edit_choice(pres_id, choice_id):
    choice = Choice.query.get_or_404(choice_id)
    form = ChoiceForm(obj=choice)
    if form.validate_on_submit():
        form.populate_obj(choice)
        choice.presentation = pres_id
        db.session.merge(choice)
        db.session.commit()
        db.session.refresh(choice)
    return render_template('wizard/choice.html', form=form,
                           choice=choice)

