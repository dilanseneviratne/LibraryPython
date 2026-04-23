class Transaction:
    def __init__(self, date, book_id, student_id, tx_type):
        self.date = date
        self.book_id = book_id
        self.student_id = student_id
        self.tx_type = int(tx_type)

    def to_csv(self):
        return f"{self.date}, {self.book_id}, {self.student_id}, {self.tx_type}"

    def type_label(self):
        return "Issue" if self.tx_type == 1 else "Return"

    def __str__(self):
        return (f" Date: {self.date}\n"
                f" Book: {self.book}\n"
                f" Student ID: {self.student_id}\n"
                f" Type: {self.tx_type}\n")