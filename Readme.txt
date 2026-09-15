# Student Management System (Python & SQLite)

A desktop application designed for educational administrators to manage student records, perform real-time roll number lookups, and generate automated mark sheets.

## Architecture
- **Language:** Python 3.x
- **GUI Framework:** Tkinter / TTK
- **Database:** SQLite3
- **Design Pattern:** Separated Data Access Layer (`database.py`) and Presentation Layer (`app.py`)

## Key Features
- **Full CRUD Support:** Add, search, update, and remove student data.
- **Data Integrity:** Parameterized SQL queries prevent injection; input validation guards against invalid data types.
- **Automated Mark Sheet Generator:** Evaluates student score thresholds and dynamically assigns grades (A+, A, B, C, F).

## How to Run
```bash
python app.py