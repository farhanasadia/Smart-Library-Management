"""
Member class for the library system.
"""

class Member:
    """
    Represents a library member.
    """

    def __init__(self, member_id, name):
        self._member_id = member_id
        self._name = name
        self._borrowed_books = []

    @property
    def member_id(self):
        return self._member_id

    def borrow_book(self, book):
        if book in self._borrowed_books:
            return False
        self._borrowed_books.append(book)
        return True

    def return_book(self, book):
        if book not in self._borrowed_books:
            return False
        self._borrowed_books.remove(book)
        return True

    def to_dict(self):
        return {
            "member_id": self._member_id,
            "name": self._name,
            "borrowed_book_ids": [b.id for b in self._borrowed_books]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["member_id"], data["name"])

    def __str__(self):
        return f"{self._member_id} - {self._name} (borrowed: {len(self._borrowed_books)})"

    def __eq__(self, other):
        return isinstance(other, Member) and self._member_id == other._member_id
