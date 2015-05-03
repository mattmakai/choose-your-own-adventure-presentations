from flask import render_template, redirect, url_for
from flask.ext.login import login_required

from . import app, db
from .models import Presentation
from .forms import PresentationForm


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

@app.route('/wizard/presentation/<int:pres_id>/decisions/')
@login_required
def wizard_list_presentation_decisions(pres_id):
    pass


@app.route('/wizard/presentation/<int:pres_id>/decision/',
           methods=['GET', 'POST'])
@login_required
def wizard_new_decision(pres_id):
    pass

@app.route('/wizard/presentation/<int:presentation_id>/decision/'
           '<int:decision_id>/', methods=['GET', 'POST'])
@login_required
def wizard_edit_decision(presentation_id, decision_id):
    pass


@app.route('/wizard/presentation/<int:pres_id>/decision/'
           '<int:decision_id>/delete/')
@login_required
def wizard_delete_decision(pres_id, decision_id):
    pass
