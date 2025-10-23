# seed.py
from Website import create_app, db
from Website.models import User, Visit, JournalEntry, Medication, MedicalDocument
from datetime import datetime, timedelta
import random

# Create a Flask app instance
app = create_app()

with app.app_context():
    
    print("Creating comprehensive demo data...")
    
    # --- Create a Demo User ---
    user = User.query.filter_by(email="demo@example.com").first()
    if not user:
        user = User(username="DemoUser", email="demo@example.com")
        user.set_password("demo123")
        db.session.add(user)
        db.session.commit()
        print("✓ New demo user created.")
    else:
        print("✓ Demo user already exists.")

    # --- SET THE DATE RANGE ---
    # We explicitly set the "end date" to today.
    end_date = datetime(2025, 10, 23)
    # Set the start date to one year before today.
    start_date = end_date - timedelta(days=364)
    
    # --- Create 8 Doctor Visits over the year ---
    visits_data = [
        {
            "reason": "Annual Physical Exam",
            "doctor": "Dr. Sarah Johnson",
            "diagnosis": "Overall health excellent. Blood pressure normal (120/80). Recommended maintaining current exercise routine.",
            "date": start_date + timedelta(days=30) # Approx. Nov 2024
        },
        {
            "reason": "Flu-like symptoms",
            "doctor": "Dr. Mark Chen",
            "diagnosis": "Diagnosed with seasonal influenza. Prescribed rest, fluids, and antiviral medication.",
            "date": start_date + timedelta(days=100) # Approx. Jan 2025
        },
        {
            "reason": "Follow-up for flu recovery",
            "doctor": "Dr. Mark Chen",
            "diagnosis": "Full recovery confirmed. Advised to get flu vaccine next season.",
            "date": start_date + timedelta(days=115) # Approx. Feb 2025
        },
        {
            "reason": "Persistent back pain",
            "doctor": "Dr. Emily Rodriguez",
            "diagnosis": "Muscle strain from poor posture. Prescribed physical therapy and pain management.",
            "date": start_date + timedelta(days=180) # Approx. Apr 2025
        },
        {
            "reason": "Skin rash examination",
            "doctor": "Dr. Amanda Lee",
            "diagnosis": "Contact dermatitis. Prescribed topical corticosteroid cream.",
            "date": start_date + timedelta(days=220) # Approx. May 2025
        },
        {
            "reason": "Routine dental checkup",
            "doctor": "Dr. James Wilson",
            "diagnosis": "Teeth and gums healthy. Recommended continuing good oral hygiene.",
            "date": start_date + timedelta(days=270) # Approx. Jul 2025
        },
        {
            "reason": "Allergy consultation",
            "doctor": "Dr. Rachel Martinez",
            "diagnosis": "Seasonal allergies confirmed. Prescribed antihistamines and nasal spray.",
            "date": start_date + timedelta(days=310) # Approx. Aug 2025
        },
        {
            "reason": "Eye strain and headaches",
            "doctor": "Dr. Kevin Patel",
            "diagnosis": "Digital eye strain. Prescribed computer glasses and recommended 20-20-20 rule.",
            "date": start_date + timedelta(days=350) # Approx. Oct 2025
        }
    ]
    
    created_visits = []
    for visit_data in visits_data:
        visit = Visit(
            reason=visit_data["reason"],
            doctor_name=visit_data["doctor"],
            diagnosis=visit_data["diagnosis"],
            visit_date=visit_data["date"],
            patient=user
        )
        db.session.add(visit)
        created_visits.append(visit)
    
    db.session.flush()
    print(f"✓ Created {len(created_visits)} doctor visits")

    # --- Create Event 2 (Standalone Journal Entry) ---
    # We use our end_date variable, dated 1 day ago.
    journal_standalone = JournalEntry(
        title="Sudden Headache",
        content="Woke up with a bad headache on the left side.",
        severity="Medium",
        created_at=end_date - timedelta(days=1), # Oct 22, 2025
        author=user
    )
    db.session.add(journal_standalone)
    
    # --- Create Event 3 (Another Visit) ---
    # We use our end_date variable to represent today.
    visit2 = Visit(
        reason="Headache Follow-up",
        doctor_name="Dr. Mark Reeves",
        diagnosis="Likely a tension headache. Prescribed rest and hydration.",
        visit_date=end_date, # Oct 23, 2025
        patient=user
    )
    db.session.add(visit2)

    # Finalize all the changes
    db.session.commit()
    
    print("Database has been seeded with demo data!")
    print("Login with: demo@example.com / demo123") 