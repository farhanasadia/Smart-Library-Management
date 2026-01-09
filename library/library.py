"""
Library controller class.
"""

import json

from library.book import PhysicalBook, EBook
from library.member import Member
from library.loan import Loan
from library.errors import BookNotFoundError, MemberNotFoundError


class Library:
    """
    Controls all library operations:
    - store books and members
    - borrow and return books
    - save/load data using JSON
    """

    def __init__(self):
        self._books = {}
        self._members = {}
        self._loans = []

    def add_book(self, book):
        """Add a book to the library. Returns False if ID already exists."""
        if book.id in self._books:
            return False
        self._books[book.id] = book
        return True

    def add_member(self, member):
        """Add a member to the library. Returns False if ID already exists."""
        if member.member_id in self._members:
            return False
        self._members[member.member_id] = member
        return True

    def borrow_book(self, member_id, book_id):
        """
        Borrow a book for a member.

        Raises:
            MemberNotFoundError, BookNotFoundError, BookNotAvailableError
        """
        member = self._members.get(member_id)
        if member is None:
            raise MemberNotFoundError("Member not found.")

        book = self._books.get(book_id)
        if book is None:
            raise BookNotFoundError("Book not found.")

        book.borrow()  # may raise BookNotAvailableError

        if not member.borrow_book(book):
            book.return_book()
            return False

        self._loans.append(Loan(book, member))
        return True

    def return_book(self, member_id, book_id):
        """
        Return a book for a member.

        Raises:
            MemberNotFoundError, BookNotFoundError
        """
        member = self._members.get(member_id)
        if member is None:
            raise MemberNotFoundError("Member not found.")

        book = self._books.get(book_id)
        if book is None:
            raise BookNotFoundError("Book not found.")

        if not member.return_book(book):
            return False

        book.return_book()

        for i, loan in enumerate(self._loans):
            if loan.member.member_id == member_id and loan.book.id == book_id:
                self._loans.pop(i)
                break

        return True

    def list_books(self):
        """Return a list of all books."""
        return list(self._books.values())

    def list_members(self):
        """Return a list of all members."""
        return list(self._members.values())

    def to_dict(self):
        """Convert library data into a dictionary for JSON."""
        return {
            "books": [b.to_dict() for b in self._books.values()],
            "members": [m.to_dict() for m in self._members.values()],
            "loans": [l.to_dict() for l in self._loans]
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Library object from a dictionary (loaded JSON)."""
        lib = cls()

        # Restore books
        for b in data.get("books", []):
            if b.get("type") == "PhysicalBook":
                book = PhysicalBook.from_dict(b)
            elif b.get("type") == "EBook":
                book = EBook.from_dict(b)
            else:
                continue
            lib._books[book.id] = book

        # Restore members and store their borrowed ids
        borrowed = {}
        for m in data.get("members", []):
            member = Member.from_dict(m)
            lib._members[member.member_id] = member
            borrowed[member.member_id] = m.get("borrowed_book_ids", [])

        # Reconnect borrowed books safely
        for member_id, book_ids in borrowed.items():
            member = lib._members.get(member_id)
            if member is None:
                continue

            for book_id in book_ids:
                book = lib._books.get(book_id)
                if book is not None:
                    member.borrow_book(book)

        # Restore loans safely
        for l in data.get("loans", []):
            loan = Loan.from_dict(l, lib._books, lib._members)
            if loan.book is not None and loan.member is not None:
                lib._loans.append(loan)

        return lib

    def save_to_file(self, filename):
        """Save library data to a JSON file. Returns True/False."""
        try:
            with open(filename, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving file: {e}")
            return False

    def load_from_file(self, filename):
        """Load library data from a JSON file. Returns True/False."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            loaded = Library.from_dict(data)
            self._books = loaded._books
            self._members = loaded._members
            self._loans = loaded._loans
            return True

        except FileNotFoundError:
            print(f"File {filename} not found.")
            return False
        except json.JSONDecodeError as e:
            print(f"Could not decode JSON: {e}")
            return False
        except IOError as e:
            print(f"Could not open file: {e}")
            return False
