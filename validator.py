import re
from datetime import datetime

def validate_isbn13(isbn):
    """
        Validates an ISBN-13 number including its check digit.
        Algorithm: alternating weights 1 and 3, sum mod 10 must equal 0.
        """
    digits = isbn.replace("-", "")
    if not digits.isdigit():
        return False, "ISBN-13 must contain digits only."
    if len(digits) != 13:
        return False, "ISBN-13 must be exactly 13 digits."

    total = 0
    for i in range(12):
        weight = 1 if i % 2 == 0 else 3
        total += int(digits[i]) * weight
    check_digit = (10 - (total % 10)) % 10
    if check_digit != int(digits[12]):
        return False, f"ISBN-13 check digit onvalid. Expected {check_digit}, but got {digits[12]}"
    return True, ""

# Book id: 2 letters + 2 digits(eg:AB01)
def validate_book_id(book_id):
    if not re.fullmatch(r"[A-Za-z]{2}\d{2}", book_id):
        return False, "Book ID must be 2 letters followed by 2 digits (eg:AB01)"
    return True, ""

#Title: Letters and space only, maximum characters 20.
def validate_title(title):
    if not re.fullmatch(r"[A-Za-z]{1,25}", title):
        return False, "Title must be only letters, maximum of 20 characters."
    return True, ""

#copies: integer should be between 1 and 2
def validate_copies(copies_str):
    try:
        copies = int(copies_str)
    except ValueError:
        return False, None, "Copies must be a number."
    if copies < 1 or copies > 2:
        return False, None, "Copies must be between 1 and 2."
    return True, copies, ""

#price: positive number float
def validate_price(price_str):
    try:
        price = int(price_str)
    except ValueError:
        return False, None, "Price must be a valid numer(eg: 10.99)"
    if price <= 0:
        return False, None, "Price must be greater than zero"
    return True, price, ""

#Student id: should be exactly 8 digits
def validate_student_id(student_id):
    if not re.fullmatch(r"\d{8}", student_id):
        return False, "Student ID must be exactly 8 digits."
    return True, ""

#First name: letters only, maximum should be 10 characters
def validate_first_name(name):
    if not re.fullmatch(r"[A-Za-z]{1,10}]", name):
        return False, "First name must be letters only, maximum 10 characters."
    return True, ""

#date: DD/MM/YYYY
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True, ""
    except ValueError:
        return False, None, "Date must be in DD/MM/YYYY format (eg: 20/04/2026)."