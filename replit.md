# Gerador de Capa de Recebimento DANFE

## Overview

This is a Python-based web application built with Streamlit that extracts data from DANFE (Documento Auxiliar da Nota Fiscal Eletrônica) PDF files and generates receipt covers. The application supports multiple PDF uploads, automatic data extraction with manual editing capabilities, and batch processing for generating freight receipt covers in landscape format.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

**Frontend**: Streamlit web interface providing an intuitive user experience for file upload, data validation, and document generation.

**Backend**: Python modules handling PDF processing, data extraction, and document generation with minimal external dependencies.

**Document Processing Pipeline**: 
1. PDF upload and temporary storage
2. Text extraction using pdfplumber
3. Data parsing with regex patterns
4. Receipt generation using ReportLab
5. File download delivery

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Streamlit web interface and application orchestration
- **Key Features**: 
  - Multiple file upload handling (PDF, max 200MB each)
  - Progressive processing with status indicators
  - Editable form fields for all extracted data
  - File selector for switching between processed PDFs
  - Individual and batch generation capabilities
  - Clean interface without sidebar instructions

### 2. DANFE Extractor (`danfe_extractor.py`)
- **Purpose**: Extract structured data from DANFE PDF documents
- **Key Features**:
  - PDF text extraction using pdfplumber
  - Regex-based pattern matching for fiscal data
  - Support for multiple DANFE formats
- **Extracted Data**: NFe number, series, access key, emission date, total value, CNPJ, state registration, operation nature, ZIP code

### 3. Receipt Generator (`receipt_generator.py`)
- **Purpose**: Generate formatted PDF receipt covers
- **Key Features**:
  - ReportLab-based PDF generation
  - Custom styling and layouts
  - Professional document formatting
  - A4 page size with proper margins

### 4. Utilities (`utils.py`)
- **Purpose**: Common helper functions for text processing
- **Key Features**:
  - Text cleaning and normalization
  - Currency formatting (Brazilian Real)
  - Date parsing and validation
  - Regex utilities for data extraction

## Data Flow

1. **Upload Phase**: User uploads multiple DANFE PDFs through Streamlit interface
2. **Storage Phase**: Files temporarily stored using Python tempfile with progress tracking
3. **Extraction Phase**: DANFEExtractor processes each PDF sequentially, extracting fiscal data using flexible regex patterns
4. **Editing Phase**: User can select and edit any extracted data field through interactive forms
5. **Generation Phase**: ReceiptGenerator creates formatted PDF receipt covers (individual or batch)
6. **Delivery Phase**: Generated documents available for download with automatic naming

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for user interface
- **pdfplumber**: PDF text extraction and processing
- **ReportLab**: PDF generation and document formatting
- **tempfile**: Temporary file management (Python standard library)
- **re**: Regular expression processing (Python standard library)

### Document Processing
- **Base64**: File encoding for downloads
- **BytesIO**: In-memory file handling
- **datetime**: Date and time utilities

## Deployment Strategy

**Platform**: Designed for Replit deployment with Streamlit hosting
**File Management**: Uses temporary file storage for processing uploaded documents
**Resource Requirements**: Minimal - handles PDF processing in memory with temporary file cleanup
**Scalability**: Single-user sessions with isolated file processing

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- **July 01, 2025**: Initial setup with single PDF processing
- **July 01, 2025**: Implemented multiple PDF upload support with sequential processing
- **July 01, 2025**: Added editable form fields for all extracted data (destinatário, remetente, NF-e details)
- **July 01, 2025**: Integrated file selector for switching between processed PDFs
- **July 01, 2025**: Added batch generation capability for processing multiple receipts at once
- **July 01, 2025**: Removed sidebar instructions and cleaned up code comments for streamlined interface
- **July 01, 2025**: Enhanced regex patterns to support multiple DANFE formats (tested with 3 different PDF structures)

## Changelog

- July 01, 2025: Multiple PDF upload and editable fields implementation