"""
MaiOpinion - Multi-Agent Healthcare Diagnostic Assistant
Main Orchestrator - Chains all four agents together
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Import agents
from agents.detection import ImageDetectionAgent
from agents.diagnostic_router import DiagnosticRouter
from agents.reasoning import ReasoningAgent
from agents.treatment import TreatmentAgent
from agents.followup import FollowUpAgent


class MaiOpinionOrchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        print("=" * 80)
        print("MaiOpinion - Multi-Agent Healthcare Diagnostic Assistant")
        print("=" * 80)
        print()
        
        # Initialize all agents
        self.detection_agent = ImageDetectionAgent()
        self.diagnostic_router = DiagnosticRouter()
        self.reasoning_agent = ReasoningAgent()
        self.treatment_agent = TreatmentAgent()
        self.followup_agent = FollowUpAgent()
        
    def run_pipeline(self, image_path: str, condition: str, patient_email: str = None, 
                     no_prompt: bool = False) -> dict:
        """
        Run the complete diagnostic pipeline through all 4 agents
        
        Args:
            image_path: Path to medical image
            condition: Patient's symptoms/condition description
            patient_email: Optional email for follow-up reminders
            no_prompt: Skip interactive email prompt
            
        Returns:
            dict: Complete diagnostic report
        """
        print("\n" + "=" * 80)
        print("Starting Multi-Agent Diagnostic Pipeline")
        print("=" * 80 + "\n")
        
        try:
            # Step 1: Image Detection Agent
            print("\n[STEP 1/5] Running Image Detection Agent...")
            print("-" * 80)
            detection_info = self.detection_agent.detect_image_type(image_path, condition)
            
            # Step 2: Specialized Diagnostic Agent (routed based on detection)
            print("\n[STEP 2/5] Running Specialized Diagnostic Agent...")
            print("-" * 80)
            diagnostic_result = self.diagnostic_router.route_and_analyze(
                image_path, condition, detection_info
            )
            diagnostic_output = diagnostic_result['findings']
            
            # Step 3: Clinical Reasoning Agent
            print("\n[STEP 3/5] Running Clinical Reasoning Agent...")
            print("-" * 80)
            reasoning_output = self.reasoning_agent.process(diagnostic_output, condition)
            
            if not self.reasoning_agent.validate_output(reasoning_output):
                raise ValueError("Reasoning agent output validation failed")
            
            # Step 4: Treatment Agent
            print("\n[STEP 4/5] Running Treatment Agent...")
            print("-" * 80)
            treatment_output = self.treatment_agent.process(reasoning_output)
            
            if not self.treatment_agent.validate_output(treatment_output):
                raise ValueError("Treatment agent output validation failed")
            
            # Step 5: Follow-Up Agent
            print("\n[STEP 5/5] Running Follow-Up Agent...")
            print("-" * 80)
            
            # Determine email for follow-ups
            if patient_email:
                email_to_use = patient_email
                print(f"✅ Using provided email: {email_to_use}")
            elif not no_prompt:
                email_to_use = self._ask_email_preference()
            else:
                email_to_use = None
            
            followup_output = self.followup_agent.process(
                treatment_output, 
                reasoning_output,
                patient_email=email_to_use,
                condition=condition
            )
            
            if not self.followup_agent.validate_output(followup_output):
                raise ValueError("Follow-up agent output validation failed")
            
            # Aggregate final report
            final_report = self._aggregate_report(
                diagnostic_output,
                reasoning_output,
                treatment_output,
                followup_output,
                image_path,
                condition,
                detection_info,
                diagnostic_result.get('agent_used', 'Diagnostic Agent')
            )
            
            print("\n" + "=" * 80)
            print("Pipeline Completed Successfully!")
            print("=" * 80 + "\n")
            
            return final_report
            
        except Exception as e:
            print(f"\n❌ ERROR: Pipeline failed - {str(e)}")
            sys.exit(1)
    
    def _ask_email_preference(self) -> str:
        """Ask patient if they want to receive follow-up emails"""
        print("\n" + "-" * 80)
        print("📧 FOLLOW-UP EMAIL REGISTRATION")
        print("-" * 80)
        print("Would you like to receive automated follow-up reminders via email?")
        
        response = input("Enter your email address (or press Enter to skip): ").strip()
        
        if response and '@' in response:
            print(f"✅ You will receive follow-up reminders at: {response}")
            return response
        else:
            print("⏭️  Skipping email registration")
            return None
    
    def _aggregate_report(self, diagnostic, reasoning, treatment, followup, 
                         image_path, condition, detection_info, agent_used) -> dict:
        """Aggregate all agent outputs into final report"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "patient_condition": condition,
            "image_analyzed": Path(image_path).name,
            "image_type": detection_info.get("image_type"),
            "body_part": detection_info.get("body_part"),
            "imaging_modality": detection_info.get("imaging_modality"),
            "detection_confidence": detection_info.get("confidence"),
            "finding": diagnostic.get("finding") if isinstance(diagnostic, dict) else diagnostic,
            "diagnosis": reasoning.get("diagnosis"),
            "confidence": reasoning.get("confidence"),
            "treatment": treatment.get("treatment"),
            "precautions": treatment.get("precautions", []),
            "follow_up": followup.get("follow_up"),
            "timeline": followup.get("timeline"),
            "patient_instructions": followup.get("patient_instructions"),
            "agent_workflow": {
                "step_1": "Image Detection Agent",
                "step_2": agent_used,
                "step_3": "Clinical Reasoning Agent",
                "step_4": "Treatment Agent",
                "step_5": "Follow-Up Agent"
            }
        }
        
        return report
    
    def print_report(self, report: dict):
        """Pretty print the final diagnostic report"""
        print("\n" + "=" * 80)
        print("📋 FINAL DIAGNOSTIC REPORT")
        print("=" * 80)
        
        print(f"\n📅 Timestamp: {report['timestamp']}")
        print(f"🏥 Patient Condition: {report['patient_condition']}")
        print(f"🖼️  Image Analyzed: {report['image_analyzed']}")
        
        # Image detection info
        print(f"\n{'=' * 80}")
        print("🔍 IMAGE DETECTION")
        print("=" * 80)
        print(f"   Image Type: {report.get('image_type', 'N/A')}")
        print(f"   Body Part: {report.get('body_part', 'N/A')}")
        print(f"   Imaging Modality: {report.get('imaging_modality', 'N/A')}")
        print(f"   Detection Confidence: {report.get('detection_confidence', 'N/A').upper()}")
        
        print("\n" + "-" * 80)
        print("🔍 FINDINGS")
        print("-" * 80)
        print(f"   {report['finding']}")
        
        print("\n" + "-" * 80)
        print("💊 DIAGNOSIS")
        print("-" * 80)
        print(f"   {report['diagnosis']}")
        print(f"   Confidence: {report['confidence'].upper()}")
        
        print("\n" + "-" * 80)
        print("💉 TREATMENT PLAN")
        print("-" * 80)
        print(f"   {report['treatment']}")
        
        if report.get('precautions'):
            print("\n   Precautions:")
            for i, precaution in enumerate(report['precautions'], 1):
                print(f"   {i}. {precaution}")
        
        print("\n" + "-" * 80)
        print("📅 FOLLOW-UP CARE")
        print("-" * 80)
        print(f"   Timeline: {report.get('timeline', 'As recommended')}")
        print(f"   {report['follow_up']}")
        print(f"\n   Patient Instructions:")
        print(f"   {report.get('patient_instructions', 'Follow treatment plan')}")
        
        print("\n" + "=" * 80)
        print()
    
    def save_report(self, report: dict, output_path: str = None):
        """Save report to JSON file"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"diagnostic_report_{timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Report saved to: {output_path}")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="MaiOpinion - Multi-Agent Healthcare Diagnostic Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --image patient1.png --condition "Tooth pain for 3 days"
  python main.py -i sample_data/xray.png -c "Wrist pain after fall" --save
        """
    )
    
    parser.add_argument(
        '--image', '-i',
        type=str,
        required=True,
        help='Path to the medical image file'
    )
    
    parser.add_argument(
        '--condition', '-c',
        type=str,
        required=True,
        help='Patient condition or symptoms description'
    )
    
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save the diagnostic report to a JSON file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output file path for the report (default: auto-generated)'
    )
    
    parser.add_argument(
        '--email', '-e',
        type=str,
        default=None,
        help='Patient email address for follow-up reminders (optional)'
    )
    
    parser.add_argument(
        '--no-prompt',
        action='store_true',
        help='Skip interactive email prompt (use with --email or to skip email registration)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Create orchestrator
    orchestrator = MaiOpinionOrchestrator()
    
    # Run diagnostic pipeline
    report = orchestrator.run_pipeline(
        args.image, 
        args.condition,
        patient_email=args.email,
        no_prompt=args.no_prompt
    )
    
    # Print report
    orchestrator.print_report(report)
    
    # Save if requested
    if args.save or args.output:
        orchestrator.save_report(report, args.output)
    
    # Also print as JSON for easy parsing
    print("\n" + "=" * 80)
    print("📄 JSON OUTPUT")
    print("=" * 80)
    print(json.dumps({
        "finding": report["finding"],
        "diagnosis": report["diagnosis"],
        "treatment": report["treatment"],
        "follow_up": report["follow_up"]
    }, indent=2))
    print()


if __name__ == "__main__":
    main()
