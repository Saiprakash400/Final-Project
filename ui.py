import tkinter as tk
from tkinter import messagebox
from users import authenticate_user
from patients import Patient, Visit, Note
from notes import load_notes
from hospital_statistics import generate_statistics
from datetime import datetime
import csv
import tkinter.ttk as ttk
from theme import UITheme

import uuid  

DATA_FILE = "Patient_data.csv"
NOTES_FILE = "Notes.csv"
CREDENTIALS_FILE = "Credentials.csv"
LOG_FILE = "usage_log.csv"

class App:
    def __init__(self, root):
        self.root = root
        UITheme.apply_theme(self.root)
        self.root.title("Hospital Clinical System")
        self.user = None
        self.notes_dict = load_notes(NOTES_FILE)
        self.patients = {}  # Will be populated after login
        self.build_login()

    def build_login(self):
        self.clear_root()
        self.root.geometry("400x250")
        self.root.configure(bg=UITheme.BG_COLOR)

        frame = tk.Frame(self.root, bg=UITheme.BG_COLOR)
        frame.pack(pady=40)

        tk.Label(frame, text="Username", font=UITheme.FONT, bg=UITheme.BG_COLOR).grid(row=0, column=0, pady=5, sticky="e")
        tk.Label(frame, text="Password", font=UITheme.FONT, bg=UITheme.BG_COLOR).grid(row=1, column=0, pady=5, sticky="e")

        self.username_entry = tk.Entry(frame, font=UITheme.FONT)
        self.password_entry = tk.Entry(frame, show="*", font=UITheme.FONT)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        ttk.Button(frame, text="Log In", style=UITheme.BUTTON_STYLE, command=self.handle_login).grid(row=2, column=0, columnspan=2, pady=15)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        self.user = authenticate_user(CREDENTIALS_FILE, username, password)

        if not self.user:
            self.log_usage(username, "unknown", "LOGIN_FAILED")
            messagebox.showerror("Login Failed", "Invalid credentials.")
        else:
            self.log_usage(username, self.user.role, "LOGIN_SUCCESS")
            self.load_patient_data()
            self.show_menu()

    def load_patient_data(self):
        self.patients = {}
        try:
            with open(DATA_FILE, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    pid = row["Patient_ID"]
                    if pid not in self.patients:
                        self.patients[pid] = Patient(pid)

                    visit = Visit(
                        visit_id=row["Visit_ID"],
                        visit_time=row["Visit_time"],
                        department=row["Visit_department"],
                        gender=row["Gender"],
                        race=row["Race"],
                        age=int(row["Age"]),
                        ethnicity=row["Ethnicity"],
                        insurance=row["Insurance"],
                        zip_code=row["Zip_code"],
                        chief_complaint=row["Chief_complaint"]
                    )

                    note_id = row["Note_ID"]
                    note_type = row["Note_type"]
                    note_text = self.notes_dict[note_id].note_text if note_id in self.notes_dict else ""
                    note = Note(note_id, note_type, note_text)
                    visit.add_note(note)
                    self.patients[pid].add_visit(visit)
        except FileNotFoundError:
            messagebox.showerror("Error", f"{DATA_FILE} not found.")

    def show_menu(self):
        self.clear_root()
        self.root.geometry("400x400")
        self.root.configure(bg=UITheme.BG_COLOR)
        tk.Label(self.root, text="Hospital Clinical Dashboard", font=UITheme.TITLE_FONT, bg=UITheme.BG_COLOR).pack(pady=10)

        tk.Label(
            self.root,
            text=f"Welcome, {self.user.username} ({self.user.role})",
            font=UITheme.TITLE_FONT,
            bg=UITheme.BG_COLOR
        ).pack(pady=15)

        button_frame = tk.Frame(self.root, bg=UITheme.BG_COLOR)
        button_frame.pack()

        def styled_button(label, cmd):
            ttk.Button(
                button_frame,
                text=label,
                command=cmd,
                style=UITheme.BUTTON_STYLE
            ).pack(pady=6, ipadx=10, ipady=5)

        if self.user.role == "admin":
            styled_button("Count Visits", self.count_visits)

        elif self.user.role == "management":
            styled_button("Generate Statistics", self.run_statistics)

        else:  # clinician or nurse
            styled_button("Retrieve Patient", self.retrieve_patient)
            styled_button("Add Patient", self.add_patient)
            styled_button("Remove Patient", self.remove_patient)
            styled_button("Count Visits", self.count_visits)
            styled_button("View Note", self.view_note)

        styled_button("Exit", self.root.destroy)
        
    def count_visits(self):
        self.clear_root()
        tk.Label(self.root, text="Enter date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(self.root)
        date_entry.pack()

        def run_count():
            try:
                target_date = datetime.strptime(date_entry.get(), "%Y-%m-%d").date()
                count = 0
                for p in self.patients.values():
                    for v in p.visits:
                        try:
                            visit_date = datetime.strptime(v.visit_time.strip(), "%m/%d/%Y").date()
                            if visit_date == target_date:
                                count += 1
                        except ValueError:
                            continue
                messagebox.showinfo("Result", f"Total visits on {target_date}: {count}")
                self.log_usage(self.user.username, self.user.role, f"count_visits: {target_date}")
                self.show_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")

        tk.Button(self.root, text="Submit", command=run_count).pack()

    def run_statistics(self):
        generate_statistics(DATA_FILE)
        messagebox.showinfo("Done", "Statistics generated and saved as image files.")
        self.log_usage(self.user.username, self.user.role, "generate_statistics")

    def placeholder(self):
        messagebox.showinfo("Info", "This function is not yet implemented.")

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def log_usage(self, username, role, action):
        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action])

    def add_patient(self):
        self.clear_root()
        self.root.configure(bg=UITheme.BG_COLOR)

        labels = [
            "Patient ID", "Visit Date (YYYY-MM-DD)", "Department", "Race", "Gender", "Ethnicity", "Age", "Zip Code", 
            "Insurance", "Chief Complaint", "Note Type", "Note Text"
        ]
        entries = {}

        for idx, label in enumerate(labels):
            tk.Label(self.root, text=label, font=UITheme.FONT, bg=UITheme.BG_COLOR).grid(row=idx, column=0, sticky="e", pady=4, padx=6)
            entry = tk.Entry(self.root, font=UITheme.FONT)
            entry.grid(row=idx, column=1, pady=4, padx=6)
            entries[label] = entry

        def submit():
            try:
                pid = entries["Patient ID"].get().strip()
                visit_time = datetime.strptime(entries["Visit Date (YYYY-MM-DD)"].get().strip(), "%Y-%m-%d").strftime("%m/%d/%Y")
                visit_id = str(uuid.uuid4().hex[:8])
                dept = entries["Department"].get().strip()
                race = entries["Race"].get().strip()
                gender = entries["Gender"].get().strip()
                ethnicity = entries["Ethnicity"].get().strip()
                age = int(entries["Age"].get().strip())
                zip_code = entries["Zip Code"].get().strip()
                insurance = entries["Insurance"].get().strip()
                complaint = entries["Chief Complaint"].get().strip()
                note_id = str(uuid.uuid4().hex[:6])
                note_type = entries["Note Type"].get().strip()
                note_text = entries["Note Text"].get().strip()

                visit = Visit(visit_id, visit_time, dept, gender, race, age, ethnicity, insurance, zip_code, complaint)
                note = Note(note_id, note_type, note_text)
                visit.add_note(note)

                if pid not in self.patients:
                    self.patients[pid] = Patient(pid)
                self.patients[pid].add_visit(visit)

                with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([
                        pid, visit_id, visit_time, dept, race, gender, ethnicity, age, zip_code, insurance, complaint, note_id, note_type
                    ])

                self.log_usage(self.user.username, self.user.role, f"add_patient: {pid}")
                messagebox.showinfo("Success", "Patient added successfully.")
                self.show_menu()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add patient: {e}")

        ttk.Button(self.root, text="Submit", command=submit, style=UITheme.BUTTON_STYLE).grid(
            row=len(labels), column=0, columnspan=2, pady=15
        )

    def retrieve_patient(self):
        self.clear_root()
        self.root.configure(bg=UITheme.BG_COLOR)

        tk.Label(
            self.root,
            text="Enter Patient ID:",
            font=UITheme.FONT,
            bg=UITheme.BG_COLOR
        ).pack(pady=10)

        pid_entry = tk.Entry(self.root, font=UITheme.FONT)
        pid_entry.pack(pady=5)

        def submit():
            pid = pid_entry.get().strip()
            if pid not in self.patients:
                messagebox.showerror("Not Found", f"Patient {pid} does not exist.")
                self.log_usage(self.user.username, self.user.role, f"retrieve_patient: {pid} NOT_FOUND")
                self.show_menu()
                return

            patient = self.patients[pid]
            if not patient.visits:
                messagebox.showinfo("No Visits", f"Patient {pid} has no visits.")
                return

            recent_visit = max(patient.visits, key=lambda v: datetime.strptime(v.visit_time.strip(), "%m/%d/%Y"))

            info = f"Patient ID: {pid}\nVisit Date: {recent_visit.visit_time}\nDept: {recent_visit.department}\n"
            info += f"Gender: {recent_visit.gender}, Race: {recent_visit.race}, Age: {recent_visit.age}\n"
            info += f"Ethnicity: {recent_visit.ethnicity}, Insurance: {recent_visit.insurance}, Zip: {recent_visit.zip_code}\n"
            info += f"Chief Complaint: {recent_visit.chief_complaint}\n\nNotes:\n"

            if recent_visit.notes:
                for note in recent_visit.notes:
                    info += f"- [{note.note_type}] {note.note_text}\n"
            else:
                info += "No notes available."

            messagebox.showinfo("Patient Info", info)
            self.log_usage(self.user.username, self.user.role, f"retrieve_patient: {pid}")
            self.show_menu()

        ttk.Button(
            self.root,
            text="Submit",
            command=submit,
            style=UITheme.BUTTON_STYLE
        ).pack(pady=10)

    def view_note(self):
        self.clear_root()
        self.root.configure(bg=UITheme.BG_COLOR)

        tk.Label(self.root, text="Enter Patient ID:", font=UITheme.FONT, bg=UITheme.BG_COLOR).pack(pady=5)
        pid_entry = tk.Entry(self.root, font=UITheme.FONT)
        pid_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Visit Date (YYYY-MM-DD):", font=UITheme.FONT, bg=UITheme.BG_COLOR).pack(pady=5)
        date_entry = tk.Entry(self.root, font=UITheme.FONT)
        date_entry.pack(pady=5)

        def submit():
            pid = pid_entry.get().strip()
            date_input = date_entry.get().strip()
            try:
                target_date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%m/%d/%Y")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            if pid not in self.patients:
                messagebox.showerror("Not Found", f"Patient {pid} not found.")
                self.log_usage(self.user.username, self.user.role, f"view_note: {pid} NOT_FOUND")
                self.show_menu()
                return

            patient = self.patients[pid]
            notes_found = False
            info = f"Notes for {pid} on {target_date}:\n\n"

            for visit in patient.visits:
                if visit.visit_time.strip() == target_date:
                    for note in visit.notes:
                        info += f"- [{note.note_type}] {note.note_text}\n"
                        notes_found = True

            if not notes_found:
                info += "No notes found for this date."

            messagebox.showinfo("Notes", info)
            self.log_usage(self.user.username, self.user.role, f"view_note: {pid} on {target_date}")
            self.show_menu()

        ttk.Button(self.root, text="Submit", command=submit, style=UITheme.BUTTON_STYLE).pack(pady=10)

    def remove_patient(self):
        self.clear_root()
        self.root.configure(bg=UITheme.BG_COLOR)

        tk.Label(self.root, text="Enter Patient ID to Remove:", font=UITheme.FONT, bg=UITheme.BG_COLOR).pack(pady=5)
        pid_entry = tk.Entry(self.root, font=UITheme.FONT)
        pid_entry.pack(pady=5)

        def submit():
            pid = pid_entry.get().strip()
            if pid not in self.patients:
                messagebox.showerror("Not Found", f"Patient {pid} does not exist.")
                self.log_usage(self.user.username, self.user.role, f"remove_patient: {pid} NOT_FOUND")
                self.show_menu()
                return

            # Confirm removal
            if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove patient {pid}?"):
                # Remove from memory
                del self.patients[pid]

                # Remove from CSV by rewriting the data (excluding the patient)
                with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    rows = [row for row in reader if row[0] != pid]

                with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(rows)

                self.log_usage(self.user.username, self.user.role, f"remove_patient: {pid}")
                messagebox.showinfo("Success", f"Patient {pid} removed successfully.")
                self.show_menu()

        ttk.Button(self.root, text="Submit", command=submit, style=UITheme.BUTTON_STYLE).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
