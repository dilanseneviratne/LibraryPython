import os
from book import Book
from student import Student
from transaction import Transaction

# File Path
BOOK_FILE = "book.csv"
STUDENT_FILE = "student.csv"
TRANSACTION_FILE = "transactions.csv"

BOOK_HEADER = "book_id, title, isbn, author, copies, availability, price"
STUDENT_HEADER = "student_id, first_name"
TRANSACTION_HEADER = "date, book_id, student_id, type"


# Book File
# reads book.csv and returns a list of book objectives
def load_books():
    books = []
    if not os.path.exists(BOOK_FILE):
        return books
    with open(BOOK_FILE, "r") as f:
        lines = f.readlines()
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) < 7:
            continue
        try:
            books.append(Book(
                book_id = parts[0].strip(),
                title = parts[1].strip(),
                isbn=parts[2].strip(),
                author = parts[3].strip(),
                copies = int(parts[4].strip()),
                availability = int(parts[5].strip()),
                price = float(parts[6].strip())
            ))
        except ValueError:
            continue
    return books


# write all book objects to book.csv
def save_books(books):
    with open(BOOK_FILE, "w") as f:
        f.write(BOOK_HEADER + "\n")
        for book in books:
            f.write(book.to_csv() + "\n")


# Student file
# reads student.csv and returns a list of student objects.
def load_students():
    students = []
    if not os.path.exists(STUDENT_FILE):
        return students
    with open(STUDENT_FILE, "r") as f:
        lines =  f.readlines()
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) < 2:
            continue
        students.append(Student(
            student_id = parts[0].strip(),
            first_name = parts[1].strip(),
        ))
    return students

def save_students(students):
    with open(STUDENT_FILE, "w") as f:
        f.write(STUDENT_HEADER + "\n")
        for student in students:
            f.write(student.to_csv() + "\n")


# Transaction File
#Reads the transaction.csv and returns a list of Transaction Objects
def load_transactions():
    transactions = []
    if not os.path.exists(TRANSACTION_FILE):
        return transactions
    with open(TRANSACTION_FILE, "r") as f:
        lines = f.readlines()
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) < 4:
            continue
        try:
            transactions.append(Transaction(
                date = parts[0].strip(),
                book_id = parts[1].strip(),
                student_id = parts[2].strip(),
                tx_type = parts[3].strip()
            ))
        except ValueError:
            continue
    return transactions


#writes all transaction objects to transaction.csv
def save_transactions(transactions):
    with open(TRANSACTION_FILE, "w") as f:
        f.write(TRANSACTION_HEADER + "\n")
        for tx in transactions:
            f.write(tx.to_csv() + "\n")

#Appends a single transaction to transaction.csv (more efficient than rewriting)
def append_transactions(tx):
    file_exists = os.path.exists(TRANSACTION_FILE)
    with open(TRANSACTION_FILE, "a") as f:
        if not file_exists:
            f.write(TRANSACTION_HEADER + "\n")
            f.write(tx.to_csv() + "\n")