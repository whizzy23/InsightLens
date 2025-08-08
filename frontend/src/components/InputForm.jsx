import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './InputForm.css';

const InputForm = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  
  const [formData, setFormData] = useState({
    persona: '',
    jobToBeDone: ''
  });
  
  const [files, setFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    // Filter only PDF files and duplicates
    const newFiles = selectedFiles.filter(newFile => 
      newFile.type === 'application/pdf' && 
      !files.some(existingFile => 
        existingFile.name === newFile.name && existingFile.size === newFile.size
      )
    );
    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFiles = Array.from(e.dataTransfer.files);
      // Filter only PDF files and duplicates
      const newFiles = droppedFiles.filter(newFile => 
        newFile.type === 'application/pdf' && 
        !files.some(existingFile => 
          existingFile.name === newFile.name && existingFile.size === newFile.size
        )
      );
      setFiles(prev => [...prev, ...newFiles]);
    }
  };

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const getTotalFileSize = () => {
    const totalBytes = files.reduce((total, file) => total + file.size, 0);
    const totalMB = totalBytes / 1024 / 1024;
    return totalMB.toFixed(2);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.persona || !formData.jobToBeDone || files.length === 0) {
      alert('Please fill in all fields and upload at least one document');
      return;
    }

    setIsLoading(true);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('persona', formData.persona);
      formDataToSend.append('jobToBeDone', formData.jobToBeDone);
      files.forEach((file) => {
        formDataToSend.append('documents', file);
      });

      // First, upload input files
      const uploadResponse = await axios.post('/api/upload_input', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (uploadResponse.data.success) {
        // Then, trigger processing
        try {
          const processResponse = await axios.post('/api/process');
          if (processResponse.data.success) {
            localStorage.setItem('analysisResult', JSON.stringify(processResponse.data));
            navigate('/output');
          } else {
            alert('Analysis error: ' + (processResponse.data.error || 'Unknown error'));
          }
        } catch (processError) {
          // Show backend error details if available
          const backendError = processError?.response?.data?.error;
          alert('Backend error: ' + (backendError || processError.message));
        }
      } else {
        alert('Error uploading input files: ' + uploadResponse.data.error);
      }
    } catch (error) {
      console.error('Error processing documents:', error);
      const backendError = error?.response?.data?.error;
      alert('Error processing documents: ' + (backendError || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="form-container">
        <h2>Document Analysis Request</h2>
        <p>Please provide the following information to analyze your documents:</p>
        
        <form onSubmit={handleSubmit}>
          {/* Persona Input */}
          <div className="form-group">
            <label htmlFor="persona">Persona *</label>
            <textarea
              id="persona"
              name="persona"
              value={formData.persona}
              onChange={handleInputChange}
              placeholder="Describe the persona or user profile (e.g., 'A busy professional looking for quick insights')"
              rows="4"
              required
            />
          </div>

          {/* Job to be Done Input */}
          <div className="form-group">
            <label htmlFor="jobToBeDone">Job to be Done *</label>
            <textarea
              id="jobToBeDone"
              name="jobToBeDone"
              value={formData.jobToBeDone}
              onChange={handleInputChange}
              placeholder="Describe what job the user is trying to accomplish (e.g., 'Quickly understand key insights from multiple documents')"
              rows="4"
              required
            />
          </div>

          {/* Document Upload */}
          <div className="form-group">
            <label>Upload Documents *</label>
            <div
              className={`file-upload ${dragActive ? 'dragover' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              <div className="upload-content">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7,10 12,15 17,10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                <p>Click to select files or drag and drop</p>
                <p className="file-types">Supported formats: PDF only</p>
              </div>
            </div>
            
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </div>

          {/* File List */}
          {files.length > 0 && (
            <div className="file-list">
              <div className="file-list-header">
                <div className="file-stats">
                  <h4>Selected Files ({files.length})</h4>
                  <span className="total-size">Total Size: {getTotalFileSize()} MB</span>
                </div>
                <button
                  type="button"
                  className="clear-all-btn"
                  onClick={() => setFiles([])}
                >
                  Clear All
                </button>
              </div>
              <div className="file-grid">
                {files.map((file, index) => (
                  <div key={index} className="file-item">
                    <div className="file-info">
                      <span className="file-name">{file.name}</span>
                      <span className="file-size">({(file.size / 1024 / 1024).toFixed(2)} MB)</span>
                    </div>
                    <button
                      type="button"
                      className="remove-file"
                      onClick={() => removeFile(index)}
                      title="Remove file"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            className="submit-btn"
            disabled={isLoading || files.length === 0}
          >
            {isLoading ? (
              <div className="loading">
                <div className="spinner"></div>
                <span>Processing...</span>
              </div>
            ) : (
              'Analyze Documents'
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default InputForm;
