from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    DRIVERS_LICENSE = "drivers_license"
    PASSPORT = "passport"
    SOCIAL_SECURITY_CARD = "social_security_card"
    PROOF_OF_ADDRESS = "proof_of_address"
    EMPLOYMENT_VERIFICATION = "employment_verification"
    BANK_STATEMENT = "bank_statement"


class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    REQUIRES_MANUAL_REVIEW = "requires_manual_review"


class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    BUSINESS = "business"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class EmploymentInfo(BaseModel):
    employer: str
    position: str
    annual_income: float
    employment_start_date: str


class Document(BaseModel):
    id: str
    type: DocumentType
    file_name: str
    file_path: str
    extracted_data: dict
    verification_status: VerificationStatus
    uploaded_at: datetime


class CustomerData(BaseModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: str
    social_security_number: str
    address: Address
    phone_number: str
    email: str
    employment_info: EmploymentInfo
    documents: List[Document]


class BankAccount(BaseModel):
    account_number: str
    account_type: AccountType
    customer_id: str
    balance: float
    status: AccountStatus
    created_at: datetime
    last_modified: datetime


class ProcessingResult(BaseModel):
    status: str
    message: str
    customer_data: Optional[CustomerData] = None
    bank_account: Optional[BankAccount] = None
    documents: Optional[List[Document]] = None
    error: Optional[str] = None