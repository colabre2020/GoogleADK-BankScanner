import re
from typing import Dict, Any, List
from ..models.types import Document, VerificationStatus, CustomerData


class ValidationTool:
    """Tool for validating documents and customer data"""
    
    def validate_document(self, document: Document) -> bool:
        """
        Validate a single document
        
        Args:
            document: Document to validate
            
        Returns:
            True if document is valid, False otherwise
        """
        if not document.extracted_data:
            return False
        
        # Document-specific validation
        if document.type == "drivers_license":
            return self._validate_drivers_license(document.extracted_data)
        elif document.type == "passport":
            return self._validate_passport(document.extracted_data)
        elif document.type == "social_security_card":
            return self._validate_ssn(document.extracted_data)
        elif document.type == "proof_of_address":
            return self._validate_address(document.extracted_data)
        elif document.type == "employment_verification":
            return self._validate_employment(document.extracted_data)
        
        return True  # Basic validation passed
    
    def validate_customer_data(self, customer_data: CustomerData) -> bool:
        """
        Validate complete customer data
        
        Args:
            customer_data: Customer data to validate
            
        Returns:
            True if all data is valid, False otherwise
        """
        validations = [
            self._validate_personal_info(customer_data),
            self._validate_address_info(customer_data.address),
            self._validate_employment_info(customer_data.employment_info),
            len(customer_data.documents) > 0
        ]
        
        return all(validations)
    
    def _validate_drivers_license(self, data: Dict[str, Any]) -> bool:
        """Validate driver's license data"""
        required_fields = ['license_number', 'first_name', 'last_name', 'date_of_birth']
        return all(data.get(field) for field in required_fields)
    
    def _validate_passport(self, data: Dict[str, Any]) -> bool:
        """Validate passport data"""
        required_fields = ['passport_number', 'first_name', 'last_name', 'date_of_birth']
        return all(data.get(field) for field in required_fields)
    
    def _validate_ssn(self, data: Dict[str, Any]) -> bool:
        """Validate SSN data"""
        ssn = data.get('social_security_number')
        if not ssn:
            return False
        
        # Check SSN format (XXX-XX-XXXX or XXXXXXXXX)
        ssn_pattern = r'^\d{3}-\d{2}-\d{4}$|^\d{9}$'
        return bool(re.match(ssn_pattern, ssn))
    
    def _validate_address(self, data: Dict[str, Any]) -> bool:
        """Validate address document data"""
        required_fields = ['street', 'city', 'state', 'zip_code']
        return all(data.get(field) for field in required_fields)
    
    def _validate_employment(self, data: Dict[str, Any]) -> bool:
        """Validate employment verification data"""
        required_fields = ['employer', 'position']
        return all(data.get(field) for field in required_fields)
    
    def _validate_personal_info(self, customer_data: CustomerData) -> bool:
        """Validate personal information"""
        return all([
            customer_data.first_name,
            customer_data.last_name,
            customer_data.date_of_birth,
            customer_data.email,
            customer_data.phone_number
        ])
    
    def _validate_address_info(self, address) -> bool:
        """Validate address information"""
        return all([
            address.street,
            address.city,
            address.state,
            address.zip_code
        ])
    
    def _validate_employment_info(self, employment_info) -> bool:
        """Validate employment information"""
        return all([
            employment_info.employer,
            employment_info.position,
            employment_info.annual_income > 0
        ])
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        # Check if it's a valid US phone number (10 digits)
        return len(digits_only) == 10