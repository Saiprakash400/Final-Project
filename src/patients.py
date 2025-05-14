import uuid

class Note:
    def __init__(self, note_id, note_type, note_text=""):
        self.note_id = note_id
        self.note_type = note_type
        self.note_text = note_text

    def __str__(self):
        return f"Note ID: {self.note_id}, Type: {self.note_type}\n{self.note_text}"


class Visit:
    def __init__(self, visit_id, visit_time, department, gender, race, age, ethnicity, insurance, zip_code, chief_complaint):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.chief_complaint = chief_complaint
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def __str__(self):
        note_texts = "\n".join(str(note) for note in self.notes)
        return (f"Visit ID: {self.visit_id}, Time: {self.visit_time}, Dept: {self.department}, Gender: {self.gender}, "
                f"Race: {self.race}, Age: {self.age}, Ethnicity: {self.ethnicity}, Insurance: {self.insurance}, "
                f"Zip: {self.zip_code}, Complaint: {self.chief_complaint}\nNotes:\n{note_texts}")


class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

    def remove_all_visits(self):
        self.visits = []

    def get_all_info(self):
        info = f"Patient ID: {self.patient_id}\n"
        for visit in self.visits:
            info += str(visit) + "\n"
        return info
