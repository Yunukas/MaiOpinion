"""
Setup GitHub Models for MaiOpinion
This script helps configure GitHub Models authentication
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def setup_github_models():
    """Setup GitHub Models configuration"""
    print("=" * 80)
    print("MaiOpinion - GitHub Models Setup")
    print("=" * 80)
    print()
    
    # Load existing .env
    env_path = Path(".env")
    load_dotenv()
    
    # Check for existing GitHub token in environment
    github_token = os.getenv("GITHUB_TOKEN")
    
    if github_token and github_token != "your_github_token_here":
        print(f"✅ GitHub token found in environment!")
        print(f"   Token: {github_token[:10]}...")
        
        # Update .env file
        env_content = env_path.read_text() if env_path.exists() else ""
        
        if "GITHUB_TOKEN=your_github_token_here" in env_content:
            env_content = env_content.replace(
                "GITHUB_TOKEN=your_github_token_here",
                f"GITHUB_TOKEN={github_token}"
            )
            env_path.write_text(env_content)
            print("✅ Updated .env file with your GitHub token")
        
        print("\n✅ GitHub Models is now configured!")
        print("\nYou can now use:")
        print("  python main.py --image sample_data/patient1.png --condition \"Tooth pain for 3 days\"")
        
    else:
        print("ℹ️  No GitHub token found in environment.")
        print("\nTo use GitHub Models:")
        print("1. Get a GitHub Personal Access Token")
        print("2. Set it in your .env file:")
        print("   GITHUB_TOKEN=your_actual_token")
        print("   USE_GITHUB_MODELS=true")
        print("\nOr the system will use mock responses (which still work great for demos!)")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    setup_github_models()
