# Bank Parser Gemini - Project Structure

## 📁 Clean Project Structure

```
bank-parser/
├── bank_parser_gemini/          # Main package directory
│   ├── __init__.py             # Package initialization and exports
│   ├── parser.py               # Core parser logic and classes
│   └── __main__.py             # Command line interface
├── Docs/                       # Sample PDF files for testing
│   ├── amazon-icici-cc.pdf
│   ├── flipkart-axis-cc.pdf
│   ├── sbi-cc.pdf
│   ├── sc-bank-statement.pdf
│   ├── yes-bank-statement.pdf
│   ├── yes-reserve-cc.pdf
│   └── yes-rupay-cc.pdf
├── README.md                   # Comprehensive documentation
├── INSTALLATION.md             # Quick installation guide
├── PROJECT_STRUCTURE.md        # This file - project overview
├── setup.py                    # Package installation configuration
├── requirements.txt            # Python dependencies
├── MANIFEST.in                 # Package file inclusion rules
├── LICENSE                     # MIT License
├── example_usage.py            # Usage examples and demonstrations
└── test_module.py              # Module testing suite
```

## 🎯 Core Files

### **Package Files**
- `bank_parser_gemini/` - Main package containing all parser logic
- `setup.py` - Package installation and distribution configuration
- `requirements.txt` - Required Python dependencies

### **Documentation**
- `README.md` - Complete documentation with examples
- `INSTALLATION.md` - Quick start guide
- `PROJECT_STRUCTURE.md` - This overview file

### **Testing & Examples**
- `test_module.py` - Module testing and validation
- `example_usage.py` - Comprehensive usage examples
- `Docs/` - Sample PDF files for testing

### **Legal & Configuration**
- `LICENSE` - MIT License
- `MANIFEST.in` - Package file inclusion rules

## 🚀 Usage

### **As a Module**
```python
from bank_parser_gemini import parse_bank_statement
transactions = parse_bank_statement("statement.pdf")
```

### **Command Line**
```bash
python -m bank_parser_gemini statement.pdf --summary
```

### **Testing**
```bash
python test_module.py
```

## 📦 Installation

```bash
# Install dependencies
pip install pdfplumber google-generativeai

# Set API key
export GEMINI_API_KEY="your-api-key"

# Test the module
python test_module.py
```

## ✅ Clean Status

- ✅ Removed all generated output files
- ✅ Removed old/original parser files
- ✅ Removed duplicate documentation
- ✅ Removed cache directories
- ✅ Removed system files
- ✅ Removed old test files
- ✅ Organized structure maintained 