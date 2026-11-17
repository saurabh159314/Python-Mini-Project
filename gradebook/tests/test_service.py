
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gradebook import service, storage


class ServiceTests(unittest.TestCase):
    """Check common service operations using temporary JSON files."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "gradebook.json"
        self.patcher = patch.object(storage, "DATA_FILE", self.data_file)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_add_student_returns_id(self):
        student_id = service.add_student("Lucifer Morningstar")
        self.assertEqual(student_id, 1)
        self.assertEqual(service.list_students()[0].name, "Lucifer Morningstar")

    def test_add_grade_and_compute_average(self):
        student_id = service.add_student("Lucifer Morningstar")
        service.add_course("CS101", "Intro to CS")
        service.enroll(student_id, "CS101")
        service.add_grade(student_id, "CS101", 80)
        service.add_grade(student_id, "CS101", 100)
        self.assertEqual(service.compute_average(student_id, "CS101"), 90)

    def test_add_grade_rejects_unenrolled_student(self):
        with self.assertRaisesRegex(ValueError, "not enrolled"):
            service.add_grade(99, "CS101", 80)

    def test_add_grade_rejects_grade_out_of_range(self):
        with self.assertRaisesRegex(ValueError, "0 to 100"):
            service.add_grade(1, "CS101", 101)


if __name__ == "__main__":
    unittest.main()