"""
Agent 3: Treatment Agent
Suggests treatment options based on diagnosis
"""

import json
import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TreatmentAgent:
    """
    Treatment Agent - Recommends evidence-based treatment plans
    """
    
    def __init__(self):
        self.name = "Treatment Agent"
        self.client = self._initialize_client()
        
    def _initialize_client(self):
        """Initialize OpenAI client (GitHub Models, Azure OpenAI, or OpenAI)"""
        # Try GitHub Models first - check both .env and system environment
        github_token = os.getenv("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
        use_github = os.getenv("USE_GITHUB_MODELS", "false").lower() == "true"
        
        if github_token and use_github and github_token != "your_github_token_here":
            print(f"[{self.name}] Using GitHub Models (token: {github_token[:10]}...)")
            return OpenAI(
                api_key=github_token,
                base_url="https://models.inference.ai.azure.com"
            )
        
        # Try Azure OpenAI
        azure_key = os.getenv("AZURE_OPENAI_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_key and azure_endpoint:
            print(f"[{self.name}] Using Azure OpenAI")
            return AzureOpenAI(
                api_key=azure_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=azure_endpoint
            )
        
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            print(f"[{self.name}] Using OpenAI")
            return OpenAI(api_key=openai_key)
        
        print(f"[{self.name}] WARNING: No API keys found, using mock responses")
        return None
    
    def process(self, diagnosis_data: dict) -> dict:
        """
        Generate treatment recommendations based on diagnosis
        
        Args:
            diagnosis_data: Output from Clinical Reasoning Agent
            
        Returns:
            dict: JSON with treatment recommendations
        """
        print(f"[{self.name}] Generating treatment plan...")
        
        diagnosis = diagnosis_data.get("diagnosis", "Unknown condition")
        confidence = diagnosis_data.get("confidence", "medium")
        
        if self.client:
            treatment_result = self._llm_treatment(diagnosis, confidence)
        else:
            treatment_result = self._mock_treatment(diagnosis)
        
        result = {
            "treatment": treatment_result["treatment"],
            "precautions": treatment_result.get("precautions", []),
            "agent": self.name
        }
        
        print(f"[{self.name}] Treatment: {result['treatment']}")
        return result
    
    def _llm_treatment(self, diagnosis: str, confidence: str) -> dict:
        """Use LLM to generate treatment recommendations"""
        prompt = f"""You are a treatment advisor. Based on the diagnosis, suggest evidence-based treatment options.

Diagnosis: {diagnosis}
Confidence Level: {confidence}

Provide your response in JSON format with these exact keys:
- treatment: Main treatment recommendation (2-3 sentences, practical and actionable)
- precautions: List of 2-3 precautions or lifestyle recommendations (array of strings)

Focus on safe, evidence-based recommendations. Respond ONLY with valid JSON, no other text."""

        try:
            if isinstance(self.client, AzureOpenAI):
                model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
            else:
                # For GitHub Models and OpenAI
                model = os.getenv("GITHUB_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a medical treatment advisor. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=250
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean up markdown if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"[{self.name}] LLM call failed: {e}")
            return self._mock_treatment(diagnosis)
    
    def _mock_treatment(self, diagnosis: str) -> dict:
        """Fallback mock treatment recommendations"""
        diagnosis_lower = diagnosis.lower()
        
        if "dental" in diagnosis_lower or "caries" in diagnosis_lower or "cavity" in diagnosis_lower:
            return {
                "treatment": "Dental filling recommended to restore tooth structure. Use fluoride toothpaste twice daily. Schedule dentist appointment within 3-5 days.",
                "precautions": [
                    "Reduce sugar intake and sugary beverages",
                    "Avoid extremely hot or cold foods",
                    "Maintain good oral hygiene with regular brushing and flossing"
                ]
            }
        elif "fracture" in diagnosis_lower:
            return {
                "treatment": "Immobilization and rest recommended. Consult orthopedic specialist for proper casting or splinting. Pain management with over-the-counter analgesics as needed.",
                "precautions": [
                    "Avoid weight-bearing or stress on affected area",
                    "Apply ice packs to reduce swelling",
                    "Keep the area elevated when possible"
                ]
            }
        elif "dermatological" in diagnosis_lower or "skin" in diagnosis_lower:
            return {
                "treatment": "Topical treatment and dermatologist consultation recommended. Keep area clean and moisturized. Avoid scratching or irritating the affected area.",
                "precautions": [
                    "Avoid harsh soaps or chemicals on affected area",
                    "Protect from direct sunlight",
                    "Monitor for changes in size, color, or symptoms"
                ]
            }
        else:
            return {
                "treatment": "Specialist consultation recommended for proper diagnosis and treatment plan. Monitor symptoms and seek immediate care if condition worsens.",
                "precautions": [
                    "Keep detailed notes of symptom progression",
                    "Avoid self-medication without professional advice",
                    "Seek emergency care if severe symptoms develop"
                ]
            }
    
    def validate_output(self, output: dict) -> bool:
        """Validate output structure"""
        required_keys = ["treatment", "agent"]
        return all(key in output for key in required_keys)


# Test the agent if run directly
if __name__ == "__main__":
    agent = TreatmentAgent()
    diagnosis_data = {
        "diagnosis": "Dental caries (early stage)",
        "confidence": "high",
        "agent": "Clinical Reasoning Agent"
    }
    result = agent.process(diagnosis_data)
    print("\nAgent Output:")
    print(json.dumps(result, indent=2))
