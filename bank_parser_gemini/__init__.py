"""
Bank Parser Gemini - A Python module to parse bank statements using Google Gemini AI
"""

from .parser import (
    Transaction,
    GeminiBankParser,
    BankParserError,
    parse_bank_statement,
    get_transactions_data,
    get_transactions_summary
)

__version__ = "1.0.0"
__author__ = "Abhay Pandey"
__email__ = "pandeyabhay443@gmail.com"

__all__ = [
    "Transaction",
    "GeminiBankParser", 
    "BankParserError",
    "parse_bank_statement",
    "get_transactions_data",
    "get_transactions_summary"
] 