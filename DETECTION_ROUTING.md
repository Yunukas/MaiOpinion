# 🎯 Detection-Based Routing Architecture

## Overview

MaiOpinion now uses a **detection-first** approach with specialized diagnostic agents for different body parts. This architecture allows for more accurate diagnoses and easy scalability to add new medical specialties.

---

## Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      Patient Input                               │
│              (Image + Condition Description)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 1: Image Detection Agent                       │
│  Analyzes image filename and condition to identify image type   │
│  Output: image_type, body_part, modality, confidence            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 2: Diagnostic Router                           │
│        Routes to appropriate specialized diagnostic agent        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Dental  │  │  Chest   │  │  Generic │
        │  Agent   │  │  X-ray   │  │  Agent   │
        │          │  │  Agent   │  │          │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             └─────────────┴─────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│            STEP 3: Clinical Reasoning Agent                      │
│     Analyzes findings + symptoms → generates diagnosis           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 4: Treatment Agent                             │
│        Recommends treatment based on diagnosis                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 5: Follow-Up Agent                             │
│    Creates follow-up plan + manages email reminders             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Final Report   │
                    └─────────────────┘
```

---

## Components

### 1. **Image Detection Agent** (`agents/detection.py`)

**Purpose**: Identifies the type of medical image to route it to the correct specialist.

**Capabilities**:
- Analyzes filename patterns
- Considers patient condition keywords
- Uses AI (optional) for advanced detection
- Falls back to intelligent mock detection

**Image Types Detected**:
- `dental` - Dental X-rays, oral photographs
- `chest_xray` - Chest X-rays, lung imaging
- `brain_scan` - Brain CT, MRI, head scans
- `skin` - Dermatology photos, lesion images
- `bone_xray` - Skeletal X-rays (non-chest)
- `eye` - Retinal scans, eye examinations
- `ultrasound` - Ultrasound imaging
- `other` - Unidentified or mixed types

**Output Format**:
```python
{
    "image_type": "chest_xray",
    "confidence": "high",
    "body_part": "chest/lungs",
    "imaging_modality": "X-ray",
    "reasoning": "Filename or condition indicates chest/lung imaging"
}
```

---

### 2. **Specialized Diagnostic Agents**

#### **Dental Diagnostic Agent** (`agents/diagnostic_dental.py`)

**Expertise**: Dental X-rays, oral photography, dental conditions

**Analyzes**:
- Cavities and dental caries
- Gum disease (periodontitis, gingivitis)
- Impacted teeth
- Root abscesses
- Tooth fractures

**Example Output**:
> "Possible dental caries (cavity) detected in upper molar region with visible decay. The affected tooth shows signs of enamel erosion and probable pulp involvement. Recommend immediate dental intervention."

---

#### **Chest X-ray Diagnostic Agent** (`agents/diagnostic_chest.py`)

**Expertise**: Chest X-rays, lung imaging, respiratory conditions

**Analyzes**:
- Pneumonia and infiltrates
- Pleural effusions
- Cardiomegaly
- COPD/emphysema
- Tuberculosis
- Pneumothorax
- Pulmonary edema

**Example Output**:
> "Chest X-ray demonstrates bilateral interstitial infiltrates with right-sided pleural effusion. Cardiac silhouette appears mildly enlarged. No pneumothorax detected. Findings consistent with community-acquired pneumonia with fluid accumulation."

---

#### **Generic Diagnostic Agent** (`agents/diagnostic_generic.py`)

**Expertise**: Brain scans, skin lesions, bone X-rays, and other imaging types

**Analyzes**:
- **Brain scans**: Strokes, hemorrhages, tumors, concussions
- **Skin imaging**: Melanoma, rashes, dermatitis, lesions
- **Bone X-rays**: Fractures, arthritis, bone density
- **Other**: Any specialized imaging not covered by dedicated agents

**Example Output (Brain)**:
> "Brain CT scan shows no acute intracranial hemorrhage or mass effect. Mild periventricular white matter changes consistent with chronic microvascular ischemia. Ventricles appear age-appropriate."

**Example Output (Skin)**:
> "Dermatoscopic examination reveals asymmetric pigmented lesion with irregular borders and color variation. ABCDE criteria suggest possible melanoma. Urgent dermatology referral and biopsy recommended."

---

### 3. **Diagnostic Router** (`agents/diagnostic_router.py`)

**Purpose**: Routes detected images to the correct specialized agent.

**Routing Logic**:
```python
if image_type == 'dental':
    → Use Dental Diagnostic Agent
elif image_type == 'chest_xray':
    → Use Chest X-ray Diagnostic Agent
else:
    → Use Generic Diagnostic Agent (handles brain, skin, bones, etc.)
```

**Output**:
```python
{
    "findings": "Detailed diagnostic findings from specialized agent...",
    "agent_used": "Chest X-ray Diagnostic Agent",
    "detection_info": {...}
}
```

---

## Benefits of This Architecture

### ✅ **Accuracy**
- Specialized agents have domain-specific knowledge
- Dental findings use dental terminology
- Chest X-rays analyzed with radiological expertise

### ✅ **Scalability**
- Easy to add new specialized agents
- Just create a new agent file and update the router
- No need to modify existing agents

### ✅ **Modularity**
- Each agent is independent
- Can test agents individually
- Easy to maintain and debug

### ✅ **Flexibility**
- Detection can be enhanced with vision AI
- Agents can be swapped or upgraded
- Router logic can become more sophisticated

---

## Adding a New Specialty

Want to add a new specialized agent? Here's how:

### Step 1: Create the Agent

```python
# agents/diagnostic_cardiology.py

