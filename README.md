# Bank Parser Gemini

A Python module to parse bank statements from different banks using Google Gemini AI. Extract transaction data from PDF bank statements with high accuracy.

## Features

- 🏦 Support for multiple bank formats (ICICI, SBI, Axis, Yes Bank, etc.)
- 🤖 Powered by Google Gemini AI for accurate data extraction
- 📊 Extract transaction details: date, particulars, amount, type, balance, etc.
- 🔧 Easy to integrate into any Python project
- 📦 Installable via pip
- 💾 **Data-focused**: Returns structured data without creating files

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key

### Install the module

```bash
# Clone the repository
git clone https://github.com/yourusername/bank-parser.git
cd bank-parser

# Install dependencies
pip install -r requirements.txt

# Install the module
pip install -e .
```

### Set up API key

Set your Google Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="XYX"
```

Or pass it directly when using the module.

## Quick Start

### Basic Usage - Get Transaction Objects

```python
from bank_parser_gemini import parse_bank_statement

# Parse a bank statement
transactions = parse_bank_statement("path/to/statement.pdf")

# Use the data
for txn in transactions:
    print(f"{txn.date} | {txn.particulars} | ₹{txn.amount} | {txn.transaction_type}")
```

### Get Data as Dictionaries

```python
from bank_parser_gemini import get_transactions_data

# Get transactions as dictionaries
transactions_data = get_transactions_data("path/to/statement.pdf")

# Use with pandas, JSON, etc.
import pandas as pd
df = pd.DataFrame(transactions_data)
```

### Get Summary Statistics Only

```python
from bank_parser_gemini import get_transactions_summary

# Get only summary
summary = get_transactions_summary("path/to/statement.pdf")
print(f"Total: {summary['total_transactions']} transactions")
print(f"Net: ₹{summary['net_amount']:,.2f}")
```

### Advanced Usage

```python
from bank_parser_gemini import GeminiBankParser

# Initialize parser with API key
parser = GeminiBankParser(api_key="your-api-key")

# Parse statement
transactions = parser.parse_statement("statement.pdf")

# Get summary
summary = parser.get_summary(transactions)
print(f"Total transactions: {summary['total_transactions']}")
print(f"Total credits: ₹{summary['total_credit']:,.2f}")
print(f"Total debits: ₹{summary['total_debit']:,.2f}")

# Convert to different formats
transactions_dict = [txn.to_dict() for txn in transactions]
transactions_json = [txn.to_json() for txn in transactions]
```

## API Reference

### Transaction Class

Represents a single bank transaction:

```python
@dataclass
class Transaction:
    date: str                    # Transaction date
    particulars: str             # Transaction description
    amount: float                # Transaction amount
    transaction_type: str        # "DR" or "CR"
    balance: Optional[float]     # Running balance
    reference_no: Optional[str]  # Reference number
    value_date: Optional[str]    # Value date
    narration: Optional[str]     # Additional details
    cheque_no: Optional[str]     # Cheque number
```

### Main Functions

```python
def parse_bank_statement(pdf_path: Union[str, Path], api_key: str = None) -> List[Transaction]
def get_transactions_data(pdf_path: Union[str, Path], api_key: str = None) -> List[Dict]
def get_transactions_summary(pdf_path: Union[str, Path], api_key: str = None) -> Dict[str, Any]
```

### GeminiBankParser Class

Main parser class:

```python
class GeminiBankParser:
    def __init__(self, api_key: str = None)
    def parse_statement(self, file_path: Union[str, Path]) -> List[Transaction]
    def get_summary(self, transactions: List[Transaction]) -> Dict[str, Any]
```

## Command Line Usage

The module can also be used from the command line:

```bash
# Basic parsing - outputs JSON
python -m bank_parser_gemini statement.pdf

# Get summary only
python -m bank_parser_gemini statement.pdf --summary

# Output as formatted text instead of JSON
python -m bank_parser_gemini statement.pdf --format dict

# With custom API key
python -m bank_parser_gemini statement.pdf --api-key YOUR_API_KEY
```

## Integration Examples

### Flask Web Application

```python
from flask import Flask, request, jsonify
from bank_parser_gemini import get_transactions_data
import os

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_statement():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)
    
    try:
        # Parse the statement and get data
        transactions_data = get_transactions_data(temp_path)
        
        return jsonify({
            'success': True,
            'transactions': transactions_data,
            'count': len(transactions_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up
        os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True)
```

### Django Integration

```python
# models.py
from django.db import models
from bank_parser_gemini import get_transactions_data

class BankStatement(models.Model):
    file = models.FileField(upload_to='statements/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def get_transactions(self):
        """Parse the uploaded statement and return transaction data"""
        return get_transactions_data(self.file.path)

# views.py
from django.http import JsonResponse
from .models import BankStatement

def parse_statement_view(request, statement_id):
    try:
        statement = BankStatement.objects.get(id=statement_id)
        transactions_data = statement.get_transactions()
        
        return JsonResponse({
            'transactions': transactions_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### Data Analysis with Pandas

```python
import pandas as pd
from bank_parser_gemini import get_transactions_data

# Parse statement
transactions_data = get_transactions_data("statement.pdf")

# Convert to DataFrame
df = pd.DataFrame(transactions_data)

# Analyze spending patterns
monthly_spending = df[df['transaction_type'] == 'DR'].groupby(
    pd.to_datetime(df['date']).dt.to_period('M')
)['amount'].sum()

print("Monthly spending:")
print(monthly_spending)
```

### JSON Processing

```python
import json
from bank_parser_gemini import get_transactions_data

# Get data as dictionaries
transactions_data = get_transactions_data("statement.pdf")

# Process with JSON
json_data = json.dumps(transactions_data, indent=2)
print(json_data)

# Save to file if needed
with open('transactions.json', 'w') as f:
    json.dump(transactions_data, f, indent=2)
```

## Error Handling

The module provides custom exceptions for better error handling:

```python
from bank_parser_gemini import BankParserError

try:
    transactions = parse_bank_statement("statement.pdf")
except BankParserError as e:
    print(f"Parsing failed: {e}")
except FileNotFoundError:
    print("PDF file not found")
except ImportError as e:
    print(f"Missing dependency: {e}")
```

## Supported Banks

The parser is designed to work with various Indian bank statement formats:

- ICICI Bank
- State Bank of India (SBI)
- Axis Bank
- Yes Bank
- HDFC Bank
- And more...

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Open an issue on GitHub
- Check the documentation
- Review the examples

## Changelog

### Version 1.0.0
- Initial release
- Support for multiple bank formats
- Data-focused approach (no file creation)
- Command line interface
- Easy integration APIs 