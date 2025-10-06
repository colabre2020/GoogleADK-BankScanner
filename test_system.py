#!/usr/bin/env python3

"""
Test script for the Google ADK Multi-Agent Bank System
"""

import asyncio
import aiohttp
import os
from pathlib import Path


async def test_health_endpoint():
    """Test the health check endpoint"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:8000/api/health') as response:
                data = await response.json()
                print("✅ Health Check:", data)
                return True
        except Exception as e:
            print("❌ Health Check Failed:", str(e))
            return False


async def test_agents_status():
    """Test the agents status endpoint"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:8000/api/agents/status') as response:
                data = await response.json()
                print("✅ Agents Status:", data)
                return True
        except Exception as e:
            print("❌ Agents Status Failed:", str(e))
            return False


async def test_document_processing():
    """Test document processing with sample files"""
    # Create sample test files (for demonstration)
    test_files = {
        'driver_license.txt': b'Sample Driver License Content\nName: John Doe\nDOB: 1990-01-01',
        'ssn_card.txt': b'Sample SSN Card\nSSN: 123-45-6789\nName: John Doe'
    }
    
    # Create temporary test files
    temp_dir = Path('temp_test_files')
    temp_dir.mkdir(exist_ok=True)
    
    file_paths = []
    for filename, content in test_files.items():
        file_path = temp_dir / filename
        with open(file_path, 'wb') as f:
            f.write(content)
        file_paths.append(file_path)
    
    # Test document processing
    async with aiohttp.ClientSession() as session:
        try:
            data = aiohttp.FormData()
            
            for file_path in file_paths:
                with open(file_path, 'rb') as f:
                    data.add_field('documents', f, filename=file_path.name)
            
            async with session.post('http://localhost:8000/api/test/document-scanner', data=data) as response:
                result = await response.json()
                print("✅ Document Processing Test:", result)
                return True
                
        except Exception as e:
            print("❌ Document Processing Failed:", str(e))
            return False
        finally:
            # Clean up test files
            for file_path in file_paths:
                if file_path.exists():
                    file_path.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()


async def main():
    """Run all tests"""
    print("🧪 Testing Google ADK Multi-Agent Bank System")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Agents Status", test_agents_status),
        ("Document Processing", test_document_processing)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        success = await test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\n🎯 {total_passed}/{len(results)} tests passed")


if __name__ == "__main__":
    print("Make sure the server is running: python main.py")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    
    asyncio.run(main())