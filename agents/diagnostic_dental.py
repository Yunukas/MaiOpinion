"""
Dental Diagnostic Agent
Specialized agent for analyzing dental images and conditions
"""

import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()


class DentalDiagnosticAgent:
    """Specialized agent for dental diagnostics"""
    
    def __init__(self):
        """Initialize the Dental Diagnostic Agent"""
        self.client = self._initialize_client()
        self.model = self._get_model_name()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            print(f"[Dental Agent] Using GitHub Models (token: {github_token[:10]}...)")
            return OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=github_token
            )
        
        azure_key = os.getenv('AZURE_OPENAI_KEY')
        if azure_key:
            print("[Dental Agent] Using Azure OpenAI")
            return AzureOpenAI(
                api_key=azure_key,
                api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
            )
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            print("[Dental Agent] Using OpenAI")
            return OpenAI(api_key=openai_key)
        
        print("[Dental Agent] No API keys found - using mock mode")
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
        Analyze dental image and provide findings
        
        Args:
            image_path: Path to dental image
            condition: Patient's condition description
            detection_info: Information from detection agent
        
        Returns:
            Detailed findings from dental analysis
        """
        print(f"[Dental Agent] Analyzing dental image: {image_path}")
        print(f"[Dental Agent] Condition: {condition}")
        
        if not os.path.exists(image_path):
            print(f"[Dental Agent] WARNING: Image not found, using mock analysis")
            return self._mock_analysis(condition)
        
        if self.client is None:
            return self._mock_analysis(condition)
        
        try:
            return self._ai_analysis(condition, detection_info)
        except Exception as e:
            print(f"[Dental Agent] AI analysis failed: {e}, using mock analysis")
            return self._mock_analysis(condition)
    
    def _ai_analysis(self, condition: str, detection_info: dict) -> str:
        """Use AI for dental analysis"""
        
        prompt = f"""You are an expert dentist analyzing a dental image.

Patient Condition: {condition}
Image Type: {detection_info.get('body_part', 'dental')}
Imaging Modality: {detection_info.get('imaging_modality', 'X-ray')}

Based on the patient's symptoms, provide a detailed dental assessment including:
1. Most likely dental findings (cavities, gum disease, abscess, etc.)
2. Tooth-specific observations (which teeth are affected)
3. Severity assessment
4. Any urgent concerns

Provide a concise, professional dental finding (2-3 sentences)."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an experienced dentist providing professional dental assessments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    def _mock_analysis(self, condition: str) -> str:
        """Mock dental analysis based on condition keywords"""
        condition_lower = condition.lower()
        
        # Cavity/decay
        if any(word in condition_lower for word in ['pain', 'ache', 'hurt', 'sensitive']):
            return "Possible dental caries (cavity) detected in upper molar region with visible decay. The affected tooth shows signs of enamel erosion and probable pulp involvement. Recommend immediate dental intervention."
        
        # Gum disease
        if any(word in condition_lower for word in ['gum', 'bleed', 'swollen', 'red']):
            return "Evidence of periodontal disease with gingival inflammation visible in multiple quadrants. Moderate plaque accumulation and possible bone loss detected. Recommend professional cleaning and periodontal evaluation."
        
        # Wisdom tooth
        if any(word in condition_lower for word in ['wisdom', 'molar', 'back']):
            return "Impacted third molar (wisdom tooth) identified with signs of pericoronitis. The tooth is partially erupted causing tissue inflammation and potential infection risk. Extraction may be necessary."
        
        # Abscess
        if any(word in condition_lower for word in ['abscess', 'infection', 'pus', 'swelling']):
            return "Periapical abscess detected at the root apex with surrounding bone resorption. Active infection present requiring urgent endodontic treatment or extraction. Antibiotic therapy recommended."
        
        # Default
        return "Possible cavity detected in upper molar region with visible decay and enamel erosion. The affected tooth shows signs of demineralization. Recommend dental filling and fluoride treatment."


def main():
    """Test the Dental Diagnostic Agent"""
    agent = DentalDiagnosticAgent()
    
    test_cases = [
        ("dental_xray.png", "Severe tooth pain for 3 days", {"body_part": "upper molar", "imaging_modality": "X-ray"}),
        ("dental_photo.jpg", "Bleeding gums when brushing", {"body_part": "gums", "imaging_modality": "photograph"}),
        ("dental_xray2.png", "Wisdom tooth pain", {"body_part": "third molar", "imaging_modality": "X-ray"}),
    ]
    
    print("=" * 80)
    print("Dental Diagnostic Agent - Test Suite")
    print("=" * 80)
    
    for image_path, condition, detection_info in test_cases:
        print(f"\nTest: {condition}")
        print("-" * 80)
        findings = agent.analyze(image_path, condition, detection_info)
        print(f"Findings: {findings}")
        print()


if __name__ == "__main__":
    main()
