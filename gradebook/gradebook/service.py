from . import storage
from .models import Course, Enrollment, Student, parse_grade


def add_student(name):
	data = storage.load_data()
	student_id = max([student["id"] for student in data["students"]], default=0) + 1
	student = Student(student_id, name)
	data["students"].append({"id": student.id, "name": student.name})
	storage.save_data(data)
	return student_id


def add_course(code, title):
	data = storage.load_data()
	course = Course(code, title)
	if any(item["code"] == course.code for item in data["courses"]):
		raise ValueError(f"Course {course.code} already exists.")
	data["courses"].append({"code": course.code, "title": course.title})
	storage.save_data(data)


def enroll(student_id, course_code):
	data = storage.load_data()
	student_exists = any(item["id"] == student_id for item in data["students"])
	course_exists = any(item["code"] == course_code for item in data["courses"])
	if not student_exists:
		raise ValueError(f"Student {student_id} does not exist.")
	if not course_exists:
		raise ValueError(f"Course {course_code} does not exist.")
	if any(
		item["student_id"] == student_id and item["course_code"] == course_code
		for item in data["enrollments"]
	):
		raise ValueError("This student is already enrolled in that course.")
	enrollment = Enrollment(student_id, course_code)
	data["enrollments"].append(
		{
			"student_id": enrollment.student_id,
			"course_code": enrollment.course_code,
			"grades": enrollment.grades,
		}
	)
	storage.save_data(data)


def add_grade(student_id, course_code, grade):
	grade = parse_grade(grade)
	data = storage.load_data()
	for enrollment in data["enrollments"]:
		if (
			enrollment["student_id"] == student_id
			and enrollment["course_code"] == course_code
		):
			enrollment["grades"].append(grade)
			storage.save_data(data)
			return
	raise ValueError("Student is not enrolled in that course.")


def list_students():
	data = storage.load_data()
	students = [Student(item["id"], item["name"]) for item in data["students"]]
	return sorted(students, key=lambda student: student.name.lower())


def list_courses():
	data = storage.load_data()
	courses = [Course(item["code"], item["title"]) for item in data["courses"]]
	return sorted(courses, key=lambda course: course.code.lower())


def list_enrollments():
	data = storage.load_data()
	enrollments = [
		Enrollment(item["student_id"], item["course_code"], item["grades"])
		for item in data["enrollments"]
	]
	return sorted(
		enrollments, key=lambda item: (item.student_id, item.course_code.lower())
	)


def compute_average(student_id, course_code):
	data = storage.load_data()
	for enrollment in data["enrollments"]:
		if (
			enrollment["student_id"] == student_id
			and enrollment["course_code"] == course_code
		):
			grades = enrollment["grades"]
			if not grades:
				raise ValueError("There are no grades for this course yet.")
			return sum(grades) / len(grades)
	raise ValueError("Student is not enrolled in that course.")


def compute_gpa(student_id):
	data = storage.load_data()
	averages = [
		sum(item["grades"]) / len(item["grades"])
		for item in data["enrollments"]
		if item["student_id"] == student_id and item["grades"]
	]
	if not averages:
		raise ValueError("This student has no graded courses yet.")
	return sum(averages) / len(averages)
