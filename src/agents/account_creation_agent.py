from google.adk import Agent
from google.adk.tools import FunctionTool
from ..tools.bank_account_tool import BankAccountTool
from ..models.types import BankAccount, CustomerData, AccountType, AccountStatus
from typing import Dict, Any


class AccountCreationAgent(Agent):
    """Agent responsible for creating and managing bank accounts"""
    
    def __init__(self):
        self.bank_account_tool = BankAccountTool()
        
        # Define account management tools
        create_account_tool = FunctionTool(
            name="create_bank_account",
            description="Create a new bank account for a verified customer",
            func=self._create_account_tool
        )
        
        activate_account_tool = FunctionTool(
            name="activate_account",
            description="Activate a pending bank account",
            func=self._activate_account_tool
        )
        
        super().__init__(
            name="AccountCreator",
            model="gemini-2.0-flash-exp",
            instruction="""You are a bank account creation specialist. Your duties include:
            1. Create new bank accounts for verified customers
            2. Generate unique account numbers and set up account details
            3. Activate accounts once all verifications are complete
            4. Ensure compliance with banking regulations
            5. Send appropriate notifications to customers
            
            Always verify that customers have passed all validation checks before creating accounts.""",
            description="I create and manage bank accounts for new customers.",
            tools=[create_account_tool, activate_account_tool]
        )
    
    def create_bank_account(self, customer_data: CustomerData, account_type: AccountType = AccountType.CHECKING) -> BankAccount:
        """
        Create a new bank account for a customer
        
        Args:
            customer_data: Verified customer data
            account_type: Type of account to create
            
        Returns:
            Created bank account
        """
        account = self.bank_account_tool.create_account(
            customer_id=customer_data.id,
            account_type=account_type
        )
        
        print(f"Created {account_type} account {account.account_number} for {customer_data.first_name} {customer_data.last_name}")
        return account
    
    def activate_account(self, account_number: str) -> bool:
        """
        Activate a pending account
        
        Args:
            account_number: Account number to activate
            
        Returns:
            True if activation successful, False otherwise
        """
        success = self.bank_account_tool.update_account_status(
            account_number=account_number,
            status=AccountStatus.ACTIVE
        )
        
        if success:
            print(f"Account {account_number} has been activated")
        else:
            print(f"Failed to activate account {account_number}")
        
        return success
    
    def _create_account_tool(self, customer_id: str, account_type: str = "checking") -> Dict[str, Any]:
        """Tool function for creating accounts"""
        account_type_enum = AccountType(account_type)
        account = self.bank_account_tool.create_account(customer_id, account_type_enum)
        return account.dict()
    
    def _activate_account_tool(self, account_number: str) -> bool:
        """Tool function for activating accounts"""
        return self.bank_account_tool.update_account_status(
            account_number, AccountStatus.ACTIVE
        )