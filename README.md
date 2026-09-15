# student-system-management
Student Management System is a lightweight desktop application engineered to digitize academic record-keeping and streamline daily administrative tasks in educational settings.
Built with Python, Tkinter, and SQLite, the application provides a central interface where administrators can store, search, modify, and audit student data without manually updating spreadsheets or physical ledgers.
Core Objectives & Value Proposition:
Centralized Data Storage: Replaces scattered spreadsheets with an ACID-compliant, persistent relational database (SQLite).
Operational Efficiency: Speeds up student lookups by Roll Number from minutes to seconds via index-based queries.
Automated Evaluation: Generates instant report cards with dynamic grade calculations based on raw marks.
Data Protection: Implements strict client-side validation rules to maintain clean data (e.g., verifying mark bounds $0\text{--}100$ and enforcing unique roll numbers).
