
# 🏥 Hospital Clinical Dashboard (Final Project)

This is a Tkinter-based clinical data dashboard developed for the HI 741 Final Project. It provides a secure and intuitive interface for hospital staff to manage patients, view clinical notes, generate insights, and track system usage.

---

## ✨ Features

- ✅ User Login with credential validation
- ✅ Role-based access control (admin, nurse, clinician, management)
- ✅ Add, retrieve, and remove patients with CSV persistence
- ✅ View clinical notes by date
- ✅ Count visits on a specific date
- ✅ Generate key statistics (age, gender, race, ethnicity, insurance)
- ✅ Monthly visit trend plot (improved from Assignment 3)
- ✅ Usage logging for login attempts and all actions
- ✅ Modern and consistent UI using a centralized theme module (`UITheme`)

---

## 👥 User Roles and Permissions

| Role        | Permissions                                  |
|-------------|----------------------------------------------|
| `admin`     | Count visits only                            |
| `nurse`     | Full access to patient records and notes     |
| `clinician` | Same as nurse                                |
| `management`| Generate statistics only                     |

---

## 🚀 How to Run the Application

1. Make sure you have **Python 3.7 or higher** installed.
2. Place the following input files in the same directory as your `.py` files:
   - `Patient_data.csv`
   - `Notes.csv`
   - `Credentials.csv`
3. Run the application with:
```bash
python ui.py
```

---

## 📁 Project Structure

```
.
├── ui.py                    # Main GUI controller
├── theme.py                 # Centralized UI styling (colors, fonts, buttons)
├── users.py                 # User class and authentication logic
├── patients.py              # Patient, Visit, and Note class definitions
├── notes.py                 # Clinical notes loader and filtering
├── hospital_statistics.py   # Statistical report generation and plotting
├── Patient_data.csv         # Visit records (input/output)
├── Notes.csv                # De-identified note content
├── Credentials.csv          # Username, password, and role data
├── usage_log.csv            # Auto-generated log of all user actions
├── gender_trends.png        # Gender statistics chart
├── race_trends.png          # Race statistics chart
├── ethnicity_trends.png     # Ethnicity statistics chart
├── age_trends.png           # Age group statistics chart
├── insurance_trends.png     # Insurance type statistics chart
├── monthly_visit_trends.png # Aggregated visit trend chart
├── UML_Diagram.pdf          # UML class design (included in submission)
└── README.md                # This documentation file
```

---

## 📊 Output Files Description

- `Patient_data.csv`: Stores all patient visits and is updated as users add or remove records.
- `usage_log.csv`: Tracks all user logins and actions (including failed attempts).
- `*.png` charts:
  - `gender_trends.png`
  - `race_trends.png`
  - `ethnicity_trends.png`
  - `age_trends.png`
  - `insurance_trends.png`
  - `monthly_visit_trends.png`: Shows visit trends aggregated by month.

These files are automatically saved in the project folder when statistics are generated.

---

## 🧪 Sample Credentials (Stored in `Credentials.csv`)

```csv
username,password,role
admin1,adminpass,admin
nurse1,nursepass,nurse
clinician1,clinipass,clinician
manager1,mgmtpass,management
```

You may add or edit credentials as needed.

---

## 📐 UML Diagram

The class design includes:

- `User`: Stores login and role logic
- `Patient`: Holds multiple `Visit` objects
- `Visit`: Contains demographics, complaint, and a list of `Note` objects
- `Note`: Stores note ID, type, and text
- `App`: Main controller class in `ui.py` that handles all GUI interaction and logic

Refer to `UML_Diagram.pdf` in the project folder for the full visual layout of class relationships and methods.

---

## 📦 Dependencies

This project uses only standard Python libraries:

- `tkinter` — for the GUI
- `csv` — for file reading/writing
- `uuid` — for generating unique IDs
- `datetime` — for date parsing and formatting
- `matplotlib` — for plotting charts
- `pandas` — for CSV aggregation and analysis

No third-party packages required.

---

## 👨‍🏫 Instructor & Submission Info

- Course: **HI 741 - Spring 2025**
- Instructor: **Lu He**
- Project: **Final Programming Project**
- Student: **Sai Prakash**
- Due Date: **May 12, 2025**

---

## ✅ Project Status

- ✔️ Functional GUI
- ✔️ All role-based features working
- ✔️ Output files and statistics tested
- ✔️ UI consistently themed and responsive
- ✔️ Logs and files persist correctly
