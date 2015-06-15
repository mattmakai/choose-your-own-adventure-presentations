from flask import render_template, redirect, url_for
from flask.ext.login import login_required

from . import app, db
from .models import Presentation, Decision
from .forms import PresentationForm, DecisionForm


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
    presentation = Presentation.query.get_or_404(pres_id)
    return render_template('wizard/decisions.html', presentation=presentation,
                           decisions=presentation.decisions.all())


@app.route('/wizard/presentation/<int:pres_id>/decision/',
           methods=['GET', 'POST'])
@login_required
def wizard_new_decision(pres_id):
    form = DecisionForm()
    if form.validate_on_submit():
        decision = Decision()
        form.populate_obj(decision)
        decision.presentation = pres_id
        db.session.add(decision)
        db.session.commit()
        return redirect(url_for('wizard_list_presentation_decisions',
                                pres_id=pres_id))
    return render_template('wizard/decision.html', form=form, is_new=True,
                           presentation_id=pres_id)


@app.route('/wizard/presentation/<int:presentation_id>/decision/'
           '<int:decision_id>/', methods=['GET', 'POST'])
@login_required
def wizard_edit_decision(presentation_id, decision_id):
    decision = Decision.query.get_or_404(decision_id)
    form = DecisionForm(obj=decision)
    if form.validate_on_submit():
        form.populate_obj(decision)
        decision.presentation = presentation_id
        db.session.merge(decision)
        db.session.commit()
        db.session.refresh(decision)
        return redirect(url_for('wizard_list_presentation_decisions',
                        pres_id=presentation_id))
    return render_template('wizard/decision.html', form=form,
                           decision=decision, presentation_id=presentation_id)


@app.route('/wizard/presentation/<int:pres_id>/decision/'
           '<int:decision_id>/delete/')
@login_required
def wizard_delete_decision(pres_id, decision_id):
    presentation = Presentation.query.get_or_404(pres_id)
    decision = Decision.query.get_or_404(decision_id)
    db.session.delete(decision)
    db.session.commit()
    return redirect(url_for('wizard_list_presentation_decisions',
                    pres_id=presentation.id))
