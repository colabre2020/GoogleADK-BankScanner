from google.adk import Agent
from google.adk.tools import FunctionTool
from ..tools.document_processor import DocumentProcessor
from ..models.types import Document, DocumentType, VerificationStatus
from typing import List, Dict, Any
import uuid
from datetime import datetime


class DocumentScannerAgent(Agent):
    """Agent responsible for scanning and processing documents"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        
        # Define the document processing tool
        document_tool = FunctionTool(
            name="process_document",
            description="Process and extract data from uploaded documents",
            func=self._process_document_tool
        )
        
        super().__init__(
            name="DocumentScanner",
            model="gemini-2.0-flash-exp",
            instruction="""You are a document scanning specialist. Your job is to:
            1. Identify the type of each uploaded document
            2. Extract relevant information using document processing tools
            3. Structure the extracted data appropriately
            4. Return processed documents with extracted information
            
            Always ensure data accuracy and flag any documents that appear suspicious or incomplete.""",
            description="I scan and extract data from various document types including IDs, passports, and financial documents.",
            tools=[document_tool]
        )
    
    def scan_documents(self, files: List[Dict[str, Any]]) -> List[Document]:
        """
        Scan and process multiple documents
        
        Args:
            files: List of file data with 'content', 'filename', etc.
            
        Returns:
            List of processed Document objects
        """
        processed_documents = []
        
        for file_data in files:
            try:
                # Identify document type from filename
                document_type = self._identify_document_type(file_data['filename'])
                
                # Process the document
                extracted_data = self.document_processor.process_document(
                    file_content=file_data['content'],
                    file_name=file_data['filename'],
                    document_type=document_type
                )
                
                # Create Document object
                document = Document(
                    id=str(uuid.uuid4()),
                    type=document_type,
                    file_name=file_data['filename'],
                    file_path=file_data.get('path', ''),
                    extracted_data=extracted_data,
                    verification_status=VerificationStatus.PENDING,
                    uploaded_at=datetime.now()
                )
                
                processed_documents.append(document)
                
            except Exception as e:
                print(f"Error processing document {file_data['filename']}: {str(e)}")
                continue
        
        return processed_documents
    
    def _process_document_tool(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Tool function for processing documents"""
        document_type = self._identify_document_type(filename)
        return self.document_processor.process_document(file_content, filename, document_type)
    
    def _identify_document_type(self, filename: str) -> DocumentType:
        """Identify document type from filename"""
        filename_lower = filename.lower()
        
        if any(keyword in filename_lower for keyword in ['license', 'dl', 'driver']):
            return DocumentType.DRIVERS_LICENSE
        elif 'passport' in filename_lower:
            return DocumentType.PASSPORT
        elif any(keyword in filename_lower for keyword in ['ssn', 'social', 'security']):
            return DocumentType.SOCIAL_SECURITY_CARD
        elif any(keyword in filename_lower for keyword in ['address', 'utility', 'bill']):
            return DocumentType.PROOF_OF_ADDRESS
        elif any(keyword in filename_lower for keyword in ['employment', 'pay', 'salary']):
            return DocumentType.EMPLOYMENT_VERIFICATION
        elif any(keyword in filename_lower for keyword in ['bank', 'statement']):
            return DocumentType.BANK_STATEMENT
        else:
            # Default to drivers license
            return DocumentType.DRIVERS_LICENSE