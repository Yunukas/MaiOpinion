# 🚀 MaiOpinion - Multi-Agent Healthcare Diagnostic Assistant

## 🎯 Project Overview
**Project Name:** MaiOpinion  
**Developer:** Yunus Yurttagul  
**Timeline:** 1 hour hackathon  
**Goal:** Multi-agent healthcare diagnostic assistant with 4 specialized agents  
**Tech Stack:** Python 3.11+, VS Code, GitHub Copilot, Azure AI Foundry/OpenAI API  

---

## 📋 Core Features (MVP - Required)

### ✅ P0: Essential Features (50 minutes)

#### 1. **Project Setup & Structure** ⏱️ 5 min
- [ ] Initialize GitHub repo with proper structure
- [ ] Create project folder structure:
  ```
  maiopinion/
  ├── main.py
  ├── requirements.txt
  ├── agents/
  │   ├── diagnostic.py
  │   ├── reasoning.py
  │   ├── treatment.py
  │   └── followup.py
  ├── sample_data/
  │   └── patient1.png
  └── README.md
  ```
- [ ] Set up Azure OpenAI/AI Foundry configuration
- [ ] Create requirements.txt with dependencies

#### 2. **Agent 1: Image Diagnostic Agent** ⏱️ 10 min
- [ ] Create `agents/diagnostic.py`
- [ ] Implement mock image analysis or Azure Vision API
- [ ] Handle image file path + patient condition input
- [ ] Return JSON: `{"finding": "possible cavity in molar region"}`
- [ ] Add error handling for invalid image paths

#### 3. **Agent 2: Clinical Reasoning Agent** ⏱️ 10 min  
- [ ] Create `agents/reasoning.py`
- [ ] Implement OpenAI API integration
- [ ] Create clinical reasoning prompt template
- [ ] Process diagnostic findings + symptom description
- [ ] Return JSON: `{"diagnosis": "dental caries", "confidence": "high"}`

#### 4. **Agent 3: Treatment Agent** ⏱️ 10 min
- [ ] Create `agents/treatment.py`
- [ ] Implement treatment recommendation logic
- [ ] Create evidence-based treatment prompt template  
- [ ] Process diagnosis JSON + patient info
- [ ] Return JSON: `{"treatment": "dental filling recommended; use fluoride toothpaste"}`

#### 5. **Agent 4: Follow-Up Agent** ⏱️ 10 min
- [ ] Create `agents/followup.py`
- [ ] Implement care coordination logic
- [ ] Create follow-up planning prompt template
- [ ] Process treatment JSON for follow-up plan
- [ ] Return JSON: `{"follow_up": "check-up in 7 days", "note": "keep good oral hygiene"}`

#### 6. **Orchestrator & Integration** ⏱️ 5 min
- [ ] Create `main.py` orchestrator
- [ ] Chain all four agents sequentially
- [ ] Handle JSON data flow between agents
- [ ] Implement CLI argument parsing (--image, --condition)
- [ ] Add JSON validation and error handling

---

## 🎨 Enhanced Features (Stretch Goals - 10 minutes)

### ✅ P1: User Experience Improvements ⏱️ 5 min
- [ ] **CLI Interface Enhancement**
  - [ ] Pretty-printed final output formatting
  - [ ] Progress indicators during agent processing
  - [ ] Colored terminal output for better readability
  - [ ] Input validation with helpful error messages

### ✅ P2: Data Persistence ⏱️ 5 min
- [ ] **Result Storage**
  - [ ] Save results to SQLite database
  - [ ] Export results to JSON file with timestamp
  - [ ] Store agent communication flow for debugging

---

## 🌟 Bonus Features (If Extra Time)

### ✅ P3: Web Interface ⏱️ 15 min
- [ ] **Simple Flask/React Web App**
  - [ ] File upload form for medical images
  - [ ] Text input for patient condition description
  - [ ] Display agent results in formatted HTML
  - [ ] Show agent workflow visualization
  - [ ] Basic CSS styling for professional look

### ✅ P4: Advanced Features ⏱️ 10 min
- [ ] **Enhanced Functionality**
  - [ ] Real Azure Vision API integration (replace mock)
  - [ ] Natural language summary for clinicians
  - [ ] Feedback loop for diagnosis correction
  - [ ] Visual agent communication flow display

---

## 📝 Technical Implementation Checklist

### Core Architecture
- [ ] **Agent Base Structure**
  ```python
  class MedicalAgent:
      def __init__(self, name, prompt_template)
      def process(self, input_data) -> dict
      def validate_output(self, output) -> bool
  ```

