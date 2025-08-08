from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import subprocess
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
INPUT_DIR = "input"
DOCS_DIR = os.path.join(INPUT_DIR, "documents")
PERSONA_FILE = os.path.join(INPUT_DIR, "persona.txt")
JOB_FILE = os.path.join(INPUT_DIR, "job_to_be_done.txt")
OUTPUT_FILE = os.path.join("output", "output.json")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)

# Helper to save uploaded files and text
def save_input_files(persona, job, files):
    # Save persona
    if persona is not None:
        with open(PERSONA_FILE, 'w', encoding='utf-8') as f:
            f.write(persona)
    # Save job
    if job is not None:
        with open(JOB_FILE, 'w', encoding='utf-8') as f:
            f.write(job)
    # Save documents
    if files:
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(DOCS_DIR, filename))

# Endpoint to receive persona, job, and documents
@app.route('/api/upload_input', methods=['POST'])
def upload_input():
    try:
        # Clear documents folder before new upload
        if os.path.exists(DOCS_DIR):
            for file in os.listdir(DOCS_DIR):
                file_path = os.path.join(DOCS_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        persona = request.form.get('persona')
        job = request.form.get('jobToBeDone')
        files = request.files.getlist('documents')
        save_input_files(persona, job, files)
        return jsonify({'success': True, 'message': 'Input files updated.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_documents():
    try:
        # Run backend analysis first
        analysis_result = run_backend_analysis()
        if not analysis_result.get('success'):
            # Return full error details from analysis
            return jsonify({'success': False, 'error': analysis_result.get('error', 'Unknown error'), 'details': analysis_result}), 500

        # Fallback: If output.json is empty, write a default output
        if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) == 0:
            default_output = {
                "metadata": {
                    "input_documents": [],
                    "processing_timestamp": "N/A"
                },
                "extracted_sections": [],
                "subsection_analysis": []
            }
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_output, f)

        # Then read and return output.json
        output_text = format_output_for_display()
        # If output_text contains error, return as error
        if output_text.startswith('Error') or output_text.startswith('No output generated'):
            return jsonify({'success': False, 'error': output_text}), 500

        return jsonify({
            'success': True,
            'output': output_text,
            'files_processed': os.listdir(DOCS_DIR)
        })
    except Exception as e:
        # Return full exception details
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_output():
    """Test endpoint to directly read and return output.json"""
    try:
        output_text = format_output_for_display()
        return jsonify({
            'success': True,
            'output': output_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def clear_previous_files():
    """Clear previous persona, job, and documents"""
    # Clear persona and job files
    if os.path.exists(PERSONA_FILE):
        os.remove(PERSONA_FILE)
    if os.path.exists(JOB_FILE):
        os.remove(JOB_FILE)
    
    # Clear documents directory
    if os.path.exists(DOCS_DIR):
        for file in os.listdir(DOCS_DIR):
            file_path = os.path.join(DOCS_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

def run_backend_analysis():
    """Run the backend analysis script"""
    try:
        # Run the main.py script
        result = subprocess.run(
            ['python', 'src/main.py'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            return {'success': True}
        else:
            return {
                'success': False,
                'error': f'Backend analysis failed: {result.stderr}'
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error running backend analysis: {str(e)}'
        }

def format_output_for_display():
    """Read output.json and format it as readable text"""
    try:
        if not os.path.exists(OUTPUT_FILE):
            return "No output generated - file not found at: " + OUTPUT_FILE

        # Check if file is empty
        if os.path.getsize(OUTPUT_FILE) == 0:
            return "No output generated - file is empty: " + OUTPUT_FILE

        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                return f"Error reading output: {str(e)}\nFile path: {OUTPUT_FILE}"

        # Format the output as readable text
        output_lines = []

        # Metadata
        output_lines.append("=== DOCUMENT ANALYSIS RESULTS ===\n")
        output_lines.append(f"Documents Processed: {', '.join(data.get('metadata', {}).get('input_documents', []))}")
        output_lines.append(f"Processing Time: {data.get('metadata', {}).get('processing_timestamp', 'N/A')}\n")

        # Extracted Sections
        output_lines.append("=== TOP EXTRACTED SECTIONS ===\n")
        for section in data.get('extracted_sections', []):
            output_lines.append(f"{section.get('importance_rank', '?')}. {section.get('section_title', '')}")
            output_lines.append(f"   Document: {section.get('document', '')}")
            output_lines.append(f"   Page: {section.get('page_number', '')}\n")

        # Subsection Analysis
        output_lines.append("=== DETAILED ANALYSIS ===\n")
        for i, analysis in enumerate(data.get('subsection_analysis', []), 1):
            output_lines.append(f"{i}. Document: {analysis.get('document', '')}")
            output_lines.append(f"   Page: {analysis.get('page_number', '')}")
            output_lines.append(f"   Analysis: {analysis.get('refined_text', '')}\n")

        return '\n'.join(output_lines)

    except Exception as e:
        return f"Error reading output: {str(e)}\nFile path: {OUTPUT_FILE}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
