##Import the necessary module
import json

## This function should load the library data from a JSON file and return it as a suitable Python data structure.
def load_library(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data
    
    pass



## This function should save the library data to a JSON file.
## This function does not need to return anything, but it should ensure that the data is saved correctly to the specified file.
def save_library(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    pass
    



## This function should find a book by its title, author, or ID.
## If the book is found, it should return the book ID.
## If the book is not found, it should return None.
def find_book(books, search_text):
    search_text = search_text.strip().lower()
    for book_id, book in books.items():
        if book_id.lower() == search_text:
            return book_id

    for book_id, book in books.items():
        title = book.get("title", "").lower()
        author = book.get("author", "").lower()
        if search_text in title or search_text in author:
            return book_id

    return None
    pass



## This function should display the list of books in a user-friendly format.
## It should show the book ID, title, category, and availability status (available or on loan).
## If the book is available, it should display "AVAILABLE", and if it is on loan, it should display "ON LOAN".
## The function should not return anything, but it should print the information to the console.
## The heading for this display should be "BOOK CATALOGUE".
def display_books(books):
    print("\nBOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        status = "AVAILABLE" if book.get("available",False) else "ON LOAN"
        print(f"{book_id} | {book.get('title', '')} | {book.get('category', '')} | {status}")
    pass


## This function should display the list of current loans in a user-friendly format.
## It should show the book ID, title, and the name of the borrower.
## The heading for this display should be "CURRENT LOANS".
## The function should not return anything, but it should print the information to the console.
def display_loans(loans, books):
    print("\nCURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan.get("book_id")
        borrower = loan.get("borrower", "")
        title = books.get(book_id, {}).get("title", "")
        print(f"{book_id} | {title} | Borrower: {borrower}")
    pass


## This function should calculate and return the library statistics
## The statsitics should include the total number of books, the number of available books, and the number of borrowed books.
## The function should return these three values in the order: total, available, borrowed. Use a suitable data structure to return these values, such as a tuple or a dictionary.

def library_statistics(books):
    total = len(books)
    available = sum(1 for book in books.values() if book.get("available", False))
    borrowed = total - available
    return total, available, borrowed
    pass


## This function should display the library statistics in a user-friendly format.
## It should first load the library data from a JSON file, 
## Then calculate the statistics, and finally print the information to the console.
## The heading for this display should be "LIBRARY STATISTICS".
## It should print the total number of books, the number of available books, and the number of borrowed books.
## The function should not return anything, but it should print the information to the console.
def main():
    filename = "library.json"
    data = load_library(filename)

    books = data.get("books", {})
    loans = data.get("loans", [])
    library_info = data.get("library", {})
    categories = data.get("categories", [])

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library_info.get('name', '')}")
    print(f"Branch: {library_info.get('branch', '')}")
    print(f"Year: {library_info.get('year', '')}")
    print(f"Categories: {', '.join(categories)}")

    display_books(books)
    display_loans(loans, books)

    total, available, borrowed = library_statistics(books)

    print("\nLIBRARY STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()

    pass


## Following is how the Admin interface should look like when the program is run. 
# The actual output may vary based on the library data and the current state of loans.

""" 
LIBRARY ADMINISTRATION
============================================================
Library: 
Branch: 
Year: 
Categories: 

BOOK CATALOGUE
------------------------------------------------------------
ID1 | Title1 | Category | Availability
ID2 | Title2 | Category | Availability
...
...
...
IDN | TitleN | Category | Availability


CURRENT LOANS
------------------------------------------------------------
ID1 | Title1 | Borrower: Borrower1
ID2 | Title2 | Borrower: Borrower2
...
...
...
IDN | TitleN | Borrower: BorrowerN

STATISTICS
------------------------------------------------------------
Total books: XX
Available: XX
Borrowed: XX
"""