"""
Google ADK Multi-Agent Bank Account Creation System

This package contains all the agents, tools, and models for the
automated bank document processing and account creation system.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .agents.coordinator_agent import CoordinatorAgent
from .agents.document_scanner_agent import DocumentScannerAgent
from .agents.validation_agent import ValidationAgent
from .agents.account_creation_agent import AccountCreationAgent

from .models.types import (
    CustomerData,
    BankAccount,
    Document,
    ProcessingResult,
    DocumentType,
    VerificationStatus,
    AccountType,
    AccountStatus
)

__all__ = [
    'CoordinatorAgent',
    'DocumentScannerAgent', 
    'ValidationAgent',
    'AccountCreationAgent',
    'CustomerData',
    'BankAccount',
    'Document',
    'ProcessingResult',
    'DocumentType',
    'VerificationStatus',
    'AccountType',
    'AccountStatus'
]