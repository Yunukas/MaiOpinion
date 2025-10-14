# Follow-Up Email System - How It Works

## Overview
The follow-up email system in MaiOpinion tracks patient diagnoses and automatically sends reminder emails based on recommended follow-up timelines.

## 🔄 System Architecture

```
Patient Submission
       ↓
Follow-Up Agent
       ↓
Save to patients_db.csv
       ↓
Scheduled Email Checker
       ↓
Send Email (when due)
```

## 📊 Patient Database

### Location
`patients_db.csv` - CSV database storing patient information

### Schema
```csv
patient_id,timestamp,email,condition,diagnosis,treatment,follow_up_timeline,follow_up_date,email_sent,created_at
```

**Fields:**
- `patient_id` - Unique ID (format: PT{YYYYMMDDHHmmSS})
- `timestamp` - When diagnosis was created
- `email` - Patient's email address
- `condition` - Original symptoms/complaint
- `diagnosis` - Clinical diagnosis
- `treatment` - Treatment plan
- `follow_up_timeline` - Human-readable (e.g., "7 days", "2 weeks")
- `follow_up_date` - Calculated date (YYYY-MM-DD)
- `email_sent` - "Yes" or "No" (tracking status)
- `created_at` - Record creation timestamp

### Example Entry
```csv
PT20251014141333,2025-10-14 14:13:33,test-patient@example.com,Severe chest pain for 3 days,Acute coronary syndrome,"Initiate dual antiplatelet therapy...",7 days,2025-10-21,No,2025-10-14 14:13:33
```

## 🎯 How It Works - Step by Step

### Step 1: Patient Provides Email (Optional)

**Web Interface:**
```jsx
// User toggles checkbox in frontend
<EmailInput 
  enabled={enableEmail}
  email={email}
  onToggle={setEnableEmail}
  onChange={setEmail}
/>
```

**CLI:**
```bash
python main.py -i image.png -c "symptoms" -e patient@email.com
```

### Step 2: Follow-Up Agent Processing

When the diagnostic pipeline runs, the **Follow-Up Agent** (step 5):

```python
# In agents/followup.py - process() method
def process(self, treatment_data, diagnosis_data, patient_email=None, condition=None):
    # Generate follow-up plan
    followup_result = self._llm_followup(diagnosis, treatment)
    
    # If email provided, save to database
    if patient_email and condition:
        patient_id = self.save_patient_data(
            patient_email=patient_email,
            condition=condition,
            diagnosis=diagnosis,
            treatment=treatment,
            follow_up_timeline=followup_result.get("timeline", "7 days")
        )
```

### Step 3: Data Storage

```python
def save_patient_data(self, patient_email, condition, diagnosis, treatment, follow_up_timeline):
    # Generate unique patient ID
    timestamp = datetime.now()
    patient_id = f"PT{timestamp.strftime('%Y%m%d%H%M%S')}"
    
    # Calculate follow-up date from timeline
    days = self._parse_timeline_days(follow_up_timeline)  # "7 days" → 7
    follow_up_date = (timestamp + timedelta(days=days)).strftime('%Y-%m-%d')
    
    # Save to CSV with UTF-8 encoding
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
            'No',  # email_sent - not sent yet
            timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])
```

### Step 4: Timeline Parsing

The agent intelligently extracts days from timeline strings:

```python
def _parse_timeline_days(self, timeline: str) -> int:
    """Parse timeline string to extract number of days"""
    # "7 days" → 7
    # "2 weeks" → 14
    # "3-5 days" → 3
    # "1 month" → 30
    
    if 'week' in timeline.lower():
        return int(re.search(r'\d+', timeline).group()) * 7
    elif 'month' in timeline.lower():
        return int(re.search(r'\d+', timeline).group()) * 30
    else:
        return int(re.search(r'\d+', timeline).group())
```

### Step 5: Scheduled Email Sending

The system has a method to send emails when they're due:

```python
def send_follow_up_emails(self):
    """Send emails to patients whose follow-up date has arrived"""
    today = datetime.now().date()
    
    # Read all patients from CSV
    with open(self.db_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        patients = list(reader)
    
    # Check each patient
    for patient in patients:
        if patient['email_sent'] == 'Yes':
            continue  # Skip already sent
        
        follow_up_date = datetime.strptime(patient['follow_up_date'], '%Y-%m-%d').date()
        
        # Send if date has arrived
        if today >= follow_up_date:
            self._send_email(
                to_email=patient['email'],
                patient_id=patient['patient_id'],
                condition=patient['condition'],
                diagnosis=patient['diagnosis'],
                treatment=patient['treatment'],
                follow_up_timeline=patient['follow_up_timeline']
            )
            
            # Mark as sent
            patient['email_sent'] = 'Yes'
    
    # Update CSV with sent status
    writer.writerows(patients)
```

### Step 6: Email Content

Currently **simulated** (prints to console):

