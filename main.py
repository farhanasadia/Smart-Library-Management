"""
Console menu for Smart Library Management System.
"""

from library.library import Library
from library.book import PhysicalBook, EBook
from library.member import Member
from library.errors import BookNotAvailableError, BookNotFoundError, MemberNotFoundError


def main():
    library = Library()

    print("Welcome to Smart Library Management System!")

    while True:
        print("\n" + "=" * 40)
        print("1. Add book")
        print("2. Add member")
        print("3. Borrow book")
        print("4. Return book")
        print("5. List books")
        print("6. List members")
        print("7. Save (data.json)")
        print("8. Load (data.json)")
        print("0. Exit")
        print("=" * 40)

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                kind = input("1=Physical, 2=EBook: ").strip()
                bid = input("Book ID: ").strip()
                title = input("Title: ").strip()
                author = input("Author: ").strip()

                if not bid or not title or not author:
                    print("Book ID, title, and author cannot be empty.")
                    continue

                if kind == "1":
                    try:
                        copies = int(input("Copies: ").strip())
                    except ValueError:
                        print("Invalid input. Copies must be a number.")
                        continue

                    book = PhysicalBook(bid, title, author, copies)

                elif kind == "2":
                    try:
                        size = float(input("File size MB: ").strip())
                    except ValueError:
                        print("Invalid input. File size must be a number.")
                        continue

                    book = EBook(bid, title, author, size)

                else:
                    print("Invalid type. Choose 1 or 2.")
                    continue

                if library.add_book(book):
                    print("✓ Book added.")
                else:
                    print("Book ID already exists.")

            elif choice == "2":
                mid = input("Member ID: ").strip()
                name = input("Name: ").strip()

                if not mid or not name:
                    print("Member ID and name cannot be empty.")
                    continue

                if library.add_member(Member(mid, name)):
                    print("✓ Member added.")
                else:
                    print("Member ID already exists.")

            elif choice == "3":
                mid = input("Member ID: ").strip()
                bid = input("Book ID: ").strip()

                success = library.borrow_book(mid, bid)
                if success:
                    print("✓ Borrow successful.")
                else:
                    print("Member already borrowed this book.")

            elif choice == "4":
                mid = input("Member ID: ").strip()
                bid = input("Book ID: ").strip()

                success = library.return_book(mid, bid)
                if success:
                    print("✓ Return successful.")
                else:
                    print("Member does not have this book.")

            elif choice == "5":
                books = library.list_books()
                if not books:
                    print("No books available.")
                else:
                    print("\nBooks:")
                    for b in books:
                        print(" ", b)

            elif choice == "6":
                members = library.list_members()
                if not members:
                    print("No members available.")
                else:
                    print("\nMembers:")
                    for m in members:
                        print(" ", m)

            elif choice == "7":
                if library.save_to_file("data.json"):
                    print("✓ Saved to data.json")
                else:
                    print("Save failed.")

            elif choice == "8":
                if library.load_from_file("data.json"):
                    print("✓ Loaded from data.json")
                else:
                    print("Load failed.")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number from the menu.")

        except (BookNotAvailableError, BookNotFoundError, MemberNotFoundError) as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
