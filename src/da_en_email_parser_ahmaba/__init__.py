"""
a_en_email_parser_ahmaba - Python package for parsing and processing English emails.
"""

from .da_en_email_parser import start_pipeline, extract_header, extract_greeting, extract_signature, clean_body, extract_submessage, drop_fields
from .resources import test_message

__version__ = "1.0.1"

__all__ = [
    'start_pipeline',
    'extract_header',
    'extract_greeting',
    'extract_signature',
    'clean_body',
    'extract_submessage',
]
