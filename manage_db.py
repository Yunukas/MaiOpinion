"""
Patient Database Manager
Utility script for managing the MaiOpinion patient database
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


DB_PATH = Path("patients_db.csv")


def view_all_patients():
    """Display all patients in a formatted table"""
    if not DB_PATH.exists():
        print("❌ No patient database found.")
        return
    
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        patients = list(reader)
    
    if not patients:
        print("📭 No patients registered yet.")
        return
    
    print("\n" + "=" * 120)
    print(f"👥 PATIENT DATABASE - {len(patients)} Patient(s) Registered")
    print("=" * 120)
    
    # Print header
    print(f"\n{'#':<4} {'Patient ID':<20} {'Email':<30} {'Condition':<25} {'Follow-Up':<12} {'Sent':<6}")
    print("-" * 120)
    
    # Print patients
    for i, patient in enumerate(patients, 1):
        print(f"{i:<4} {patient['patient_id']:<20} {patient['email']:<30} "
              f"{patient['condition'][:22]+'...' if len(patient['condition']) > 25 else patient['condition']:<25} "
              f"{patient['follow_up_date']:<12} {'✅' if patient['email_sent'] == 'Yes' else '❌':<6}")
    
    print("-" * 120 + "\n")


def view_patient_details(patient_id: str):
    """Display detailed information for a specific patient"""
    if not DB_PATH.exists():
        print("❌ No patient database found.")
        return
    
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for patient in reader:
            if patient['patient_id'] == patient_id:
                print("\n" + "=" * 80)
                print(f"📋 PATIENT DETAILS: {patient_id}")
                print("=" * 80)
                print(f"\n📧 Email:            {patient['email']}")
                print(f"📅 Registered:       {patient['created_at']}")
                print(f"🩺 Condition:        {patient['condition']}")
                print(f"🔬 Diagnosis:        {patient['diagnosis']}")
                print(f"\n💊 Treatment Plan:")
                print(f"   {patient['treatment']}")
                print(f"\n📅 Follow-Up:")
                print(f"   Timeline:         {patient['follow_up_timeline']}")
                print(f"   Scheduled Date:   {patient['follow_up_date']}")
                print(f"   Email Sent:       {'✅ Yes' if patient['email_sent'] == 'Yes' else '❌ No'}")
                print("\n" + "=" * 80 + "\n")
                return
    
    print(f"❌ Patient ID '{patient_id}' not found.")


def count_statistics():
    """Display database statistics"""
    if not DB_PATH.exists():
        print("❌ No patient database found.")
        return
    
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        patients = list(reader)
    
    if not patients:
        print("📭 No patients registered yet.")
        return
    
    total = len(patients)
    sent = sum(1 for p in patients if p['email_sent'] == 'Yes')
    pending = total - sent
    
    # Count by follow-up status
    today = datetime.now().date()
    overdue = 0
    upcoming = 0
    
    for p in patients:
        if p['email_sent'] == 'No':
            follow_date = datetime.strptime(p['follow_up_date'], '%Y-%m-%d').date()
            if follow_date < today:
                overdue += 1
            else:
                upcoming += 1
    
    print("\n" + "=" * 60)
    print("📊 DATABASE STATISTICS")
    print("=" * 60)
    print(f"\n📈 Total Patients:        {total}")
    print(f"✅ Emails Sent:           {sent}")
    print(f"⏳ Pending Emails:        {pending}")
    print(f"\n⚠️  Overdue Follow-ups:   {overdue}")
    print(f"📅 Upcoming Follow-ups:   {upcoming}")
    print("\n" + "=" * 60 + "\n")


def clear_database():
    """Clear all patient data (with confirmation)"""
    if not DB_PATH.exists():
        print("❌ No patient database found.")
        return
    
    print("\n⚠️  WARNING: This will delete ALL patient data!")
    confirm = input("Type 'DELETE' to confirm: ")
    
    if confirm == "DELETE":
        DB_PATH.unlink()
        print("✅ Patient database deleted.")
    else:
        print("❌ Operation cancelled.")


def export_to_csv(output_path: str):
    """Export database to a different location"""
    if not DB_PATH.exists():
        print("❌ No patient database found.")
        return
    
    import shutil
    shutil.copy(DB_PATH, output_path)
    print(f"✅ Database exported to: {output_path}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MaiOpinion Patient Database Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_db.py --list              # List all patients
  python manage_db.py --stats             # Show statistics
  python manage_db.py --view PT12345      # View patient details
  python manage_db.py --export backup.csv # Export database
  python manage_db.py --clear             # Clear database (dangerous!)
        """
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all registered patients'
    )
    
    parser.add_argument(
        '--stats', '-s',
        action='store_true',
        help='Show database statistics'
    )
    
    parser.add_argument(
        '--view', '-v',
        metavar='PATIENT_ID',
        help='View detailed information for a patient'
    )
    
    parser.add_argument(
        '--export', '-e',
        metavar='OUTPUT_FILE',
        help='Export database to file'
    )
    
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all patient data (requires confirmation)'
    )
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # Execute commands
    if args.list:
        view_all_patients()
    
    if args.stats:
        count_statistics()
    
    if args.view:
        view_patient_details(args.view)
    
    if args.export:
        export_to_csv(args.export)
    
    if args.clear:
        clear_database()


if __name__ == "__main__":
    main()
