# MaiOpinion Setup Guide

## Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

## Backend Setup

1. **Install Python Dependencies**
   ```powershell
   pip install -r requirements-api.txt
   ```

2. **Configure Environment Variables**
   - Ensure your `.env` file contains:
     ```
     GITHUB_TOKEN=your_github_token_here
     ```

3. **Start the API Server**
   ```powershell
   python api_server.py
   ```
   - Server will run on `http://localhost:5000`
   - Endpoints:
     - `GET /api/health` - Health check
     - `POST /api/diagnose` - Diagnostic processing with SSE streaming

## Frontend Setup

1. **Navigate to Frontend Directory**
   ```powershell
   cd frontend
   ```

2. **Install Dependencies**
   ```powershell
   npm install
   ```

3. **Start Development Server**
   ```powershell
   npm run dev
   ```
   - Frontend will run on `http://localhost:3000`
   - Vite proxy configured to forward `/api/*` requests to backend

## Running the Full Application

1. **Terminal 1 - Backend**
   ```powershell
   python api_server.py
   ```

2. **Terminal 2 - Frontend**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   - Open browser to `http://localhost:3000`
   - Upload medical image
   - Enter condition description
   - (Optional) Enable email follow-ups
   - Watch real-time agent progress
   - Download final diagnostic report

## Architecture

### Agent Pipeline (5 Steps)
1. **Image Detection Agent** - Identifies image type (dental, chest X-ray, brain scan, etc.)
2. **Specialized Diagnostic Agent** - Routes to appropriate specialist:
   - Dental Agent (cavities, gum disease, etc.)
   - Chest X-ray Agent (pneumonia, pleural effusion, etc.)
   - Generic Agent (brain, skin, bones)
3. **Clinical Reasoning Agent** - Generates diagnosis from findings
4. **Treatment Agent** - Creates treatment plan
5. **Follow-Up Agent** - Schedules follow-up care and reminders

### Technology Stack
- **Backend**: Flask, OpenAI SDK, GitHub Models
- **Frontend**: React 18, Vite, TailwindCSS, Axios
- **Communication**: Server-Sent Events (SSE) for real-time updates
- **Image Processing**: PIL/Pillow

## Supported Image Types
- Dental X-rays
- Chest X-rays
- Brain scans (CT/MRI)
- Skin lesions
- Bone X-rays
- Eye scans
- Ultrasound
- Other medical images

## File Upload Limits
- Maximum file size: 16MB
- Supported formats: PNG, JPG, JPEG, GIF, BMP

## Troubleshooting

### Backend Issues
- **Port 5000 in use**: Change port in `api_server.py` line `app.run(port=5000)`
- **Import errors**: Run `pip install -r requirements-api.txt`
- **Agent errors**: Check `.env` file has valid `GITHUB_TOKEN`

### Frontend Issues
- **Port 3000 in use**: Change port in `frontend/vite.config.js`
- **CORS errors**: Ensure backend is running on port 5000
- **Blank screen**: Check browser console for errors, verify backend is running

### SSE Streaming Issues
- **No progress updates**: Check network tab for `/api/diagnose` SSE connection
- **Connection closed**: Backend might have crashed, check terminal logs
- **Incomplete data**: Increase browser's SSE buffer or check backend error logs

## Development Notes

### Adding New Specialized Agents
1. Create new agent file in `agents/` directory
2. Implement `analyze(image_path, condition)` method
3. Update `agents/diagnostic_router.py` to route to new specialist
4. Update `agents/detection.py` if new image type needed

### Customizing Frontend
- Colors: Edit `frontend/tailwind.config.js`
- Components: Modify files in `frontend/src/components/`
- API endpoint: Update `frontend/src/App.jsx` line with fetch URL

### Mock Mode
- Detection agent supports mock mode (no API calls)
- Set `use_mock=True` in `ImageDetectionAgent()` initialization
- Useful for testing without consuming API credits

## Production Deployment

### Backend
- Use production WSGI server (gunicorn, waitress)
- Configure proper CORS settings
- Set up proper logging
- Use environment variables for configuration

### Frontend
- Build production bundle: `npm run build`
- Serve static files via nginx/Apache
- Update API URL for production backend

### Security
- Validate all file uploads
- Implement rate limiting
- Add authentication/authorization
- Use HTTPS in production
- Sanitize user inputs
- Store uploaded files securely (temp files auto-deleted)

## License
See LICENSE file for details.
