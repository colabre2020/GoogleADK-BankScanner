#!/usr/bin/env python3
"""
Demo script for Google ADK Multi-Agent Bank Account Creation System
This script demonstrates the multi-agent workflow with sample data.
"""

import asyncio
from src.agents.coordinator_agent import CoordinatorAgent
from src.models.types import DocumentType
import json


def create_sample_documents():
    """Create sample document data for testing"""
    return [
        {
            'filename': 'john_doe_drivers_license.pdf',
            'content': b'Sample Driver License\nName: John Doe\nDOB: 1990-05-15\nAddress: 123 Main St, Anytown, CA 90210\nLicense #: D1234567',
            'content_type': 'application/pdf',
            'size': 150
        },
        {
            'filename': 'john_doe_ssn_card.jpg',
            'content': b'Social Security Card\nSSN: 123-45-6789\nName: John Doe',
            'content_type': 'image/jpeg',
            'size': 120
        },
        {
            'filename': 'utility_bill.pdf',
            'content': b'Electric Bill\nService Address: 123 Main St\nAnytown, CA 90210\nAccount Holder: John Doe',
            'content_type': 'application/pdf',
            'size': 200
        }
    ]


async def run_demo():
    """Run the multi-agent demo"""
    print("🚀 Google ADK Multi-Agent Bank Account Creation Demo")
    print("=" * 60)
    
    # Initialize the coordinator agent
    print("🤖 Initializing Coordinator Agent...")
    coordinator = CoordinatorAgent()
    
    # Create sample documents
    print("📄 Creating sample documents...")
    sample_files = create_sample_documents()
    
    print(f"📋 Processing {len(sample_files)} documents:")
    for i, file_data in enumerate(sample_files, 1):
        print(f"   {i}. {file_data['filename']} ({file_data['content_type']})")
    
    print("\n🔄 Starting multi-agent workflow...")
    print("-" * 40)
    
    try:
        # Process documents through the multi-agent system
        result = coordinator.process_new_customer(sample_files)
        
        print("\n✅ Multi-Agent Processing Complete!")
        print("=" * 60)
        
        # Display results
        print(f"📊 Status: {result.status}")
        print(f"💬 Message: {result.message}")
        
        if result.customer_data:
            print(f"\n👤 Customer Information:")
            print(f"   ID: {result.customer_data.id}")
            print(f"   Name: {result.customer_data.first_name} {result.customer_data.last_name}")
            print(f"   Email: {result.customer_data.email}")
            print(f"   Phone: {result.customer_data.phone_number}")
            print(f"   Address: {result.customer_data.address.street}, {result.customer_data.address.city}")
        
        if result.bank_account:
            print(f"\n🏦 Bank Account Created:")
            print(f"   Account Number: {result.bank_account.account_number}")
            print(f"   Account Type: {result.bank_account.account_type}")
            print(f"   Status: {result.bank_account.status}")
            print(f"   Balance: ${result.bank_account.balance}")
        
        if result.documents:
            print(f"\n📋 Document Processing Summary:")
            for i, doc in enumerate(result.documents, 1):
                print(f"   {i}. {doc.file_name} - {doc.verification_status}")
        
        print(f"\n🎉 Demo completed successfully!")
        
        # Save results to file for reference
        with open('demo_results.json', 'w') as f:
            json.dump(result.dict(), f, indent=2, default=str)
        print("💾 Results saved to demo_results.json")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("🔍 Check your Google Cloud configuration and ensure all services are set up correctly.")


def print_agent_architecture():
    """Display the agent architecture"""
    print("\n🏗️  Google ADK Multi-Agent Architecture:")
    print("=" * 50)
    print("""
    CoordinatorAgent (Main Agent)
    ├── DocumentScannerAgent (Sub-Agent)
    │   └── 🔧 Tools: DocumentProcessor
    ├── ValidationAgent (Sub-Agent)
    │   └── 🔧 Tools: ValidationTool
    └── AccountCreationAgent (Sub-Agent)
        └── 🔧 Tools: BankAccountTool
    
    🌟 Features:
    • Multi-agent coordination with Google ADK
    • Document AI integration for data extraction
    • Automated validation and compliance checking
    • Bank account creation with Firestore storage
    • End-to-end workflow orchestration
    """)


if __name__ == "__main__":
    print_agent_architecture()
    
    print("\n🚨 Prerequisites:")
    print("1. Set up Google Cloud credentials (.env file)")
    print("2. Configure Document AI processors")
    print("3. Set up Firestore database")
    print("4. Install all dependencies (pip install -r requirements.txt)")
    
    user_input = input("\n▶️  Ready to run the demo? (y/n): ").lower().strip()
    
    if user_input == 'y':
        asyncio.run(run_demo())
    else:
        print("👋 Demo cancelled. Set up your Google Cloud environment and try again!")