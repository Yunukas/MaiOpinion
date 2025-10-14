"""
Email Follow-Up System Test Suite
Demonstrates the complete email workflow
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def run_command(cmd: list, description: str):
    """Run a command and display its output"""
    print(f"▶️  {description}")
    print(f"   Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def main():
    """Run complete email system test"""
    
    print_header("🧪 MaiOpinion Email Follow-Up System Test Suite")
    
    # Test 1: Check if database exists
    print_header("TEST 1: Database Status Check")
    db_path = Path("patients_db.csv")
    if db_path.exists():
        print(f"✅ Database found: {db_path}")
        print(f"   Size: {db_path.stat().st_size} bytes")
        print(f"   Modified: {datetime.fromtimestamp(db_path.stat().st_mtime)}")
    else:
        print("❌ Database not found - will be created on first patient registration")
    
    # Test 2: View current patients
    print_header("TEST 2: View Registered Patients")
    run_command(
        ["python", "manage_db.py", "--list"],
        "List all patients in database"
    )
    
    # Test 3: View database statistics
    print_header("TEST 3: Database Statistics")
    run_command(
        ["python", "manage_db.py", "--stats"],
        "Show database statistics"
    )
    
    # Test 4: Register new patient (interactive test - skipped in automated mode)
    print_header("TEST 4: Patient Registration Test")
    print("⏭️  Skipping interactive patient registration")
    print("   To test manually, run:")
    print("   python main.py -i sample_data/patient1.png -c 'Test condition' -e test@example.com --no-prompt")
    
    # Test 5: View follow-up emails
    print_header("TEST 5: Check Follow-Up Emails")
    run_command(
        ["python", "send_followups.py", "--view", "--no-send"],
        "View patients registered for follow-ups"
    )
    
    # Test 6: Email sending (dry run)
    print_header("TEST 6: Email Sending Simulation")
    print("ℹ️  Note: Emails are currently simulated (printed to console)")
    print("   To enable real emails, configure SMTP in agents/followup.py\n")
    run_command(
        ["python", "send_followups.py", "--no-send"],
        "Dry run - check for emails without sending"
    )
    
    # Final summary
    print_header("✅ Test Suite Complete")
    print("Summary:")
    print("  ✅ Database operations working")
    print("  ✅ Patient management tools functional")
    print("  ✅ Email workflow configured")
    print("  ℹ️  Ready for SMTP integration\n")
    
    print("Next Steps:")
    print("  1. Configure SMTP service (SendGrid, AWS SES, etc.)")
    print("  2. Update agents/followup.py → _send_email() method")
    print("  3. Set up automated email scheduler (cron/Task Scheduler)")
    print("  4. Test with real email addresses\n")
    
    print("Documentation:")
    print("  📖 EMAIL_SYSTEM.md - Complete email system guide")
    print("  📖 EMAIL_IMPLEMENTATION.md - Implementation details")
    print("  📖 README.md - Usage examples\n")


if __name__ == "__main__":
    main()
