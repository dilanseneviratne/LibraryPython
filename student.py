class Student:
    def __init__(self, student_id, first_name):
        self.student_id = student_id
        self.first_name = first_name

    def to_csv(self):
        return f"Student ID: {self.student_id}, First Name: {self.first_name}"

    def __str__(self):
        return (f" Student ID: {self.student_id}\n"
                f" First Name: {self.first_name}")