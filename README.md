##Title: Smart Library Management System

##Description: This project is a console-based Smart Library Management System in Python.
The system allows a small library to:
- Add books (Physical books and EBooks)
- Register library members
- Borrow and return books
- Save and load library data using a JSON file
- View members and books

##How to run the application: 
1. Open a terminal or command prompt.
2. Navigate to the project root folder.
3. Run the program using: python main.py


Example usage :
From the menu:

1. Add a physical book with 1 copy.

2. Add a library member.

3. Borrow the book using the member ID and book ID.

4. Add another member and try to borrow the same book to see error message.

5. Return the book.

6. Try to borrow again and see success message.

7. List all books and members.

##How to save and load data:

1. After following example usage, save the data using menu and exit.
2. Run the program again
3. View all members (will show nothing)
4. Load the data from the menu
5. View all members and books again (will show from previous data)


##How to run tests :

from root project folder, in command terminal : python -m pytests