"""
Handles book issuing and retaining operations
"""

import file_handler as fh
import validator as v


"""
Issues a book to a student.
Validates: book id, student id, date, availability, duplicate issue
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

    # Check: same student cannot borrow same book two times( must return first inorder to ake the second time)
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
    fh.save_books(book)

    fh.append_transaction({
        "date": date,
        "book_id": book_id,
        "student_id": student_id,
        "type": 1
    })

    print(f"Book '{book['title']} issued to student '{student_id}' od date '{date}'.")
    print(f"remaining copies available: {book['availability']}")