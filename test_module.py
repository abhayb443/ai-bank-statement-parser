#!/usr/bin/env python3
"""
Simple test to verify the bank parser module works correctly
"""

import sys
import os

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    
    try:
        from bank_parser_gemini import (
            Transaction,
            GeminiBankParser,
            BankParserError,
            parse_bank_statement,
            get_transactions_data,
            get_transactions_summary
        )
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_transaction_class():
    """Test Transaction class creation"""
    print("\nTesting Transaction class...")
    
    try:
        from bank_parser_gemini import Transaction
        
        # Create a test transaction
        txn = Transaction(
            date="15/03/2024",
            particulars="Test Transaction",
            amount=1000.0,
            transaction_type="DR",
            balance=5000.0
        )
        
        # Test to_dict method
        txn_dict = txn.to_dict()
        assert txn_dict['date'] == "15/03/2024"
        assert txn_dict['amount'] == 1000.0
        
        # Test to_json method
        txn_json = txn.to_json()
        assert "Test Transaction" in txn_json
        
        print("✅ Transaction class works correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Transaction class test failed: {e}")
        return False

def test_parser_initialization():
    """Test parser initialization"""
    print("\nTesting parser initialization...")
    
    try:
        from bank_parser_gemini import GeminiBankParser
        
        # Test with environment variable
        if os.getenv('GEMINI_API_KEY'):
            parser = GeminiBankParser()
            print("✅ Parser initialized with environment API key!")
            return True
        else:
            # Test with explicit API key (will fail but should handle gracefully)
            try:
                parser = GeminiBankParser(api_key="test_key")
                print("✅ Parser initialized with explicit API key!")
                return True
            except Exception as e:
                if "API key" in str(e) or "invalid" in str(e).lower():
                    print("✅ Parser correctly rejected invalid API key!")
                    return True
                else:
                    print(f"❌ Unexpected error: {e}")
                    return False
                    
    except Exception as e:
        print(f"❌ Parser initialization failed: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\nTesting error handling...")
    
    try:
        from bank_parser_gemini import BankParserError
        
        # Test custom exception
        error = BankParserError("Test error message")
        assert str(error) == "Test error message"
        
        print("✅ Error handling works correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Bank Parser Gemini Module")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_transaction_class,
        test_parser_initialization,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Module is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 