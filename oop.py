class Student:
    def __init__(self, name, roll_number, grade):
        self.__name = name
        self.__roll_number = roll_number
        self.__grade = grade

    def show_info(self):
        print("Name:", self.__name)
        print("Roll Number:", self.__roll_number)
        print("Grade:", self.__grade)

    def get_roll_number(self):
        return self.__roll_number

    def update_grade(self, new_grade):
        self.__grade = new_grade.upper()


class Students_class:
    def __init__(self):
        self.students = []

    def add_student(self):
        name = input("Enter student name: ")
        roll_number = int(input("Enter roll number: "))
        grade = input("Enter grade: ").upper()

        student = Student(name, roll_number, grade)

        self.students.append(student)

        print("Student added successfully")

    def show_all_students(self):
        if len(self.students) == 0:
            print("No students found")
            return

        for student in self.students:
            student.show_info()

    def find_student(self):
        roll_number = int(input("Enter roll number: "))

        for student in self.students:
            if student.get_roll_number() == roll_number:
                student.show_info()
                return

        print("Student not found")

    def update_grade(self):
        roll_number = int(input("Enter roll number: "))

        for student in self.students:
            if student.get_roll_number() == roll_number:
                new_grade = input("Enter new grade: ").upper()
                student.update_grade(new_grade)
                print("Grade updated successfully")
                return
        print("Student not found.")


students_class = Students_class()

while True:
    print("1. Add new student")
    print("2. Show all students")
    print("3. Find student by roll number")
    print("4. Update student grade")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        students_class.add_student()

    elif choice == "2":
        students_class.show_all_students()

    elif choice == "3":
        students_class.find_student()

    elif choice == "4":
        students_class.update_grade()

    elif choice == "5":
        print("Program ended")
        break

    else:
        print("Invalid choice")
