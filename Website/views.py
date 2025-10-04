from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from flask import current_app
from .forms import JournalEntryForm, MedicationForm, DocumentUploadForm, VisitForm
from .models import JournalEntry, Medication, MedicalDocument, Visit
from werkzeug.utils import secure_filename
from . import db
import os
from flask import send_from_directory

views = Blueprint('views',__name__)

@views.route('/', endpoint='home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    
    return render_template("home.html")

@views.route('/dashboard')
@login_required
def dashboard():
    # --- Start of Debugging ---
    print("\n--- DEBUG: Dashboard Route Started ---")

    # Step 1: Fetching the data
    visits = Visit.query.filter_by(user_id=current_user.id).all()
    journals = JournalEntry.query.filter_by(user_id=current_user.id).all()
    print(f"Found {len(visits)} visits in the database.")
    print(f"Found {len(journals)} journal entries in the database.")

    # Step 2: Combining the data
    timeline_events = []
    for visit in visits:
        timeline_events.append({'type': 'visit', 'date': visit.visit_date, 'data': visit})
    print(f"After adding visits, the timeline has {len(timeline_events)} events.")

    for journal in journals:
        if not journal.visit_id:
            timeline_events.append({'type': 'journal', 'date': journal.created_at, 'data': journal})
    print(f"After adding journal entries, the timeline now has {len(timeline_events)} events.")

    # Step 3: Sorting
    print("Sorting the timeline events...")
    try:
        timeline_events.sort(key=lambda x: x['date'], reverse=True)
        print(f"Sorting complete. The final timeline has {len(timeline_events)} events.")
    except Exception as e:
        print(f"!!! ERROR DURING SORTING: {e}")

    # Step 4: Rendering
    print("--- DEBUG: Sending final list to template and rendering. ---\n")
    return render_template("dashboard.html", user=current_user, timeline_events=timeline_events)


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
    if medication_to_delete and medication_to_delete.user_id == current_user.id:
        db.session.delete(medication_to_delete)
        db.session.commit()
        flash('Medication removed.', category='success')
    else:
        flash('Medication not found or you do not have permission.', category='error')
    return redirect(url_for('views.dashboard'))

@views.route('/upload-document', methods=['GET', 'POST'])
@login_required
def upload_document():
    form = DocumentUploadForm()
    visits = Visit.query.filter_by(user_id=current_user.id).order_by(Visit.visit_date.desc()).all()
    form.visit.choices = [(v.id, f"{v.visit_date.strftime('%Y-%m-%d')} - {v.reason}") for v in visits]
    form.visit.choices.insert(0, (0, '--- Do not link to a specific visit ---'))
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        
        # Ensure the upload directory exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        selected_visit_id = form.visit.data if form.visit.data > 0 else None

        # Save file info to the database
        new_doc = MedicalDocument(
            filename=filename,
            filepath=filepath,
            user_id=current_user.id,
            visit_id=selected_visit_id  # Save the selected visit_id
        )
        db.session.add(new_doc)
        db.session.commit()
        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('views.dashboard'))
    return render_template('upload_document.html', form=form)


@views.route('/add-visit', methods=['GET', 'POST'])
@login_required
def add_visit():
    form = VisitForm()
    if form.validate_on_submit():
        new_visit = Visit(
            doctor_name=form.doctor_name.data,
            reason=form.reason.data,
            diagnosis=form.diagnosis.data,
            visit_date=form.visit_date.data,
            user_id=current_user.id
        )
        db.session.add(new_visit)
        db.session.commit()
        flash('Visit has been recorded!', 'success')
        return redirect(url_for('views.dashboard'))
    return render_template('add_visit.html', form=form)

@views.route('/visit/<int:visit_id>')
@login_required
def visit_detail(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    
    # Security check: ensure the visit belongs to the current user
    if visit.user_id != current_user.id:
        abort(403) # Forbidden
        
    return render_template("visit_detail.html", visit=visit)

# In Website/views.py

@views.route('/medications')
@login_required
def medications():
    meds = Medication.query.filter_by(user_id=current_user.id).order_by(Medication.name).all()
    return render_template("medications.html", medications=meds)

@views.route('/documents')
@login_required
def documents():
    docs = MedicalDocument.query.filter_by(user_id=current_user.id).order_by(MedicalDocument.upload_date.desc()).all()
    return render_template("documents.html", documents=docs)

# This route serves the files securely
@views.route('/uploads/<filename>')
@login_required
def get_file(filename):
    # Security check to ensure user can only access their own files
    doc = MedicalDocument.query.filter_by(user_id=current_user.id, filename=filename).first_or_404()
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], doc.filename, as_attachment=True)

@views.route('/delete-document/<int:doc_id>', methods=['POST'])
@login_required
def delete_document(doc_id):
    doc_to_delete = MedicalDocument.query.get(doc_id)
    if doc_to_delete and doc_to_delete.user_id == current_user.id:
        # Delete the file from the server
        try:
            os.remove(doc_to_delete.filepath)
        except OSError as e:
            flash(f"Error deleting file from server: {e}", category='error')
        
        # Delete the record from the database
        db.session.delete(doc_to_delete)
        db.session.commit()
        flash('Document deleted.', category='success')
    else:
        flash('Document not found or you do not have permission.', category='error')
    return redirect(url_for('views.documents'))

# Static page routes
@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/privacy')
def privacy():
    return render_template("privacy.html")

@views.route('/terms')
def terms():
    return render_template("terms.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

