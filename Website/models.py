# In Website/models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    # ... (no changes to the User model itself)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='patient', nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    journal_entries = db.relationship('JournalEntry', backref='author', lazy=True)
    medications = db.relationship('Medication', backref='patient', lazy=True)
    documents = db.relationship('MedicalDocument', backref='patient', lazy=True)
    # NEW: Add relationship to Visits
    visits = db.relationship('Visit', backref='patient', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# NEW MODEL: The central hub for events
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_name = db.Column(db.String(150))
    reason = db.Column(db.String(255), nullable=False)
    diagnosis = db.Column(db.Text)
    visit_date = db.Column(db.DateTime(timezone=True), default=func.now)
    
    # These relationships will link other items to this visit
    journal_entries = db.relationship('JournalEntry', backref='visit', lazy=True)
    prescriptions = db.relationship('Medication', backref='visit', lazy=True)
    documents = db.relationship('MedicalDocument', backref='visit', lazy=True)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    # NEW: Add an optional link to a Visit
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), nullable=True)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    notes = db.Column(db.Text)
    # NEW: Add an optional link to a Visit where this was prescribed
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), nullable=True)

class MedicalDocument(db.Model):
    # ... (no changes to this model yet, but you could add a visit_id here too)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)
    upload_date = db.Column(db.DateTime(timezone=True), default=func.now())
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), nullable=True)