```
================================================================================
[FOLLOW-UP EMAIL]
================================================================================

To: patient@email.com
From: MaiOpinion Healthcare Assistant
Subject: Your Follow-Up Reminder - Patient ID: PT20251014141333

Dear Patient,

This is a friendly reminder about your healthcare follow-up based on your 
recent consultation with MaiOpinion.

Original Condition: Severe chest pain for 3 days
Diagnosis: Acute coronary syndrome
Recommended Timeline: 7 days

Treatment Plan:
Initiate dual antiplatelet therapy...

Next Steps:
- Please schedule an appointment with your healthcare provider
- Continue following the treatment recommendations
- Monitor your symptoms and report any changes

If you have any concerns or your symptoms have worsened, please seek 
medical attention immediately.

Stay healthy!
MaiOpinion Healthcare Team
================================================================================
```

## 🚀 Usage Examples

### Example 1: Web Interface
1. Upload medical image
2. Enter symptoms: "Chest pain for 3 days"
3. Toggle "Send follow-up reminders" ✓
4. Enter email: "patient@email.com"
5. Submit
6. **Result:** Patient saved to database, email scheduled for 7 days

### Example 2: CLI
```bash
python main.py -i chest_xray.png -c "Chest pain" -e patient@email.com
```
**Result:** Same as above

### Example 3: Check Pending Emails
```python
from agents.followup import FollowUpAgent

agent = FollowUpAgent()
agent.send_follow_up_emails()  # Sends all due emails
```

## ⚙️ Current Status: SIMULATION MODE

### What Works Now
✅ Patient data saved to CSV  
✅ Follow-up dates calculated  
✅ Email content generated  
✅ Email printed to console  
✅ Email status tracked (Yes/No)  

### What's NOT Implemented Yet
❌ Actual email sending (SMTP/API)  
❌ Scheduled background job (cron/task scheduler)  
❌ Email service integration (SendGrid, AWS SES)  
❌ Automated trigger system  

## 🔧 Enabling Real Email Sending

To enable actual email sending, you would need to:

### Option 1: SMTP (Gmail, Outlook)
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def _send_email(self, to_email, ...):
    msg = MIMEMultipart()
    msg['From'] = 'noreply@maiopinion.com'
    msg['To'] = to_email
    msg['Subject'] = f'Follow-Up Reminder - {patient_id}'
    
    msg.attach(MIMEText(email_content, 'plain'))
    
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    
    return True
```

### Option 2: SendGrid API
```python
import sendgrid
from sendgrid.helpers.mail import Mail

def _send_email(self, to_email, ...):
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    
    message = Mail(
        from_email='noreply@maiopinion.com',
        to_emails=to_email,
        subject=f'Follow-Up Reminder - {patient_id}',
        plain_text_content=email_content
    )
    
    response = sg.send(message)
    return response.status_code == 202
```

### Option 3: AWS SES
```python
import boto3

def _send_email(self, to_email, ...):
    ses = boto3.client('ses', region_name='us-east-1')
    
    response = ses.send_email(
        Source='noreply@maiopinion.com',
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': f'Follow-Up Reminder - {patient_id}'},
            'Body': {'Text': {'Data': email_content}}
        }
    )
    
    return response['ResponseMetadata']['HTTPStatusCode'] == 200
```

## 🕐 Setting Up Scheduled Sending

### Windows Task Scheduler
```powershell
# Create a scheduled task to run daily
$action = New-ScheduledTaskAction -Execute 'python' -Argument 'send_emails.py'
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "MaiOpinion-EmailReminders"
```

### Cron (Linux/Mac)
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/MaiOpinion && python send_emails.py
```

### Create `send_emails.py`
```python
from agents.followup import FollowUpAgent

if __name__ == "__main__":
    agent = FollowUpAgent()
    count = agent.send_follow_up_emails()
    print(f"Sent {count} follow-up emails")
```

## 📈 Database Management

### View All Patients
```python
import csv

with open('patients_db.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for patient in reader:
        print(f"{patient['patient_id']}: {patient['email']} - Due: {patient['follow_up_date']}")
```

### Check Pending Emails
```python
from datetime import datetime

with open('patients_db.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    today = datetime.now().date()
    
    for patient in reader:
        if patient['email_sent'] == 'No':
            due_date = datetime.strptime(patient['follow_up_date'], '%Y-%m-%d').date()
            if today >= due_date:
                print(f"OVERDUE: {patient['email']} - {patient['condition']}")
```

## 🔒 Privacy & Security Notes

⚠️ **Important Considerations:**

1. **HIPAA Compliance**: Current implementation is NOT HIPAA compliant
2. **Encryption**: Patient data stored in plain text CSV
3. **Email Security**: No encryption for email content
4. **Authentication**: No patient authentication system

**For Production:**
- Encrypt database (SQLite with encryption, PostgreSQL)
- Use secure email services with TLS
- Implement patient authentication
- Add consent management
- Include opt-out mechanisms
- Follow healthcare data regulations

## 🎓 Summary

The follow-up email system:
1. ✅ Captures patient email during diagnosis
2. ✅ Stores patient data in CSV database
3. ✅ Calculates follow-up dates from timeline
4. ✅ Generates personalized email content
5. ⏳ **Currently simulates sending** (prints to console)
6. ⏳ Requires integration for real email delivery
7. ⏳ Needs scheduled job for automated sending

**Current State:** Fully functional for demo/educational purposes  
**Production Ready:** Requires email service integration and scheduling
