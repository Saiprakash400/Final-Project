import csv
from patients import Note


def load_notes(note_file_path):
    """Load clinical notes into a dictionary keyed by Note_ID."""
    notes = {}
    try:
        with open(note_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                note_id = row["Note_ID"]
                note_text = row["Note_text"]
                note_type = "Unknown"  # fallback since Note_type is missing
                notes[note_id] = Note(note_id, note_type, note_text)
    except FileNotFoundError:
        print(f" Note file {note_file_path} not found.")
    return notes


from datetime import datetime

def get_notes_by_date(patient, date_str):
    """Return a list of notes for a patient that match a given visit date."""
    matching_notes = []
    target_date = datetime.strptime(date_str, "%m/%d/%Y").date()

    for visit in patient.visits:
        try:
            visit_date = datetime.strptime(visit.visit_time.strip(), "%m/%d/%Y").date()
            if visit_date == target_date:
                matching_notes.extend(visit.notes)
        except ValueError:
            continue  # skip invalid dates silently

    return matching_notes

