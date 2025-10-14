"""
Diagnostic Router
Routes images to specialized diagnostic agents based on detection results
"""

from agents.diagnostic_dental import DentalDiagnosticAgent
from agents.diagnostic_chest import ChestXrayDiagnosticAgent
from agents.diagnostic_generic import GenericDiagnosticAgent


class DiagnosticRouter:
    """Routes medical images to appropriate specialized diagnostic agents"""
    
    def __init__(self):
        """Initialize all specialized diagnostic agents"""
        self.agents = {
            'dental': DentalDiagnosticAgent(),
            'chest_xray': ChestXrayDiagnosticAgent(),
            'generic': GenericDiagnosticAgent()
        }
    
    def route_and_analyze(self, image_path: str, condition: str, detection_info: dict) -> dict:
        """
        Route image to appropriate agent and get analysis
        
        Args:
            image_path: Path to medical image
            condition: Patient condition description
            detection_info: Detection results from ImageDetectionAgent
        
        Returns:
            dict with:
                - findings: Diagnostic findings from specialized agent
                - agent_used: Which agent performed the analysis
                - detection_info: Original detection information
        """
        image_type = detection_info.get('image_type', 'other')
        
        print(f"[Diagnostic Router] Routing {image_type} image to specialized agent")
        
        # Route to appropriate specialized agent
        if image_type == 'dental':
            agent = self.agents['dental']
            agent_name = 'Dental Diagnostic Agent'
        elif image_type == 'chest_xray':
            agent = self.agents['chest_xray']
            agent_name = 'Chest X-ray Diagnostic Agent'
        else:
            # Use generic agent for brain_scan, skin, bone_xray, etc.
            agent = self.agents['generic']
            agent_name = 'Generic Diagnostic Agent'
        
        print(f"[Diagnostic Router] Using: {agent_name}")
        
        # Get analysis from specialized agent
        findings = agent.analyze(image_path, condition, detection_info)
        
        return {
            'findings': findings,
            'agent_used': agent_name,
            'detection_info': detection_info
        }


def main():
    """Test the Diagnostic Router"""
    from agents.detection import ImageDetectionAgent
    
    router = DiagnosticRouter()
    detector = ImageDetectionAgent()
    
    test_cases = [
        ("sample_data/dental.png", "Tooth pain for 3 days"),
        ("sample_data/chest_xray.png", "Severe chest pain and coughing"),
        ("sample_data/brain_mri.png", "Headache and dizziness"),
    ]
    
    print("=" * 80)
    print("Diagnostic Router - Test Suite")
    print("=" * 80)
    
    for image_path, condition in test_cases:
        print(f"\n{'=' * 80}")
        print(f"Test Case: {condition}")
        print(f"Image: {image_path}")
        print("=" * 80)
        
        # Step 1: Detect image type
        detection_info = detector.detect_image_type(image_path, condition)
        print(f"\nDetection: {detection_info['image_type']} ({detection_info['confidence']} confidence)")
        
        # Step 2: Route to specialized agent
        result = router.route_and_analyze(image_path, condition, detection_info)
        
        print(f"\nAgent Used: {result['agent_used']}")
        print(f"Findings: {result['findings']}")
        print()


if __name__ == "__main__":
    main()
