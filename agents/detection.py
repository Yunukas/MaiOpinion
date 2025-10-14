"""
Image Detection Agent
Identifies the type of medical image (dental, chest X-ray, brain scan, etc.)
This agent routes images to specialized diagnostic agents.
"""

import os
import json
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()


class ImageDetectionAgent:
    """Agent that detects the type of medical image"""
    
    def __init__(self):
        """Initialize the Image Detection Agent"""
        self.client = self._initialize_client()
        self.model = self._get_model_name()
    
    def _initialize_client(self):
        """Initialize OpenAI client with GitHub Models, Azure, or OpenAI fallback"""
        
        # Try GitHub Models first (FREE for hackathons!)
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            print(f"[Detection Agent] Using GitHub Models (token: {github_token[:10]}...)")
            return OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=github_token
            )
        
        # Try Azure OpenAI
        azure_key = os.getenv('AZURE_OPENAI_KEY')
        if azure_key:
            print("[Detection Agent] Using Azure OpenAI")
            return AzureOpenAI(
                api_key=azure_key,
                api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
            )
        
        # Try OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            print("[Detection Agent] Using OpenAI")
            return OpenAI(api_key=openai_key)
        
        # No API keys - will use mock mode
        print("[Detection Agent] No API keys found - using mock mode")
        return None
    
    def _get_model_name(self):
        """Get the appropriate model name based on the client"""
        if self.client is None:
            return None
        
        # GitHub Models uses gpt-4o-mini
        if "github" in os.getenv('GITHUB_TOKEN', '').lower() or \
           os.getenv('USE_GITHUB_MODELS', '').lower() == 'true':
            return "gpt-4o-mini"
        
        # Azure uses deployment name
        if os.getenv('AZURE_OPENAI_DEPLOYMENT'):
            return os.getenv('AZURE_OPENAI_DEPLOYMENT')
        
        # OpenAI
        return os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    def detect_image_type(self, image_path: str, condition: str = "") -> dict:
        """
        Detect the type of medical image
        
        Args:
            image_path: Path to the medical image
            condition: Optional patient condition description
        
        Returns:
            dict with keys:
                - image_type: Type of image (dental, chest_xray, brain_scan, etc.)
                - confidence: Confidence level (high, medium, low)
                - body_part: Specific body part identified
                - imaging_modality: X-ray, CT, MRI, photograph, etc.
                - reasoning: Why this classification was made
        """
        print(f"[Detection Agent] Analyzing image: {image_path}")
        if condition:
            print(f"[Detection Agent] Patient condition: {condition}")
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"[Detection Agent] WARNING: Image not found, using mock detection")
            return self._mock_detection(image_path, condition)
        
        # If no API client, use mock mode
        if self.client is None:
            return self._mock_detection(image_path, condition)
        
        # Use AI to detect image type
        try:
            result = self._ai_detection(image_path, condition)
            print(f"[Detection Agent] Detected: {result['image_type']} (Confidence: {result['confidence']})")
            return result
        except Exception as e:
            print(f"[Detection Agent] AI detection failed: {e}, using mock detection")
            return self._mock_detection(image_path, condition)
    
    def _ai_detection(self, image_path: str, condition: str) -> dict:
        """Use AI to detect image type"""
        
        # For now, we'll use text-based detection based on filename and condition
        # In production, you'd use vision models to analyze the actual image
        
        prompt = f"""You are a medical imaging specialist. Based on the information provided, identify the type of medical image.

Image filename: {os.path.basename(image_path)}
Patient condition: {condition if condition else 'Not specified'}

Classify this as one of the following image types:
- dental: Dental X-rays, intraoral photos, teeth images
- chest_xray: Chest X-rays, lung imaging
- brain_scan: Brain CT, MRI, head scans
- skin: Dermatology photos, skin lesions
- bone_xray: Bone fractures, skeletal X-rays (non-chest)
- eye: Retinal scans, eye examinations
- ultrasound: Ultrasound imaging
- other: Any other type

Respond ONLY with valid JSON in this exact format:
{{
    "image_type": "one of the types above",
    "confidence": "high/medium/low",
    "body_part": "specific body part identified",
    "imaging_modality": "X-ray/CT/MRI/photograph/ultrasound/other",
    "reasoning": "brief explanation of classification"
}}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a medical imaging classification expert. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        # Remove markdown code blocks if present
        if result_text.startswith('```'):
            result_text = result_text.split('```')[1]
            if result_text.startswith('json'):
                result_text = result_text[4:]
        
        result = json.loads(result_text)
        return result
    
    def _mock_detection(self, image_path: str, condition: str) -> dict:
        """Mock detection based on filename and condition keywords"""
        
        filename = os.path.basename(image_path).lower()
        condition_lower = condition.lower() if condition else ""
        
        # Dental detection
        if any(word in filename for word in ['tooth', 'teeth', 'dental', 'molar', 'cavity']) or \
           any(word in condition_lower for word in ['tooth', 'teeth', 'dental', 'cavity', 'gum', 'molar']):
            return {
                "image_type": "dental",
                "confidence": "high",
                "body_part": "teeth/oral cavity",
                "imaging_modality": "X-ray or photograph",
                "reasoning": "Filename or condition indicates dental imaging"
            }
        
        # Chest X-ray detection
        if any(word in filename for word in ['chest', 'lung', 'thorax', 'respiratory']) or \
           any(word in condition_lower for word in ['chest', 'lung', 'breathing', 'cough', 'respiratory', 'pneumonia']):
            return {
                "image_type": "chest_xray",
                "confidence": "high",
                "body_part": "chest/lungs",
                "imaging_modality": "X-ray",
                "reasoning": "Filename or condition indicates chest/lung imaging"
            }
        
        # Brain scan detection
        if any(word in filename for word in ['brain', 'head', 'skull', 'cranial', 'mri', 'ct']) or \
           any(word in condition_lower for word in ['brain', 'head', 'headache', 'concussion', 'stroke', 'seizure']):
            return {
                "image_type": "brain_scan",
                "confidence": "high",
                "body_part": "brain/head",
                "imaging_modality": "CT or MRI",
                "reasoning": "Filename or condition indicates brain imaging"
            }
        
        # Skin detection
        if any(word in filename for word in ['skin', 'lesion', 'mole', 'rash', 'derma']) or \
           any(word in condition_lower for word in ['skin', 'rash', 'lesion', 'mole', 'itch']):
            return {
                "image_type": "skin",
                "confidence": "high",
                "body_part": "skin",
                "imaging_modality": "photograph",
                "reasoning": "Filename or condition indicates dermatology imaging"
            }
        
        # Default to other
        return {
            "image_type": "other",
            "confidence": "low",
            "body_part": "unspecified",
            "imaging_modality": "unknown",
            "reasoning": "Could not determine specific image type from available information"
        }


def main():
    """Test the Image Detection Agent"""
    agent = ImageDetectionAgent()
    
    # Test cases
    test_cases = [
        ("sample_data/dental_xray.png", "Tooth pain for 3 days"),
        ("sample_data/chest_xray.png", "Severe chest pain and coughing"),
        ("sample_data/brain_mri.png", "Headache and dizziness"),
        ("sample_data/skin_lesion.jpg", "Suspicious mole on arm"),
    ]
    
    print("=" * 80)
    print("Image Detection Agent - Test Suite")
    print("=" * 80)
    
    for image_path, condition in test_cases:
        print(f"\nTest: {image_path}")
        print(f"Condition: {condition}")
        print("-" * 80)
        
        result = agent.detect_image_type(image_path, condition)
        
        print(f"Result:")
        print(f"  Type: {result['image_type']}")
        print(f"  Body Part: {result['body_part']}")
        print(f"  Modality: {result['imaging_modality']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Reasoning: {result['reasoning']}")
        print()


if __name__ == "__main__":
    main()
