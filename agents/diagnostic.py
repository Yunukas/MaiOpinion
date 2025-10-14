"""
Agent 1: Image Diagnostic Agent
Analyzes medical images and returns visual findings
"""

import json
import os
from pathlib import Path


class DiagnosticAgent:
    """
    Image Diagnostic Agent - Analyzes medical images for visual findings
    For hackathon: Uses mock responses. Can be upgraded to Azure Vision API.
    """
    
    def __init__(self):
        self.name = "Diagnostic Agent"
        
    def process(self, image_path: str, condition: str) -> dict:
        """
        Analyze the image and patient condition to extract visual findings
        
        Args:
            image_path: Path to the medical image file
            condition: Patient's described condition/symptoms
            
        Returns:
            dict: JSON with finding information
        """
        print(f"[{self.name}] Analyzing image: {image_path}")
        print(f"[{self.name}] Patient condition: {condition}")
        
        # Validate image exists
        if not os.path.exists(image_path):
            print(f"[{self.name}] WARNING: Image not found, using mock analysis")
        
        # Mock image analysis based on condition keywords
        # In production, this would call Azure Vision API or similar
        finding = self._mock_image_analysis(condition, image_path)
        
        result = {
            "finding": finding,
            "image_analyzed": os.path.basename(image_path),
            "agent": self.name
        }
        
        print(f"[{self.name}] Finding: {finding}")
        return result
    
    def _mock_image_analysis(self, condition: str, image_path: str) -> str:
        """
        Mock image analysis based on keywords in condition
        Replace this with real Azure Vision API call for production
        """
        condition_lower = condition.lower()
        
        # Dental-related conditions
        if "tooth" in condition_lower or "dental" in condition_lower:
            if "pain" in condition_lower:
                return "Possible cavity detected in upper molar region with visible decay"
            else:
                return "Minor dental irregularity observed in molar area"
        
        # Skin-related conditions
        elif "skin" in condition_lower or "rash" in condition_lower:
            return "Irregular skin discoloration pattern observed, possible dermatological concern"
        
        # Bone/X-ray related
        elif "bone" in condition_lower or "fracture" in condition_lower:
            return "Possible hairline fracture detected in bone structure"
        
        # Eye-related
        elif "eye" in condition_lower or "vision" in condition_lower:
            return "Abnormal eye structure pattern detected, requires specialist review"
        
        # Generic fallback
        else:
            return "Visual abnormality detected requiring further clinical assessment"
    
    def validate_output(self, output: dict) -> bool:
        """Validate that the output has the required structure"""
        required_keys = ["finding", "agent"]
        return all(key in output for key in required_keys)


# Test the agent if run directly
if __name__ == "__main__":
    agent = DiagnosticAgent()
    result = agent.process("sample_data/patient1.png", "Tooth pain for 3 days")
    print("\nAgent Output:")
    print(json.dumps(result, indent=2))
