class Person: 
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return (f"\nHi, my name is {self.name.title()} and I'm {self.age} years old.")

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    # Method Overriding
    def introduce(self):
        student_intro = super().introduce()
        return (f"{student_intro} My student ID is {self.student_id}.\n")

class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject
    
    def introduce(self):
        teacher_intro = super().introduce()
        return (f"{teacher_intro} I teach {self.subject}.\n")

s1 = Student("Alice", 16, "S001")
t1 = Teacher("Mr. Smith", 35, "Mathematics")
print(s1.introduce())
print(t1.introduce())