# Bank Parser Gemini - Installation & Usage Guide

## Quick Installation

### 1. Install Dependencies

```bash
# Install required packages
pip install pdfplumber google-generativeai

# Or install from requirements.txt
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Set your Gemini API key
export GEMINI_API_KEY="AIzaSyBHQETXMQX5ezmdyayaGfanpai_trPf4Aw"
```

## Usage Methods

### Method 1: As a Python Module (Recommended)

```python
# Import and use in your Python code
from bank_parser_gemini import parse_bank_statement

# Parse a bank statement
transactions = parse_bank_statement("path/to/statement.pdf")

# Print results
for txn in transactions:
    print(f"{txn.date} | {txn.particulars} | ₹{txn.amount} | {txn.transaction_type}")
```

### Method 2: Command Line Interface

```bash
# Basic parsing
python -m bank_parser_gemini statement.pdf

# With summary
python -m bank_parser_gemini statement.pdf --summary

# Export to JSON
python -m bank_parser_gemini statement.pdf --output-json transactions.json

# Export to CSV
python -m bank_parser_gemini statement.pdf --output-csv transactions.csv

# With custom API key
python -m bank_parser_gemini statement.pdf --api-key YOUR_API_KEY
```

### Method 3: Advanced Usage

```python
from bank_parser_gemini import GeminiBankParser

# Initialize parser
parser = GeminiBankParser()

# Parse statement
transactions = parser.parse_statement("statement.pdf")

# Get summary
summary = parser.get_summary(transactions)
print(f"Total: {summary['total_transactions']} transactions")

# Export
parser.export_to_json(transactions, "output.json")
parser.export_to_csv(transactions, "output.csv")
```

## Testing

Run the test file to verify everything works:

```bash
python test_module.py
```

## Example Files

- `example_usage.py` - Comprehensive usage examples
- `test_module.py` - Module testing
- `Docs/` - Sample PDF files for testing

## Troubleshooting

### Common Issues:

1. **Missing Dependencies**:
   ```bash
   pip install pdfplumber google-generativeai
   ```

2. **API Key Not Set**:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

3. **PDF File Not Found**:
   - Check file path
   - Ensure file exists and is readable

4. **Import Errors**:
   - Make sure you're in the correct directory
   - Check Python path

## Integration Examples

See `README.md` for detailed integration examples with:
- Flask web applications
- Django projects
- Data analysis with Pandas
- Command line tools 