- [ ] **Data Flow Schema** (4-Agent Pipeline)
  ```json
  {
    "input": {"image_path": "patient1.png", "condition": "Tooth pain for 3 days"},
    "diagnostic_output": {"finding": "Possible cavity in upper molar region"},
    "reasoning_output": {"diagnosis": "Dental caries (early stage)", "confidence": "high"},
    "treatment_output": {"treatment": "Dental filling recommended; reduce sugar intake; use fluoride toothpaste"},
    "followup_output": {"follow_up": "Check-up in 7 days to assess pain reduction", "note": "Reminder: rinse with warm salt water twice daily"},
    "final_report": {
      "finding": "Possible cavity in upper molar region",
      "diagnosis": "Dental caries (early stage)", 
      "treatment": "Dental filling recommended; reduce sugar intake; use fluoride toothpaste",
      "follow_up": "Check-up in 7 days to assess pain reduction. Reminder: rinse with warm salt water twice daily"
    }
  }
  ```

### Required Dependencies
- [ ] `openai` or `azure-openai` for LLM integration
- [ ] `python-dotenv` for environment variables
- [ ] `argparse` for CLI interface
- [ ] `json` for data handling
- [ ] `pathlib` for file path management
- [ ] `sqlite3` for data storage (optional)

### Configuration Setup
- [ ] `.env` file for API keys and endpoints
- [ ] Agent prompt templates configuration
- [ ] JSON validation schemas
- [ ] Comprehensive error handling and logging

### Agent Prompt Templates
- [ ] **Diagnostic Agent Prompt:** "You are a medical imaging assistant..."
- [ ] **Clinical Reasoning Prompt:** "You are a clinical reasoning assistant..."
- [ ] **Treatment Agent Prompt:** "You are a treatment advisor..."
- [ ] **Follow-Up Agent Prompt:** "You are a care coordinator..."

---

## 🎯 Success Criteria

### Minimum Viable Demo
✅ **Input:** `python main.py --image patient1.png --condition "Tooth pain for 3 days"`  
✅ **Expected Output:** 
```json
{
  "finding": "Possible cavity in upper molar region",
  "diagnosis": "Dental caries (early stage)",
  "treatment": "Dental filling recommended; reduce sugar intake; use fluoride toothpaste.",
  "follow_up": "Check-up in 7 days to assess pain reduction. Reminder: rinse with warm salt water twice daily."
}
```

### Quality Gates
- [ ] All 4 agents return valid, structured JSON
- [ ] Sequential agent pipeline executes successfully  
- [ ] End-to-end execution under 30 seconds
- [ ] Proper error handling for invalid inputs/API failures
- [ ] Clean, modular code structure with separated concerns
- [ ] Working demo ready for hackathon presentation

### Validation Checklist
- [ ] Each agent validates JSON output format
- [ ] Orchestrator verifies expected keys before proceeding
- [ ] Fallback responses available if API calls fail
- [ ] Pretty-printed final output for demo purposes

---

## ⚡ Development Priority Order

1. **Setup + Diagnostic Agent** (15 min) - Project structure + Agent 1
2. **Reasoning + Treatment Agents** (20 min) - Agent 2 & 3 with LLM integration  
3. **Follow-Up Agent** (10 min) - Agent 4 completion
4. **Orchestrator Integration** (10 min) - Chain all 4 agents together
5. **Polish + Demo Prep** (5 min) - Error handling, formatting
6. **Stretch Goals** (Extra time) - Web UI or advanced features

---

## 🚨 Hackathon Time Management Tips

### Development Strategy
- **Use GitHub Copilot aggressively** for agent boilerplate and prompt templates
- **Mock first, integrate later** - start with hardcoded responses, add API calls after
- **Keep prompts simple and focused** - complex prompts can be refined post-hackathon
- **Test each agent independently** before chaining them together
- **Have fallback responses ready** - if OpenAI API fails, show mock data

### Agent Development Order
1. **Start with Treatment Agent** - easiest to mock and test
2. **Build Diagnostic Agent** - can use simple image description parsing
3. **Add Clinical Reasoning** - integrates findings with symptoms
4. **Finish with Follow-Up** - synthesizes all previous outputs

### Demo Preparation
- **Test with sample data** - prepare `patient1.png` and test condition
- **Have backup scenarios** ready in case primary demo fails
- **Practice the CLI command** - ensure smooth presentation flow
- **Prepare explanation** of agent workflow and collaboration

### Emergency Fallbacks
- If Azure API fails → Use OpenAI API directly
- If APIs are slow → Show pre-generated sample outputs  
- If image processing fails → Use text descriptions instead
- If agents break → Show individual agent outputs manually

**Remember: Working 4-agent demo > Perfect individual agents!** 🏆

---

## 🎪 Demo Script Template

```bash
# Show project structure
tree maiopinion/

# Run the full pipeline
python main.py --image sample_data/patient1.png --condition "Tooth pain for 3 days"

# Explain agent collaboration:
# 1. Diagnostic Agent analyzes image → finds cavity
# 2. Clinical Reasoning Agent → diagnoses dental caries  
# 3. Treatment Agent → recommends filling + care
# 4. Follow-Up Agent → schedules check-up + patient notes
```