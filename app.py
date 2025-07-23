from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import json
from resume_parser import extract_text_from_pdf, extract_text_from_docx, parse_resume_text, process_resume_file
from job_matcher import analyze_job_match

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')

# Add this route to app.py
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        # Validate file upload
        if 'resume' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Process the resume file with AI parsing
                parsed_results = process_resume_file(filepath)
                
                # Add job matching analysis if job description provided
                if job_description.strip():
                    job_match_results = analyze_job_match(parsed_results, job_description)
                    parsed_results['job_match'] = job_match_results
                
                # Clean up uploaded file after successful processing
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                return jsonify({
                    'success': True,
                    'results': parsed_results
                })
                
            except Exception as parsing_error:
                # Clean up file on parsing error
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': f'Error parsing resume: {str(parsing_error)}'}), 500
        
        else:
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOC, or DOCX files.'}), 400
            
    except Exception as e:
        return jsonify({'error': f'An error occurred during file upload: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 AI Resume Parser starting...")
    print("📄 Navigate to http://localhost:5000 to use the application")
    print("🧠 AI-powered resume parsing enabled!")
    app.run(debug=True, host='0.0.0.0', port=5000)