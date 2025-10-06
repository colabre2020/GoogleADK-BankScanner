from google.cloud import firestore
import os
from typing import Dict, Any, List, Optional
from ..models.types import BankAccount, AccountStatus, AccountType
from datetime import datetime


class BankAccountTool:
    """Tool for managing bank accounts using Firestore"""
    
    def __init__(self):
        self.db = firestore.Client(
            project=os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        )
        self.collection = "bank_accounts"
    
    def create_account(self, customer_id: str, account_type: AccountType = AccountType.CHECKING) -> BankAccount:
        """
        Create a new bank account
        
        Args:
            customer_id: ID of the customer
            account_type: Type of account to create
            
        Returns:
            Created bank account
        """
        account_number = self._generate_account_number()
        
        bank_account = BankAccount(
            account_number=account_number,
            account_type=account_type,
            customer_id=customer_id,
            balance=0.0,
            status=AccountStatus.PENDING,
            created_at=datetime.now(),
            last_modified=datetime.now()
        )
        
        # Save to Firestore
        doc_ref = self.db.collection(self.collection).document(account_number)
        doc_ref.set(bank_account.dict())
        
        return bank_account
    
    def get_account(self, account_number: str) -> Optional[BankAccount]:
        """Get account by account number"""
        try:
            doc_ref = self.db.collection(self.collection).document(account_number)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return BankAccount(**data)
            return None
        except Exception as e:
            print(f"Error getting account: {str(e)}")
            return None
    
    def update_account_status(self, account_number: str, status: AccountStatus) -> bool:
        """Update account status"""
        try:
            doc_ref = self.db.collection(self.collection).document(account_number)
            doc_ref.update({
                'status': status.value,
                'last_modified': datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error updating account status: {str(e)}")
            return False
    
    def get_accounts_by_customer(self, customer_id: str) -> List[BankAccount]:
        """Get all accounts for a customer"""
        try:
            query = self.db.collection(self.collection).where('customer_id', '==', customer_id)
            docs = query.stream()
            
            accounts = []
            for doc in docs:
                data = doc.to_dict()
                accounts.append(BankAccount(**data))
            
            return accounts
        except Exception as e:
            print(f"Error getting customer accounts: {str(e)}")
            return []
    
    def _generate_account_number(self) -> str:
        """Generate a unique account number"""
        import time
        import random
        
        timestamp = str(int(time.time()))[-6:]  # Last 6 digits of timestamp
        random_part = f"{random.randint(1000, 9999)}"
        return f"{timestamp}{random_part}"