import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("850x550")
        self.db = DatabaseManager()

        # UI Form Variables
        self.roll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.marks_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Header Title
        title = tk.Label(self.root, text="Student Management System", font=("Arial", 18, "bold"), bg="#1e293b", fg="white", pady=10)
        title.pack(fill=tk.X)

        # Main Layout Container
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Frame: Data Entry Form
        form_frame = tk.LabelFrame(main_frame, text="Student Information", font=("Arial", 11, "bold"), padx=10, pady=10)
        form_frame.place(x=0, y=0, width=320, height=450)

        fields = [
            ("Roll No:", self.roll_var),
            ("Name:", self.name_var),
            ("Email:", self.email_var),
            ("Course:", self.course_var),
            ("Marks (out of 100):", self.marks_var)
        ]

        for idx, (label_text, var) in enumerate(fields):
            tk.Label(form_frame, text=label_text, font=("Arial", 10)).grid(row=idx*2, column=0, sticky="w", pady=(5, 0))
            tk.Entry(form_frame, textvariable=var, font=("Arial", 10)).grid(row=idx*2+1, column=0, sticky="ew", pady=(0, 5))

        form_frame.columnconfigure(0, weight=1)

        # Form Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=10, column=0, pady=15, sticky="ew")

        tk.Button(btn_frame, text="Add", command=self.add_student, bg="#16a34a", fg="white", width=8).grid(row=0, column=0, padx=2)
        tk.Button(btn_frame, text="Update", command=self.update_student, bg="#2563eb", fg="white", width=8).grid(row=0, column=1, padx=2)
        tk.Button(btn_frame, text="Delete", command=self.delete_student, bg="#dc2626", fg="white", width=8).grid(row=0, column=2, padx=2)
        tk.Button(btn_frame, text="Clear", command=self.clear_entries, bg="#475569", fg="white", width=8).grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

        # Right Frame: Search & Table View
        display_frame = tk.Frame(main_frame)
        display_frame.place(x=335, y=0, width=485, height=450)

        # Search Bar
        search_frame = tk.Frame(display_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(search_frame, text="Search Roll No:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 5))
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(search_frame, text="Search", command=self.search_student, bg="#0284c7", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(search_frame, text="Reset", command=self.load_data, bg="#64748b", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(search_frame, text="Mark Sheet", command=self.generate_marksheet, bg="#8b5cf6", fg="white").pack(side=tk.RIGHT)

        # Data Table (Treeview)
        scroll_y = tk.Scrollbar(display_frame, orient=tk.VERTICAL)
        self.student_table = ttk.Treeview(display_frame, columns=("roll", "name", "email", "course", "marks"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("marks", text="Marks")
        self.student_table["show"] = "headings"

        self.student_table.column("roll", width=60)
        self.student_table.column("name", width=110)
        self.student_table.column("email", width=130)
        self.student_table.column("course", width=80)
        self.student_table.column("marks", width=50)

        self.student_table.pack(fill=tk.BOTH, expand=True)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor_data)

    # Controller Actions
    def load_data(self):
        """Refreshes the Treeview table with current database records."""
        self.student_table.delete(*self.student_table.get_children())
        rows = self.db.fetch_all_students()
        for row in rows:
            self.student_table.insert("", tk.END, values=row)

    def add_student(self):
        if not self.validate_inputs():
            return
        success, msg = self.db.add_student(
            int(self.roll_var.get()), self.name_var.get(),
            self.email_var.get(), self.course_var.get(), int(self.marks_var.get())
        )
        if success:
            messagebox.showinfo("Success", msg)
            self.load_data()
            self.clear_entries()
        else:
            messagebox.showerror("Error", msg)

    def update_student(self):
        if not self.validate_inputs():
            return
        updated = self.db.update_student(
            int(self.roll_var.get()), self.name_var.get(),
            self.email_var.get(), self.course_var.get(), int(self.marks_var.get())
        )
        if updated:
            messagebox.showinfo("Success", "Record updated successfully!")
            self.load_data()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Roll Number not found!")

    def delete_student(self):
        roll = self.roll_var.get()
        if not roll:
            messagebox.showerror("Error", "Please select or enter a Roll Number to delete.")
            return
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete Roll No: {roll}?"):
            if self.db.delete_student(int(roll)):
                messagebox.showinfo("Success", "Record deleted!")
                self.load_data()
                self.clear_entries()
            else:
                messagebox.showerror("Error", "Record not found.")

    def search_student(self):
        query = self.search_var.get()
        if not query.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Roll Number.")
            return
        row = self.db.search_student(int(query))
        self.student_table.delete(*self.student_table.get_children())
        if row:
            self.student_table.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("Not Found", "No student found with that Roll Number.")

    def generate_marksheet(self):
        selected = self.student_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a student from the table first.")
            return
        values = self.student_table.item(selected, "values")
        
        # Calculate Grade
        marks = int(values[4])
        grade = "A+" if marks >= 90 else "A" if marks >= 75 else "B" if marks >= 60 else "C" if marks >= 50 else "F"
        status = "PASSED" if marks >= 50 else "FAILED"

        # Display Pop-up Mark Sheet
        ms_window = tk.Toplevel(self.root)
        ms_window.title(f"Mark Sheet - {values[1]}")
        ms_window.geometry("300x260")
        
        tk.Label(ms_window, text="OFFICIAL MARK SHEET", font=("Arial", 12, "bold")).pack(pady=10)
        details = f"""
        Roll Number: {values[0]}
        Name: {values[1]}
        Course: {values[3]}
        ----------------------------------
        Total Marks: {values[4]} / 100
        Grade Assigned: {grade}
        Final Status: {status}
        """
        tk.Label(ms_window, text=details, font=("Courier", 10), justify=tk.LEFT).pack(pady=5)

    def get_cursor_data(self, ev):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        row = content["values"]
        if row:
            self.roll_var.set(row[0])
            self.name_var.set(row[1])
            self.email_var.set(row[2])
            self.course_var.set(row[3])
            self.marks_var.set(row[4])

    def clear_entries(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.course_var.set("")
        self.marks_var.set("")
        self.search_var.set("")

    def validate_inputs(self):
        if not (self.roll_var.get() and self.name_var.get() and self.email_var.get() and self.course_var.get() and self.marks_var.get()):
            messagebox.showerror("Validation Error", "All fields are required!")
            return False
        if not self.roll_var.get().isdigit():
            messagebox.showerror("Validation Error", "Roll Number must be an integer!")
            return False
        if not self.marks_var.get().isdigit() or not (0 <= int(self.marks_var.get()) <= 100):
            messagebox.showerror("Validation Error", "Marks must be an integer between 0 and 100!")
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()