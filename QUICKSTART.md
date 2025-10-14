# 🚀 MaiOpinion - Quick Start Guide

## ⚡ 60-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application (works with mock data, no API keys needed!)
python main.py --image sample_data/patient1.png --condition "Tooth pain for 3 days"
```

## 🎯 Common Commands

### Basic Diagnosis
```bash
python main.py -i patient.png -c "Your symptoms here"
```

### Save Results to File
```bash
python main.py -i patient.png -c "Your symptoms" --save
```

### Custom Output Location
```bash
python main.py -i patient.png -c "Your symptoms" -o my_report.json
```

## 🔑 Using Real AI (Optional)

1. Copy `.env.example` to `.env`
2. Add your API keys:

### For Azure OpenAI:
```env
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

### For OpenAI:
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

## 🧪 Test Individual Agents

```bash
# Test each agent separately
python agents/diagnostic.py
python agents/reasoning.py
python agents/treatment.py
python agents/followup.py
```

## 🎪 Run Demo

```bash
python demo.py
```

## 📊 Expected Output

```json
{
  "finding": "Possible cavity in upper molar region",
  "diagnosis": "Dental caries (early stage)",
  "treatment": "Dental filling recommended...",
  "follow_up": "Check-up in 7 days..."
}
```

## 🆘 Troubleshooting

**Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**No API keys?**
- System works with intelligent mock responses!
- Great for testing and demos

**Missing images?**
- System will warn but continue with mock analysis
- Add your own images to `sample_data/`

## 📚 Learn More

- Full docs: [README.md](README.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Features: [FEATURES.md](FEATURES.md)

---

**Ready to diagnose! 🏥**
