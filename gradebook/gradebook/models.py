
def parse_grade(value):
    try:
        grade = float(value)
    except (TypeError, ValueError):
        raise ValueError("Grade must be a number from 0 to 100.")

    if isinstance(value, bool) or not 0 <= grade <= 100:
        raise ValueError("Grade must be a number from 0 to 100.")
    return grade


class Student:

    def __init__(self, student_id, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty.")
        self.id = student_id
        self.name = name.strip()

    def __str__(self):
        return f"[{self.id}] {self.name}"


class Course:

    def __init__(self, code, title):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code cannot be empty.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Course title cannot be empty.")
        self.code = code.strip()
        self.title = title.strip()

    def __str__(self):
        return f"{self.code}: {self.title}"


class Enrollment:

    def __init__(self, student_id, course_code, grades=None):
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code cannot be empty.")
        self.student_id = student_id
        self.course_code = course_code.strip()
        self.grades = [parse_grade(grade) for grade in (grades or [])]

    def __str__(self):
        return f"Student {self.student_id} in {self.course_code}: {self.grades}"


