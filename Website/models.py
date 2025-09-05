from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="patient", nullable=False)  # patient | doctor | admin
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    # Relationships
    journal_entries = db.relationship('JournalEntry', backref='author', lazy=True)
    appointments = db.relationship('Appointment', backref='patient', foreign_keys="Appointment.patient_id")

    # 🔑 Functions
    def set_password(self, password):
        """Hashes and stores the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies if input matches stored password hash."""
        return check_password_hash(self.password_hash, password)

    def is_doctor(self):
        return self.role == "doctor"

    def is_patient(self):
        return self.role == "patient"

class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 🔑 Functions
    def summary(self, length=50):
        """Return a short preview of the journal content."""
        return (self.content[:length] + '...') if len(self.content) > length else self.content

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="scheduled")  # scheduled | completed | cancelled
    notes = db.Column(db.Text)

    # 🔑 Functions
    def mark_completed(self):
        """Mark appointment as completed."""
        self.status = "completed"

    def cancel(self):
        """Cancel appointment."""
        self.status = "cancelled"
