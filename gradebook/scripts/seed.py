
from gradebook import service
from gradebook.storage import empty_data, save_data


def seed():
	save_data(empty_data())
	sau_id = service.add_student("Saurabh")
	moh_id = service.add_student("mohit")
	geo_id = service.add_student("george")
	service.add_course("CS101", "Introduction to Computer Science")
	service.add_course("MTL201", "Introduction to Algebra")
	service.enroll(sau_id, "CS101")
	service.enroll(sau_id, "MTL201")
	service.enroll(geo_id, "MTL201")
	service.enroll(moh_id, "CS101")
	service.add_grade(sau_id, "CS101", 95)
	service.add_grade(sau_id, "CS101", 65)
	service.add_grade(sau_id, "MTL201", 88)
	service.add_grade(geo_id, "MTL201", 91)
	service.add_grade(moh_id, "CS101", 84)
	print("Sample gradebook created.")


if __name__ == "__main__":
	seed()
