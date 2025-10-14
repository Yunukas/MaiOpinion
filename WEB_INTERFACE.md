# MaiOpinion Web Interface - Quick Start

## 🚀 You now have a complete web application!

### What's Been Created

✅ **Backend API Server** (`api_server.py`)
- Flask server with SSE (Server-Sent Events) streaming
- `/api/diagnose` endpoint that processes images through 5 agent steps
- Real-time progress updates sent to frontend
- Automatic file cleanup and validation

✅ **React Frontend** (`frontend/`)
- Modern, responsive web UI
- Drag-and-drop file upload
- Real-time agent progress display
- Downloadable diagnostic reports
- Optional email follow-up feature

### Quick Start

**Option 1: PowerShell Script (Easiest)**
```powershell
.\start.ps1
```

**Option 2: Manual (Two Terminals)**

Terminal 1:
```powershell
python api_server.py
```

Terminal 2:
```powershell
cd frontend
npm install  # First time only
npm run dev
```

Then open: **http://localhost:3000**

### First Time Setup

1. **Install Backend Dependencies**
   ```powershell
   pip install -r requirements-api.txt
   ```

2. **Install Frontend Dependencies**
   ```powershell
   cd frontend
   npm install
   cd ..
   ```

3. **Verify .env File**
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

### How It Works

1. **Upload Image** - Drag & drop or click to select medical image
2. **Describe Condition** - Enter symptoms, pain level, duration
3. **Optional Email** - Toggle to receive follow-up reminders
4. **Submit** - Watch 5 agents work in real-time:
   - Step 1: Detecting image type...
   - Step 2: Specialized diagnostic analysis...
   - Step 3: Clinical reasoning...
   - Step 4: Treatment planning...
   - Step 5: Follow-up care scheduling...
5. **Download Report** - Get comprehensive PDF-ready report

### File Limits
- Max size: 16MB
- Formats: PNG, JPG, JPEG, GIF, BMP

### Ports
- Backend: http://localhost:5000
- Frontend: http://localhost:3000

### Troubleshooting

**"Cannot connect to backend"**
- Ensure backend is running on port 5000
- Check `python api_server.py` terminal for errors

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**"No progress updates"**
- Check browser console (F12)
- Verify SSE connection in Network tab

**"Import errors in Python"**
- Run: `pip install -r requirements-api.txt`

### Architecture Diagram

```
┌─────────────────┐
│   Web Browser   │
│  (localhost:3000)│
└────────┬────────┘
         │ HTTP + SSE
         ▼
┌─────────────────┐
│  Flask API      │
│  (localhost:5000)│
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│       Agent Pipeline (5 Steps)      │
├─────────────────────────────────────┤
│ 1. Image Detection Agent            │
│    ↓                                 │
│ 2. Diagnostic Router                │
│    ├→ Dental Agent                  │
│    ├→ Chest X-ray Agent             │
│    └→ Generic Agent                 │
│    ↓                                 │
│ 3. Clinical Reasoning Agent         │
│    ↓                                 │
│ 4. Treatment Agent                  │
│    ↓                                 │
│ 5. Follow-Up Agent                  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  GitHub Models  │
│  (GPT-4o, etc.) │
└─────────────────┘
```

### Key Features

🔍 **Smart Detection** - Automatically identifies dental, chest, brain, skin, bone images

🤖 **Specialized Agents** - Routes to appropriate medical specialist

⚡ **Real-time Updates** - See each agent's progress as it happens

📊 **Comprehensive Reports** - Detailed findings, diagnosis, treatment, follow-up

📧 **Email Reminders** - Optional follow-up care notifications

🎨 **Modern UI** - Clean, responsive design with TailwindCSS

### Next Steps

1. **Test the Application**
   - Upload a test image (chest X-ray, dental X-ray, etc.)
   - Try with different image types
   - Test email follow-up feature

2. **Customize**
   - Edit colors in `frontend/tailwind.config.js`
   - Modify components in `frontend/src/components/`
   - Add new specialized agents in `agents/`

3. **Deploy** (Optional)
   - Build frontend: `npm run build` in frontend/
   - Use production WSGI server for backend (gunicorn, waitress)
   - Configure HTTPS and proper CORS

### Important Notes

⚠️ **Educational Use Only** - Not for actual medical diagnosis
⚠️ **Not HIPAA Compliant** - Do not use with real patient data
⚠️ **API Costs** - Each request uses GitHub Models credits

### Support Files

- `SETUP.md` - Detailed setup instructions
- `README.md` - Full project documentation
- `requirements-api.txt` - Python dependencies
- `frontend/package.json` - JavaScript dependencies

---

**You're all set! Run `.\start.ps1` to launch the application. 🚀**
