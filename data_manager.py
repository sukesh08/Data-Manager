import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="Sukesh@123",  
        database="student_management"
    )

def add_student():
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()
    contact = entry_contact.get()

    if not name or not age or not grade or not contact:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    
    try:
        age = int(age)
    except ValueError:
        messagebox.showwarning("Input Error", "Age must be a valid number!")
        return

    if not contact.isdigit() or len(contact) != 10:
        messagebox.showwarning("Input Error", "Contact number must contain exactly 10 digits!")
        return

    try:
        grade = float(grade)
        if grade > 10: 
            messagebox.showwarning("Input Error", "Grade must be less than 10!")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Grade must be a valid number!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, grade, contact) VALUES (%s, %s, %s, %s)",
                       (name, age, grade, contact))
        conn.commit()
        conn.close()
        
        clear_fields()
        display_students()

        messagebox.showinfo("Success", "Student record added successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def update_student():
    student_id = entry_student_id.get()
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()
    contact = entry_contact.get()


    if not student_id or not name or not age or not grade or not contact:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showwarning("Input Error", "Age must be a valid number!")
        return

    if not contact.isdigit():
        messagebox.showwarning("Input Error", "Contact number must contain digits only!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()

        if not student: 
            messagebox.showerror("Student Not Found", "No student found with the given ID.")
            conn.close()
            return
        
        cursor.execute("UPDATE students SET name=%s, age=%s, grade=%s, contact=%s WHERE student_id=%s",
                       (name, age, grade, contact, student_id))
        conn.commit()
        conn.close()
        
        clear_fields()
        display_students()

        messagebox.showinfo("Success", "Student record updated successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def delete_student():
    student_id = entry_student_id.get()
    if not student_id:
        messagebox.showwarning("Input Error", "Student ID is required!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
        conn.commit()
        conn.close()
        clear_fields()
        display_students()
        messagebox.showinfo("Success", "Student record deleted successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def display_students():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        conn.close()

        for widget in frame_records.winfo_children():
            widget.destroy()

        tk.Label(frame_records, text="Student ID", width=15, bg="lightblue").grid(row=0, column=0)
        tk.Label(frame_records, text="Name", width=20, bg="lightblue").grid(row=0, column=1)
        tk.Label(frame_records, text="Age", width=10, bg="lightblue").grid(row=0, column=2)
        tk.Label(frame_records, text="Grade", width=10, bg="lightblue").grid(row=0, column=3)
        tk.Label(frame_records, text="Contact", width=15, bg="lightblue").grid(row=0, column=4)

        for i, record in enumerate(records, start=1):
            for j, value in enumerate(record):
                tk.Label(frame_records, text=value, width=15, borderwidth=1, relief="solid").grid(row=i, column=j)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def clear_fields():
    entry_student_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_grade.delete(0, tk.END)
    entry_contact.delete(0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("700x500")
root.config(bg="lightblue")

# Add a frame for the form
frame_form = tk.Frame(root, bg="lightblue")
frame_form.pack(pady=20)

# Create labels and entry widgets for student details
tk.Label(frame_form, text="Student ID:", bg="lightblue").grid(row=0, column=0)
entry_student_id = tk.Entry(frame_form)
entry_student_id.grid(row=0, column=1)

tk.Label(frame_form, text="Name:", bg="lightblue").grid(row=1, column=0)
entry_name = tk.Entry(frame_form)
entry_name.grid(row=1, column=1)

tk.Label(frame_form, text="Age:", bg="lightblue").grid(row=2, column=0)
entry_age = tk.Entry(frame_form)
entry_age.grid(row=2, column=1)

tk.Label(frame_form, text="Grade:", bg="lightblue").grid(row=3, column=0)
entry_grade = tk.Entry(frame_form)
entry_grade.grid(row=3, column=1)

tk.Label(frame_form, text="Contact:", bg="lightblue").grid(row=4, column=0)
entry_contact = tk.Entry(frame_form)
entry_contact.grid(row=4, column=1)

# Add buttons for adding, updating, and deleting records
tk.Button(frame_form, text="Add Student", command=add_student, bg="lightgreen").grid(row=5, column=0, pady=10)
tk.Button(frame_form, text="Update Student", command=update_student, bg="lightyellow").grid(row=5, column=1, pady=10)
tk.Button(frame_form, text="Delete Student", command=delete_student, bg="lightcoral").grid(row=5, column=2, pady=10)

# Add a frame to display student records
frame_records = tk.Frame(root, bg="lightblue")
frame_records.pack(pady=20)

# Display the student records on startup
display_students()

# Start the Tkinter main loop
root.mainloop()
