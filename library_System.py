"""
Library Management System
"""
from random import choice

from book import Book
from student import Student
from transaction import Transaction
import file_manager as fm
import validator as v
from graph import show_trend_graph

books = []
students = []
transactions = []


def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title}")
    print("=" * 50)

def print_success(msg):
    print(f"\n [OK] {msg}")

def print_error(msg):
    print(f"\n [ERROR] {msg}")

def print_info(msg):
    print(f"\n [INFO] {msg}")

def pause():
    input("\n Press Enter to continue ...")


# Find Helpers

def find_book(book_id):
    for book in books:
        if book.book_id.upper() == book_id.upper():
            return book
    return None

def find_student(student_id):
    for student in students:
        if student.student_id == student_id:
            return student
    return None

def active_issues(book_id, student_id):
    issued   = sum(1 for tx in transactions if tx.book_id.upper() == book_id.upper() and tx.student_id == student_id and tx.tx_type == 1)
    returned = sum(1 for tx in transactions if tx.book_id.upper() == book_id.upper() and tx.student_id == student_id and tx.tx_type == 2)
    return issued - returned


# Book Management

def add_book():
    print_header("Add Book")

    while True:
        book_id = input("Enter Book ID (eg: AB01): ").strip()
        ok, err = v.validate_book_id(book_id)
        if not ok: print_error(err); continue
        if find_book(book_id): print_error(f"Book ID '{book_id} already exists"); continue
        break

    while True:
        title = input("Enter Title (letters only, max 20 chars): ").strip()
        ok, err = v.validate_title(title)
        if not ok: print_error(err)
        else:
            break

    while True:
        isbn = input("Enter ISBN-13 (13 digits): ").strip()
        ok, err = v.validate_isbn13(isbn)
        if not ok: 
            print_error(err)
            continue
            
        if any(b.isbn == isbn for b in books):
            print_error(f"Book with ISBN '{isbn}' already exists.")
            continue
            
        break

    author = input("Enter Author Name: ").strip()

    while True:
        ok, copies, err = v.validate_copies(input("Enter Number of Copies(1 or 2): ").strip())
        if not ok: print_error(err)
        else:
            break

    while True:
        ok, price, err = v.validate_price(input("Enter Price (eg 10.99): Rs.").strip())
        if not ok: print_error(err)
        else:
            break

    book = Book(book_id.upper(), title, isbn, author, copies, copies, price)
    books.append(book)
    fm.save_books(books)
    print_success(f"Book '{ title}' added successfully")
    pause()


def edit_book():
    print_header("EDIT BOOK")
    book_id = input("Enter Book ID to edit: ").strip()
    book = find_book(book_id)
    if not book:
        print_error(f"Book ID '{book_id}' not found.")
        pause(); return

    print(f"\n Current Details:\n{book}")
    print("\n Leave blank to keep currant value.\n")

    new_title = input(f"New Title [{book.title}]: ").strip()
    if new_title:
        ok, err = v.validate_title(new_title)
        if ok: book.title = new_title
        else: print_error(err + "- keeping original.")

    new_author = input(f"New Author [{book.author}]: ").strip()
    if new_author:
        book.author = new_author

    new_price = input(f"new Price [Rs. {book.price:.2f}]: Rs. ").strip()
    if new_price:
        ok, price, err = v.validate_price(new_price)
        if ok: book.price = price
        else: print_error(err + "- keeping original.")

    fm.save_books(books)
    print_success("Book updated successfully")
    pause()


def search_book():
    print_header("SEARCH BOOK")
    query = input("Enter Book ID or part of Title: ").strip().lower()
    results = [b for b in books if query in b.book_id.lower() or query in b.title.lower()]
    if not results:
        print_info("No books found.")
    else:
        print(f"\n Found {len(results)} result(s):\n")
        for book in results:
            print(book)
            print(" " + "-" * 40)
    pause()


def view_all_books():
    print_header("VIEW All BOOKS")
    if not books:
        print_info("No books in the library yet.")
    else:
        print(f" Total: {len(books)} book(s)\n")
        for book in books:
            print(book)
            print("  " + "-" * 40)
    pause()


