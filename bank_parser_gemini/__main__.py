#!/usr/bin/env python3
"""
Main entry point for the bank parser module
Allows running the module with: python -m bank_parser_gemini
"""

import sys
import argparse
import json
from pathlib import Path

from .parser import GeminiBankParser, BankParserError


def main():
    """Main function to run the parser from command line"""
    parser = argparse.ArgumentParser(description='Parse bank statements using Gemini AI')
    parser.add_argument('pdf_file', help='Path to the PDF bank statement')
    parser.add_argument('--api-key', help='Google Gemini API key')
    parser.add_argument('--summary', action='store_true', help='Print transaction summary only')
    parser.add_argument('--format', choices=['json', 'dict'], default='json', 
                       help='Output format (json or dict)')
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not Path(args.pdf_file).exists():
        print(f"Error: PDF file '{args.pdf_file}' not found.")
        sys.exit(1)
    
    try:
        # Initialize parser
        bank_parser = GeminiBankParser(args.api_key)
        
        # Parse statement
        transactions = bank_parser.parse_statement(args.pdf_file)
        
        # Print summary if requested
        if args.summary:
            summary = bank_parser.get_summary(transactions)
            if args.format == 'json':
                print(json.dumps(summary, indent=2))
            else:
                print(f"Total Transactions: {summary['total_transactions']}")
                print(f"Total Debits: ₹{summary['total_debit']:,.2f}")
                print(f"Total Credits: ₹{summary['total_credit']:,.2f}")
                print(f"Net: ₹{summary['net_amount']:,.2f}")
        else:
            # Output transactions
            if args.format == 'json':
                transactions_data = [txn.to_dict() for txn in transactions]
                print(json.dumps(transactions_data, indent=2))
            else:
                for i, txn in enumerate(transactions, 1):
                    print(f"{i}. {txn.date} | {txn.particulars} | ₹{txn.amount:,.2f} | {txn.transaction_type}")
        
    except BankParserError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 