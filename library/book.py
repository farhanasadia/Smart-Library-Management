"""
Book classes for the Smart Library Management System.
"""

from abc import ABC, abstractmethod
from library.errors import BookNotAvailableError


class Book(ABC):
    """
    Abstract base class for books.
    """

    def __init__(self, book_id, title, author):
        self._id = book_id
        self._title = title
        self._author = author

    @property
    def id(self):
        return self._id

    @abstractmethod
    def borrow(self):
        pass

    @abstractmethod
    def return_book(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    def __str__(self):
        return f"{self._id} - {self._title} by {self._author}"

    def __eq__(self, other):
        return isinstance(other, Book) and self._id == other._id


class PhysicalBook(Book):
    """
    Physical book with limited copies.
    """

    def __init__(self, book_id, title, author, available_copies):
        super().__init__(book_id, title, author)
        self._available_copies = available_copies

    def borrow(self):
        if self._available_copies <= 0:
            raise BookNotAvailableError("No copies available.")
        self._available_copies -= 1

    def return_book(self):
        self._available_copies += 1

    def to_dict(self):
        return {
            "type": "PhysicalBook",
            "id": self._id,
            "title": self._title,
            "author": self._author,
            "available_copies": self._available_copies
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data["author"],
            data["available_copies"]
        )

    def __str__(self):
        return f"{super().__str__()} (copies: {self._available_copies})"


class EBook(Book):
    """
    EBook that is always available.
    """

    def __init__(self, book_id, title, author, file_size_mb):
        super().__init__(book_id, title, author)
        self._file_size_mb = file_size_mb

    def borrow(self):
        return

    def return_book(self):
        return

    def to_dict(self):
        return {
            "type": "EBook",
            "id": self._id,
            "title": self._title,
            "author": self._author,
            "file_size_mb": self._file_size_mb
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data["author"],
            data["file_size_mb"]
        )

    def __str__(self):
        return f"{super().__str__()} (size: {self._file_size_mb} MB)"
