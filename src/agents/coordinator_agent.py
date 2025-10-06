from google.adk import Agent
from .document_scanner_agent import DocumentScannerAgent
from .validation_agent import ValidationAgent
from .account_creation_agent import AccountCreationAgent
from ..models.types import CustomerData, Document, Address, EmploymentInfo, ProcessingResult, VerificationStatus, AccountType
from typing import List, Dict, Any
import uuid
from datetime import datetime


class CoordinatorAgent(Agent):
    """Main coordinator agent that orchestrates the entire bank account creation process"""
    
    def __init__(self):
        # Initialize sub-agents
        self.document_scanner = DocumentScannerAgent()
        self.validator = ValidationAgent()
        self.account_creator = AccountCreationAgent()
        
        super().__init__(
            name="Coordinator",
            model="gemini-2.0-flash-exp",
            instruction="""You are the main coordinator for the bank account creation process. 
            You manage the entire workflow from document scanning to account activation:
            
            1. Coordinate document scanning and data extraction
            2. Oversee validation of all customer information
            3. Compile customer data from multiple sources
            4. Manage account creation and activation
            5. Handle errors and edge cases appropriately
            6. Provide clear status updates throughout the process
            
            Always ensure proper sequencing of operations and handle failures gracefully.""",
            description="I coordinate the entire customer onboarding and account creation process.",
            sub_agents=[
                self.document_scanner,
                self.validator,
                self.account_creator
            ]
        )
    
    def process_new_customer(self, files: List[Dict[str, Any]]) -> ProcessingResult:
        """
        Process a new customer through the complete onboarding workflow
        
        Args:
            files: List of uploaded document files
            
        Returns:
            ProcessingResult with status and data
        """
        try:
            print(f"Starting customer onboarding process with {len(files)} documents")
            
            # Step 1: Scan and extract data from documents
            print("Step 1: Scanning documents...")
            scanned_documents = self.document_scanner.scan_documents(files)
            
            if not scanned_documents:
                return ProcessingResult(
                    status="error",
                    message="No documents could be processed",
                    error="Document scanning failed"
                )
            
            # Step 2: Validate documents
            print("Step 2: Validating documents...")
            validated_documents = self.validator.validate_documents(scanned_documents)
            
            # Step 3: Compile customer data
            print("Step 3: Compiling customer data...")
            customer_data = self._compile_customer_data(validated_documents)
            
            # Step 4: Validate complete customer data
            print("Step 4: Validating customer data...")
            is_customer_valid = self.validator.validate_customer_data(customer_data)
            
            if not is_customer_valid:
                return ProcessingResult(
                    status="validation_failed",
                    message="Customer data validation failed",
                    customer_data=customer_data,
                    documents=validated_documents
                )
            
            # Step 5: Create bank account
            print("Step 5: Creating bank account...")
            bank_account = self.account_creator.create_bank_account(
                customer_data, AccountType.CHECKING
            )
            
            # Step 6: Check if all documents are verified
            all_documents_verified = all(
                doc.verification_status == VerificationStatus.VERIFIED 
                for doc in validated_documents
            )
            
            if all_documents_verified:
                # Activate account immediately
                print("Step 6: Activating account...")
                self.account_creator.activate_account(bank_account.account_number)
                status = "completed"
                message = "Account created and activated successfully"
            else:
                status = "pending_verification"
                message = "Account created, pending document verification"
            
            return ProcessingResult(
                status=status,
                message=message,
                customer_data=customer_data,
                bank_account=bank_account,
                documents=validated_documents
            )
            
        except Exception as e:
            print(f"Error in customer onboarding process: {str(e)}")
            return ProcessingResult(
                status="error",
                message="An error occurred during the onboarding process",
                error=str(e)
            )
    
    def _compile_customer_data(self, documents: List[Document]) -> CustomerData:
        """
        Compile customer data from processed documents
        
        Args:
            documents: List of processed documents
            
        Returns:
            Compiled customer data
        """
        print(f"Compiling customer data from {len(documents)} documents")
        
        # Initialize customer data structure
        customer_data = CustomerData(
            id=str(uuid.uuid4()),
            first_name="",
            last_name="",
            date_of_birth="",
            social_security_number="",
            address=Address(
                street="",
                city="",
                state="",
                zip_code="",
                country="USA"
            ),
            phone_number="",
            email="",
            employment_info=EmploymentInfo(
                employer="",
                position="",
                annual_income=0.0,
                employment_start_date=""
            ),
            documents=documents
        )
        
        # Extract data from documents
        for document in documents:
            data = document.extracted_data
            
            if document.type == "drivers_license" or document.type == "passport":
                if data.get('first_name'):
                    customer_data.first_name = data['first_name']
                if data.get('last_name'):
                    customer_data.last_name = data['last_name']
                if data.get('date_of_birth'):
                    customer_data.date_of_birth = data['date_of_birth']
                if data.get('address'):
                    customer_data.address.street = data['address']
            
            elif document.type == "social_security_card":
                if data.get('social_security_number'):
                    customer_data.social_security_number = data['social_security_number']
            
            elif document.type == "proof_of_address":
                if data.get('street'):
                    customer_data.address.street = data['street']
                if data.get('city'):
                    customer_data.address.city = data['city']
                if data.get('state'):
                    customer_data.address.state = data['state']
                if data.get('zip_code'):
                    customer_data.address.zip_code = data['zip_code']
            
            elif document.type == "employment_verification":
                if data.get('employer'):
                    customer_data.employment_info.employer = data['employer']
                if data.get('position'):
                    customer_data.employment_info.position = data['position']
                if data.get('salary'):
                    try:
                        customer_data.employment_info.annual_income = float(data['salary'])
                    except (ValueError, TypeError):
                        pass
                if data.get('start_date'):
                    customer_data.employment_info.employment_start_date = data['start_date']
        
        # Set placeholder values for missing required fields
        if not customer_data.email:
            customer_data.email = "customer@example.com"
        if not customer_data.phone_number:
            customer_data.phone_number = "555-0123"
        
        return customer_data