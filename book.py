class Book:
    def __init__(self, book_id, title, author, isbn, copies, availability, price):
        self.book_id = book_id
        self.title = title
        self.isbn = isbn
        self.author = author
        self.copies = copies
        self.availability = availability
        self.price = price

    def to(self):
        return f"{self.book_id}, {self.title}, {self.author}, {self.isbn}, {self.copies}, {self.availability}, {self.price:.2f}"

    def __str__(self):
        status = "Available" if self.availability > 0 else "All Issued"
        return (f" ID: {self.book_id}\n"
                f" Title: {self.title}\n"
                f" ISBN: {self.isbn}\n"
                f" Author: {self.author}\n"
                f" Copies: {self.copies}\n"
                f" Availability: {self.availability}\n"
                f" Price: {self.price:.2f}\n"
                f" Status: {status}")