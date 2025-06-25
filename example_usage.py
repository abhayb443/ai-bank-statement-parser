#!/usr/bin/env python3
"""
Example usage of the Bank Parser Gemini module
Demonstrates various ways to use the module for data extraction
"""

import os
import json
from pathlib import Path

# Import the bank parser module
from bank_parser_gemini import (
    parse_bank_statement,
    get_transactions_data,
    get_transactions_summary,
    GeminiBankParser,
    BankParserError
)

def example_basic_usage():
    """Basic usage example - get Transaction objects"""
    print("=== Basic Usage Example ===")
    
    pdf_file = "Docs/sbi-cc.pdf"  # Change this to your PDF file
    
    if not os.path.exists(pdf_file):
        print(f"PDF file {pdf_file} not found. Please update the path.")
        return
    
    try:
        # Get Transaction objects
        transactions = parse_bank_statement(pdf_file)
        
        print(f"Found {len(transactions)} transactions")
        
        # Print first few transactions
        for i, txn in enumerate(transactions[:5]):
            print(f"{i+1}. {txn.date} | {txn.particulars[:30]}... | ₹{txn.amount:,.2f} | {txn.transaction_type}")
            
    except BankParserError as e:
        print(f"Parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_dict_data():
    """Get transactions as dictionaries"""
    print("\n=== Dictionary Data Example ===")
    
    pdf_file = "Docs/sbi-cc.pdf"  # Change this to your PDF file
    
    if not os.path.exists(pdf_file):
        print(f"PDF file {pdf_file} not found. Please update the path.")
        return
    
    try:
        # Get transactions as dictionaries
        transactions_data = get_transactions_data(pdf_file)
        
        print(f"Found {len(transactions_data)} transactions as dictionaries")
        
        # Show first transaction structure
        if transactions_data:
            print("First transaction structure:")
            print(json.dumps(transactions_data[0], indent=2))
            
    except BankParserError as e:
        print(f"Parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_summary_only():
    """Get only summary statistics"""
    print("\n=== Summary Only Example ===")
    
    pdf_file = "Docs/sbi-cc.pdf"  # Change this to your PDF file
    
    if not os.path.exists(pdf_file):
        print(f"PDF file {pdf_file} not found. Please update the path.")
        return
    
    try:
        # Get only summary
        summary = get_transactions_summary(pdf_file)
        
        print("📊 Summary Statistics:")
        print(json.dumps(summary, indent=2))
        
    except BankParserError as e:
        print(f"Parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_advanced_usage():
    """Advanced usage with parser class"""
    print("\n=== Advanced Usage Example ===")
    
    pdf_file = "Docs/sbi-cc.pdf"  # Change this to your PDF file
    
    if not os.path.exists(pdf_file):
        print(f"PDF file {pdf_file} not found. Please update the path.")
        return
    
    try:
        # Initialize parser
        parser = GeminiBankParser()
        
        # Parse statement
        transactions = parser.parse_statement(pdf_file)
        
        # Get summary
        summary = parser.get_summary(transactions)
        
        print(f"📊 Summary:")
        print(f"   Total Transactions: {summary['total_transactions']}")
        print(f"   Total Credits: ₹{summary['total_credit']:,.2f}")
        print(f"   Total Debits: ₹{summary['total_debit']:,.2f}")
        print(f"   Net Amount: ₹{summary['net_amount']:,.2f}")
        
        # Convert to different formats
        transactions_dict = [txn.to_dict() for txn in transactions]
        transactions_json = [txn.to_json() for txn in transactions]
        
        print(f"\n📋 Data Formats Available:")
        print(f"   - Transaction objects: {len(transactions)}")
        print(f"   - Dictionary format: {len(transactions_dict)}")
        print(f"   - JSON strings: {len(transactions_json)}")
        
    except BankParserError as e:
        print(f"Parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_data_analysis():
    """Example of data analysis with parsed transactions"""
    print("\n=== Data Analysis Example ===")
    
    pdf_file = "Docs/sbi-cc.pdf"  # Change this to your PDF file
    
    if not os.path.exists(pdf_file):
        print(f"PDF file {pdf_file} not found. Please update the path.")
        return
    
    try:
        # Get transactions as dictionaries for easy analysis
        transactions_data = get_transactions_data(pdf_file)
        
        if not transactions_data:
            print("No transactions found for analysis")
            return
        
        # Basic analysis
        total_amount = sum(txn['amount'] for txn in transactions_data)
        avg_amount = total_amount / len(transactions_data)
        
        # Separate debits and credits
        debits = [txn for txn in transactions_data if txn['transaction_type'] in ['DR', 'DEBIT']]
        credits = [txn for txn in transactions_data if txn['transaction_type'] in ['CR', 'CREDIT']]
        
        print(f"📈 Analysis Results:")
        print(f"   Total Transactions: {len(transactions_data)}")
        print(f"   Total Amount: ₹{total_amount:,.2f}")
        print(f"   Average Amount: ₹{avg_amount:,.2f}")
        print(f"   Debit Transactions: {len(debits)}")
        print(f"   Credit Transactions: {len(credits)}")
        
        # Find largest transaction
        largest_txn = max(transactions_data, key=lambda x: x['amount'])
        print(f"   Largest Transaction: ₹{largest_txn['amount']:,.2f} - {largest_txn['particulars'][:30]}...")
        
        # Find smallest transaction
        smallest_txn = min(transactions_data, key=lambda x: x['amount'])
        print(f"   Smallest Transaction: ₹{smallest_txn['amount']:,.2f} - {smallest_txn['particulars'][:30]}...")
        
    except BankParserError as e:
        print(f"Parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_error_handling():
    """Example of proper error handling"""
    print("\n=== Error Handling Example ===")
    
    # Test with non-existent file
    try:
        transactions = parse_bank_statement("non_existent_file.pdf")
    except FileNotFoundError:
        print("✅ Correctly caught FileNotFoundError for non-existent file")
    except BankParserError as e:
        print(f"BankParserError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Run all examples"""
    print("🚀 Bank Parser Gemini - Data Extraction Examples")
    print("=" * 50)
    
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  Warning: GEMINI_API_KEY environment variable not set.")
        print("   Set it with: export GEMINI_API_KEY='your-api-key'")
        print("   Or pass it directly to the functions.\n")
    
    # Run examples
    example_basic_usage()
    example_dict_data()
    example_summary_only()
    example_advanced_usage()
    example_data_analysis()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("✅ All examples completed!")
    print("\n💡 Key Functions:")
    print("   - parse_bank_statement() -> List[Transaction]")
    print("   - get_transactions_data() -> List[Dict]")
    print("   - get_transactions_summary() -> Dict")


if __name__ == "__main__":
    main() 