class CardiologyDiagnosticAgent:
    def analyze(self, image_path: str, condition: str, detection_info: dict) -> str:
        # Your cardiology-specific analysis
        return "ECG shows ST-segment elevation suggesting acute myocardial infarction..."
```

### Step 2: Update the Router

```python
# agents/diagnostic_router.py

from agents.diagnostic_cardiology import CardiologyDiagnosticAgent

class DiagnosticRouter:
    def __init__(self):
        self.agents = {
            'dental': DentalDiagnosticAgent(),
            'chest_xray': ChestXrayDiagnosticAgent(),
            'cardiology': CardiologyDiagnosticAgent(),  # New!
            'generic': GenericDiagnosticAgent()
        }
    
    def route_and_analyze(self, ...):
        if image_type == 'ecg':  # New!
            agent = self.agents['cardiology']
        # ...
```

### Step 3: Update Detection

```python
# agents/detection.py

def _mock_detection(self, image_path: str, condition: str) -> dict:
    # Add ECG detection
    if any(word in condition_lower for word in ['ecg', 'heart attack', 'chest pain']):
        return {
            "image_type": "ecg",
            "body_part": "heart",
            "imaging_modality": "ECG",
            # ...
        }
```

### Done! 🎉

Your new specialty is now integrated!

---

## Testing

### Test Individual Agents

```bash
# Test Detection Agent
python -m agents.detection

# Test Dental Agent
python -m agents.diagnostic_dental

# Test Chest X-ray Agent
python -m agents.diagnostic_chest

# Test Generic Agent
python -m agents.diagnostic_generic

# Test Router
python -m agents.diagnostic_router
```

### Test Complete Pipeline

```bash
# Dental case
python main.py -i sample_teeth.png -c "Tooth pain" --no-prompt

# Chest X-ray case
python main.py -i sample_lungs.png -c "Chest pain" --no-prompt

# Brain scan case
python main.py -i brain_mri.png -c "Headache" --no-prompt
```

---

## File Structure

```
agents/
├── detection.py              # Image detection agent
├── diagnostic_router.py      # Routes to specialized agents
├── diagnostic_dental.py      # Dental specialist
├── diagnostic_chest.py       # Chest X-ray specialist
├── diagnostic_generic.py     # Generic specialist (brain, skin, bones)
├── reasoning.py              # Clinical reasoning (unchanged)
├── treatment.py              # Treatment recommendations (unchanged)
└── followup.py               # Follow-up care (unchanged)
```

---

## Example Outputs

### Dental Case

```
[STEP 1/5] Running Image Detection Agent...
Detected: dental (Confidence: high)

[STEP 2/5] Running Specialized Diagnostic Agent...
Using: Dental Diagnostic Agent
Findings: Possible dental caries detected in upper molar region...

[STEP 3/5] Running Clinical Reasoning Agent...
Diagnosis: Dental caries with pulpitis

[STEP 4/5] Running Treatment Agent...
Treatment: Root canal therapy or extraction...

[STEP 5/5] Running Follow-Up Agent...
Follow-up: Dental check-up in 1 week
```

### Chest X-ray Case

```
[STEP 1/5] Running Image Detection Agent...
Detected: chest_xray (Confidence: high)

[STEP 2/5] Running Specialized Diagnostic Agent...
Using: Chest X-ray Diagnostic Agent
Findings: Bilateral infiltrates with pleural effusion...

[STEP 3/5] Running Clinical Reasoning Agent...
Diagnosis: Pneumonia with pleural effusion

[STEP 4/5] Running Treatment Agent...
Treatment: Antibiotics and thoracentesis...

[STEP 5/5] Running Follow-Up Agent...
Follow-up: Reassess in 7 days
```

---

## Future Enhancements

### Planned Features

- [ ] **Vision AI Integration** - Use GPT-4 Vision for actual image analysis
- [ ] **Confidence Thresholds** - Route low-confidence cases to generic agent
- [ ] **Multi-Specialty Cases** - Handle images requiring multiple specialists
- [ ] **Learning System** - Improve detection based on past accuracy
- [ ] **Specialty Hierarchy** - Sub-specialties within main specialties

### Potential New Specialists

- **Cardiology Agent** - ECG, echocardiograms
- **Orthopedic Agent** - Bone fractures, joint imaging
- **Neurology Agent** - Brain scans, EEG
- **Ophthalmology Agent** - Retinal scans, eye imaging
- **Dermatology Agent** - Skin lesions, rashes
- **Radiology Agent** - Advanced CT/MRI interpretation

---

## API Reference

### Image Detection Agent

```python
agent = ImageDetectionAgent()
result = agent.detect_image_type(image_path, condition)

# Returns:
{
    "image_type": str,
    "confidence": str,
    "body_part": str,
    "imaging_modality": str,
    "reasoning": str
}
```

### Diagnostic Router

```python
router = DiagnosticRouter()
result = router.route_and_analyze(image_path, condition, detection_info)

# Returns:
{
    "findings": str,
    "agent_used": str,
    "detection_info": dict
}
```

### Specialized Agents

```python
agent = DentalDiagnosticAgent()
findings = agent.analyze(image_path, condition, detection_info)

# Returns: str (diagnostic findings)
```

---

## Summary

The new **detection-based routing architecture** makes MaiOpinion:

1. **More Accurate** - Specialized agents for different body parts
2. **More Scalable** - Easy to add new specialties
3. **More Maintainable** - Modular, independent agents
4. **More Professional** - Domain-specific medical terminology

**Perfect for hackathons and ready for production scaling!** 🚀

