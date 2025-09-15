from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import JournalEntryForm, MedicationForm
from .models import JournalEntry, Medication
from . import db

views = Blueprint('views',__name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.created_at.desc()).all()
        return render_template("dashboard.html", user=current_user, entries=entries)
    return render_template("home.html")

@views.route('/dashboard')
@login_required
def dashboard():
    # Always load current user's entries when landing on the dashboard
    entries = (
        JournalEntry.query
        .filter_by(user_id=current_user.id)
        .order_by(JournalEntry.created_at.desc())
        .all()
    )
    return render_template("dashboard.html", user=current_user, entries=entries)

@views.route('/add-journal',methods=['GET','POST'])
@login_required
def add_journal():
    form = JournalEntryForm()
    if form.validate_on_submit():
        new_entry=JournalEntry(title=form.title.data,
                               content=form.content.data,
                               severity=form.severity.data,
            user_id=current_user.id)  # Link the entry to the logged-in user
        db.session.add(new_entry)
        db.session.commit()
        flash('Journal added successfully!', category='success')
        return redirect(url_for('views.dashboard'))
    return render_template("add_journal.html",form=form)

#1. HTML forms don’t support DELETE natively
@views.route('/delete-journal/<int:entry_id>', methods=['POST'])
#{{ url_for('views.delete_journal', entry_id=entry.id) }} passes the id aswell when button is clicked
@login_required
def delete_journal(entry_id):
    entry_to_delete = JournalEntry.query.get(entry_id)

    #doesnt matter in normal use but prevents malicious access of other users journal
    if entry_to_delete and entry_to_delete.user_id == current_user.id:
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash('Journal entry deleted.', category = 'success')
    else:
        flash('Entry not found or you do not have permission to delete it',category='error')
    return redirect(url_for('views.dashboard'))

@views.route('/add-medication',methods=['GET','POST'])
@login_required
def add_medication():
    form = MedicationForm()
    if form.validate_on_submit():
        new_med = Medication(
            name = form.name.data,
            dosage = form.dosage.data,
            frequency=form.frequency.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(new_med)
        db.session.commit()
        flash('Medication added!', category='success')
        return redirect(url_for('views.dashboard'))
    return render_template("add_medication.html", form=form)

@views.route('/delete-medication/<int:med_id>',methods=['POST'])
@login_required
def delete_medication(med_id):
    medication_to_delete = Medication.query.get(med_id)
    if medication_to_delete and medication_to_delete.med_id == current_user.med_id:
        db.session.delete(medication_to_delete)
        db.session.commit()
        flash('Medication removed.', category='success')
    else:
        flash('Medication not found or you do not have permission.', category='error')
    return redirect(url_for('views.dashboard'))