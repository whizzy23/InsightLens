# InsightLens Frontend

A React-based frontend application for the InsightLens document analysis system.

## Features

- **Persona Input**: Text area for describing the target persona
- **Job to be Done Input**: Text area for describing what the user is trying to accomplish
- **Document Upload**: Drag-and-drop file upload with support for PDF, DOC, DOCX, and TXT files
- **Analysis Results**: Tabbed interface displaying:
  - Executive Summary
  - Key Insights
  - Recommendations
  - Detailed Analysis
  - Raw Data

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

## API Integration

The frontend is configured to communicate with the backend API running on `http://localhost:5000`. The Vite configuration includes a proxy to forward API requests to the backend.

## Technologies Used

- React 18
- Vite
- React Router DOM
- Axios
- Modern CSS with Flexbox and Grid

## Project Structure

```
src/
├── components/
│   ├── InputForm.jsx      # Main input form component
│   ├── InputForm.css      # Input form styles
│   ├── OutputPage.jsx     # Results display component
│   └── OutputPage.css     # Output page styles
├── App.jsx                # Main app component with routing
├── App.css               # App-level styles
├── main.jsx              # Application entry point
└── index.css             # Global styles
```
