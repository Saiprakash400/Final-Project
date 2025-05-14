import csv


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def can_access_phi(self):
        return self.role in ["clinician", "nurse"]

    def can_add_remove(self):
        return self.role in ["clinician", "nurse"]

    def can_view_notes(self):
        return self.role in ["clinician", "nurse"]

    def can_generate_stats(self):
        return self.role == "management"

    def can_count_visits(self):
        return True  # All roles can count visits


def authenticate_user(credentials_file, input_username, input_password):
    try:
        with open(credentials_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == input_username and row['password'] == input_password:
                    print(f"Login successful as '{row['role']}'")
                    return User(input_username, row['role'])
    except FileNotFoundError:
        print("Credentials file not found.")
    print("Invalid username or password.")
    return None
