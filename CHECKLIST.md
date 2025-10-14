# MaiOpinion - Complete Setup Checklist

## ✅ System Requirements

- [ ] Python 3.11 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] Git installed (optional, for version control)
- [ ] GitHub Personal Access Token obtained

## ✅ Backend Setup

- [ ] Virtual environment created (`.venv` folder exists)
- [ ] Python dependencies installed (`pip install -r requirements-api.txt`)
- [ ] `.env` file created with `GITHUB_TOKEN`
- [ ] Backend packages verified:
  ```powershell
  python -c "import flask, werkzeug, PIL; print('✅ All packages installed')"
  ```

## ✅ Frontend Setup

- [ ] Node.js installed and verified (`node --version`)
- [ ] Frontend directory exists (`frontend/` folder)
- [ ] Frontend dependencies installed (`cd frontend && npm install`)
- [ ] Frontend packages verified:
  ```powershell
  cd frontend
  npm list react vite tailwindcss
  ```

## ✅ File Structure Verification

```
MaiOpinion/
├── .env                          ✅ Environment variables
├── .venv/                        ✅ Python virtual environment
├── agents/
│   ├── detection.py              ✅ Image detection agent
│   ├── diagnostic_router.py      ✅ Routing logic
│   ├── diagnostic_dental.py      ✅ Dental specialist
│   ├── diagnostic_chest.py       ✅ Chest specialist
│   ├── diagnostic_generic.py     ✅ Generic specialist
│   ├── reasoning.py              ✅ Clinical reasoning
│   ├── treatment.py              ✅ Treatment planning
│   └── followup.py               ✅ Follow-up care
├── frontend/
│   ├── node_modules/             ✅ Frontend dependencies
│   ├── src/
│   │   ├── components/           ✅ React components
│   │   ├── App.jsx               ✅ Main application
│   │   └── main.jsx              ✅ Entry point
│   ├── package.json              ✅ Dependencies
│   └── vite.config.js            ✅ Vite config
├── api_server.py                 ✅ Flask API server
├── main.py                       ✅ CLI entry point
├── test_api.py                   ✅ API test script
├── start.ps1                     ✅ Quick start script
├── requirements-api.txt          ✅ Python dependencies
├── README.md                     ✅ Documentation
├── SETUP.md                      ✅ Setup guide
└── WEB_INTERFACE.md              ✅ Web interface guide
```

## ✅ Testing Backend

1. [ ] Start backend server:
   ```powershell
   python api_server.py
   ```

2. [ ] Backend runs without errors
3. [ ] See message: "Running on http://localhost:5000"
4. [ ] Run API tests (in new terminal):
   ```powershell
   python test_api.py
   ```

5. [ ] All tests pass ✅

## ✅ Testing Frontend

1. [ ] Navigate to frontend:
   ```powershell
   cd frontend
   ```

2. [ ] Start dev server:
   ```powershell
   npm run dev
   ```

3. [ ] Frontend runs without errors
4. [ ] See message: "Local: http://localhost:3000"
5. [ ] Open browser to http://localhost:3000
6. [ ] Page loads with "MaiOpinion" header
7. [ ] Upload area is visible
8. [ ] No console errors (press F12)

## ✅ End-to-End Testing

1. [ ] Both backend and frontend running
2. [ ] Navigate to http://localhost:3000
3. [ ] Upload test image (any medical image or photo)
4. [ ] Enter test condition: "Testing the system - chest pain"
5. [ ] Click "Analyze Medical Case"
6. [ ] See 5 steps progress in real-time:
   - [ ] Step 1: Detecting image type...
   - [ ] Step 2: Specialized diagnostic...
   - [ ] Step 3: Clinical reasoning...
   - [ ] Step 4: Treatment planning...
   - [ ] Step 5: Follow-up care...
7. [ ] Final report appears
8. [ ] Download button works
9. [ ] No errors in browser console
10. [ ] No errors in backend terminal

