"""
Handles all student related operations such as add, view
"""

import file_handler as fh
import validator as v


# Print all students in a formatted table
def display_students(students: list[dict]):
    if not students:
        print("No students found.")
        return
    print("\n" + "-" * 35)
    print(f"{'Student ID':<12} {'First Name':<15}")
    print("-" * 35)
    for s in students:
        print(f"{s['student_id']:<12} {s['first_name']:<15}")
    print("-" * 35)


# Prompt the librarian for student details and save to the csv
def add_student():
    print("\n Add New Student")
    students = fh.load_students()

    # Student ID
    while True:
        student_id = input("Enter student ID (8 digits): ").strip()
        if not v.is_valid_student_id(student_id):
            print("Invalid Student ID. Must be exactly 8 digits.")
            continue
        if any(s["student_id"] == student_id for s in students):
            print("Student ID already exists. Must be unique")
            continue
        break


    # First Name
    while True:
        first_name = input("Enter First Name (letters only, maximum 10 characters): ").strip()
        if not v.validate_first_name(first_name):
            print("Invalid name. Letters only, maximum 10 characters only.")
            continue
        break

    students.append({"student_id": student_id, "first_name": first_name})
    fh.save_students(students)
    print(f"\n Student '{first_name}' (ID: {student_id}) added successfully.")


# display all registered students
def view_students():
    print("\n All Students ")
    students = fh.load_students()
    display_students(students)