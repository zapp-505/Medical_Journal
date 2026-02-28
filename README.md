# ?? My Health Journal

A personal health tracking web app built with Flask. Log symptoms, manage medications, record doctor visits, upload medical documents, and generate AI-powered pre-consultation reports using Google Gemini.

---

## Features

- ?? **Symptom Journal** � Log daily symptoms with severity levels (Low / Medium / High)
- ?? **Medication Tracker** � Track medications with dosage and frequency
- ?? **Doctor Visits** � Record visits and link related journal entries, medications, and documents to them
- ?? **Document Upload** � Upload and manage medical documents (PDF, JPG, PNG)
- ?? **AI Health Reports** � Generate SOAP-format consultation briefs powered by Google Gemini 2.5 Flash
- ?? **Global Search** � Search across all your health records at once
- ?? **User Profiles** � Manage account info and profile picture

---

## Tech Stack

- **Backend:** Python 3.10, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate
- **Database:** PostgreSQL
- **AI:** Google Gemini 2.5 Flash (`google-genai`)
- **Frontend:** Bootstrap 5, Jinja2, Font Awesome
- **Deployment:** Gunicorn, Heroku

---

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Steps

**1. Clone the repo**
```bash
git clone <repository-url>
cd Medical_Journal
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:
```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/medical_journal
GEMINI_API_KEY=your_gemini_api_key_here
```

**5. Run database migrations**
```bash
flask db upgrade
```

**6. Start the development server**
```bash
python app.py
```

App runs at `http://127.0.0.1:5000`

---

## Demo Data

To populate the app with 6 months of sample data:

```bash
python seed.py
```

Demo account credentials:
- **Email:** `demo@example.com`
- **Password:** `demo123`

---


## Project Structure

```
Medical_Journal/
+-- app.py              # Entry point
+-- config.py           # App configuration
+-- seed.py             # Demo data seeder
+-- requirements.txt
+-- migrations/         # Database migration files
+-- Website/
    +-- __init__.py     # App factory
    +-- models.py       # Database models
    +-- views.py        # Main routes
    +-- auth.py         # Auth routes
    +-- forms.py        # WTForms classes
    +-- ai_report.py    # Gemini AI integration
    +-- static/         # Uploaded files & profile pics
    +-- templates/      # Jinja2 HTML templates
```
