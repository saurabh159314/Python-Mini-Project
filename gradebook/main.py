import argparse
import logging

from gradebook import service

logger = logging.getLogger(__name__)


def make_parser():
	parser = argparse.ArgumentParser(description="Manage a simple gradebook.")
	commands = parser.add_subparsers(dest="command", required=True)

	student = commands.add_parser("add-student", help="Add a student")
	student.add_argument("--name", required=True)

	course = commands.add_parser("add-course", help="Add a course")
	course.add_argument("--code", required=True)
	course.add_argument("--title", required=True)

	enrollment = commands.add_parser("enroll", help="Enroll a student in a course")
	enrollment.add_argument("--student-id", type=int, required=True)
	enrollment.add_argument("--course", required=True)

	grade = commands.add_parser("add-grade", help="Add a course grade")
	grade.add_argument("--student-id", type=int, required=True)
	grade.add_argument("--course", required=True)
	grade.add_argument("--grade", required=True)

	listing = commands.add_parser("list", help="List gradebook records")
	listing.add_argument(
		"kind", nargs="?", choices=("students", "courses", "enrollments"),
		default="students"
	)
	listing.add_argument("--sort", choices=("name", "code"))

	average = commands.add_parser("avg", help="Show a course average")
	average.add_argument("--student-id", type=int, required=True)
	average.add_argument("--course", required=True)

	gpa = commands.add_parser("gpa", help="Show a student's GPA")
	gpa.add_argument("--student-id", type=int, required=True)
	return parser


def run_command(args):
	if args.command == "add-student":
		student_id = service.add_student(args.name)
		print(f"Added student with ID {student_id}.")
	elif args.command == "add-course":
		service.add_course(args.code, args.title)
		print(f"Added course {args.code}.")
	elif args.command == "enroll":
		service.enroll(args.student_id, args.course)
		print(f"Enrolled student {args.student_id} in {args.course}.")
	elif args.command == "add-grade":
		service.add_grade(args.student_id, args.course, args.grade)
		print(f"Added grade for student {args.student_id} in {args.course}.")
	elif args.command == "list":
		show_list(args.kind, args.sort)
	elif args.command == "avg":
		average = service.compute_average(args.student_id, args.course)
		print(f"Average: {average:.2f}")
	elif args.command == "gpa":
		gpa = service.compute_gpa(args.student_id)
		print(f"GPA: {gpa:.2f}")


def show_list(kind, sort_by):
	if kind == "students":
		items = service.list_students()
		if sort_by == "code":
			raise ValueError("Students can only be sorted by name.")
	elif kind == "courses":
		items = service.list_courses()
		if sort_by == "name":
			items = sorted(items, key=lambda course: course.title.lower())
	else:
		items = service.list_enrollments()

	if not items:
		print("No records found.")
	else:
		for item in items:
			print(item)


def main():
	parser = make_parser()
	args = parser.parse_args()
	try:
		run_command(args)
	except (ValueError, OSError) as error:
		logger.error("Command failed: %s", error)
		print(f"Error: {error}")
		return 1
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