def book_menu():
        while True:
            print_header("BOOK MANAGEMENT")
            print("1. Add Book")
            print("2. Edit Book")
            print("3. Search Book")
            print("4. View All Books")
            print("0. Back")

            choice = input("\n Select option: ").strip()
            if choice == "1": add_book()
            elif choice == "2": edit_book()
            elif choice == "3": search_book()
            elif choice == "4": view_all_books()
            elif choice == "0": break
            else: print_error("Invalid option.")



# Add Student

def add_student():
    print_header("ADD STUDENT")

    while True:
        student_id = input("Enter Student ID (8 digits): ").strip()
        ok, err = v.validate_student_id(student_id)
        if not ok:
            print_error(err); continue
        if find_student(student_id):
            print_error(f"Student ID '{student_id}' already exists"); continue
        break

    while True:
        first_name = input("Enter First Name (letters only, max 10 characters): ").strip()
        ok, err = v.validate_first_name(first_name)
        if not ok: print_error(err)
        else: break

    students.append(Student(student_id, first_name))
    fm.save_students(students)
    print_success(f"Student '{first_name}' (ID: {student_id}) added successfully")
    pause()



# Issue Book

def issue_book():
    print_header("ISSUE BOOK")

    book_id = input("Enter Book ID: ").strip()
    book = find_book(book_id)
    if not book:
        print_error(f"Book ID '{book_id}' not found.")
        pause(); return

    if book.availability <= 0:
        print_error(f"No copies of '{book.title}' are available.")
        pause(); return

    student_id = input("Enter Student ID: ").strip()
    student = find_student(student_id)
    if not student:
        print_error(f"Student ID '{student_id}' not found.")
        pause(); return

    if active_issues(book_id, student_id) > 0:
        print_error(f"Student '{student.first_name}' already has '{book.title}' issued.")
        pause(); return

    while True:
        date_str = input("Enter Issue Date (DD/MM/YYYY): ").strip()
        ok, err = v.validate_date(date_str)
        if not ok: print_error(err)
        else: break

    tx = Transaction(date_str, book.book_id, student_id, 1)
    transactions.append(tx)
    fm.append_transactions(tx)

    book.availability -= 1
    fm.save_books(books)

    print_success(f"Book '{book.title}' issued to {student.first_name} on {date_str}.")
    print(f"Remaining copies available: {book.availability}")
    pause()



# Return Book

def return_book():
    print_header("RETURN BOOK")

    book_id = input("Enter Book ID: ").strip()
    book = find_book(book_id)
    if not book:
        print_error(f"Book ID '{book_id}' not found.")
        pause(); return

    student_id = input("Enter Student ID: ").strip()
    student = find_student(student_id)
    if not student:
        print_error(f"Student ID '{student_id}' not found.")
        pause(); return

    if active_issues(book_id, student_id) <= 0:
        print_error(f"No active issue found for student '{student.first_name}' and book '{book.title}'.")
        pause(); return

    if book.availability >= book.copies:
        print_error(f"All copies of '{book.title}' are already returned.")
        pause(); return

    while True:
        date_str = input("Enter Return Date (DD/MM/YYYY): ").strip()
        ok, err = v.validate_date(date_str)
        if not ok:
            print_error(err)
        else:
            break

    tx = Transaction(date_str, book.book_id, student_id, 1)
    transactions.append(tx)
    fm.append_transactions(tx)

    book.availability += 1
    fm.save_books(books)

    print_success(f"Book '{book.title}' returned by {student.first_name} on {date_str}.")
    print(f"Copies now available: {book.availability}")
    pause()



# Main Menu

def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("Library Management System")
        print("=" * 50)
        print("1. Book Management")
        print("2. Add Student")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View Trend Graph")
        print("0. Exit")
        print("-" * 50)

        choice = input("Select an option: ").strip()
        if choice == "1": book_menu()
        elif choice == "2": add_student()
        elif choice == "3": issue_book()
        elif choice == "4": return_book()
        elif choice == "5": show_trend_graph(transactions)
        elif choice == "0":
            print("\n Goodbye!\n")
            break
        else:
            print_error("Invalid option. Please try again.")



# Entry Point

if __name__ == "__main__":
    books = fm.load_books()
    students = fm.load_students()
    transactions = fm.load_transactions()
    print(f"\n  [INFO] Loaded {len(books)} books, {len(students)} students, {len(transactions)} transactions.")
    main_menu()