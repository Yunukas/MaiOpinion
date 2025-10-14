# 📧 Email Follow-Up System Documentation

## Overview

MaiOpinion's email follow-up system helps patients stay on track with their healthcare by sending automated reminders for scheduled check-ups and follow-up appointments.

## Features

✅ **Patient Email Registration** - Collect patient emails during diagnosis  
✅ **Local Database Storage** - CSV-based patient tracking  
✅ **Automated Scheduling** - Calculate follow-up dates from treatment timeline  
✅ **Email Automation** - Send reminders on scheduled dates  
✅ **CLI Integration** - Simple command-line interface  
✅ **Privacy First** - All data stored locally  

---

## How It Works

### 1. Patient Registration Flow

```
[Patient Diagnosis]
        ↓
[Email Preference Prompt] ← "Would you like follow-up reminders?"
        ↓
[Store Patient Data] ← Save to patients_db.csv
        ↓
[Calculate Follow-up Date] ← Based on treatment timeline
        ↓
[Email Scheduled] ← Ready for automated sending
```

### 2. Email Sending Flow

```
[Run send_followups.py]
        ↓
[Check patients_db.csv]
        ↓
[Find Patients Due Today]
        ↓
[Send Email Reminders]
        ↓
[Mark as Sent]
```

---

## Usage Guide

### Register Patient for Follow-Ups

**Method 1: Interactive Prompt** (Default)
```bash
python main.py -i patient.png -c "Tooth pain for 3 days"
```
You'll see:
```
Would you like to receive follow-up reminders via email? (yes/no): yes
Please enter your email address: patient@example.com
✅ Email registered for follow-up reminders!
```

**Method 2: Direct Email Argument**
```bash
python main.py -i patient.png -c "Tooth pain" -e patient@example.com
```
Still prompts for confirmation.

**Method 3: Non-Interactive (Skip Prompt)**
```bash
python main.py -i patient.png -c "Tooth pain" -e user@email.com --no-prompt
```
Directly registers email without asking.

### Send Follow-Up Emails

**Basic Usage**
```bash
python send_followups.py
```

**View Patient Database**
```bash
python send_followups.py --view
```

**View Without Sending**
```bash
python send_followups.py --view --no-send
```

---

## Database Structure

### `patients_db.csv` Schema

| Column | Type | Description |
|--------|------|-------------|
| `patient_id` | String | Unique identifier (UUID) |
| `timestamp` | DateTime | Registration timestamp |
| `email` | String | Patient email address |
| `condition` | String | Original patient complaint |
| `diagnosis` | String | AI-generated diagnosis |
| `treatment` | String | Recommended treatment plan |
| `follow_up_timeline` | String | Timeline text (e.g., "7 days") |
| `follow_up_date` | Date | Calculated follow-up date |
| `email_sent` | Boolean | Email delivery status |
| `created_at` | DateTime | Record creation timestamp |

### Example Database Entry

```csv
patient_id,timestamp,email,condition,diagnosis,treatment,follow_up_timeline,follow_up_date,email_sent,created_at
a1b2c3d4-...,2025-01-15 10:30:00,patient@example.com,Tooth pain for 3 days,Dental caries (early stage),Dental filling recommended; reduce sugar intake,Check-up in 7 days,2025-01-22,No,2025-01-15 10:30:00
```

---

## Email Template

### Follow-Up Reminder Email

```
Subject: 🏥 MaiOpinion - Your Follow-Up Reminder

Hello!

This is a friendly reminder about your scheduled follow-up appointment.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 APPOINTMENT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Original Condition: Tooth pain for 3 days
Diagnosis: Dental caries (early stage)

📅 Follow-up Date: 2025-01-22

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 TREATMENT REMINDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please continue following your treatment plan:
- Dental filling recommended
- Reduce sugar intake
- Use fluoride toothpaste

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you have any concerns or your symptoms have worsened,
please consult with a healthcare professional immediately.

Best regards,
MaiOpinion Healthcare Team
```

---

## Architecture

### Components

1. **Follow-Up Agent** (`agents/followup.py`)
   - `_initialize_database()` - Creates CSV if not exists
   - `save_patient_data()` - Stores patient information
   - `send_follow_up_emails()` - Checks and sends due emails
   - `_send_email()` - Email sending logic
   - `_parse_timeline_days()` - Extracts days from timeline text

2. **Main Orchestrator** (`main.py`)
   - `_ask_email_preference()` - Interactive email collection
   - `run_pipeline()` - Passes email through agent chain
   - CLI argument parsing for `--email` and `--no-prompt`

3. **Email Scheduler** (`send_followups.py`)
   - Standalone script for automated email sending
   - Can be run as a cron job
   - Includes patient database viewer

### Data Flow

```python
# Patient registers during diagnosis
main.py → run_pipeline(patient_email="user@email.com")
    ↓
agents/followup.py → process(patient_email="user@email.com")
    ↓
save_patient_data() → Append to patients_db.csv
    ↓
Calculate follow_up_date from treatment timeline
```

```python
# Automated email sending
send_followups.py → FollowUpAgent.send_follow_up_emails()
    ↓
Read patients_db.csv
    ↓
Filter: follow_up_date <= today AND email_sent == "No"
    ↓
For each patient: _send_email()
    ↓
Update email_sent = "Yes"
```

---

## Customization

### Change Email Template

Edit the template in `agents/followup.py` → `_send_email()` method:

