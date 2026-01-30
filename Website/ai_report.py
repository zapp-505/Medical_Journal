from .models import JournalEntry, Medication, Visit
from datetime import datetime
from flask import current_app
from google import genai
from google.genai import types
import os 

class ReportGenerator:
    def __init__(self,user_id):
        self.id=user_id


    def fetch_data(self,start,end):

        j_list=[]
        journals =JournalEntry.query.filter(JournalEntry.user_id==self.id,JournalEntry.created_at.between(start,end)).all()

        for journal in journals:
            j_list.append(f"{journal.created_at.strftime('%Y-%m-%d')}: {journal.content}. {journal.severity}")

        if not j_list:
            journal_details = "No symptom logs found for this specific period."
        else:
            journal_details = "### RECENT SYMPTOMS\n"+"\n".join(j_list)

        
        v_list=[]
        visits= Visit.query.filter(Visit.user_id==self.id).all()
        
        for visit in visits:
            v_list.append(f"{visit.visit_date.strftime('%Y-%m-%d')}: {visit.reason}.  {visit.diagnosis}")

        if not v_list:
            visit_details = "No visits found."
        else:
            visit_details = "### CLINICAL HISTORY\n" + "\n".join(v_list)

        m_list=[]
        medications = Medication.query.filter(Medication.user_id==self.id).all()

        for medicine in medications:
            m_list.append(f"{medicine.name}  {medicine.dosage}")

        if not m_list:
            medication_details = "No medications found."
        else:
            medication_details = "### CURRENT MEDICATIONS\n" +"\n".join(m_list)

        return [journal_details, visit_details, medication_details]
    


    def generate_summary(self,raw_data_list):
        journals, visits, meds = raw_data_list

        api_key = current_app.config['GEMINI_API_KEY']
        client = genai.Client(api_key=api_key)

        prompt = f"""You are an expert Medical Documentation Specialist creating a pre-consultation brief for a physician.

## PATIENT DATA PROVIDED:

### Recent Symptom Logs (Patient-Reported):
{journals}

### Clinical Visit History:
{visits}

### Current Medications:
{meds}

---

## YOUR TASK:
Create a concise, scannable consultation brief using the SOAP format. The doctor should be able to read and understand this in under 60 seconds.

## OUTPUT FORMAT (Use Markdown):

## Chief Concerns
*Provide a 2-3 sentence overview of the most pressing issues from recent logs. Use bullet points for multiple concerns.*

---

## Subjective (Patient Narrative)
**Recent Symptoms:**
- Use bullet points for each distinct symptom cluster
- Include dates, severity levels, and progression
- Group related symptoms together
- Format: `[Date]: Symptom description (Severity: High/Medium/Low)`

**Patient Context:**
- Briefly note any patterns in timing, triggers, or frequency
- Keep each point to one line

---

## Objective (Clinical Data)

**Current Medications:**
- Medication Name, Dosage, Frequency
- Note purpose if relevant (e.g., "for allergies")

**Recent Clinical Findings:**
- Extract key vitals, lab results, or diagnoses from visit history
- Use bullet format with dates
- Include only objective measurements, not subjective notes

---

## Assessment (Clinical History & Patterns)

**Historical Context:**
- Summarize relevant past conditions in chronological order
- Note resolution status of previous issues

**Observed Patterns:**
- Identify correlations between symptoms and history
- Note any recurring issues or trends
- Highlight gaps in information that may need clarification

---

## Plan (Physician Discussion Points)

**Recommended Questions for Patient:**
1. [Specific question based on symptom progression or gaps in data]
2. [Question about medication adherence or effectiveness]
3. [Question to clarify inconsistencies or explore new symptoms]

**Considerations:**
- Note any red flags requiring immediate attention
- Suggest areas that may benefit from further evaluation

---

## CRITICAL GUIDELINES:
✓ Use clear headings and bullet points for scannability
✓ Keep sentences short and clinical (under 20 words each)
✓ Highlight dates and severity levels
✓ Use consistent formatting throughout
✓ Group related information together
✓ Maintain objective, clinical tone

✗ Do NOT diagnose - use "suggests," "consistent with," "may indicate"
✗ Do NOT add information not present in the data
✗ Do NOT use long paragraphs - break into bullets
✗ Do NOT include filler words or unnecessary elaboration

Remember: Clarity and scannability are paramount. The physician needs to grasp the patient's status at a glance."""
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"