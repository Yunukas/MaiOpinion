# 🏗️ MaiOpinion - System Architecture

## 📐 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MaiOpinion System                                   │
│                   Multi-Agent Healthcare Diagnostic Assistant                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INPUT                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   CLI Command:                                                               │
│   python main.py --image patient1.png --condition "Tooth pain for 3 days"   │
│                                                                              │
│   OR                                                                         │
│                                                                              │
│   Web Interface (Optional):                                                  │
│   [File Upload] + [Text Input] → [Submit Button]                            │
│                                                                              │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MAIN ORCHESTRATOR                                   │
│                              (main.py)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  • Parses user input (image path + patient condition)                       │
│  • Validates input data                                                     │
│  • Orchestrates sequential agent execution                                  │
│  • Manages JSON data flow between agents                                    │
│  • Handles errors and fallback responses                                    │
│  • Formats and returns final diagnostic report                              │
│                                                                              │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
                ┌──────────────────┴──────────────────┐
                │      Sequential Agent Pipeline       │
                └─────────────────────────────────────┘
                                   │
                                   ▼
        ╔══════════════════════════════════════════════════════╗
        ║          AGENT 1: IMAGE DIAGNOSTIC AGENT             ║
        ║              (agents/diagnostic.py)                  ║
        ╠══════════════════════════════════════════════════════╣
        ║                                                      ║
        ║  Input:  • Image file path                          ║
        ║          • Patient condition description            ║
        ║                                                      ║
        ║  Process:                                            ║
        ║          • Mock image analysis OR                    ║
        ║          • Azure Vision API call                     ║
        ║          • Extract visual findings                   ║
        ║                                                      ║
        ║  Output: {"finding": "Possible cavity in molar"}    ║
        ║                                                      ║
        ╚══════════════════════════════════════════════════════╝
                                   │
                                   │ JSON findings
                                   ▼
        ╔══════════════════════════════════════════════════════╗
        ║       AGENT 2: CLINICAL REASONING AGENT              ║
        ║              (agents/reasoning.py)                   ║
        ╠══════════════════════════════════════════════════════╣
        ║                                                      ║
        ║  Input:  • Diagnostic findings (from Agent 1)       ║
        ║          • Patient symptoms                          ║
        ║                                                      ║
        ║  Process:                                            ║
        ║          • Azure OpenAI API call                     ║
        ║          • LLM-based clinical reasoning              ║
        ║          • Correlate findings with symptoms          ║
        ║                                                      ║
        ║  Output: {"diagnosis": "Dental caries",             ║
        ║           "confidence": "high"}                      ║
        ║                                                      ║
        ╚══════════════════════════════════════════════════════╝
                                   │
                                   │ JSON diagnosis
                                   ▼
        ╔══════════════════════════════════════════════════════╗
        ║           AGENT 3: TREATMENT AGENT                   ║
        ║              (agents/treatment.py)                   ║
        ╠══════════════════════════════════════════════════════╣
        ║                                                      ║
        ║  Input:  • Diagnosis (from Agent 2)                 ║
        ║          • Patient information                       ║
        ║                                                      ║
        ║  Process:                                            ║
        ║          • Azure OpenAI API call                     ║
        ║          • Evidence-based treatment lookup           ║
        ║          • Generate recommendations                  ║
        ║                                                      ║
        ║  Output: {"treatment": "Dental filling; reduce      ║
        ║            sugar intake; fluoride toothpaste"}       ║
        ║                                                      ║
        ╚══════════════════════════════════════════════════════╝
                                   │
                                   │ JSON treatment plan
                                   ▼
        ╔══════════════════════════════════════════════════════╗
        ║           AGENT 4: FOLLOW-UP AGENT                   ║
        ║              (agents/followup.py)                    ║
        ╠══════════════════════════════════════════════════════╣
        ║                                                      ║
        ║  Input:  • Treatment plan (from Agent 3)            ║
        ║          • All previous agent outputs                ║
        ║                                                      ║
        ║  Process:                                            ║
        ║          • Azure OpenAI API call                     ║
        ║          • Generate care schedule                    ║
        ║          • Create patient instructions               ║
        ║                                                      ║
        ║  Output: {"follow_up": "Check-up in 7 days",        ║
        ║           "note": "Rinse with warm salt water"}      ║
        ║                                                      ║
        ╚══════════════════════════════════════════════════════╝
                                   │
                                   │ Complete diagnostic report
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FINAL OUTPUT LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Aggregated JSON Report:                                                     │
│  {                                                                           │
│    "finding": "Possible cavity in upper molar region",                      │
│    "diagnosis": "Dental caries (early stage)",                              │
│    "treatment": "Dental filling recommended; reduce sugar intake...",       │
│    "follow_up": "Check-up in 7 days to assess pain reduction..."           │
│  }                                                                           │
│                                                                              │
│  Output Options:                                                             │
│  • Console (pretty-printed JSON)                                            │
│  • JSON file (with timestamp)                                               │
│  • SQLite database (optional)                                               │
│  • Web UI response (if Flask/React enabled)                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌──────────────┐
│ User Input   │
│ - Image Path │
│ - Condition  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                    Data Processing Flow                       │
└──────────────────────────────────────────────────────────────┘

Step 1: Image Analysis
─────────────────────────────────────────────────────────────
Input:    image_path = "patient1.png"
          condition = "Tooth pain for 3 days"
          
Process:  diagnostic_agent.process(image_path, condition)
          
Output:   finding_json = {
            "finding": "Possible cavity in upper molar region"
          }

          │
          ▼

Step 2: Clinical Reasoning
─────────────────────────────────────────────────────────────
Input:    finding_json (from Step 1)
          condition = "Tooth pain for 3 days"
          
Process:  reasoning_agent.process(finding_json, condition)
          
Output:   diagnosis_json = {
            "diagnosis": "Dental caries (early stage)",
            "confidence": "high"
          }

          │
          ▼

Step 3: Treatment Planning
─────────────────────────────────────────────────────────────
Input:    diagnosis_json (from Step 2)
          patient_info (optional)
          
Process:  treatment_agent.process(diagnosis_json)
          
Output:   treatment_json = {
            "treatment": "Dental filling recommended; 
                         reduce sugar intake; 
                         use fluoride toothpaste"
          }

          │
          ▼

Step 4: Follow-Up Coordination
─────────────────────────────────────────────────────────────
Input:    treatment_json (from Step 3)
          all_previous_outputs
          
Process:  followup_agent.process(treatment_json, context)
          
Output:   followup_json = {
            "follow_up": "Check-up in 7 days to assess 
                         pain reduction",
            "note": "Reminder: rinse with warm salt 
                    water twice daily"
          }

          │
          ▼

Step 5: Report Aggregation
─────────────────────────────────────────────────────────────
Input:    All agent outputs (Steps 1-4)
          
Process:  orchestrator.aggregate_results()
          
Output:   final_report = {
            "finding": "...",
            "diagnosis": "...",
            "treatment": "...",
            "follow_up": "..."
          }
```

---

## 🧩 Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      PROJECT STRUCTURE                       │
└─────────────────────────────────────────────────────────────┘

maiopinion/
│
├── main.py                         ← Main Orchestrator
│   ├── parse_arguments()
│   ├── validate_input()
│   ├── run_agent_pipeline()
│   └── format_output()
│
├── agents/                         ← Agent Module Directory
│   │
│   ├── __init__.py
│   │
│   ├── diagnostic.py               ← Agent 1
│   │   ├── class DiagnosticAgent
│   │   ├── analyze_image()
│   │   └── return JSON findings
│   │
│   ├── reasoning.py                ← Agent 2
│   │   ├── class ReasoningAgent
│   │   ├── diagnose()
│   │   └── return JSON diagnosis
│   │
│   ├── treatment.py                ← Agent 3
│   │   ├── class TreatmentAgent
│   │   ├── recommend_treatment()
│   │   └── return JSON treatment
│   │
│   └── followup.py                 ← Agent 4
│       ├── class FollowUpAgent
│       ├── generate_followup()
│       └── return JSON follow-up
│
├── sample_data/                    ← Test Data
│   └── patient1.png
│
├── config/                         ← Configuration (Optional)
│   ├── prompts.py
│   └── settings.py
│
├── .env                            ← API Keys & Secrets
├── requirements.txt                ← Python Dependencies
└── README.md                       ← Documentation
```

---

## 🔌 External Service Integration

```
┌────────────────────────────────────────────────────────────┐
│                  EXTERNAL API SERVICES                      │
└────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│  Azure AI Foundry   │
│    / OpenAI API     │
└──────────┬──────────┘
           │
           ├─────────────► Agent 2: Clinical Reasoning
           │                (GPT-4o or GPT-4o-mini)
           │
           ├─────────────► Agent 3: Treatment
           │                (GPT-4o or GPT-4o-mini)
           │
           └─────────────► Agent 4: Follow-Up
                            (GPT-4o or GPT-4o-mini)

┌─────────────────────┐
│  Azure Vision API   │  (Optional - can be mocked)
└──────────┬──────────┘
           │
           └─────────────► Agent 1: Image Diagnostic
                            (Computer Vision Analysis)

┌─────────────────────┐
│   Environment Vars  │
│      (.env file)    │
├─────────────────────┤
│ AZURE_OPENAI_KEY    │
│ AZURE_OPENAI_ENDPOINT│
│ AZURE_VISION_KEY    │
│ MODEL_NAME          │
└─────────────────────┘
```

---

## 🔐 Security & Configuration

```
┌────────────────────────────────────────────────────────────┐
│              CONFIGURATION MANAGEMENT                       │
└────────────────────────────────────────────────────────────┘

.env File (NOT committed to GitHub)
─────────────────────────────────────
AZURE_OPENAI_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_VISION_KEY=your_vision_key_here
MODEL_NAME=gpt-4o-mini
DEPLOYMENT_NAME=gpt-4o-mini

prompts.py (Agent Prompt Templates)
─────────────────────────────────────
DIAGNOSTIC_PROMPT = """You are a medical imaging assistant..."""
REASONING_PROMPT = """You are a clinical reasoning assistant..."""
TREATMENT_PROMPT = """You are a treatment advisor..."""
FOLLOWUP_PROMPT = """You are a care coordinator..."""
```

---

## 🚀 Deployment Options

```
┌────────────────────────────────────────────────────────────┐
│                  DEPLOYMENT ARCHITECTURE                    │
└────────────────────────────────────────────────────────────┘

Option 1: Local CLI Execution
─────────────────────────────────────────────
┌──────────────┐
│ Local Machine│
│ (Windows)    │
│              │
│ python main.py --image ... --condition ... │
│              │
└──────────────┘


Option 2: Flask Web Application
─────────────────────────────────────────────
┌──────────────┐     HTTP      ┌─────────────┐
│  Web Browser │ ◄──────────►  │ Flask App   │
│              │               │ (main.py)   │
│ [Upload Form]│               │             │
└──────────────┘               └──────┬──────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │   Agents    │
                               │  Pipeline   │
                               └─────────────┘


Option 3: Azure Function (Serverless)
─────────────────────────────────────────────
┌──────────────┐               ┌──────────────┐
│   HTTP       │               │    Azure     │
│   Request    │──────────────►│   Function   │
│              │               │              │
└──────────────┘               └──────┬───────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │   Agents    │
                               │  (Isolated) │
                               └─────────────┘
```

---

## 📊 Agent Interaction Sequence Diagram

```
User    Main.py    Agent1    Agent2    Agent3    Agent4    Output
 │         │          │         │         │         │         │
 │ Input   │          │         │         │         │         │
 ├────────►│          │         │         │         │         │
 │         │          │         │         │         │         │
 │         │ Analyze  │         │         │         │         │
 │         ├─────────►│         │         │         │         │
 │         │          │         │         │         │         │
 │         │ Finding  │         │         │         │         │
 │         │◄─────────┤         │         │         │         │
 │         │          │         │         │         │         │
 │         │      Diagnose      │         │         │         │
 │         ├────────────────────►│         │         │         │
 │         │                     │         │         │         │
 │         │      Diagnosis      │         │         │         │
 │         │◄────────────────────┤         │         │         │
 │         │                     │         │         │         │
 │         │            Recommend Treatment│         │         │
 │         ├─────────────────────────────►│         │         │
 │         │                               │         │         │
 │         │            Treatment Plan     │         │         │
 │         │◄─────────────────────────────┤         │         │
 │         │                               │         │         │
 │         │                      Follow-Up Planning │         │
 │         ├───────────────────────────────────────►│         │
 │         │                                         │         │
 │         │                      Follow-Up Plan    │         │
 │         │◄───────────────────────────────────────┤         │
 │         │                                         │         │
 │         │ Aggregate                               │         │
 │         ├─────────────────────────────────────────────────►│
 │         │                                                   │
 │ Result  │                                                   │
 │◄────────┤                                                   │
 │         │                                                   │
```

---

## ⚙️ Technology Stack Details

```
┌────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY LAYERS                        │
└────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Presentation Layer                                       │
├─────────────────────────────────────────────────────────┤
│ • Command Line Interface (argparse)                     │
│ • Flask Web UI (optional)                               │
│ • React Frontend (stretch goal)                         │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Application Layer                                        │
├─────────────────────────────────────────────────────────┤
│ • Python 3.11+                                          │
│ • Main Orchestrator (main.py)                           │
│ • Agent Modules (agents/*.py)                           │
│ • JSON Schema Validation                                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ AI/ML Layer                                              │
├─────────────────────────────────────────────────────────┤
│ • Azure OpenAI Service (GPT-4o/GPT-4o-mini)            │
│ • Azure AI Foundry                                      │
│ • Azure Computer Vision API (optional)                  │
│ • LangChain (optional for advanced orchestration)       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Data Layer                                               │
├─────────────────────────────────────────────────────────┤
│ • JSON Files (results storage)                          │
│ • SQLite Database (optional)                            │
│ • File System (image storage)                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Design Principles

1. **Modularity**: Each agent is an independent module with clear input/output contracts
2. **Sequential Processing**: Agents execute in order, building on previous outputs
3. **JSON Communication**: All inter-agent communication uses structured JSON
4. **Error Resilience**: Each agent validates inputs and has fallback mechanisms
5. **Simplicity**: Hackathon-focused design prioritizes working demo over complexity
6. **Extensibility**: Easy to add new agents or modify existing ones
7. **Testability**: Each agent can be tested independently before integration

---

**Generated for:** MaiOpinion Hackathon Project  
**Developer:** Yunus Yurttagul  
**Date:** October 14, 2025
