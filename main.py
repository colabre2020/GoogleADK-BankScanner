from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
from dotenv import load_dotenv

from src.agents.coordinator_agent import CoordinatorAgent
from src.models.types import ProcessingResult

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Google ADK Multi-Agent Bank Account Creation System",
    description="A sophisticated multi-agent system for automated bank document processing and account creation",
    version="1.0.0"
)

# Initialize the coordinator agent
coordinator = CoordinatorAgent()


@app.post("/api/process-documents", response_model=dict)
async def process_documents(documents: List[UploadFile] = File(...)):
    """
    Process uploaded documents and create a bank account
    
    Args:
        documents: List of uploaded document files
        
    Returns:
        Processing result with status and account information
    """
    try:
        if not documents:
            raise HTTPException(status_code=400, detail="No documents provided")
        
        # Convert uploaded files to the format expected by agents
        files_data = []
        for doc in documents:
            content = await doc.read()
            files_data.append({
                'filename': doc.filename,
                'content': content,
                'content_type': doc.content_type,
                'size': len(content)
            })
        
        # Process documents through the coordinator agent
        result = coordinator.process_new_customer(files_data)
        
        # Convert Pydantic model to dict for JSON response
        return {
            "success": True,
            "data": result.dict()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-06T00:00:00Z",
        "service": "Google ADK Multi-Agent Bank System"
    }


@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    return {
        "coordinator": "active",
        "document_scanner": "active",
        "validator": "active",
        "account_creator": "active",
        "timestamp": "2025-01-06T00:00:00Z"
    }


@app.post("/api/test/document-scanner")
async def test_document_scanner(documents: List[UploadFile] = File(...)):
    """Test endpoint for document scanner agent only"""
    try:
        files_data = []
        for doc in documents:
            content = await doc.read()
            files_data.append({
                'filename': doc.filename,
                'content': content,
                'content_type': doc.content_type
            })
        
        scanned_docs = coordinator.document_scanner.scan_documents(files_data)
        
        return {
            "success": True,
            "scanned_documents": [doc.dict() for doc in scanned_docs]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )