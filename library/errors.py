"""
Custom exceptions for the library system.
"""

class BookNotAvailableError(Exception):
    pass

class BookNotFoundError(Exception):
    pass

class MemberNotFoundError(Exception):
    pass