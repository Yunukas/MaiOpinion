# 🏥 MaiOpinion - Multi-Agent Healthcare Diagnostic Assistant

![Hackathon Project](https://img.shields.io/badge/Hackathon-2025-blue)
![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**MaiOpinion** is a lightweight, multi-agent AI system designed to assist with patient diagnosis and treatment planning through intelligent agent collaboration.

## Download and Run: 
.\start.ps1


## 🎯 Overview

MaiOpinion processes diagnostic images and patient condition descriptions through a chain of **five specialized AI agents**, with intelligent routing based on image type:

1. **Image Detection Agent** - Identifies image type (dental, chest X-ray, brain scan, etc.)
2. **Specialized Diagnostic Agents** - Routes to appropriate specialist:
   - **Dental Agent** - Dental X-rays and oral imaging
   - **Chest X-ray Agent** - Lung and respiratory imaging  
   - **Generic Agent** - Brain scans, skin lesions, bone X-rays, etc.
3. **Clinical Reasoning Agent** - Infers diagnosis from findings and symptoms
4. **Treatment Agent** - Suggests evidence-based treatment options
5. **Follow-Up Agent** - Generates care schedule and email reminders

## ✨ Features

- 🎯 **Detection-Based Routing** - Automatically routes to specialized diagnostic agents
- 🏥 **Medical Specialists** - Dental, chest X-ray, and generic diagnostic agents
- 🤖 **Multi-Agent Architecture** - Five specialized agents working in sequence
- 📧 **Email Follow-Ups** - Automated patient reminder system
- 🔗 **Agent Orchestration** - Seamless data flow between agents
- 🧠 **AI-Powered** - Uses GitHub Models / Azure OpenAI / OpenAI
- 📋 **Structured Output** - Clean JSON reports with detection metadata
- 🚀 **Fast Setup** - Built for hackathon speed
- 💻 **CLI Interface** - Simple command-line operation
- 🎨 **Mock Fallbacks** - Works without API keys for testing
- ⚡ **Scalable** - Easy to add new specialty agents

## 🏗️ Architecture

```
[User Input: Image + Condition]
         ↓
[Agent 1: Image Detection]
         ↓ Detects image type
    ┌────┴────┐
    │  Router │
    └────┬────┘
         ├─→ [Dental Agent] → Findings
         ├─→ [Chest X-ray Agent] → Findings
         └─→ [Generic Agent] → Findings
         ↓
[Agent 2: Clinical Reasoning]
         ↓ JSON diagnosis
[Agent 3: Treatment]
         ↓ JSON treatment plan
[Agent 4: Follow-Up + Email]
         ↓
[Final Report: Complete Diagnostic]
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- GitHub Token (FREE!) OR Azure OpenAI / OpenAI API key
- VS Code (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yunukas/MaiOpinion.git
   cd MaiOpinion
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your API keys
   
   # Option 1: GitHub Models (FREE for hackathons!) ⭐ RECOMMENDED
   GITHUB_TOKEN=your_github_personal_access_token
   USE_GITHUB_MODELS=true
   
   # Option 2: Azure OpenAI
   AZURE_OPENAI_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
   
   # Option 3: OpenAI
   OPENAI_API_KEY=your_openai_key_here
   ```

4. **Run the application**
   ```bash
   python main.py --image sample_data/patient1.png --condition "Tooth pain for 3 days"
   ```

## 💡 Usage

### Basic Usage

```bash
python main.py --image <path-to-image> --condition "<patient symptoms>"
```

### Examples

```bash
# Dental issue
python main.py --image patient1.png --condition "Tooth pain for 3 days"

# With email follow-up registration
python main.py -i patient1.png -c "Tooth pain for 3 days" -e patient@example.com

# Save report to file
python main.py -i patient1.png -c "Tooth pain for 3 days" --save

# Skip email prompt and provide email directly
python main.py -i patient1.png -c "Tooth pain" -e user@email.com --no-prompt

# Custom output path
python main.py -i xray.png -c "Wrist pain after fall" -o report.json
```

### Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--image` | `-i` | Path to medical image file (required) |
| `--condition` | `-c` | Patient symptoms description (required) |
| `--email` | `-e` | Patient email for follow-up reminders (optional) |
| `--save` | `-s` | Save diagnostic report to JSON file |
| `--output` | `-o` | Custom output file path |
| `--no-prompt` | | Skip email preference prompt (use with --email) |

## 📊 Sample Output

```json
{
  "finding": "Possible cavity in upper molar region",
  "diagnosis": "Dental caries (early stage)",
  "treatment": "Dental filling recommended; reduce sugar intake; use fluoride toothpaste.",
  "follow_up": "Check-up in 7 days to assess pain reduction. Reminder: rinse with warm salt water twice daily."
}
```

## 🧩 Project Structure

```
MaiOpinion/
├── main.py                 # Main orchestrator
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── agents/
│   ├── __init__.py        # Agent package init
│   ├── diagnostic.py      # Agent 1: Image analysis
│   ├── reasoning.py       # Agent 2: Clinical reasoning
│   ├── treatment.py       # Agent 3: Treatment suggestions
│   └── followup.py        # Agent 4: Follow-up care
├── sample_data/           # Test data directory
├── patients_db.csv        # Patient follow-up database
├── send_followups.py      # Email scheduler script
├── ARCHITECTURE.md        # System architecture documentation
├── FEATURES.md           # Feature development checklist
└── README.md             # This file
```

## 📧 Email Follow-Up System

MaiOpinion includes an automated email follow-up system to help patients remember their scheduled check-ups.

### How It Works

1. **During Diagnosis**: Patient can register their email for follow-up reminders
2. **Data Storage**: Patient information is stored in `patients_db.csv`
3. **Automated Emails**: Run the email scheduler to send reminders on scheduled dates

### Register for Email Follow-Ups

```bash
# Interactive prompt for email
python main.py -i patient.png -c "Tooth pain"
# You'll be asked: "Would you like to receive follow-up reminders via email?"

# Provide email directly
python main.py -i patient.png -c "Tooth pain" -e patient@example.com

# Skip prompt and use provided email
python main.py -i patient.png -c "Tooth pain" -e patient@example.com --no-prompt
```

### Send Scheduled Follow-Up Emails

```bash
# Send all due follow-up emails
python send_followups.py

# View registered patients
python send_followups.py --view

# View patients without sending emails
python send_followups.py --view --no-send
```

### Patient Database Structure

The `patients_db.csv` file tracks:
- Patient ID and registration timestamp
- Email address
- Original condition and diagnosis
- Treatment plan
- Follow-up timeline and scheduled date
- Email sent status

**Note**: Email sending is currently simulated (prints to console). To enable real emails, integrate an SMTP service (see `TODO` comments in `agents/followup.py`).

### Database Management

Utility script for managing patient data:

```bash
# List all patients
python manage_db.py --list

# Show database statistics
python manage_db.py --stats

# View patient details
python manage_db.py --view PT12345

# Export database backup
python manage_db.py --export backup.csv

# Clear database (requires confirmation)
python manage_db.py --clear
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Azure OpenAI (recommended)
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# OR OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
```

### Mock Mode

The system works without API keys using intelligent mock responses based on symptom keywords. Perfect for testing and demos!

## 🧪 Testing Individual Agents

Each agent can be tested independently:

```bash
# Test Diagnostic Agent
cd agents
python diagnostic.py

# Test Reasoning Agent
python reasoning.py

# Test Treatment Agent
python treatment.py

# Test Follow-Up Agent
python followup.py
```

## 🎯 Development Workflow

1. **Agent 1** analyzes the image (or uses mock data)
2. **Agent 2** receives findings + symptoms → generates diagnosis
3. **Agent 3** receives diagnosis → recommends treatment
4. **Agent 4** receives treatment → creates follow-up plan
5. **Orchestrator** aggregates all outputs into final report

## 🌟 Key Features by Agent

### Agent 1: Diagnostic Agent
- Mock image analysis with keyword detection
- Extensible to Azure Vision API
- Returns structured visual findings

### Agent 2: Clinical Reasoning Agent
- GPT-4o-mini powered diagnosis
- Confidence scoring
- Clinical reasoning explanation

### Agent 3: Treatment Agent
- Evidence-based treatment suggestions
- Precautions and lifestyle recommendations
- Actionable medical advice

### Agent 4: Follow-Up Agent
- Care timeline generation
- Patient-friendly instructions
- Supportive messaging

## 📈 Future Enhancements

- [ ] Real Azure Computer Vision integration
- [ ] Web UI with Flask/React
- [ ] Database storage (SQLite)
- [ ] Multi-language support
- [ ] Feedback loop for diagnosis correction
- [ ] Agent workflow visualization
- [ ] PDF report generation

## 🤝 Contributing

This is a hackathon project built in under 1 hour! Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Developer

**Yunus Yurttagul**
- GitHub: [@Yunukas](https://github.com/Yunukas)
- Project: Hackathon 2025

## 🙏 Acknowledgments

- Built with Azure OpenAI / OpenAI GPT-4o-mini
- Developed in VS Code with GitHub Copilot assistance
- Hackathon project demonstrating multi-agent AI collaboration

## ⚠️ Disclaimer

**This is a prototype demonstration system for educational and hackathon purposes only.**

- NOT intended for actual medical diagnosis
- NOT a substitute for professional medical advice
- Always consult qualified healthcare professionals
- For demonstration of multi-agent AI architecture only

## 📚 Documentation

- [Architecture Documentation](ARCHITECTURE.md) - Detailed system architecture
- [Feature Checklist](FEATURES.md) - Development feature list
- [Requirements](Requirements.prd) - Original project requirements

---

**Built with ❤️ for AI Hackathon 2025**
