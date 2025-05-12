import argparse
from users import authenticate_user
from patients import Patient, Visit, Note
from notes import load_notes, get_notes_by_date
from hospital_statistics import generate_statistics
import csv
from datetime import datetime
import uuid

# -------------------- Data Handling --------------------

def load_patient_data(data_file, notes_dict):
    patients = {}
    try:
        with open(data_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pid = row["Patient_ID"]
                if pid not in patients:
                    patients[pid] = Patient(pid)

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
                note_text = notes_dict[note_id].note_text if note_id in notes_dict else ""
                note = Note(note_id, note_type, note_text)
                visit.add_note(note)

                patients[pid].add_visit(visit)
    except FileNotFoundError:
        print(f"Data file {data_file} not found.")
    return patients


def save_visit(data_file, patient_id, visit, note):
    with open(data_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            patient_id,
            visit.visit_id,
            visit.visit_time,
            visit.department,
            visit.gender,
            visit.race,
            visit.age,
            visit.ethnicity,
            visit.insurance,
            visit.zip_code,
            visit.chief_complaint,
            note.note_id,
            note.note_type
        ])


def write_all_patients(data_file, patients):
    with open(data_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Patient_ID", "Visit_ID", "Visit_time", "Visit_department",
            "Gender", "Race", "Age", "Ethnicity", "Insurance",
            "Zip_code", "Chief_complaint", "Note_ID", "Note_type"
        ])
        for patient in patients.values():
            for visit in patient.visits:
                for note in visit.notes:
                    writer.writerow([
                        patient.patient_id,
                        visit.visit_id,
                        visit.visit_time,
                        visit.department,
                        visit.gender,
                        visit.race,
                        visit.age,
                        visit.ethnicity,
                        visit.insurance,
                        visit.zip_code,
                        visit.chief_complaint,
                        note.note_id,
                        note.note_type
                    ])

# -------------------- Command-Line Logic --------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-username", required=True)
    parser.add_argument("-password", required=True)
    args = parser.parse_args()

    credential_file = "Credentials.csv"
    data_file = "Patient_data.csv"
    notes_file = "Notes.csv"

    user = authenticate_user(credential_file, args.username, args.password)
    if not user:
        return

    notes_dict = load_notes(notes_file)
    patients = load_patient_data(data_file, notes_dict)

    if user.can_generate_stats():
        generate_statistics(data_file)
        return

    elif user.role == "admin":
        while True:
            date_input = input("Enter date to count visits (YYYY-MM-DD): ")
            try:
                target_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                target_str = target_date.strftime("%m/%d/%Y")
                break
            except ValueError:
                print("Invalid format. Please enter date as YYYY-MM-DD (e.g., 2019-04-05)")

        count = 0
        for p in patients.values():
            for v in p.visits:
                if v.visit_time.strip() == target_str:
                    count += 1

        print(f"Total visits on {target_date.isoformat()}: {count}")
        return

    while True:
        action = input("\nEnter action (add_patient, remove_patient, retrieve_patient, count_visits, view_note, Stop): ")
        if action == "Stop":
            break

        if action == "add_patient" and user.can_add_remove():
            pid = input("Enter Patient ID: ")
            if pid not in patients:
                patients[pid] = Patient(pid)

            visit_id = str(uuid.uuid4().hex[:8])
            visit_input = input("Enter visit date (YYYY-MM-DD): ")
            visit_time = datetime.strptime(visit_input, "%Y-%m-%d").strftime("%m/%d/%Y")
            dept = input("Enter department: ")
            gender = input("Enter gender: ")
            race = input("Enter race: ")
            age = int(input("Enter age: "))
            ethnicity = input("Enter ethnicity: ")
            insurance = input("Enter insurance: ")
            zip_code = input("Enter zip code: ")
            complaint = input("Enter chief complaint: ")
            note_id = str(uuid.uuid4().hex[:6])
            note_type = input("Enter note type: ")
            note_text = input("Enter note text: ")

            visit = Visit(visit_id, visit_time, dept, gender, race, age, ethnicity, insurance, zip_code, complaint)
            note = Note(note_id, note_type, note_text)
            visit.add_note(note)
            patients[pid].add_visit(visit)
            save_visit(data_file, pid, visit, note)
            print("Visit added.")

        elif action == "remove_patient" and user.can_add_remove():
            pid = input("Enter Patient ID to remove: ")
            if pid in patients:
                del patients[pid]
                write_all_patients(data_file, patients)
                print("Patient removed.")
            else:
                print("Patient not found.")

        elif action == "retrieve_patient" and user.can_access_phi():
            pid = input("Enter Patient ID to retrieve: ")
            if pid in patients:
                print(patients[pid].get_all_info())
            else:
                print("Patient not found.")

        elif action == "count_visits" and user.can_count_visits():
            date = input("Enter date to count visits (YYYY-MM-DD): ")
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
                count = 0
                for p in patients.values():
                    for v in p.visits:
                        try:
                            visit_date = datetime.strptime(v.visit_time.strip(), "%m/%d/%Y").date()
                            if visit_date == target_date:
                                count += 1
                        except ValueError:
                            continue 
                print(f"Total visits on {date}: {count}")
            except ValueError:
                print("Invalid date format.")

        elif action == "view_note" and user.can_view_notes():
            pid = input("Enter Patient ID: ")
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                target_str = datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%Y")
                if pid in patients:
                    notes = get_notes_by_date(patients[pid], target_str)
                    if notes:
                        for note in notes:
                            print(note)
                    else:
                        print("No notes found on that date.")
                else:
                    print("Patient not found.")
            except ValueError:
                print("Invalid date format.")

        else:
            print("Invalid action or insufficient permission.")


if __name__ == "__main__":
    main()
