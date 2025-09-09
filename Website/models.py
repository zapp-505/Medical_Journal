from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='patient', nullable=False) # Roles: 'patient', 'doctor'
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    '''backref='author' → lets you do
    entry = JournalEntry.query.first() - first record in databse
    entry.author gives the User who wrote it
    you can also do  user.journal_entries to get all entry by the user'''
    journal_entries = db.relationship('JournalEntry', backref='author', lazy=True)
    medications = db.relationship('Medication', backref='patient', lazy=True)
    documents = db.relationship('MedicalDocument', backref='patient', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50)) # e.g., 'Low', 'Medium', 'High'
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    dosage = db.Column(db.String(100)) # e.g., "500mg"
    frequency = db.Column(db.String(100)) # e.g., "Twice a day"
    notes = db.Column(db.Text)

class MedicalDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(300), nullable=False) # Path where the file is stored
    upload_date = db.Column(db.DateTime(timezone=True), default=func.now())