# Gradebook

A small command-line gradebook that stores students, courses, enrollments, and grades in a JSON file. It uses only Python's standard library.

## Sample data

Run the seed script from the project folder. This replaces the current data with three students, two courses, and sample grades:

```powershell
python -m scripts.seed
```

## Usage

Run commands from the project folder:

```powershell
python main.py add-student --name "Jordan Park"
```

Expected output:

```text
Added student with ID 4.
```

More examples:

```powershell
python main.py add-course --code CS101 --title "Programming Basics"
python main.py enroll --student-id 4 --course CS102
python main.py add-grade --student-id 4 --course CS102 --grade 95
python main.py list students --sort name
python main.py list courses --sort code
python main.py list enrollments
python main.py avg --student-id 4 --course CS102
python main.py gpa --student-id 4
```

The JSON data is stored in `data/gradebook.json`; activity is logged to `logs/app.log`.

## Design decisions & limitations

- The program reads and writes the whole JSON file for each operation, which is easy to understand but not suitable for large data sets or simultaneous users.
- GPA is the simple mean of a student's available course averages. It is not weighted by credits.
- IDs are assigned in order. Grades accept numbers from 0 through 100.
