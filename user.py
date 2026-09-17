## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book,
    display_books,
    library_statistics
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    result = []
    category = category.strip().lower()
    for book_id, book in books.items():
        if book.get("category", "").lower() == category:
            result.append(book_id)
    return result
    pass

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    result = []
    search_text = search_text.strip().lower()
    for book_id, book in books.items():
        if search_text in book.get("title", "").lower():
            result.append(book_id)
    return result
    pass
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    if borrower is None or borrower.strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[book_id]
    if not book.get("available", False):
        return "NOT_AVAILABLE"

    book["available"] = False
    loans.append({
        "book_id": book_id,
        "borrower": borrower.strip()
    })
    return "OK"
    pass

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    if borrower is None or borrower.strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[book_id]
    if book.get("available", False):
        return "NOT_ON_LOAN"

    for loan in loans:
        if loan.get("book_id") == book_id and loan.get("borrower", "").lower() == borrower.strip().lower():
            loans.remove(loan)
            book["available"] = True
            return "OK"

    return "NOT_ON_LOAN"
    pass

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    filename = "library.json"
    data = load_library(filename)

    books = data.get("books", {})
    loans = data.get("loans", [])

    while True:
        print("\n" + "=" * 60)
        print("LIBRARY USER SYSTEM")
        print("=" * 60)
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Display all books")
        print("6. Show library statistics")
        print("7. Exit")

        try:
            choice = input("Please select an option (1-7): ").strip()
        except EOFError:
            save_library(data, filename)
            print("\nLibrary data saved. Goodbye!")
            break

        if choice == "1":
            search_text = input("Enter title or part of title: ").strip()
            book_ids = search_by_title(books, search_text)
            if not book_ids:
                print("No books found.")
            else:
                for book_id in book_ids:
                    book = books[book_id]
                    status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
                    print(f"{book_id} | {book.get('title')} | {book.get('category')} | {status}")

        elif choice == "2":
            category = input("Enter category: ").strip()
            book_ids = books_in_category(books, category)
            if not book_ids:
                print("No books found in this category.")
            else:
                for book_id in book_ids:
                    book = books[book_id]
                    status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
                    print(f"{book_id} | {book.get('title')} | {book.get('category')} | {status}")

        elif choice == "3":
            search_text = input("Enter book title or ID: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = borrow_book(books, loans, search_text, borrower)
            if result == "OK":
                print("Book borrowed successfully.")
            elif result == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif result == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif result == "NOT_AVAILABLE":
                print("Book is not available (already on loan).")

        elif choice == "4":
            book_title = input("Enter book title or ID: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = return_book(books, loans, book_title, borrower)
            if result == "OK":
                print("Book returned successfully.")
            elif result == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif result == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif result == "NOT_ON_LOAN":
                print("This book is not on loan by this borrower.")

        elif choice == "5":
            display_books(books)

        elif choice == "6":
            total, available, borrowed = library_statistics(books)
            print("\nLIBRARY STATISTICS")
            print("-" * 60)
            print(f"Total books: {total}")
            print(f"Available: {available}")
            print(f"Borrowed: {borrowed}")

        elif choice == "7":
            save_library(data, filename)
            print("Library data saved. Goodbye!")
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()

    pass

