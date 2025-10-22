# seed.py
from Website import create_app, db
from Website.models import User, Visit, JournalEntry, Medication
from datetime import datetime

# Create a Flask app instance
app = create_app()

with app.app_context():
    
    # We will not delete old data, as requested.
    print("Creating new data...")
    
    # --- Create a Demo User ---
    # Check if user already exists to avoid errors on re-run
    user = User.query.filter_by(email="demo@example.com").first()
    if not user:
        user = User(username="DemoUser", email="demo@example.com")
        user.set_password("demo123")
        db.session.add(user)
        db.session.commit() # Commit to get the user.id
        print("New demo user created.")
    else:
        print("Demo user already exists.")

    # --- Create Event 1 (A Full Visit) ---
    visit1 = Visit(
        reason="Annual Checkup",
        doctor_name="Dr. Sarah Johnson",
        diagnosis="All clear, recommended light exercise.",
        visit_date=datetime(2025, 10, 20),
        patient=user
    )
    db.session.add(visit1)

    # Add items LINKED to this visit
    visit1.journal_entries.append(
        JournalEntry(title="Pre-checkup notes", 
                     content="Feeling good, just here for the annual.", 
                     severity="Low", 
                     author=user)  # <-- FIX 1: We must also link the entry to the user.
    )
    visit1.prescriptions.append(
        Medication(name="Vitamin D", 
                   dosage="1000 IU", 
                   frequency="Once a day", 
                   patient=user)  # <-- FIX 2: We must also link the medication to the user.
    )

    # --- Create Event 2 (A Standalone Journal Entry) ---
    journal_standalone = JournalEntry(
        title="Sudden Headache",
        content="Woke up with a bad headache on the left side.",
        severity="Medium",
        created_at=datetime(2025, 10, 22),
        author=user
    )
    db.session.add(journal_standalone)
    
    # --- Create Event 3 (Another Visit) ---
    visit2 = Visit(
        reason="Headache Follow-up",
        doctor_name="Dr. Mark Reeves",
        diagnosis="Likely a tension headache. Prescribed rest and hydration.",
        visit_date=datetime(2025, 10, 23),
        patient=user
    )
    db.session.add(visit2)

    # Finalize all the changes
    db.session.commit()
    
    print("Database has been seeded with demo data!")
    print("Login with: demo@example.com / demo123")