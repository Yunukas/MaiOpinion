"""
Agent 4: Follow-Up Agent
Generates follow-up care plans and patient instructions
Handles email preferences and patient data storage
"""

import json
import os
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def safe_print(message: str):
    """Safely print message, handling Unicode encoding issues on Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII if console can't handle Unicode
        print(message.encode('ascii', errors='replace').decode('ascii'))


class FollowUpAgent:
    """
    Follow-Up Agent - Creates care schedules, patient instructions, and email follow-ups
    """
    
    def __init__(self):
        self.name = "Follow-Up Agent"
        self.client = self._initialize_client()
        self.db_path = Path("patients_db.csv")
        self._initialize_database()
        
    def _initialize_client(self):
        """Initialize OpenAI client (GitHub Models, Azure OpenAI, or OpenAI)"""
        # Try GitHub Models first - check both .env and system environment
        github_token = os.getenv("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
        use_github = os.getenv("USE_GITHUB_MODELS", "false").lower() == "true"
        
        if github_token and use_github and github_token != "your_github_token_here":
            print(f"[{self.name}] Using GitHub Models (token: {github_token[:10]}...)")
            return OpenAI(
                api_key=github_token,
                base_url="https://models.inference.ai.azure.com"
            )
        
        # Try Azure OpenAI
        azure_key = os.getenv("AZURE_OPENAI_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_key and azure_endpoint:
            print(f"[{self.name}] Using Azure OpenAI")
            return AzureOpenAI(
                api_key=azure_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=azure_endpoint
            )
        
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            print(f"[{self.name}] Using OpenAI")
            return OpenAI(api_key=openai_key)
        
        print(f"[{self.name}] WARNING: No API keys found, using mock responses")
        return None
    
    def _initialize_database(self):
        """Initialize CSV database if it doesn't exist"""
        if not self.db_path.exists():
            with open(self.db_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'patient_id', 'timestamp', 'email', 'condition', 
                    'diagnosis', 'treatment', 'follow_up_timeline', 
                    'follow_up_date', 'email_sent', 'created_at'
                ])
            print(f"[{self.name}] Created patient database: {self.db_path}")
    
    def save_patient_data(self, patient_email: str, condition: str, diagnosis: str, 
                         treatment: str, follow_up_timeline: str) -> str:
        """
        Save patient data to CSV database
        
        Args:
            patient_email: Patient's email address
            condition: Patient's condition
            diagnosis: Diagnosis from Clinical Reasoning Agent
            treatment: Treatment plan
            follow_up_timeline: Follow-up schedule (e.g., "7 days")
            
        Returns:
            str: Generated patient ID
        """
        # Generate patient ID
        timestamp = datetime.now()
        patient_id = f"PT{timestamp.strftime('%Y%m%d%H%M%S')}"
        
        # Calculate follow-up date
        days = self._parse_timeline_days(follow_up_timeline)
        follow_up_date = (timestamp + timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Save to CSV
        with open(self.db_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                patient_id,
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                patient_email,
                condition,
                diagnosis,
                treatment,
                follow_up_timeline,
                follow_up_date,
                'No',  # email_sent
                timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        print(f"[{self.name}] Saved patient data: {patient_id} ({patient_email})")
        return patient_id
    
    def _parse_timeline_days(self, timeline: str) -> int:
        """Parse timeline string to extract number of days"""
        import re
        # Extract first number from timeline string
        match = re.search(r'(\d+)', timeline)
        if match:
            return int(match.group(1))
        return 7  # Default to 7 days
    
    def process(self, treatment_data: dict, diagnosis_data: dict = None, 
                patient_email: str = None, condition: str = None) -> dict:
        """
        Generate follow-up care plan and optionally register patient for email follow-ups
        
        Args:
            treatment_data: Output from Treatment Agent
            diagnosis_data: Optional diagnosis context
            patient_email: Optional patient email for follow-up emails
            condition: Patient's original condition/symptoms
            
        Returns:
            dict: JSON with follow-up schedule and patient notes
        """
        print(f"[{self.name}] Creating follow-up care plan...")
        
        treatment = treatment_data.get("treatment", "Standard care")
        diagnosis = diagnosis_data.get("diagnosis", "General condition") if diagnosis_data else "General condition"
        
        if self.client:
            followup_result = self._llm_followup(diagnosis, treatment)
        else:
            followup_result = self._mock_followup(diagnosis, treatment)
        
        # Save patient data if email provided
        patient_id = None
        if patient_email and condition:
            patient_id = self.save_patient_data(
                patient_email=patient_email,
                condition=condition,
                diagnosis=diagnosis,
                treatment=treatment,
                follow_up_timeline=followup_result.get("timeline", "7 days")
            )
        
        result = {
            "follow_up": followup_result["follow_up"],
            "timeline": followup_result.get("timeline", "7 days"),
            "patient_instructions": followup_result.get("patient_instructions", "Follow treatment plan as prescribed"),
            "patient_id": patient_id,
            "email_registered": patient_email is not None,
            "agent": self.name
        }
        
        if patient_email:
            result["registered_email"] = patient_email
            print(f"[{self.name}] [OK] Patient registered for email follow-ups: {patient_email}")
        
        print(f"[{self.name}] Follow-up: {result['follow_up']}")
        return result
    
    def _llm_followup(self, diagnosis: str, treatment: str) -> dict:
        """Use LLM to generate follow-up plan"""
        prompt = f"""You are a care coordinator. Create a follow-up plan for the patient.

Diagnosis: {diagnosis}
Treatment Plan: {treatment}

Provide your response in JSON format with these exact keys:
- follow_up: Main follow-up recommendation (1-2 sentences about when and why to follow up)
- timeline: Specific timeframe (e.g., "7 days", "2 weeks", "3-5 days")
- patient_instructions: Encouraging and supportive message for patient (1-2 sentences)

Be supportive and clear. Respond ONLY with valid JSON, no other text."""

        try:
            if isinstance(self.client, AzureOpenAI):
                model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
            else:
                # For GitHub Models and OpenAI
                model = os.getenv("GITHUB_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a care coordinator. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=200
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean up markdown if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"[{self.name}] LLM call failed: {e}")
            return self._mock_followup(diagnosis, treatment)
    
    def _mock_followup(self, diagnosis: str, treatment: str) -> dict:
        """Fallback mock follow-up recommendations"""
        diagnosis_lower = diagnosis.lower()
        
        if "dental" in diagnosis_lower or "caries" in diagnosis_lower:
            return {
                "follow_up": "Schedule dental check-up within 7 days to assess pain reduction and treatment effectiveness.",
                "timeline": "7 days",
                "patient_instructions": "Rinse with warm salt water twice daily and monitor pain levels. Contact your dentist immediately if pain worsens or swelling occurs."
            }
        elif "fracture" in diagnosis_lower:
            return {
                "follow_up": "Follow up with orthopedic specialist in 2 weeks for healing assessment and potential imaging.",
                "timeline": "2 weeks",
                "patient_instructions": "Rest and immobilize the affected area. Track healing progress and report any increased pain, numbness, or discoloration."
            }
        elif "dermatological" in diagnosis_lower or "skin" in diagnosis_lower:
            return {
                "follow_up": "Dermatology appointment recommended within 10-14 days to evaluate treatment response.",
                "timeline": "10-14 days",
                "patient_instructions": "Monitor the affected area daily for changes. Take photos to track progression and avoid known irritants."
            }
        else:
            return {
                "follow_up": "Specialist consultation recommended within 5-7 days for comprehensive evaluation.",
                "timeline": "5-7 days",
                "patient_instructions": "Keep a symptom diary and note any changes. Seek immediate medical attention if symptoms worsen significantly."
            }
    
    def validate_output(self, output: dict) -> bool:
        """Validate output structure"""
        required_keys = ["follow_up", "agent"]
        return all(key in output for key in required_keys)


    
    def send_follow_up_emails(self):
        """
        Send follow-up emails to patients based on their schedule
        Checks patients_db.csv and sends emails to those due for follow-up
        """
        if not self.db_path.exists():
            print(f"[{self.name}] No patient database found")
            return
        
        today = datetime.now().date()
        emails_sent = 0
        
        # Read all patients
        with open(self.db_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            patients = list(reader)
        
        # Check each patient
        for patient in patients:
            if patient['email_sent'] == 'Yes':
                continue  # Already sent
            
            follow_up_date = datetime.strptime(patient['follow_up_date'], '%Y-%m-%d').date()
            
            # Send email if follow-up date has arrived
            if today >= follow_up_date:
                success = self._send_email(
                    to_email=patient['email'],
                    patient_id=patient['patient_id'],
                    condition=patient['condition'],
                    diagnosis=patient['diagnosis'],
                    treatment=patient['treatment'],
                    follow_up_timeline=patient['follow_up_timeline']
                )
                
                if success:
                    # Mark as sent
                    patient['email_sent'] = 'Yes'
                    emails_sent += 1
        
        # Write back updated data
        if emails_sent > 0:
            with open(self.db_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['patient_id', 'timestamp', 'email', 'condition', 
                            'diagnosis', 'treatment', 'follow_up_timeline', 
                            'follow_up_date', 'email_sent', 'created_at']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(patients)
        
        print(f"[{self.name}] Follow-up emails sent: {emails_sent}")
        return emails_sent
    
    def _send_email(self, to_email: str, patient_id: str, condition: str, 
                    diagnosis: str, treatment: str, follow_up_timeline: str) -> bool:
        """
        Send follow-up email to patient
        For now, simulates email sending by printing the content
        TODO: Integrate with actual email service (SendGrid, AWS SES, etc.)
        """
        email_content = f"""
{'='*80}
[FOLLOW-UP EMAIL]
{'='*80}

To: {to_email}
From: MaiOpinion Healthcare Assistant
Subject: Your Follow-Up Reminder - Patient ID: {patient_id}

Dear Patient,

This is a friendly reminder about your healthcare follow-up based on your 
recent consultation with MaiOpinion.

Original Condition: {condition}
Diagnosis: {diagnosis}
Recommended Timeline: {follow_up_timeline}

Treatment Plan:
{treatment}

Next Steps:
- Please schedule an appointment with your healthcare provider
- Continue following the treatment recommendations
- Monitor your symptoms and report any changes

If you have any concerns or your symptoms have worsened, please seek 
medical attention immediately.

Stay healthy!
MaiOpinion Healthcare Team

{'='*80}
        """
        
        safe_print(email_content)
        
        # TODO: Replace with actual email sending
        # import smtplib
        # from email.mime.text import MIMEText
        # msg = MIMEText(email_content)
        # msg['To'] = to_email
        # msg['From'] = 'noreply@maiopinion.com'
        # msg['Subject'] = f'Your Follow-Up Reminder - Patient ID: {patient_id}'
        # ... send email
        
        return True  # Simulate successful send


# Test the agent if run directly
if __name__ == "__main__":
    agent = FollowUpAgent()
    treatment_data = {
        "treatment": "Dental filling recommended; use fluoride toothpaste",
        "agent": "Treatment Agent"
    }
    diagnosis_data = {
        "diagnosis": "Dental caries (early stage)",
        "confidence": "high"
    }
    
    # Test with email registration
    result = agent.process(
        treatment_data, 
        diagnosis_data,
        patient_email="patient@example.com",
        condition="Tooth pain for 3 days"
    )
    print("\nAgent Output:")
    print(json.dumps(result, indent=2))
    
    # Test sending follow-up emails
    print("\n" + "="*80)
    print("Testing Follow-Up Email System")
    print("="*80)
    agent.send_follow_up_emails()
