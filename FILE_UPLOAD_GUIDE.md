# 📁 MedIntel File Upload Feature

## Overview

MedIntel now supports uploading medical reports in various formats for automated text extraction and AI-powered analysis.

## Supported File Formats

### ✅ Fully Supported

- **PDF Files** (.pdf) - Text-based and image-based PDFs
- **Images** (.jpg, .jpeg, .png, .bmp, .tiff) - OCR text extraction
- **Word Documents** (.docx) - Microsoft Word format
- **Text Files** (.txt) - Plain text documents

## How to Use

### 1. Upload a File

1. Navigate to **Report Analyzer** section
2. Click on the **Upload File** tab
3. Either:
   - **Drag and drop** your file onto the upload area
   - **Click to browse** and select a file

### 2. Preview

- Files are automatically previewed before analysis
- **PDFs**: Embedded viewer
- **Images**: Full image display
- **Text**: Formatted text preview

### 3. Analyze

1. Select the report type (optional)
2. Click **Analyze Uploaded File**
3. Wait for processing (extraction + analysis)
4. View results with:
   - Medical entities extraction
   - Key findings
   - Abnormal values
   - Recommendations

## Features

### 📄 PDF Processing

- **Text-based PDFs**: Direct text extraction
- **Image-based PDFs**: OCR on each page
- Multi-page support

### 🖼️ Image OCR

- Pre-processing for better accuracy
- Denoising and thresholding
- Support for medical document formats

### 📝 Document Processing

- Word document text extraction
- Table content extraction
- Formatted text preservation

## API Endpoints

### Extract Text from Document

```
POST /api/v1/ocr/extract
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "text": "extracted text...",
  "filename": "report.pdf",
  "extraction_method": "PDF text extraction"
}
```

### Analyze File Directly

```
POST /api/v1/analyze/report/file
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "summary": "...",
  "entities": {...},
  "recommendations": [...]
}
```

## Technical Details

### Backend Components

- **DocumentProcessor**: Handles all file type processing
- **PDF Libraries**: PyPDF2, pdfplumber, pdf2image
- **OCR**: EasyOCR (primary), Tesseract (fallback)
- **DOCX**: python-docx

### Processing Pipeline

1. File upload via FormData
2. File type detection
3. Text extraction (format-specific)
4. NLP entity extraction
5. Medical analysis
6. Results formatting

## Troubleshooting

### Common Issues

**"Could not extract text"**

- File may be corrupted
- PDF may be password-protected
- Image quality too low for OCR

**"Unsupported file format"**

- Check file extension
- Ensure file is not encrypted
- Try converting to supported format

**"OCR not available"**

- Backend OCR libraries not installed
- Try uploading text-based PDF instead
- Use manual text input as fallback

## Performance Notes

- **PDF text extraction**: < 1 second per page
- **OCR processing**: 2-5 seconds per page
- **Large files**: May take longer, progress shown via toast notifications
- **Recommended**: Files under 10MB for optimal performance

## Privacy & Security

- Files are processed in-memory only
- No permanent storage on server
- Text extraction happens locally
- All data deleted after response

## Future Enhancements

- [ ] Real-time progress bars
- [ ] Batch file processing
- [ ] OCR language selection
- [ ] PDF form field extraction
- [ ] DICOM medical image support
- [ ] HL7 message parsing
