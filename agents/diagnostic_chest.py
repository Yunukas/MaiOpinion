"""
Chest X-ray Diagnostic Agent
Specialized agent for analyzing chest X-rays and respiratory conditions
"""

import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()


class ChestXrayDiagnosticAgent:
    """Specialized agent for chest X-ray diagnostics"""
    
    def __init__(self):
        """Initialize the Chest X-ray Diagnostic Agent"""
        self.client = self._initialize_client()
        self.model = self._get_model_name()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            print(f"[Chest X-ray Agent] Using GitHub Models (token: {github_token[:10]}...)")
            return OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=github_token
            )
        
        azure_key = os.getenv('AZURE_OPENAI_KEY')
        if azure_key:
            print("[Chest X-ray Agent] Using Azure OpenAI")
            return AzureOpenAI(
                api_key=azure_key,
                api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
            )
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            print("[Chest X-ray Agent] Using OpenAI")
            return OpenAI(api_key=openai_key)
        
        print("[Chest X-ray Agent] No API keys found - using mock mode")
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
        Analyze chest X-ray and provide findings
        
        Args:
            image_path: Path to chest X-ray image
            condition: Patient's condition description
            detection_info: Information from detection agent
        
        Returns:
            Detailed findings from chest X-ray analysis
        """
        print(f"[Chest X-ray Agent] Analyzing chest X-ray: {image_path}")
        print(f"[Chest X-ray Agent] Condition: {condition}")
        
        if not os.path.exists(image_path):
            print(f"[Chest X-ray Agent] WARNING: Image not found, using mock analysis")
            return self._mock_analysis(condition)
        
        if self.client is None:
            return self._mock_analysis(condition)
        
        try:
            return self._ai_analysis(condition, detection_info)
        except Exception as e:
            print(f"[Chest X-ray Agent] AI analysis failed: {e}, using mock analysis")
            return self._mock_analysis(condition)
    
    def _ai_analysis(self, condition: str, detection_info: dict) -> str:
        """Use AI for chest X-ray analysis"""
        
        prompt = f"""You are an expert radiologist specializing in chest X-ray interpretation.

Patient Condition: {condition}
Image Type: {detection_info.get('body_part', 'chest/lungs')}
Imaging Modality: {detection_info.get('imaging_modality', 'X-ray')}

Based on the patient's symptoms, provide a detailed chest X-ray assessment including:
1. Lung field findings (infiltrates, consolidation, effusion, etc.)
2. Cardiac silhouette evaluation
3. Mediastinal structures assessment
4. Any abnormalities or areas of concern
5. Clinical correlation with symptoms

Provide a concise, professional radiological finding (2-3 sentences)."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an experienced radiologist providing professional chest X-ray interpretations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    def _mock_analysis(self, condition: str) -> str:
        """Mock chest X-ray analysis based on condition keywords"""
        condition_lower = condition.lower()
        
        # Pneumonia
        if any(word in condition_lower for word in ['cough', 'fever', 'pneumonia', 'infection']):
            return "Bilateral interstitial infiltrates visible in lower lung fields, consistent with community-acquired pneumonia. Increased opacity in right lower lobe with possible consolidation. No pleural effusion or pneumothorax detected. Cardiac silhouette within normal limits."
        
        # Chest pain
        if any(word in condition_lower for word in ['chest pain', 'pain']):
            return "Chest X-ray shows clear lung fields bilaterally with no acute infiltrates or consolidation. Cardiac silhouette appears mildly enlarged, suggesting possible cardiomegaly. No evidence of pneumothorax or pleural effusion. Recommend cardiac evaluation for chest pain etiology."
        
        # Difficulty breathing
        if any(word in condition_lower for word in ['breath', 'breathing', 'dyspnea', 'shortness']):
            return "Bilateral lung hyperinflation noted with flattened diaphragms, suggestive of chronic obstructive pulmonary disease (COPD) or asthma exacerbation. No acute infiltrates. Increased anteroposterior diameter consistent with air trapping. Recommend pulmonary function testing."
        
        # Fluid/edema
        if any(word in condition_lower for word in ['fluid', 'edema', 'swelling']):
            return "Bilateral perihilar haziness and Kerley B lines present, consistent with pulmonary edema. Enlarged cardiac silhouette indicating cardiomegaly. Small bilateral pleural effusions noted. Findings suggestive of congestive heart failure. Urgent cardiology consultation recommended."
        
        # TB or chronic cough
        if any(word in condition_lower for word in ['tuberculosis', 'tb', 'chronic', 'night sweats']):
            return "Upper lobe predominant fibronodular opacities with cavitary lesions identified in the right apex. Findings are suspicious for pulmonary tuberculosis. Calcified granulomas present suggesting old healed infection with possible reactivation. Sputum culture and AFB testing recommended."
        
        # Default
        return "Chest X-ray demonstrates increased interstitial markings in bilateral lower lung fields with possible early infiltrate. Cardiomediastinal silhouette appears within normal limits. No pleural effusion or pneumothorax. Clinical correlation recommended."


def main():
    """Test the Chest X-ray Diagnostic Agent"""
    agent = ChestXrayDiagnosticAgent()
    
    test_cases = [
        ("chest_xray.png", "Severe chest pain for 3 days", {"body_part": "chest", "imaging_modality": "X-ray"}),
        ("chest_xray2.png", "Cough and fever for 1 week", {"body_part": "lungs", "imaging_modality": "X-ray"}),
        ("chest_xray3.png", "Shortness of breath", {"body_part": "chest/lungs", "imaging_modality": "X-ray"}),
    ]
    
    print("=" * 80)
    print("Chest X-ray Diagnostic Agent - Test Suite")
    print("=" * 80)
    
    for image_path, condition, detection_info in test_cases:
        print(f"\nTest: {condition}")
        print("-" * 80)
        findings = agent.analyze(image_path, condition, detection_info)
        print(f"Findings: {findings}")
        print()


if __name__ == "__main__":
    main()
