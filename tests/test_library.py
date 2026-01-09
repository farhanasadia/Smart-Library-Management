import pytest
import sys

sys.path.append(".")

from library.library import Library
from library.book import PhysicalBook
from library.member import Member
from library.errors import BookNotAvailableError


def test_add_book():
    lib = Library()
    assert lib.add_book(PhysicalBook("B1", "Python", "John", 1)) is True


def test_add_member():
    lib = Library()
    assert lib.add_member(Member("M1", "Alice")) is True


def test_borrow_book():
    lib = Library()
    lib.add_book(PhysicalBook("B1", "Python", "John", 1))
    lib.add_member(Member("M1", "Alice"))

    assert lib.borrow_book("M1", "B1") is True


def test_borrow_unavailable():
    lib = Library()
    lib.add_book(PhysicalBook("B1", "Python", "John", 0))
    lib.add_member(Member("M1", "Alice"))

    with pytest.raises(BookNotAvailableError):
        lib.borrow_book("M1", "B1")
