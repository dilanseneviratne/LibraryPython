""""
Handles all book related tasks such as search, add, edit, view.
"""

import file_handler as fh
import validator as v


#display all books in a formatted table
def display_books(books: list[dict]):
    if not books:
        print("\n No books found.")
        return
    print("\n" + "-" * 85)
    print(f"{'ID':<6} {'Title':<22} {'ISBN-13':<15} {'Author':<20} {'Cop':>4} {'Avail':>6} {'Price':>7}")
    print("-" * 85)
    for b in books:
        print(f"{b['book_id']:<6} {b['title']:<22} {b['isbn']:<15} {b['author']:<20} "
              f"{b['copies']:>4} {b['availability']:>6} £{b['price']:>6.2f}")
        print("-" * 85)


#prompt the librarian for book details and save to csv
def add_book():
    print("\n Add New Book")
    books = fh.load_books()

    # Book ID
    while True:
        book_id = input("Enter Book ID (2 letters + 2 digits, eg:AB01): ").strip().upper()
        if not v.is_valid_book_id(book_id):
            print("Invalid Book ID. Must be 2 letters followed by 2 digits.")
            continue
        if any(b["book_id"] == book_id for b in books):
            print("Book ID already exists. Please choose another ID which is unique.")
            continue
        break

    # ISBN-13
    while True:
        isbn = input("Enter ISBN: ").strip()
        if not v.validate_isbn13(isbn):
            print("Invalid ISBN-13. Check digit validation failed.")
            continue
        break

    # Title
    while True:
        title = input("Enter Title (letters only, max 20 characters): ").strip()
        if not v.validate_title(title):
            print("Invalid title. Letters and spaces only, maximum of 20 characters only.")
            continue
        break

    # Author
    author = input("Enter Author name: ").strip()

    # Copies
    while True:
        try:
            copies = int(input("Enter number of copies (1 or 2): ").strip())
            if not v.validate_copies(copies):
                print("Copies must be 1 or 2.")
                continue
            break
        except ValueError:
            print("Please enter a number.")

    # Price
    while True:
        price_str = input("Enter Price (eg: 10.99): ").strip()
        if not v.validate_price(price_str):
            print("Invalid price. Enter a positive number.")
            continue
        price = float(price_str)
        break

    book = {
        "book_id": book_id,
        "title": title,
        "isbn": isbn,
        "author": author,
        "copies": copies,
        "availability": copies,
        "price": price
    }

    books.append(book)
    fh.save_books(books)
    print(f"\n Book '{title}' (ID: {book_id}) has been added successfully.")


# Edit an existing book's details using its ID
def edit_book():
    print("\n Edit Book")
    books = fh.load_books()
    display_books(books)

    book_id = input("\n Enter Book ID to edit: ").strip().upper()
    book = next((b for b in books if b["book_id"] == book_id), None)

    if not book:
        print(f"Book ID '{book_id}' not found.")
        return

    print(f"\n Editing: {book['title']} - press Enter to keep the current value.")

    # Title
    new_title = input(f"Title [{book['title']}]: ").strip()
    if new_title:
        if not v.is_validate_title(new_title):
            book['title'] = new_title
        else:
            print("Invalid title - Not updated.")

    # Author
    new_author = input(f"Author [{book['author']}]: ").strip()
    if new_author:
        book["author"] = new_author

    #Price
    new_price = input(f"Price [Rs.{book['price']:.2f}]: ").strip()
    if new_price:
        if v.is_validate_price(new_price):
            book["price"] = float(new_price)
        else:
            print("Invalid price - Not updated.")

    fh.save_books(books)
    print(f"\n Book'{book_id}' has been updated successfully.")


#Search books by title (partial match, case-insensitive).
def search_books():
    print("\n Search Books")
    books = fh.load_books()
    query = input("Enter Title to search: ").strip().lower()
    results = [b for b in books if query in b["title"].lower()]
    if results:
        display_books(results)
    else:
        print(f"No books found matching '{query}'.")


#Display all the books in the library
def view_all_books():
    print("\n View All Books")
    books = fh.load_books()
    display_books(books)