## ✅ Optional: Email Follow-up Testing

1. [ ] Toggle "Send follow-up reminders" checkbox
2. [ ] Enter test email
3. [ ] Submit diagnosis
4. [ ] Check report includes follow-up instructions

## ✅ Quick Start Script Testing

1. [ ] Run PowerShell script:
   ```powershell
   .\start.ps1
   ```

2. [ ] Backend starts automatically
3. [ ] Frontend starts automatically
4. [ ] Both servers running without errors

## 🔧 Troubleshooting Checklist

### Backend Issues

- [ ] **Port 5000 in use**
  - Close other applications using port 5000
  - Or change port in `api_server.py`: `app.run(port=5001)`

- [ ] **Import errors**
  - Verify virtual environment: `python -c "import sys; print(sys.prefix)"`
  - Reinstall: `pip install -r requirements-api.txt`

- [ ] **No .env file**
  - Create: `echo "GITHUB_TOKEN=your_token" > .env`
  - Verify: `type .env` (should show token)

- [ ] **GitHub token invalid**
  - Check token: https://github.com/settings/tokens
  - Ensure token has correct permissions

### Frontend Issues

- [ ] **Port 3000 in use**
  - Change in `vite.config.js`: `port: 3001`

- [ ] **npm install fails**
  - Clear cache: `npm cache clean --force`
  - Delete `node_modules`: `rm -r node_modules`
  - Reinstall: `npm install`

- [ ] **Vite errors**
  - Check Node version: `node --version` (should be 18+)
  - Update npm: `npm install -g npm@latest`

- [ ] **CORS errors**
  - Ensure backend is on port 5000
  - Check `vite.config.js` proxy configuration

### SSE Streaming Issues

- [ ] **No progress updates**
  - Open browser DevTools (F12)
  - Check Network tab → `/api/diagnose` → EventStream
  - Look for "data: {..." messages

- [ ] **Connection closed**
  - Check backend terminal for errors
  - Verify agent pipeline isn't crashing

## 📊 Performance Checklist

- [ ] Image processing takes < 60 seconds
- [ ] UI remains responsive during processing
- [ ] No memory leaks in browser (check Task Manager)
- [ ] Backend terminal shows no errors

## 🚀 Production Ready Checklist

### Security

- [ ] Remove debug mode: `app.run(debug=False)`
- [ ] Configure CORS properly (specific origins)
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Use HTTPS

### Performance

- [ ] Use production WSGI server (gunicorn, waitress)
- [ ] Build frontend: `npm run build`
- [ ] Enable gzip compression
- [ ] Configure caching headers

### Monitoring

- [ ] Set up logging
- [ ] Add error tracking (Sentry, etc.)
- [ ] Monitor API usage
- [ ] Set up health checks

## 📝 Final Verification

Run all commands in sequence:

```powershell
# 1. Backend health check
python test_api.py

# 2. Start backend (Terminal 1)
python api_server.py

# 3. Start frontend (Terminal 2)
cd frontend
npm run dev

# 4. Open browser
start http://localhost:3000

# 5. Upload test image and verify
```

## ✅ Success Criteria

- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] File upload works
- [ ] 5-step progress displays
- [ ] Final report generates
- [ ] Download button works
- [ ] No console errors
- [ ] No server errors

---

**When all items are checked, your MaiOpinion system is fully operational! 🎉**

## 🆘 Still Having Issues?

1. Check all terminals for error messages
2. Review browser console (F12) for JavaScript errors
3. Verify `.env` file has valid GitHub token
4. Ensure all dependencies installed correctly
5. Try restarting both servers
6. Check firewall isn't blocking ports 3000 or 5000

## 📞 Support

Refer to documentation:
- `SETUP.md` - Detailed setup guide
- `WEB_INTERFACE.md` - Web interface quick start
- `README.md` - Full project documentation
