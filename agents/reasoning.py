"""
Agent 2: Clinical Reasoning Agent
Infers diagnosis from visual findings and patient symptoms using AI
"""

import json
import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ReasoningAgent:
    """
    Clinical Reasoning Agent - Uses LLM to diagnose based on findings and symptoms
    """
    
    def __init__(self):
        self.name = "Clinical Reasoning Agent"
        self.client = self._initialize_client()
        
    def _initialize_client(self):
        """Initialize OpenAI client (GitHub Models, Azure OpenAI, or OpenAI)"""
        # Try GitHub Models first (models.inference.ai.azure.com)
        # Check both .env file and system environment
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
        
        # Fallback to OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            print(f"[{self.name}] Using OpenAI")
            return OpenAI(api_key=openai_key)
        
        print(f"[{self.name}] WARNING: No API keys found, using mock responses")
        return None
    
    def process(self, finding_data: dict, condition: str) -> dict:
        """
        Analyze findings and symptoms to provide diagnosis
        
        Args:
            finding_data: Output from Diagnostic Agent (dict or string)
            condition: Patient's described symptoms
            
        Returns:
            dict: JSON with diagnosis and confidence
        """
        print(f"[{self.name}] Processing findings and symptoms...")
        
        # Handle both dict and string inputs from diagnostic agents
        if isinstance(finding_data, dict):
            finding = finding_data.get("finding", str(finding_data))
        else:
            finding = finding_data
        
        if self.client:
            diagnosis_result = self._llm_diagnosis(finding, condition)
        else:
            diagnosis_result = self._mock_diagnosis(finding, condition)
        
        result = {
            "diagnosis": diagnosis_result["diagnosis"],
            "confidence": diagnosis_result.get("confidence", "medium"),
            "reasoning": diagnosis_result.get("reasoning", "Based on visual findings and symptoms"),
            "agent": self.name
        }
        
        print(f"[{self.name}] Diagnosis: {result['diagnosis']} (Confidence: {result['confidence']})")
        return result
    
    def _llm_diagnosis(self, finding: str, condition: str) -> dict:
        """Use LLM to generate diagnosis"""
        prompt = f"""You are a clinical reasoning assistant. Based on the following information, provide a diagnosis.

Visual Finding: {finding}
Patient Symptoms: {condition}

Provide your response in JSON format with these exact keys:
- diagnosis: The most likely diagnosis (brief, 2-5 words)
- confidence: Your confidence level (high/medium/low)
- reasoning: Brief explanation (one sentence)

Respond ONLY with valid JSON, no other text."""

        try:
            # Get deployment name for Azure or model for OpenAI/GitHub
            if isinstance(self.client, AzureOpenAI):
                model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
            else:
                # For GitHub Models and OpenAI
                model = os.getenv("GITHUB_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a clinical reasoning assistant. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON from response
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"[{self.name}] LLM call failed: {e}")
            return self._mock_diagnosis(finding, condition)
    
    def _mock_diagnosis(self, finding: str, condition: str) -> dict:
        """Fallback mock diagnosis based on keywords"""
        finding_lower = finding.lower()
        condition_lower = condition.lower()
        
        if "cavity" in finding_lower or "decay" in finding_lower:
            return {
                "diagnosis": "Dental caries (early stage)",
                "confidence": "high",
                "reasoning": "Visual cavity detection with pain symptoms indicates active caries"
            }
        elif "fracture" in finding_lower:
            return {
                "diagnosis": "Possible bone fracture",
                "confidence": "medium",
                "reasoning": "Visual fracture pattern requires radiological confirmation"
            }
        elif "skin" in finding_lower:
            return {
                "diagnosis": "Dermatological condition",
                "confidence": "medium",
                "reasoning": "Skin irregularity pattern suggests inflammatory response"
            }
        else:
            return {
                "diagnosis": "Condition requiring specialist evaluation",
                "confidence": "low",
                "reasoning": "Visual findings are non-specific, need additional clinical context"
            }
    
    def validate_output(self, output: dict) -> bool:
        """Validate output structure"""
        required_keys = ["diagnosis", "confidence", "agent"]
        return all(key in output for key in required_keys)


# Test the agent if run directly
if __name__ == "__main__":
    agent = ReasoningAgent()
    finding_data = {
        "finding": "Possible cavity detected in upper molar region",
        "agent": "Diagnostic Agent"
    }
    result = agent.process(finding_data, "Tooth pain for 3 days")
    print("\nAgent Output:")
    print(json.dumps(result, indent=2))
