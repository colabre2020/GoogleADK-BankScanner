#!/usr/bin/env python3
"""
Simplified FastAPI application for testing without Google Cloud credentials
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
from datetime import datetime
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Google ADK Multi-Agent Bank Account Creation System",
    description="A sophisticated multi-agent system for automated bank document processing and account creation",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Google ADK Multi-Agent Bank Account Creation System",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Google ADK Multi-Agent Bank System",
        "agents": {
            "coordinator": "ready",
            "document_scanner": "ready", 
            "validator": "ready",
            "account_creator": "ready"
        }
    }


@app.post("/api/process-documents-demo")
async def process_documents_demo(documents: List[UploadFile] = File(...)):
    """
    Demo endpoint for document processing (without Google Cloud dependencies)
    """
    try:
        if not documents:
            raise HTTPException(status_code=400, detail="No documents provided")
        
        # Simulate document processing
        processed_docs = []
        customer_id = f"cust_{uuid.uuid4().hex[:8]}"
        
        for doc in documents:
            content = await doc.read()
            
            # Simulate document analysis
            processed_docs.append({
                "id": f"doc_{uuid.uuid4().hex[:8]}",
                "filename": doc.filename,
                "type": "drivers_license" if "license" in doc.filename.lower() else "unknown",
                "size": len(content),
                "status": "processed",
                "extracted_data": {
                    "first_name": "John",
                    "last_name": "Doe", 
                    "date_of_birth": "1990-05-15"
                }
            })
        
        # Simulate account creation
        account_number = f"{int(datetime.now().timestamp())}".replace(".", "")[-10:]
        
        return {
            "success": True,
            "data": {
                "status": "completed",
                "message": "Demo processing completed successfully",
                "customer_data": {
                    "id": customer_id,
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "555-0123"
                },
                "bank_account": {
                    "account_number": account_number,
                    "account_type": "checking",
                    "status": "active",
                    "balance": 0.0,
                    "created_at": datetime.now().isoformat()
                },
                "documents": processed_docs
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Demo processing failed"
            }
        )


@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    return {
        "coordinator": {
            "status": "active",
            "model": "gemini-2.0-flash-exp",
            "description": "Main workflow coordinator"
        },
        "document_scanner": {
            "status": "active",
            "model": "gemini-2.0-flash-exp", 
            "description": "Document processing specialist"
        },
        "validator": {
            "status": "active",
            "model": "gemini-2.0-flash-exp",
            "description": "Data validation specialist"
        },
        "account_creator": {
            "status": "active",
            "model": "gemini-2.0-flash-exp",
            "description": "Bank account creation specialist"
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/demo/workflow")
async def demo_workflow():
    """Demonstrate the multi-agent workflow"""
    return {
        "workflow": {
            "step_1": {
                "agent": "DocumentScannerAgent",
                "action": "Scan and extract data from uploaded documents",
                "tools": ["DocumentProcessor", "Google Document AI"]
            },
            "step_2": {
                "agent": "ValidationAgent", 
                "action": "Validate extracted data and documents",
                "tools": ["ValidationTool", "Compliance Checker"]
            },
            "step_3": {
                "agent": "AccountCreationAgent",
                "action": "Create bank account and setup customer profile",
                "tools": ["BankAccountTool", "Firestore Database"]
            },
            "step_4": {
                "agent": "CoordinatorAgent",
                "action": "Orchestrate workflow and handle edge cases",
                "tools": ["Multi-agent coordination", "Error handling"]
            }
        },
        "status": "demo_ready"
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting Google ADK Multi-Agent Bank System on port {port}")
    print(f"📖 API Documentation: http://localhost:{port}/docs")
    print(f"💻 Demo Endpoints:")
    print(f"   - Health Check: http://localhost:{port}/api/health")
    print(f"   - Agent Status: http://localhost:{port}/api/agents/status")
    print(f"   - Demo Workflow: http://localhost:{port}/api/demo/workflow")
    print(f"   - Process Documents (Demo): http://localhost:{port}/api/process-documents-demo")
    
    uvicorn.run(
        "main_demo:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )