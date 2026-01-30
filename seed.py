# seed.py
from Website import create_app, db
from Website.models import User, Visit, JournalEntry, Medication, MedicalDocument
from datetime import datetime, timedelta
import random

# Create a Flask app instance
app = create_app()

with app.app_context():
    
    print("🧹 Clearing existing demo data...")
    
    # --- Create or Get Demo User ---
    user = User.query.filter_by(email="demo@example.com").first()
    if not user:
        user = User(username="DemoUser", email="demo@example.com")
        user.set_password("demo123")
        db.session.add(user)
        db.session.commit()
        print("✓ New demo user created.")
    else:
        # Clear existing data for this user
        JournalEntry.query.filter_by(user_id=user.id).delete()
        Medication.query.filter_by(user_id=user.id).delete()
        Visit.query.filter_by(user_id=user.id).delete()
        MedicalDocument.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        print("✓ Demo user exists. Cleared old data.")

    print("\n📊 Creating comprehensive demo data...")
    
    # --- SET THE DATE RANGE ---
    # Use current date as end date for realistic testing
    end_date = datetime.now()
    # Set the start date to 6 months ago
    start_date = end_date - timedelta(days=180)
    
    # --- Create 8 Doctor Visits over the 6 months ---
    visits_data = [
        {
            "reason": "Annual Physical Exam",
            "doctor": "Dr. Sarah Johnson",
            "diagnosis": "Overall health excellent. Blood pressure 120/80. BMI 23.5. Recommended maintaining current exercise routine and balanced diet.",
            "days_ago": 170
        },
        {
            "reason": "Persistent cough and congestion",
            "doctor": "Dr. Mark Chen",
            "diagnosis": "Upper respiratory infection. Prescribed azithromycin 500mg and recommended rest, fluids, and humidifier use.",
            "days_ago": 140
        },
        {
            "reason": "Follow-up for respiratory infection",
            "doctor": "Dr. Mark Chen",
            "diagnosis": "Full recovery confirmed. Lungs clear. Advised to complete antibiotic course and get flu vaccine.",
            "days_ago": 130
        },
        {
            "reason": "Lower back pain",
            "doctor": "Dr. Emily Rodriguez",
            "diagnosis": "Lumbar muscle strain from poor ergonomics. Prescribed ibuprofen 400mg TID, physical therapy referral, and posture correction exercises.",
            "days_ago": 95
        },
        {
            "reason": "Skin rash on arms",
            "doctor": "Dr. Amanda Lee",
            "diagnosis": "Contact dermatitis likely from laundry detergent. Prescribed hydrocortisone 1% cream BID and recommended hypoallergenic products.",
            "days_ago": 70
        },
        {
            "reason": "Seasonal allergy consultation",
            "doctor": "Dr. Rachel Martinez",
            "diagnosis": "Allergic rhinitis to pollen. Prescribed cetirizine 10mg daily and fluticasone nasal spray. Recommended air purifier.",
            "days_ago": 45
        },
        {
            "reason": "Migraine headaches",
            "doctor": "Dr. Kevin Patel",
            "diagnosis": "Tension-type migraine with visual aura. Prescribed sumatriptan 50mg as needed. Recommended stress management and sleep hygiene.",
            "days_ago": 20
        },
        {
            "reason": "Routine follow-up",
            "doctor": "Dr. Sarah Johnson",
            "diagnosis": "All previous conditions resolved. Blood work normal. Continue current medications and healthy lifestyle habits.",
            "days_ago": 5
        }
    ]
    
    created_visits = []
    for visit_data in visits_data:
        visit = Visit(
            reason=visit_data["reason"],
            doctor_name=visit_data["doctor"],
            diagnosis=visit_data["diagnosis"],
            visit_date=end_date - timedelta(days=visit_data["days_ago"]),
            patient=user
        )
        db.session.add(visit)
        created_visits.append(visit)
    
    db.session.flush()
    print(f"✓ Created {len(created_visits)} doctor visits")

    # --- Create Journal Entries (Symptom Logs) ---
    journal_entries_data = [
        {"title": "Feeling under the weather", "content": "Started feeling congested and tired. Slight fever of 99.8°F. Taking it easy today.", "severity": "Medium", "days_ago": 142},
        {"title": "Cough getting worse", "content": "Cough is more persistent today. Some chest tightness. Scheduled doctor appointment.", "severity": "High", "days_ago": 141},
        {"title": "Post-appointment update", "content": "Doctor prescribed antibiotics. Already feeling a bit better after first dose.", "severity": "Medium", "days_ago": 140},
        {"title": "Much better!", "content": "Cough almost gone. Energy levels back to normal. Glad the antibiotics worked.", "severity": "Low", "days_ago": 135},
        
        {"title": "Back pain after work", "content": "Lower back is really sore after sitting at desk all day. Must improve my posture.", "severity": "Medium", "days_ago": 100},
        {"title": "Back pain worse", "content": "Pain radiating down left leg. Hard to stand up straight. Need to see doctor.", "severity": "High", "days_ago": 96},
        {"title": "Started PT exercises", "content": "Physical therapist showed me stretches. Doing them 3x daily. Some relief already.", "severity": "Medium", "days_ago": 90},
        {"title": "Back feeling better", "content": "PT exercises are helping. Pain down to 3/10. Can sit for longer periods now.", "severity": "Low", "days_ago": 80},
        
        {"title": "Itchy rash on forearms", "content": "Red, itchy patches appeared overnight. Maybe new laundry detergent?", "severity": "Medium", "days_ago": 72},
        {"title": "Rash spreading", "content": "Rash now on both arms and chest. Very itchy. Appointment with dermatologist tomorrow.", "severity": "High", "days_ago": 71},
        {"title": "Cream helping", "content": "Hydrocortisone cream from doctor is working. Rash fading and less itchy.", "severity": "Low", "days_ago": 68},
        
        {"title": "Sneezing all morning", "content": "Seasonal allergies are back. Constant sneezing, runny nose, itchy eyes.", "severity": "Medium", "days_ago": 50},
        {"title": "Allergy symptoms persist", "content": "Still sneezing a lot. Eyes watery. Pollen count must be high.", "severity": "Medium", "days_ago": 48},
        {"title": "Allergies under control", "content": "New allergy medication working well. Minimal symptoms now.", "severity": "Low", "days_ago": 42},
        
        {"title": "Bad headache", "content": "Woke up with throbbing headache on right side. Light sensitivity. Possible migraine.", "severity": "High", "days_ago": 22},
        {"title": "Migraine with aura", "content": "Visual disturbances before headache. Took prescribed medication. Resting in dark room.", "severity": "High", "days_ago": 21},
        {"title": "Headache improving", "content": "Sumatriptan helped. Headache down to dull ache. Able to eat light meal.", "severity": "Low", "days_ago": 20},
        
        {"title": "Mild headache today", "content": "Tension headache from work stress. Taking breaks and staying hydrated.", "severity": "Low", "days_ago": 10},
        {"title": "Feeling great!", "content": "No symptoms today. Energy is good. Maintaining healthy habits.", "severity": "Low", "days_ago": 3},
        {"title": "Regular check-in", "content": "Overall health stable. Exercising 4x week, eating well, sleeping 7-8 hours.", "severity": "Low", "days_ago": 1},
    ]
    
    for entry_data in journal_entries_data:
        journal = JournalEntry(
            title=entry_data["title"],
            content=entry_data["content"],
            severity=entry_data["severity"],
            created_at=end_date - timedelta(days=entry_data["days_ago"]),
            author=user
        )
        db.session.add(journal)
    
    print(f"✓ Created {len(journal_entries_data)} journal entries")

    # --- Create Medications ---
    medications_data = [
        {"name": "Cetirizine (Zyrtec)", "dosage": "10mg", "frequency": "Once daily in the morning", "notes": "For seasonal allergies. Take with or without food."},
        {"name": "Fluticasone Nasal Spray", "dosage": "2 sprays each nostril", "frequency": "Once daily", "notes": "For allergy symptoms. Use consistently for best results."},
        {"name": "Ibuprofen", "dosage": "400mg", "frequency": "As needed (max 3x daily)", "notes": "For back pain and inflammation. Take with food."},
        {"name": "Sumatriptan", "dosage": "50mg", "frequency": "As needed for migraine", "notes": "Take at first sign of migraine. Max 2 doses per 24 hours."},
        {"name": "Hydrocortisone Cream 1%", "dosage": "Topical", "frequency": "Apply twice daily", "notes": "For skin rash. Apply thin layer to affected areas."},
    ]
    
    for med_data in medications_data:
        medication = Medication(
            name=med_data["name"],
            dosage=med_data["dosage"],
            frequency=med_data["frequency"],
            notes=med_data["notes"],
            patient=user
        )
        db.session.add(medication)
    
    print(f"✓ Created {len(medications_data)} medications")

    # Finalize all the changes
    db.session.commit()
    
    print("\n✅ Database has been seeded with comprehensive demo data!")
    print(f"📅 Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"👤 Login with: demo@example.com / demo123")
    print(f"\n📊 Summary:")
    print(f"   - {len(created_visits)} doctor visits")
    print(f"   - {len(journal_entries_data)} journal entries (symptom logs)")
    print(f"   - {len(medications_data)} current medications")
    print("\n💡 Try generating a report for different date ranges to test the AI summary!") 