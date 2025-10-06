# Google ADK Multi-Agent Bank Account Creation System

A sophisticated multi-agent system built with **Google ADK (Application Development Kit)** for automating bank document processing and account creation using Python.

## Overview

This system uses multiple specialized agents built with Google ADK to handle different aspects of the bank account creation process:

- **DocumentScannerAgent**: Scans and extracts data from uploaded documents using Google Document AI
- **ValidationAgent**: Validates extracted data and ensures document authenticity
- **AccountCreationAgent**: Creates bank accounts and manages account lifecycle
- **CoordinatorAgent**: Orchestrates the entire process across all sub-agents

## Google ADK Architecture

```python
from google.adk.agents import LlmAgent

# Define individual agents
document_scanner = LlmAgent(name="DocumentScanner", model="gemini-2.0-flash-exp", ...)
validator = LlmAgent(name="Validator", model="gemini-2.0-flash-exp", ...)
account_creator = LlmAgent(name="AccountCreator", model="gemini-2.0-flash-exp", ...)

# Create coordinator agent with sub-agents
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash-exp",
    description="I coordinate the entire customer onboarding process.",
    sub_agents=[
        document_scanner,
        validator,
        account_creator
    ]
)
```

## Features

- **Multi-document Processing**: Supports various document types (Driver's License, Passport, SSN Card, etc.)
- **Intelligent Data Extraction**: Uses Google Document AI for accurate text extraction
- **Automated Validation**: Comprehensive validation of customer data and documents
- **Account Management**: Automated bank account creation with status tracking
- **Cloud Storage**: Secure document storage using Google Cloud Storage
- **Real-time Processing**: RESTful API for real-time document processing

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Document        │    │ Validation      │    │ Account         │
│ Scanner Agent   │───▶│ Agent           │───▶│ Creation Agent  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Document AI     │    │ Data Validation │    │ Bank Account    │
│ Service         │    │ Rules           │    │ Service         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Google Cloud    │    │ Business Logic  │    │ Firestore       │
│ Storage         │    │ Engine          │    │ Database        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Supported Document Types

- Driver's License
- Passport
- Social Security Card
- Proof of Address (Utility Bills, Bank Statements)
- Employment Verification
- Bank Statements

## Prerequisites

- Python 3.8+ and pip
- Google ADK Python library
- Google Cloud Platform account
- Google Cloud Storage bucket
- Google Document AI processors configured
- Firestore database set up

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GoogleADK
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.template .env
   # Edit .env with your Google Cloud configuration
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Configuration

### Google Cloud Setup

1. **Create a Google Cloud Project**
2. **Enable APIs**:
   - Document AI API
   - Cloud Storage API
   - Firestore API

3. **Create Document AI Processors**:
   - Driver's License Processor
   - Passport Processor
   - General Form Processor (for other documents)

4. **Set up Service Account**:
   - Create a service account with appropriate permissions
   - Download the JSON key file
   - Set the path in your `.env` file

5. **Create Cloud Storage Bucket**:
   - Create a bucket for document storage
   - Set appropriate permissions

### Environment Variables

Update your `.env` file with the following:

```env
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_KEY_FILE=path/to/service-account-key.json
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
DRIVERS_LICENSE_PROCESSOR_ID=your-processor-id
# ... other processor IDs
```

## Usage

### Development Mode

```bash
python main.py
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Process Customer Documents

```bash
POST /api/process-documents
Content-Type: multipart/form-data

# Form data with file uploads
documents: [file1.pdf, file2.jpg, ...]
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "completed",
    "message": "Account created and activated successfully",
    "customerData": {
      "id": "cust_123...",
      "firstName": "John",
      "lastName": "Doe",
      // ... other customer data
    },
    "bankAccount": {
      "accountNumber": "1234567890",
      "accountType": "checking",
      "status": "active"
    },
    "documents": [
      // ... processed documents
    ]
  }
}
```

#### Health Check

```bash
GET /api/health
```

## Agent Details

### DocumentScannerAgent
- Processes uploaded files
- Identifies document types
- Extracts structured data using Google Document AI
- Handles multiple document formats (PDF, JPG, PNG)

### ValidationAgent
- Validates extracted data against business rules
- Performs document authenticity checks
- Cross-references information across documents
- Flags documents requiring manual review

### AccountCreationAgent
- Generates unique account numbers
- Creates bank accounts in the database
- Manages account lifecycle (pending → active)
- Sends welcome notifications

### OrchestratorAgent
- Coordinates the entire workflow
- Handles error scenarios
- Provides status updates
- Manages agent communication

## Testing

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## API Examples

### Using cURL

```bash
# Process documents
curl -X POST http://localhost:8000/api/process-documents \
  -F "documents=@driver_license.pdf" \
  -F "documents=@ssn_card.jpg" \
  -F "documents=@proof_of_address.pdf"

# Health check
curl http://localhost:8000/api/health

# Test document scanner only
curl -X POST http://localhost:8000/api/test/document-scanner \
  -F "documents=@driver_license.pdf"
```

### Using Postman

1. Set method to POST
2. URL: `http://localhost:8000/api/process-documents`
3. Body type: form-data
4. Add files under key "documents"

## Google ADK Agent Details

### CoordinatorAgent (Main Agent)
```python
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash-exp",
    instruction="You coordinate the entire customer onboarding process...",
    sub_agents=[document_scanner, validator, account_creator]
)
```

### DocumentScannerAgent (Sub-Agent)
```python
document_scanner = LlmAgent(
    name="DocumentScanner", 
    model="gemini-2.0-flash-exp",
    instruction="You scan and extract data from documents...",
    tools=[document_processing_tool]
)
```

### ValidationAgent (Sub-Agent)
```python
validator = LlmAgent(
    name="Validator",
    model="gemini-2.0-flash-exp", 
    instruction="You validate documents and customer data...",
    tools=[validation_tool]
)
```

### AccountCreationAgent (Sub-Agent)
```python
account_creator = LlmAgent(
    name="AccountCreator",
    model="gemini-2.0-flash-exp",
    instruction="You create and manage bank accounts...",
    tools=[bank_account_tool]
)
```

## Error Handling

The system includes comprehensive error handling:

- **Validation Errors**: Documents that fail validation are flagged for manual review
- **Processing Errors**: Failed document processing returns detailed error messages
- **Service Errors**: Google Cloud service errors are caught and handled gracefully
- **Network Errors**: Retry mechanisms for transient failures

## Security Considerations

- All documents are encrypted in transit and at rest
- Service account keys should be securely managed
- Input validation prevents malicious file uploads
- Rate limiting should be implemented for production use
- Audit logging for compliance requirements

## Monitoring and Logging

The system includes comprehensive logging:

- **Info Logs**: Normal operation flow
- **Error Logs**: Error conditions with stack traces
- **Debug Logs**: Detailed debugging information (development only)
- **Audit Logs**: Compliance and security events

## Scaling Considerations

For production deployment:

- Use Google Cloud Run for serverless scaling
- Implement proper load balancing
- Use Cloud Firestore for scalable database
- Add Redis for caching
- Implement proper monitoring with Cloud Monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support, please contact [your-email] or create an issue in the repository.# VERTICAL_DATASET_RESEARCH
# GoogleADK-BankScanner
