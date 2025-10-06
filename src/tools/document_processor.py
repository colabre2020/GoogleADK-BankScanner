from google.cloud import documentai
from google.cloud import storage
import os
from typing import Dict, Any, List
from ..models.types import DocumentType


class DocumentProcessor:
    """Tool for processing documents using Google Document AI"""
    
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
        self.client = documentai.DocumentProcessorServiceClient()
        self.storage_client = storage.Client()
        
    def process_document(self, file_content: bytes, file_name: str, document_type: DocumentType) -> Dict[str, Any]:
        """
        Process a document using Google Document AI
        
        Args:
            file_content: The document content as bytes
            file_name: Name of the file
            document_type: Type of document to process
            
        Returns:
            Extracted data from the document
        """
        try:
            # Get the appropriate processor for the document type
            processor_name = self._get_processor_name(document_type)
            
            # Create the document request
            raw_document = documentai.RawDocument(
                content=file_content,
                mime_type=self._get_mime_type(file_name)
            )
            
            request = documentai.ProcessRequest(
                name=processor_name,
                raw_document=raw_document
            )
            
            # Process the document
            result = self.client.process_document(request=request)
            document = result.document
            
            # Extract and structure the data based on document type
            extracted_data = self._extract_structured_data(document, document_type)
            
            return extracted_data
            
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            return {}
    
    def _get_processor_name(self, document_type: DocumentType) -> str:
        """Get the processor name for the given document type"""
        processor_map = {
            DocumentType.DRIVERS_LICENSE: os.getenv("DRIVERS_LICENSE_PROCESSOR_ID"),
            DocumentType.PASSPORT: os.getenv("PASSPORT_PROCESSOR_ID"),
            DocumentType.SOCIAL_SECURITY_CARD: os.getenv("SSN_PROCESSOR_ID"),
            DocumentType.PROOF_OF_ADDRESS: os.getenv("ADDRESS_PROCESSOR_ID"),
            DocumentType.EMPLOYMENT_VERIFICATION: os.getenv("EMPLOYMENT_PROCESSOR_ID"),
            DocumentType.BANK_STATEMENT: os.getenv("BANK_STATEMENT_PROCESSOR_ID")
        }
        
        processor_id = processor_map.get(document_type, os.getenv("DEFAULT_PROCESSOR_ID"))
        return f"projects/{self.project_id}/locations/{self.location}/processors/{processor_id}"
    
    def _get_mime_type(self, file_name: str) -> str:
        """Determine MIME type from file extension"""
        extension = file_name.lower().split('.')[-1]
        mime_types = {
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'tiff': 'image/tiff',
            'tif': 'image/tiff'
        }
        return mime_types.get(extension, 'application/pdf')
    
    def _extract_structured_data(self, document, document_type: DocumentType) -> Dict[str, Any]:
        """Extract structured data based on document type"""
        if not document.entities:
            return {}
            
        extracted_data = {}
        
        # Extract entities based on document type
        for entity in document.entities:
            if entity.type_ and entity.mention_text:
                extracted_data[entity.type_] = entity.mention_text
        
        # Apply document-specific parsing
        if document_type == DocumentType.DRIVERS_LICENSE:
            return self._parse_drivers_license(extracted_data)
        elif document_type == DocumentType.PASSPORT:
            return self._parse_passport(extracted_data)
        elif document_type == DocumentType.SOCIAL_SECURITY_CARD:
            return self._parse_ssn(extracted_data)
        elif document_type == DocumentType.PROOF_OF_ADDRESS:
            return self._parse_address(extracted_data)
        elif document_type == DocumentType.EMPLOYMENT_VERIFICATION:
            return self._parse_employment(extracted_data)
        elif document_type == DocumentType.BANK_STATEMENT:
            return self._parse_bank_statement(extracted_data)
        
        return extracted_data
    
    def _parse_drivers_license(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse driver's license specific data"""
        return {
            'license_number': data.get('license_number'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'date_of_birth': data.get('date_of_birth'),
            'address': data.get('address'),
            'expiration_date': data.get('expiration_date'),
            'state': data.get('state')
        }
    
    def _parse_passport(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse passport specific data"""
        return {
            'passport_number': data.get('passport_number'),
            'first_name': data.get('given_names'),
            'last_name': data.get('surname'),
            'date_of_birth': data.get('date_of_birth'),
            'nationality': data.get('nationality'),
            'expiration_date': data.get('expiration_date')
        }
    
    def _parse_ssn(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SSN card specific data"""
        return {
            'social_security_number': data.get('ssn'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name')
        }
    
    def _parse_address(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse address document specific data"""
        return {
            'street': data.get('street_address'),
            'city': data.get('city'),
            'state': data.get('state'),
            'zip_code': data.get('zip_code'),
            'country': data.get('country')
        }
    
    def _parse_employment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse employment verification specific data"""
        return {
            'employer': data.get('employer'),
            'position': data.get('position'),
            'salary': data.get('salary'),
            'start_date': data.get('start_date')
        }
    
    def _parse_bank_statement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse bank statement specific data"""
        return {
            'bank_name': data.get('bank_name'),
            'account_number': data.get('account_number'),
            'balance': data.get('balance'),
            'statement_date': data.get('statement_date')
        }