# InsightLens - AI Document Analysis System

A full-stack application that analyzes PDF documents using AI to extract insights based on user personas and job requirements.

## Features

- **Frontend**: React-based UI with drag-and-drop PDF upload
- **Backend**: Python Flask API with AI-powered document analysis
- **Document Processing**: PDF-only support with intelligent section extraction
- **Analysis**: Context-aware insights based on persona and job requirements

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend server will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Fill in the form**:
   - **Persona**: Describe the target user (e.g., "A busy professional looking for quick insights")
   - **Job to be Done**: Describe what the user is trying to accomplish
   - **Upload Documents**: Drag and drop PDF files (only PDFs are supported)

3. **Click "Analyze Documents"** to start the analysis

4. **View Results**: The analysis results will be displayed in a readable text format

## How It Works

1. **File Upload**: PDF documents are uploaded to the backend
2. **Text Extraction**: Documents are processed to extract text and sections
3. **AI Analysis**: The system analyzes content based on the provided persona and job requirements
4. **Results**: Formatted analysis results are displayed to the user

## File Structure

```
InsightLens/
├── backend/
│   ├── app.py              # Flask API server
│   ├── src/                # Core analysis modules
│   ├── input/              # Input files (persona.txt, job_to_be_done.txt, documents/)
│   ├── output/             # Analysis output
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/                # React components
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md
```

## API Endpoints

- `POST /api/process` - Process documents and generate analysis

## Requirements

- Python 3.8+
- Node.js 16+
- PDF files for analysis

## Notes

- Only PDF files are supported for document upload
- Previous analysis files are automatically cleared before each new analysis
- Results are displayed in a human-readable text format, not JSON
