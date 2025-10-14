# 🚀 MaiOpinion - Quick Reference Card

## ⚡ Most Common Commands

### Run Diagnosis with Email Follow-Up
```bash
python main.py -i patient.png -c "Condition description" -e patient@email.com --no-prompt
```

### Send Scheduled Follow-Up Emails
```bash
python send_followups.py
```

### View All Patients
```bash
python manage_db.py --list
```

### View Database Statistics
```bash
python manage_db.py --stats
```

---

## 📋 Command-Line Arguments

### main.py
| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--image` | `-i` | Medical image path | `-i patient.png` |
| `--condition` | `-c` | Patient symptoms | `-c "Tooth pain"` |
| `--email` | `-e` | Patient email | `-e user@email.com` |
| `--save` | `-s` | Save JSON report | `--save` |
| `--output` | `-o` | Custom output file | `-o report.json` |
| `--no-prompt` | | Skip email prompt | `--no-prompt` |

### send_followups.py
| Argument | Short | Description |
|----------|-------|-------------|
| `--view` | `-v` | View patient database |
| `--no-send` | | Skip sending emails |

### manage_db.py
| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--list` | `-l` | List all patients | `--list` |
| `--stats` | `-s` | Show statistics | `--stats` |
| `--view` | `-v` | View patient details | `--view PT12345` |
| `--export` | `-e` | Export database | `--export backup.csv` |
| `--clear` | | Clear database | `--clear` |

---

## 📧 Email Workflow

### 1. Patient Registration
```bash
# Method 1: Interactive
python main.py -i patient.png -c "Condition"
# You'll be asked: "Would you like follow-up reminders?"

# Method 2: CLI with prompt
python main.py -i patient.png -c "Condition" -e user@email.com

# Method 3: CLI without prompt (automated)
python main.py -i patient.png -c "Condition" -e user@email.com --no-prompt
```

### 2. Check Registered Patients
```bash
# View all patients
python send_followups.py --view --no-send

# Or use database manager
python manage_db.py --list
```

### 3. Send Follow-Up Emails
```bash
# Send all scheduled emails
python send_followups.py

# View patients without sending
python send_followups.py --view --no-send
```

---

## 🗂️ Database Schema

**File**: `patients_db.csv`

| Column | Example | Description |
|--------|---------|-------------|
| `patient_id` | PT20251014140551 | Unique ID |
| `timestamp` | 2025-10-14 14:05:51 | Registration time |
| `email` | patient@email.com | Patient email |
| `condition` | Tooth pain | Original complaint |
| `diagnosis` | Dental caries | AI diagnosis |
| `treatment` | Dental filling... | Treatment plan |
| `follow_up_timeline` | 2 weeks | Timeline text |
| `follow_up_date` | 2025-10-28 | Scheduled date |
| `email_sent` | Yes/No | Email status |
| `created_at` | 2025-10-14 14:05:51 | Creation time |

---

## 🔧 Environment Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Edit .env file
GITHUB_TOKEN=your_github_token_here
```

### 3. Test the System
```bash
python test_email_system.py
```

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Main documentation |
| **EMAIL_SYSTEM.md** | Complete email guide (500+ lines) |
| **EMAIL_IMPLEMENTATION.md** | Implementation details |
| **COMPLETE.md** | Completion summary |
| **PROJECT_STRUCTURE.md** | Project organization |
| **QUICKSTART.md** | Quick start guide |
| **ARCHITECTURE.md** | System architecture |

---

## 🎯 Example Workflows

### Dental Clinic Workflow
```bash
# 1. Patient comes in with tooth pain
python main.py -i dental-xray.png -c "Tooth pain 3 days" -e patient@email.com --no-prompt

# 2. System registers patient and schedules 2-week follow-up

# 3. Two weeks later, automated email reminder
python send_followups.py

# 4. View patient history
python manage_db.py --view PT20251014140551
```

### Batch Processing
```bash
# Process multiple patients
python main.py -i patient1.png -c "Condition 1" -e email1@test.com --no-prompt
python main.py -i patient2.png -c "Condition 2" -e email2@test.com --no-prompt
python main.py -i patient3.png -c "Condition 3" -e email3@test.com --no-prompt

# View all patients
python manage_db.py --list

# Show statistics
python manage_db.py --stats
```

---

## 🔐 Production Setup

### Enable Real Email Sending

**Step 1**: Choose SMTP service
- SendGrid (recommended for hackathons)
- AWS SES (production)
- Mailgun
- Gmail SMTP

**Step 2**: Update code
```python
# In agents/followup.py → _send_email()
import smtplib
from email.mime.text import MIMEText

msg = MIMEText(email_body)
msg['Subject'] = 'Your Follow-Up Reminder'
msg['From'] = 'noreply@maiopinion.com'
msg['To'] = patient_data['email']

with smtplib.SMTP('smtp.sendgrid.net', 587) as server:
    server.starttls()
    server.login('apikey', os.getenv('SENDGRID_API_KEY'))
    server.send_message(msg)
```

**Step 3**: Schedule automated sending
```bash
# Windows
schtasks /create /tn "MaiOpinion" /tr "python send_followups.py" /sc daily /st 09:00

# Linux/Mac
0 9 * * * cd /path/to/MaiOpinion && python send_followups.py
```

---

## 🧪 Testing Commands

```bash
# Full test suite
python test_email_system.py

# Test patient registration
python main.py -i sample_data/patient1.png -c "Test" -e test@email.com --no-prompt

# Test database viewing
python manage_db.py --list

# Test email scheduler
python send_followups.py --view --no-send
```

---

## 🆘 Troubleshooting

### "No patient database found"
```bash
# Create database by registering a patient
python main.py -i sample_data/patient1.png -c "Test" -e test@email.com --no-prompt
```

### View patient details
```bash
# Get patient ID from list
python manage_db.py --list

# View specific patient
python manage_db.py --view PT20251014140551
```

### Export database backup
```bash
python manage_db.py --export backup-$(date +%Y%m%d).csv
```

---

## 📊 Statistics & Metrics

```bash
# Quick overview
python manage_db.py --stats
```

**Output:**
- Total Patients
- Emails Sent
- Pending Emails
- Overdue Follow-ups
- Upcoming Follow-ups

---

## 🎯 Hackathon Demo Checklist

- [ ] Run test suite: `python test_email_system.py`
- [ ] Register test patient: `python main.py -i sample_data/patient1.png -c "Demo" -e demo@test.com --no-prompt`
- [ ] Show database: `python manage_db.py --list`
- [ ] Show statistics: `python manage_db.py --stats`
- [ ] Simulate email: `python send_followups.py`
- [ ] Show documentation: Open `EMAIL_SYSTEM.md`

---

## 💡 Pro Tips

1. **Use --no-prompt** for automated workflows
2. **Export backups regularly** with `--export`
3. **Check stats daily** with `--stats`
4. **View emails before sending** with `--view --no-send`
5. **Read EMAIL_SYSTEM.md** for complete guide

---

## 📞 Quick Help

```bash
# Get help for any command
python main.py --help
python send_followups.py --help
python manage_db.py --help
```

---

**Print this card for quick reference during development! 📄**
