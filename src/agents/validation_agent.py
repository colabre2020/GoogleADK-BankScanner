from google.adk import Agent
from google.adk.tools import FunctionTool
from ..tools.validation_tool import ValidationTool
from ..models.types import Document, VerificationStatus, CustomerData
from typing import List


class ValidationAgent(Agent):
    """Agent responsible for validating documents and customer data"""
    
    def __init__(self):
        self.validation_tool = ValidationTool()
        
        # Define validation tools
        validate_doc_tool = FunctionTool(
            name="validate_document",
            description="Validate a single document for completeness and accuracy",
            func=self._validate_document_tool
        )
        
        validate_customer_tool = FunctionTool(
            name="validate_customer_data",
            description="Validate complete customer data for account creation",
            func=self._validate_customer_tool
        )
        
        super().__init__(
            name="Validator",
            model="gemini-2.0-flash-exp",
            instruction="""You are a data validation specialist. Your responsibilities include:
            1. Verify the accuracy and completeness of extracted document data
            2. Check for inconsistencies across multiple documents
            3. Validate that all required information is present
            4. Flag any suspicious or incomplete data for manual review
            5. Ensure compliance with banking regulations and KYC requirements
            
            Always be thorough and conservative in your validation approach.""",
            description="I validate documents and customer data to ensure accuracy and compliance.",
            tools=[validate_doc_tool, validate_customer_tool]
        )
    
    def validate_documents(self, documents: List[Document]) -> List[Document]:
        """
        Validate a list of documents
        
        Args:
            documents: List of documents to validate
            
        Returns:
            List of documents with updated verification status
        """
        validated_documents = []
        
        for document in documents:
            is_valid = self.validation_tool.validate_document(document)
            
            if is_valid:
                document.verification_status = VerificationStatus.VERIFIED
            else:
                document.verification_status = VerificationStatus.REJECTED
            
            validated_documents.append(document)
        
        return validated_documents
    
    def validate_customer_data(self, customer_data: CustomerData) -> bool:
        """
        Validate complete customer data
        
        Args:
            customer_data: Customer data to validate
            
        Returns:
            True if valid, False otherwise
        """
        return self.validation_tool.validate_customer_data(customer_data)
    
    def _validate_document_tool(self, document_data: dict) -> bool:
        """Tool function for document validation"""
        # Convert dict to Document object for validation
        document = Document(**document_data)
        return self.validation_tool.validate_document(document)
    
    def _validate_customer_tool(self, customer_data: dict) -> bool:
        """Tool function for customer data validation"""
        # Convert dict to CustomerData object for validation
        customer = CustomerData(**customer_data)
        return self.validation_tool.validate_customer_data(customer)