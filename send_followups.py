"""
Send Follow-Up Emails Script
Checks patient database and sends scheduled follow-up reminders
"""

import sys
from pathlib import Path
from datetime import datetime
from agents.followup import FollowUpAgent

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def send_scheduled_emails():
    """Check and send all scheduled follow-up emails"""
    print("=" * 80)
    print("📧 MaiOpinion - Follow-Up Email Scheduler")
    print("=" * 80)
    print(f"Current Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if database exists
    db_path = Path("patients_db.csv")
    if not db_path.exists():
        print("❌ No patient database found (patients_db.csv)")
        print("   Run a diagnosis with email registration first.")
        return
    
    # Initialize Follow-Up Agent
    agent = FollowUpAgent()
    
    # Send scheduled emails
    print("\nChecking for patients due for follow-up...")
    print("-" * 80)
    
    emails_sent = agent.send_follow_up_emails()
    
    print("-" * 80)
    if emails_sent > 0:
        print(f"\n✅ Successfully sent {emails_sent} follow-up email(s)!")
    else:
        print("\n📭 No follow-up emails due at this time.")
    
    print("\n" + "=" * 80)


def view_patient_database():
    """View all registered patients"""
    import csv
    
    db_path = Path("patients_db.csv")
    if not db_path.exists():
        print("❌ No patient database found")
        return
    
    print("\n" + "=" * 80)
    print("👥 REGISTERED PATIENTS")
    print("=" * 80 + "\n")
    
    with open(db_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        patients = list(reader)
    
    if not patients:
        print("No patients registered yet.")
        return
    
    for i, patient in enumerate(patients, 1):
        print(f"Patient #{i}")
        print(f"  ID: {patient['patient_id']}")
        print(f"  Email: {patient['email']}")
        print(f"  Condition: {patient['condition']}")
        print(f"  Diagnosis: {patient['diagnosis']}")
        print(f"  Follow-up Date: {patient['follow_up_date']}")
        print(f"  Email Sent: {'✅ Yes' if patient['email_sent'] == 'Yes' else '❌ No'}")
        print(f"  Registered: {patient['created_at']}")
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MaiOpinion Follow-Up Email Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python send_followups.py                    # Send scheduled emails
  python send_followups.py --view             # View patient database
  python send_followups.py --send --view      # Send emails and view database
        """
    )
    
    parser.add_argument(
        '--send',
        action='store_true',
        default=True,
        help='Send scheduled follow-up emails (default)'
    )
    
    parser.add_argument(
        '--view', '-v',
        action='store_true',
        help='View registered patients in database'
    )
    
    parser.add_argument(
        '--no-send',
        action='store_true',
        help='Skip sending emails (useful with --view)'
    )
    
    args = parser.parse_args()
    
    # View database if requested
    if args.view:
        view_patient_database()
    
    # Send emails unless explicitly disabled
    if not args.no_send:
        send_scheduled_emails()


if __name__ == "__main__":
    main()
