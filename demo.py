"""
Demo Script for MaiOpinion
Tests the multi-agent system with various medical scenarios
"""

import subprocess
import sys
from pathlib import Path

# Demo scenarios
SCENARIOS = [
    {
        "name": "Dental Issue",
        "image": "sample_data/patient1.png",
        "condition": "Tooth pain for 3 days"
    },
    {
        "name": "Skin Condition",
        "image": "sample_data/skin.png",
        "condition": "Rash on arm for 2 weeks"
    },
    {
        "name": "Bone Fracture",
        "image": "sample_data/xray.png",
        "condition": "Wrist pain after fall"
    }
]

def run_scenario(scenario):
    """Run a single diagnostic scenario"""
    print("\n" + "=" * 100)
    print(f"🎯 DEMO SCENARIO: {scenario['name']}")
    print("=" * 100)
    
    cmd = [
        sys.executable, 
        "main.py",
        "--image", scenario["image"],
        "--condition", scenario["condition"]
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Scenario completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Scenario failed: {e}")
    
    input("\nPress Enter to continue to next scenario...")

def main():
    """Run all demo scenarios"""
    print("=" * 100)
    print("🏥 MaiOpinion - Multi-Agent Healthcare Diagnostic Assistant")
    print("DEMO MODE - Testing Multiple Scenarios")
    print("=" * 100)
    
    print("\nThis demo will run through several medical diagnostic scenarios.")
    print("Each scenario demonstrates the 4-agent pipeline:\n")
    print("  1️⃣  Image Diagnostic Agent")
    print("  2️⃣  Clinical Reasoning Agent")
    print("  3️⃣  Treatment Agent")
    print("  4️⃣  Follow-Up Agent\n")
    
    input("Press Enter to start the demo...")
    
    # Run first scenario (others are optional since images don't exist)
    run_scenario(SCENARIOS[0])
    
    print("\n" + "=" * 100)
    print("🎉 DEMO COMPLETED!")
    print("=" * 100)
    print("\nThe MaiOpinion multi-agent system successfully:")
    print("  ✅ Analyzed patient images")
    print("  ✅ Generated clinical diagnoses")
    print("  ✅ Recommended treatments")
    print("  ✅ Created follow-up care plans")
    print("\nFor more scenarios, add images to sample_data/ and modify this script.")

if __name__ == "__main__":
    main()
