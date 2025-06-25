#!/usr/bin/env python3
"""
Bank Statement Parser Module
A reusable module to parse bank statements from different banks using AI.
"""

import os
import re
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PDF processing
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    logger.warning("pdfplumber not available. Install with: pip install pdfplumber")

# Google Gemini API
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not available. Install with: pip install google-generativeai")


@dataclass
class Transaction:
    """Represents a single bank transaction"""
    date: str
    particulars: str
    amount: float
    transaction_type: str
    balance: Optional[float] = None
    reference_no: Optional[str] = None
    value_date: Optional[str] = None
    narration: Optional[str] = None
    cheque_no: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


class BankParserError(Exception):
    """Custom exception for bank parser errors"""
    pass


class GeminiBankParser:
    """Bank statement parser using Google Gemini AI"""
    
    def __init__(self, api_key: str = None):
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI library not available. Install with: pip install google-generativeai")
        
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("API key required. Either pass it to constructor or set GEMINI_API_KEY environment variable")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def extract_content(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extract text and tables from PDF"""
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber not available. Install with: pip install pdfplumber")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            with pdfplumber.open(file_path) as pdf:
                text_content = ""
                tables_content = []
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
                    
                    tables = page.extract_tables()
                    if tables:
                        for table_num, table in enumerate(tables):
                            tables_content.append({
                                'page': page_num + 1,
                                'table': table_num + 1,
                                'data': table
                            })
                
                return {'text': text_content, 'tables': tables_content}
        except Exception as e:
            raise BankParserError(f"Failed to extract content from PDF: {e}")
    
    def parse_statement(self, file_path: Union[str, Path]) -> List[Transaction]:
        """Parse bank statement and return list of transactions"""
        try:
            content = self.extract_content(file_path)
            prompt = self._create_prompt(content)
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            json_str = json_match.group(0) if json_match else response_text
            
            transactions_data = json.loads(json_str)
            transactions = []
            
            for txn_data in transactions_data:
                try:
                    transaction = Transaction(
                        date=txn_data.get('date', ''),
                        particulars=txn_data.get('particulars', ''),
                        amount=float(txn_data.get('amount', 0)),
                        transaction_type=txn_data.get('transaction_type', 'DR'),
                        balance=float(txn_data.get('balance', 0)) if txn_data.get('balance') else None,
                        reference_no=txn_data.get('reference_no'),
                        value_date=txn_data.get('value_date'),
                        narration=txn_data.get('narration'),
                        cheque_no=txn_data.get('cheque_no')
                    )
                    transactions.append(transaction)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Error parsing transaction: {e}")
                    continue
            
            return transactions
            
        except Exception as e:
            raise BankParserError(f"Failed to parse statement: {e}")
    
    def _create_prompt(self, content: Dict[str, Any]) -> str:
        """Create prompt for Gemini"""
        text_content = content['text']
        tables_content = content['tables']
        
        return f"""
You are a financial data extraction expert. Extract all transactions from this bank statement.

INSTRUCTIONS:
1. Extract each transaction with: date, particulars, amount, transaction_type (DR/CR), balance, reference_no, value_date, narration, cheque_no
2. Handle different bank formats (ICICI, SBI, Axis, Yes Bank, etc.)
3. Return ONLY valid JSON array of transactions

TEXT CONTENT:
{text_content[:8000]}

TABLES:
{json.dumps(tables_content[:3], indent=2) if tables_content else "No tables found"}

OUTPUT FORMAT:
[
  {{
    "date": "15/03/2024",
    "particulars": "ATM WITHDRAWAL",
    "amount": 1000.00,
    "transaction_type": "DR",
    "balance": 5000.00,
    "reference_no": "TXN123456",
    "value_date": "15/03/2024",
    "narration": "ATM withdrawal",
    "cheque_no": null
  }}
]

Return ONLY the JSON array, no additional text.
"""
    
    def export_to_json(self, transactions: List[Transaction], output_file: Union[str, Path]):
        """Export transactions to JSON file"""
        try:
            output_file = Path(output_file)
            data = {
                'extracted_at': datetime.now().isoformat(),
                'total_transactions': len(transactions),
                'transactions': [txn.to_dict() for txn in transactions]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            raise BankParserError(f"Failed to export to JSON: {e}")
    
    def export_to_csv(self, transactions: List[Transaction], output_file: Union[str, Path]):
        """Export transactions to CSV file"""
        try:
            import csv
            
            output_file = Path(output_file)
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if not transactions:
                    return
                
                fieldnames = ['date', 'particulars', 'amount', 'transaction_type', 
                            'balance', 'reference_no', 'value_date', 'narration', 'cheque_no']
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for txn in transactions:
                    writer.writerow(txn.to_dict())
            
        except Exception as e:
            raise BankParserError(f"Failed to export to CSV: {e}")
    
    def get_summary(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """Get summary of transactions"""
        if not transactions:
            return {'total_transactions': 0, 'total_debit': 0, 'total_credit': 0, 'net_amount': 0}
        
        total_debit = sum(txn.amount for txn in transactions if txn.transaction_type in ['DR', 'DEBIT'])
        total_credit = sum(txn.amount for txn in transactions if txn.transaction_type in ['CR', 'CREDIT'])
        
        return {
            'total_transactions': len(transactions),
            'total_debit': total_debit,
            'total_credit': total_credit,
            'net_amount': total_credit - total_debit
        }


# Convenience functions
def parse_bank_statement(pdf_path: Union[str, Path], api_key: str = None) -> List[Transaction]:
    """Parse a bank statement and return transactions"""
    parser = GeminiBankParser(api_key)
    return parser.parse_statement(pdf_path)


def get_transactions_data(pdf_path: Union[str, Path], api_key: str = None) -> List[Dict]:
    """Parse bank statement and return transactions as dictionaries"""
    parser = GeminiBankParser(api_key)
    transactions = parser.parse_statement(pdf_path)
    return [txn.to_dict() for txn in transactions]


def get_transactions_summary(pdf_path: Union[str, Path], api_key: str = None) -> Dict[str, Any]:
    """Parse bank statement and return summary statistics"""
    parser = GeminiBankParser(api_key)
    transactions = parser.parse_statement(pdf_path)
    return parser.get_summary(transactions) 