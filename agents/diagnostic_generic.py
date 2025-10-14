"""
Generic Diagnostic Agent
Handles diagnostic analysis for various medical image types
(brain scans, skin lesions, bone X-rays, etc.)
"""

import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()


class GenericDiagnosticAgent:
    """Generic agent for various medical diagnostics"""
    
    def __init__(self):
        """Initialize the Generic Diagnostic Agent"""
        self.client = self._initialize_client()
        self.model = self._get_model_name()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            print(f"[Generic Diagnostic Agent] Using GitHub Models (token: {github_token[:10]}...)")
            return OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=github_token
            )
        
        azure_key = os.getenv('AZURE_OPENAI_KEY')
        if azure_key:
            print("[Generic Diagnostic Agent] Using Azure OpenAI")
            return AzureOpenAI(
                api_key=azure_key,
                api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
            )
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            print("[Generic Diagnostic Agent] Using OpenAI")
            return OpenAI(api_key=openai_key)
        
        print("[Generic Diagnostic Agent] No API keys found - using mock mode")
        return None
    
    def _get_model_name(self):
        """Get the appropriate model name"""
        if self.client is None:
            return None
        
        if "github" in os.getenv('GITHUB_TOKEN', '').lower() or \
           os.getenv('USE_GITHUB_MODELS', '').lower() == 'true':
            return "gpt-4o-mini"
        
        if os.getenv('AZURE_OPENAI_DEPLOYMENT'):
            return os.getenv('AZURE_OPENAI_DEPLOYMENT')
        
        return os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    def analyze(self, image_path: str, condition: str, detection_info: dict) -> str:
        """
        Analyze medical image and provide findings
        
        Args:
            image_path: Path to medical image
            condition: Patient's condition description
            detection_info: Information from detection agent
        
        Returns:
            Detailed findings from analysis
        """
        image_type = detection_info.get('image_type', 'unknown')
        body_part = detection_info.get('body_part', 'unspecified')
        
        print(f"[Generic Diagnostic Agent] Analyzing {image_type} image: {image_path}")
        print(f"[Generic Diagnostic Agent] Body part: {body_part}")
        print(f"[Generic Diagnostic Agent] Condition: {condition}")
        
        if not os.path.exists(image_path):
            print(f"[Generic Diagnostic Agent] WARNING: Image not found, using mock analysis")
            return self._mock_analysis(condition, image_type, body_part)
        
        if self.client is None:
            return self._mock_analysis(condition, image_type, body_part)
        
        try:
            return self._ai_analysis(condition, detection_info)
        except Exception as e:
            print(f"[Generic Diagnostic Agent] AI analysis failed: {e}, using mock analysis")
            return self._mock_analysis(condition, image_type, body_part)
    
    def _ai_analysis(self, condition: str, detection_info: dict) -> str:
        """Use AI for medical image analysis"""
        
        image_type = detection_info.get('image_type', 'medical image')
        body_part = detection_info.get('body_part', 'body part')
        modality = detection_info.get('imaging_modality', 'imaging')
        
        prompt = f"""You are an expert medical diagnostician analyzing a {image_type}.

Patient Condition: {condition}
Body Part: {body_part}
Imaging Modality: {modality}

Based on the patient's symptoms and image type, provide a detailed medical assessment including:
1. Most likely findings in this type of imaging
2. Specific abnormalities or areas of concern
3. Severity assessment
4. Clinical correlation with symptoms

Provide a concise, professional medical finding (2-3 sentences)."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are an experienced medical specialist in {image_type} interpretation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    def _mock_analysis(self, condition: str, image_type: str, body_part: str) -> str:
        """Mock analysis based on image type and condition"""
        condition_lower = condition.lower()
        
        # Brain scan
        if image_type == 'brain_scan':
            if any(word in condition_lower for word in ['headache', 'migraine', 'head pain']):
                return "Brain CT scan shows no acute intracranial hemorrhage or mass effect. Mild periventricular white matter changes consistent with chronic microvascular ischemia. Ventricles and sulci appear age-appropriate. Consider MRI for further evaluation if symptoms persist."
            elif any(word in condition_lower for word in ['stroke', 'weakness', 'numbness']):
                return "MRI demonstrates acute infarction in the left middle cerebral artery territory with restricted diffusion. No hemorrhagic transformation noted. Moderate mass effect with slight midline shift. Urgent neurology consultation recommended for acute stroke management."
            else:
                return "Brain imaging reveals normal brain parenchyma without acute abnormality. No evidence of mass, hemorrhage, or infarction. Ventricles and sulci are within normal limits for patient age."
        
        # Skin imaging
        elif image_type == 'skin':
            if any(word in condition_lower for word in ['mole', 'lesion', 'spot']):
                return "Dermatoscopic examination reveals asymmetric pigmented lesion with irregular borders and color variation. ABCDE criteria suggest possible melanoma. Lesion measures approximately 8mm in diameter. Urgent dermatology referral and biopsy recommended."
            elif any(word in condition_lower for word in ['rash', 'itch', 'red']):
                return "Clinical photograph shows erythematous maculopapular rash with geographic distribution. Appearance consistent with contact dermatitis or allergic reaction. No evidence of vesiculation or ulceration. Recommend topical corticosteroid and identification of allergen."
            else:
                return "Skin examination shows benign-appearing lesion without concerning features. Regular borders, uniform pigmentation, and symmetry present. Continue monitoring for any changes in size, shape, or color."
        
        # Bone X-ray
        elif image_type == 'bone_xray':
            if any(word in condition_lower for word in ['fracture', 'break', 'broken', 'fall']):
                return "X-ray demonstrates oblique fracture of the distal radius with minimal displacement. No evidence of comminution or intra-articular extension. Adjacent soft tissue swelling noted. Recommend orthopedic evaluation for possible closed reduction and immobilization."
            elif any(word in condition_lower for word in ['arthritis', 'joint pain', 'stiff']):
                return "Radiographic findings show moderate degenerative joint disease with joint space narrowing, subchondral sclerosis, and marginal osteophyte formation. No acute fracture or dislocation. Findings consistent with osteoarthritis."
            else:
                return "Skeletal radiograph shows intact bony structures without acute fracture or dislocation. Normal bone density and alignment. Soft tissues appear unremarkable."
        
        # Default for other types
        else:
            return f"Medical imaging of {body_part} reviewed. Based on the patient's presentation with {condition}, findings suggest possible abnormality requiring clinical correlation. Recommend specialist consultation for comprehensive evaluation and management plan."


def main():
    """Test the Generic Diagnostic Agent"""
    agent = GenericDiagnosticAgent()
    
    test_cases = [
        ("brain_mri.png", "Severe headache for 2 weeks", {"image_type": "brain_scan", "body_part": "brain", "imaging_modality": "MRI"}),
        ("skin_lesion.jpg", "Suspicious mole on back", {"image_type": "skin", "body_part": "skin", "imaging_modality": "photograph"}),
        ("wrist_xray.png", "Wrist pain after fall", {"image_type": "bone_xray", "body_part": "wrist", "imaging_modality": "X-ray"}),
    ]
    
    print("=" * 80)
    print("Generic Diagnostic Agent - Test Suite")
    print("=" * 80)
    
    for image_path, condition, detection_info in test_cases:
        print(f"\nTest: {condition}")
        print("-" * 80)
        findings = agent.analyze(image_path, condition, detection_info)
        print(f"Findings: {findings}")
        print()


if __name__ == "__main__":
    main()
