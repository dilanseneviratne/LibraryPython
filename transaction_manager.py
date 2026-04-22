"""
Handles book issuing and retaining operations
"""
import file_handler as fh
import validator as v


"""
Issues a book to a student.
"""
def issue_book():
    print("\n Issue Book")
    books = fh.load_books()
    students = fh.load_students()
    transactions = fh.load_transactions()

    # Book ID
    book_id = input("Enter book id: ").strip().upper()
    book = next((b for b in books if b["book_id"] == book_id), None)
    if not book:
        print(f"Invalid Book ID '{book_id}'. Book not found.")
        return

    # Student ID
    student_id = input("Enter student id: ").strip()
    if not any(s['student_id'] == student_id for s in students):
        print(f"Invalid Student ID '{student_id}'. Student not found.")
        return

    # Date
    date = input("Enter Issue Date (DD/MM/YYYY): ").strip()
    if not v.is_valid_date(date):
        print("Invalid date format. Use DD/MM/YYYY format.")
        return

    # Check Availability
    if book["availability"] <=0:
        print(f"Book '{book['title']} has no available copies.")
        return

    # Check: same student cannot borrow same book two times( must return first inorder to take the second time)
    already_issued = any(
        t["book_id"] == book_id and
        t["student_id"] == student_id and
        t["type"] == 1
        for t in _get_active_issues(transactions)
    )
    if already_issued:
        print(f"Student '{student_id}' already has a copy of '{book['title']}'.")
        return

    # Issue the Book
    book["availability"] -= 1
    fh.save_books(books)

    fh.append_transaction({
        "date": date,
        "book_id": book_id,
        "student_id": student_id,
        "type": 1
    })

    print(f"Book '{book['title']} issued to student '{student_id}' od date '{date}'.")
    print(f"remaining copies available: {book['availability']}")


def return_book():
    print("\n Return Book")
    books = fh.load_books()
    students = fh.load_students()
    transactions = fh.load_transactions()

    # Book ID
    book_id = input("Enter Book ID: ").strip().upper()
    book = next((b for b in books if b["book_id"] == book_id), None)
    if not book:
        print(f"Invalid Book ID '{book_id}'. Book not found.")
        return

    #Student ID
    student_id = input("Enter student ID: ").strip()
    if not any(s['student_id'] == student_id for s in students):
        print(f"Invalid Student ID '{student_id}'. Student not found.")
        return

    #date
    date = input("Enter return date (DD/MM/YYYY): ").strip()
    if not v.is_valid_date(date):
        print("Invalid date format. Use DD/MM/YYYY format.")
        return

    # Check that the book is actually issued to the student
    active = _get_active_issues(transactions)
    issue_exists = any(
        t["book_id"] == book_id and t["student_id"] == student_id
        for t in active
    )
    if not issue_exists:
        print(f"No active issue found for Book '{book_id}' and Student '{student_id}'.")
        return

    #Check availability won't exceed copies
    if book['availability'] >= book["copies"]:
        print(f"Book already returned. Availability cannot exceed total copies.")
        return

    # Return the book
    book['availability'] += 1
    fh.save_books(book)

    fh.save_students({
        "date": date,
        "book_id": book_id,
        "student_id": student_id,
        "type": 2
    })

    print(f"\n Book '{book['title']}' returned by student {student_id} on {date}.")
    print(f"Copies now available: {book['availability']}")


def _get_active_issues(transactions: list[dict]) -> list[dict]:
    active = []
    for t in transactions:
        if t["type"] == 1:
            #Check if this issue has a corresponding return
            returned  = any(
                r['book_id'] == t["book_id"] and
                r["student_id"] == t["student_id"] and
                r["type"] == 2
                for r in transactions
                if transactions.index(r) > transactions.index(t)
            )
            if not returned:
                active.append(t)
    return active


def view_transactions():
    print("\n All transactions")
    transactions = fh.load_transactions()
    if not transactions:
        print("No transactions found.")
        return
    print("\n" + "-" * 55)
    print(f"{'Date':<12} {'Book ID':<10} {'Student ID':<12} {'Type':<10}")
    print("-" * 55)
    for t in transactions:
        type_label = "Issue" if t['type'] == 1 else "Return"
        print(f"{t['date']:<12} {t['book_id']:<10} {t['student_id']:<12} {type_label:<10}")
    print("-" * 55)