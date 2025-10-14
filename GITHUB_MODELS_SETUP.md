# 🔑 GitHub Models Setup Instructions

## Quick Setup (Choose One Method)

### Method 1: Add Token to .env File (Recommended)

1. Open `.env` file
2. Find the line with `# GITHUB_TOKEN=your_github_token_here`
3. Uncomment it and add your GitHub Personal Access Token:
   ```
   GITHUB_TOKEN=github_pat_YOUR_ACTUAL_TOKEN_HERE
   ```
4. Save the file
5. Run: `python main.py --image sample_data/patient1.png --condition "Tooth pain"`

### Method 2: Use Environment Variable

**PowerShell:**
```powershell
$env:GITHUB_TOKEN="github_pat_YOUR_TOKEN_HERE"
python main.py --image sample_data/patient1.png --condition "Tooth pain"
```

**CMD:**
```cmd
set GITHUB_TOKEN=github_pat_YOUR_TOKEN_HERE
python main.py --image sample_data/patient1.png --condition "Tooth pain"
```

## How to Get a GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "MaiOpinion Hackathon"
4. Select scopes (no specific scopes needed for Models API)
5. Click "Generate token"
6. Copy the token (starts with `github_pat_...` or `ghp_...`)

## What GitHub Models Provides

- ✅ Free access to GPT-4o-mini and other models
- ✅ Great for hackathons and testing
- ✅ No credit card required
- ✅ Uses `https://models.inference.ai.azure.com` endpoint

## Current Configuration

The `.env` file is configured to use GitHub Models with:
- **Endpoint:** https://models.inference.ai.azure.com
- **Model:** gpt-4o-mini
- **Enabled:** USE_GITHUB_MODELS=true

## Test Without GitHub Token

The system still works perfectly in **mock mode** if no token is provided:
```bash
python main.py --image sample_data/patient1.png --condition "Tooth pain"
```

Mock responses are intelligent and work great for demos!

## Verify GitHub Models is Working

When running with GitHub token, you should see:
```
[Clinical Reasoning Agent] Using GitHub Models (token: github_pat...)
[Treatment Agent] Using GitHub Models (token: github_pat...)
[Follow-Up Agent] Using GitHub Models (token: github_pat...)
```

## Troubleshooting

**"WARNING: No API keys found"**
- Token not found in .env or environment
- System will use mock responses instead

**API Error:**
- Check token is valid
- Ensure you have GitHub Models access
- Try regenerating token

**Still want to test?**
- Mock mode works without any tokens!
- Just run the command and see intelligent responses

---

**Ready to use GitHub Models? Add your token and run!** 🚀
