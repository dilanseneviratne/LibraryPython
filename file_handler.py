import csv
import os

from pandas.io.common import file_exists

BOOK_FILE = "book.csv"
STUDENT_FILE = "student.csv"
TRANSACTION_FILE = "transaction.csv"

BOOK_HEADER = ["book_id", "title", "isbn", "author", "copies", "availability", "price"]
STUDENT_HEADER = ["student_id", "first_name"]
TRANSACTION_HEADER = ["date", "book_id", "student_id", "type"]


# Ensure data directory and files exist
#create the data directory and csv files with headers if they don't exist
def initialize_files():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, "w", newline ="") as f:
            csv.writer(f).writerow(BOOK_HEADER)

    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "w", newline ="") as f:
            csv.writer(f).writerow(STUDENT_HEADER)

    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "w", newline ="") as f:
            csv.writer(f).writerow(TRANSACTION_HEADER)


# Books
#Loads all books from book.csv.
def load_books():
    books = []
    try:
        with open(BOOK_FILE, "r", newline ="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                row["copies"] = int(row["copies"])
                row["availability"] = int(row["availability"])
                row["price"] = int(row["price"])
                books.append(row)
    except FileNotFoundError:
        pass
    return books

# Save the full books list back to book.csv
def save_books(books: list[dict]):
    with open(BOOK_FILE, "w", newline ="") as f:
        writer = csv.DictWriter(f, fieldnames=BOOK_HEADER)
        writer.writeheader()
        writer.writerows(books)


# Students
def load_students():
    students = []
    try:
        with open(STUDENT_FILE, "r", newline ="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        pass
    return students

def save_students(students: list[dict]):
    with open(STUDENT_FILE, "w", newline ="") as f:
        writer = csv.DictWriter(f, fieldnames=STUDENT_HEADER)
        writer.writeheader()
        writer.writerows(students)


# Transactions
def load_transactions() -> list[dict]:
    transactions = []
    try:
        with open(TRANSACTION_FILE, "r", newline ="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["type"] = int(row["type"])
                transactions.append(row)
    except FileNotFoundError:
        pass
    return transactions

def append_transaction(transaction: dict):
    file_exists = os.path.exists(TRANSACTION_FILE)
    with open(TRANSACTION_FILE, "a", newline ="") as f:
        writer = csv.DictWriter(f, fieldnames=TRANSACTION_HEADER)
        if not file_exists:
            writer.writerheader()
        writer.writerow(transaction)