```python
def _send_email(self, patient_data: dict) -> bool:
    """Send follow-up email to patient"""
    
    # TODO: Integrate with SMTP service (SendGrid, AWS SES, etc.)
    
    email_body = f"""
    Your custom email template here...
    """
    
    # Current: Prints to console
    # Future: Send via SMTP
    print(email_body)
```

### Add SMTP Integration

Replace the `TODO` section in `_send_email()`:

```python
import smtplib
from email.mime.text import MIMEText

def _send_email(self, patient_data: dict) -> bool:
    msg = MIMEText(email_body)
    msg['Subject'] = '🏥 MaiOpinion - Your Follow-Up Reminder'
    msg['From'] = 'noreply@maiopinion.com'
    msg['To'] = patient_data['email']
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.send_message(msg)
    
    return True
```

### Schedule Automated Sending

**Windows Task Scheduler**
```powershell
# Create scheduled task to run daily at 9 AM
schtasks /create /tn "MaiOpinion Email Reminders" /tr "python C:\path\to\send_followups.py" /sc daily /st 09:00
```

**Linux/Mac Cron Job**
```bash
# Add to crontab (run daily at 9 AM)
0 9 * * * cd /path/to/MaiOpinion && python send_followups.py >> logs/emails.log 2>&1
```

---

## Testing

### Test Email Registration

```bash
# Test with sample data
python main.py -i sample_data/patient1.png -c "Tooth pain" -e test@example.com --no-prompt
```

Expected output:
```
✅ Email registered for follow-up reminders!
✅ Patient data saved to database!
```

### Verify Database

```bash
python send_followups.py --view --no-send
```

Expected output:
```
👥 REGISTERED PATIENTS

Patient #1
  ID: a1b2c3d4-5e6f-7890-abcd-ef1234567890
  Email: test@example.com
  Condition: Tooth pain
  Diagnosis: Dental caries (early stage)
  Follow-up Date: 2025-01-22
  Email Sent: ❌ No
  Registered: 2025-01-15 10:30:00
```

### Test Email Sending

```bash
# Manually adjust follow_up_date in CSV to today's date
# Then run:
python send_followups.py
```

Expected output:
```
📧 Sending follow-up email to test@example.com...
[Email body preview]
✅ Email sent successfully!
```

---

## Security & Privacy

### Best Practices

✅ **Local Storage** - All patient data stored locally in CSV  
✅ **No Cloud Sync** - Data never leaves your machine  
✅ **Git Ignored** - `patients_db.csv` excluded from version control  
✅ **Email Validation** - Basic email format validation  

### HIPAA Compliance Considerations

⚠️ **Important**: This system is a **prototype** and not HIPAA-compliant out-of-the-box.

For production medical use, you need:
- [ ] Encrypted database (not CSV)
- [ ] Encrypted email transmission (TLS)
- [ ] Access logging and audit trails
- [ ] Patient consent forms
- [ ] Data retention policies
- [ ] Secure credential storage (not .env files)

---

## Troubleshooting

### "No patient database found"
**Solution**: Run a diagnosis with email registration first
```bash
python main.py -i sample.png -c "Test" -e test@email.com --no-prompt
```

### Emails not sending
**Solution**: Check console output - emails are currently simulated  
**Next Step**: Implement SMTP integration (see Customization section)

### Invalid email format
**Solution**: Email validation is basic - accepts `user@domain.com` format  
**Next Step**: Add stricter validation if needed

### Database corrupted
**Solution**: CSV is human-readable - open in Excel/text editor to fix  
**Backup**: Keep regular backups of `patients_db.csv`

---

## Future Enhancements

### Planned Features

- [ ] **SMTP Integration** - Real email sending via SendGrid/AWS SES
- [ ] **SMS Notifications** - Twilio integration for text reminders
- [ ] **Email Templates** - Multiple customizable templates
- [ ] **Unsubscribe Links** - Allow patients to opt-out
- [ ] **Reminder Series** - Multiple reminders (24hr, 1 week, etc.)
- [ ] **Email Analytics** - Track open rates and engagement
- [ ] **Web Dashboard** - View patient database in browser
- [ ] **Database Migration** - Move from CSV to SQLite/PostgreSQL

### Contributing

Want to add a feature? Fork the repo and submit a PR!

---

## API Reference

### FollowUpAgent Methods

```python
class FollowUpAgent:
    def _initialize_database(self) -> None:
        """Create patients_db.csv if not exists"""
    
    def save_patient_data(self, patient_email: str, condition: str, 
                         diagnosis: str, treatment: str, 
                         follow_up_timeline: str) -> bool:
        """Save patient data to database"""
    
    def send_follow_up_emails(self) -> int:
        """Send all scheduled follow-up emails. Returns count sent."""
    
    def _send_email(self, patient_data: dict) -> bool:
        """Send individual follow-up email"""
    
    def _parse_timeline_days(self, timeline: str) -> int:
        """Extract days from timeline string (e.g., "7 days" → 7)"""
```

### CLI Arguments

```python
# main.py
--email, -e          # Patient email address
--no-prompt          # Skip email preference prompt

# send_followups.py
--send               # Send scheduled emails (default)
--view, -v           # View patient database
--no-send            # Skip sending emails
```

---

## License

MIT License - See LICENSE file for details

---

## Support

Need help? Open an issue on GitHub!

**Happy Healthcare! 🏥💚**
