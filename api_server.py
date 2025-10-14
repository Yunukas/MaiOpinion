"""
Flask API Backend for MaiOpinion
Handles image upload and diagnostic processing with SSE streaming
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path to import agents
sys.path.insert(0, str(Path(__file__).parent))

from agents.detection import ImageDetectionAgent
from agents.diagnostic_router import DiagnosticRouter
from agents.reasoning import ReasoningAgent
from agents.treatment import TreatmentAgent
from agents.followup import FollowUpAgent

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def send_sse(data):
    """Send Server-Sent Event"""
    return f"data: {json.dumps(data)}\n\n"


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'MaiOpinion API is running'})


@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """Main diagnostic endpoint with SSE streaming"""
    
    # Validate request BEFORE entering generator
    if 'image' not in request.files:
        return Response(send_sse({'type': 'error', 'message': 'No image file provided'}), 
                       mimetype='text/event-stream')
    
    if 'condition' not in request.form:
        return Response(send_sse({'type': 'error', 'message': 'No condition description provided'}), 
                       mimetype='text/event-stream')
    
    file = request.files['image']
    condition = request.form['condition']
    email = request.form.get('email', None)
    
    if file.filename == '':
        return Response(send_sse({'type': 'error', 'message': 'No file selected'}), 
                       mimetype='text/event-stream')
    
    if not allowed_file(file.filename):
        return Response(send_sse({'type': 'error', 'message': 'Invalid file type'}), 
                       mimetype='text/event-stream')
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    def generate(filepath, condition, email, filename):
        try:
            # Initialize agents
            detection_agent = ImageDetectionAgent()
            diagnostic_router = DiagnosticRouter()
            reasoning_agent = ReasoningAgent()
            treatment_agent = TreatmentAgent()
            followup_agent = FollowUpAgent()
            
            # Step 1: Image Detection
            yield send_sse({
                'type': 'step_start',
                'step': 1,
                'message': 'Detecting image type and body part...'
            })
            
            detection_info = detection_agent.detect_image_type(filepath, condition)
            
            yield send_sse({
                'type': 'step_complete',
                'step': 1,
                'message': f"Detected: {detection_info['image_type']} ({detection_info['confidence']} confidence)",
                'result': f"{detection_info['image_type']} - {detection_info['body_part']}"
            })
            
            # Step 2: Specialized Diagnostic
            yield send_sse({
                'type': 'step_start',
                'step': 2,
                'message': 'Routing to specialized diagnostic agent...'
            })
            
            diagnostic_result = diagnostic_router.route_and_analyze(
                filepath, condition, detection_info
            )
            diagnostic_output = diagnostic_result['findings']
            
            yield send_sse({
                'type': 'step_complete',
                'step': 2,
                'message': f"Analysis complete using {diagnostic_result['agent_used']}",
                'result': diagnostic_output[:200] + '...' if len(diagnostic_output) > 200 else diagnostic_output
            })
            
            # Step 3: Clinical Reasoning
            yield send_sse({
                'type': 'step_start',
                'step': 3,
                'message': 'Analyzing findings to generate diagnosis...'
            })
            
            reasoning_output = reasoning_agent.process(diagnostic_output, condition)
            
            yield send_sse({
                'type': 'step_complete',
                'step': 3,
                'message': f"Diagnosis: {reasoning_output['diagnosis']}",
                'result': f"{reasoning_output['diagnosis']} (Confidence: {reasoning_output['confidence']})"
            })
            
            # Step 4: Treatment Planning
            yield send_sse({
                'type': 'step_start',
                'step': 4,
                'message': 'Creating treatment plan...'
            })
            
            treatment_output = treatment_agent.process(reasoning_output)
            
            yield send_sse({
                'type': 'step_complete',
                'step': 4,
                'message': 'Treatment plan generated',
                'result': treatment_output['treatment'][:150] + '...' if len(treatment_output['treatment']) > 150 else treatment_output['treatment']
            })
            
            # Step 5: Follow-Up Care
            yield send_sse({
                'type': 'step_start',
                'step': 5,
                'message': 'Generating follow-up care plan...'
            })
            
            followup_output = followup_agent.process(
                treatment_output,
                reasoning_output,
                patient_email=email,
                condition=condition
            )
            
            yield send_sse({
                'type': 'step_complete',
                'step': 5,
                'message': f"Follow-up timeline: {followup_output.get('timeline', 'N/A')}",
                'result': followup_output['follow_up'][:150] + '...' if len(followup_output['follow_up']) > 150 else followup_output['follow_up']
            })
            
            # Generate final report
            final_report = {
                "timestamp": detection_info.get('timestamp', ''),
                "patient_condition": condition,
                "image_analyzed": filename,
                "image_type": detection_info.get("image_type"),
                "body_part": detection_info.get("body_part"),
                "imaging_modality": detection_info.get("imaging_modality"),
                "detection_confidence": detection_info.get("confidence"),
                "finding": diagnostic_output,
                "diagnosis": reasoning_output.get("diagnosis"),
                "confidence": reasoning_output.get("confidence"),
                "treatment": treatment_output.get("treatment"),
                "precautions": treatment_output.get("precautions", []),
                "follow_up": followup_output.get("follow_up"),
                "timeline": followup_output.get("timeline"),
                "patient_instructions": followup_output.get("patient_instructions"),
                "agent_workflow": {
                    "step_1": "Image Detection Agent",
                    "step_2": diagnostic_result.get('agent_used', 'Diagnostic Agent'),
                    "step_3": "Clinical Reasoning Agent",
                    "step_4": "Treatment Agent",
                    "step_5": "Follow-Up Agent"
                }
            }
            
            yield send_sse({
                'type': 'complete',
                'report': final_report
            })
                
        except Exception as e:
            yield send_sse({
                'type': 'error',
                'message': str(e)
            })
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return Response(generate(filepath, condition, email, filename), mimetype='text/event-stream')


if __name__ == '__main__':
    print("=" * 80)
    print("MaiOpinion API Server")
    print("=" * 80)
    print("\nStarting Flask server on http://localhost:5000")
    print("API Endpoints:")
    print("  - GET  /api/health   - Health check")
    print("  - POST /api/diagnose - Diagnostic endpoint")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80)
    
    app.run(debug=True, port=5000, threaded=True)
