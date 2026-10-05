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


class ScholarshipStudent(Student):
    def __init__(self, name, roll_number, grade, scholarship):
        super().__init__(name, roll_number, grade)
        self.__scholarship = scholarship

    def show_info(self):
        super().show_info()
        print("Scholarship:", self.__scholarship)


class StudentsClass:
    def __init__(self):
        self.students = []

    def add_student(self):
        name = input("Enter student name: ")

        try:
            roll_number = int(input("Enter roll number: "))
        except ValueError:
            print("Roll number must be a number")
            return

        grade = input("Enter grade: ").upper()
        
        student = Student(name, roll_number, grade)
        
        self.students.append(student)

        print("Student added successfully")

    def add_scholarship_student(self):
        name = input("Enter student name: ")

        try:
            roll_number = int(input("Enter roll number: "))
        except ValueError:
            print("Roll number must be a number.")
            return

        grade = input("Enter grade: ").upper()

        try:
            scholarship = float(input("Enter scholarship amount: "))
        except ValueError:
            print("Scholarship must be a number")
            return

        student = ScholarshipStudent(
            name,
            roll_number,
            grade,
            scholarship
        )

        self.students.append(student)

        print("Scholarship student added successfully")

    def show_all_students(self):
        if len(self.students) == 0:
            print("No students found")
            return

        for student in self.students:
            student.show_info()

    def find_student(self):
        try:
            roll_number = int(input("Enter roll number: "))
        except ValueError:
            print("Roll number must be a number.")
            return

        for student in self.students:
            if student.get_roll_number() == roll_number:
                student.show_info()
                return

        print("Student not found")

    def update_grade(self):
        try:
            roll_number = int(input("Enter roll number: "))
        except ValueError:
            print("Roll number must be a number.")
            return

        for student in self.students:
            if student.get_roll_number() == roll_number:

                new_grade = input("Enter new grade: ").upper()

                student.update_grade(new_grade)

                print("Grade updated successfully")
                return

        print("Student not found")


students_class = StudentsClass()


while True:

    print("1. Add new student")
    print("2. Add scholarship student")
    print("3. Show all students")
    print("4. Find student by roll number")
    print("5. Update student grade")
    print("6. Exit")

    choice = input("Choose an option: ")

    try:
        if choice == "1":
            students_class.add_student()

        elif choice == "2":
            students_class.add_scholarship_student()

        elif choice == "3":
            students_class.show_all_students()

        elif choice == "4":
            students_class.find_student()

        elif choice == "5":
            students_class.update_grade()

        elif choice == "6":
            print("Program ended")
            break

        else:
            print("Invalid choice")

    except Exception as e:
        print("Something went wrong:", e)
