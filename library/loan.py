"""
Loan class representing a borrowing event.
"""

from datetime import datetime


class Loan:
    def __init__(self, book, member, date_borrowed=None):
        self.book = book
        self.member = member
        self.date_borrowed = date_borrowed or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "book_id": self.book.id,
            "member_id": self.member.member_id,
            "date_borrowed": self.date_borrowed
        }

    @classmethod
    def from_dict(cls, data, books, members):
        return cls(
            books.get(data["book_id"]),
            members.get(data["member_id"]),
            data["date_borrowed"]
        )

    def __str__(self):
        return f"{self.member.member_id} borrowed {self.book.id} on {self.date_borrowed}"
