import sqlite3

class DatabaseManager:
    def __init__(self, db_name="student_app.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        """Creates and returns a database connection."""
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Creates the students table if it doesn't already exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    roll_no INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    course TEXT NOT NULL,
                    marks INTEGER NOT NULL
                )
            """)
            conn.commit()

    def add_student(self, roll_no, name, email, course, marks):
        """Inserts a new student record into the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (roll_no, name, email, course, marks) VALUES (?, ?, ?, ?, ?)",
                    (roll_no, name, email, course, marks)
                )
                conn.commit()
                return True, "Student added successfully!"
        except sqlite3.IntegrityError:
            return False, "Error: Roll Number already exists!"
        except Exception as e:
            return False, f"Database Error: {str(e)}"

    def fetch_all_students(self):
        """Retrieves all student records."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            return cursor.fetchall()

    def search_student(self, roll_no):
        """Searches for a student by their Roll Number."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
            return cursor.fetchone()

    def update_student(self, roll_no, name, email, course, marks):
        """Updates an existing student's details."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students 
                SET name = ?, email = ?, course = ?, marks = ? 
                WHERE roll_no = ?
            """, (name, email, course, marks, roll_no))
            conn.commit()
            return cursor.rowcount > 0

    def delete_student(self, roll_no):
        """Deletes a student record by Roll Number."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
            conn.commit()
            return cursor.rowcount > 0