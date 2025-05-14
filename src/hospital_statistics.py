import pandas as pd
import matplotlib.pyplot as plt

def load_patient_data(file_path):
    """Load and clean the patient visit data."""
    try:
        df = pd.read_csv(file_path)
        df['Visit_time'] = pd.to_datetime(df['Visit_time'], errors='coerce')
        df = df[df['Visit_time'] >= pd.to_datetime("2020-01-01")]

        if df['Visit_time'].isnull().any():
            print("⚠️ Warning: Some Visit_time values could not be parsed as dates.")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def plot_gender_trends(df):
    counts = df['Gender'].value_counts().sort_index()
    plt.figure(figsize=(8, 6))
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Gender Trends", fontsize=14)
    plt.xlabel("Gender", fontsize=12)
    plt.ylabel("Number of Visits", fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("gender_trends.png", dpi=300)
    plt.close()
    print("✅ Saved: gender_trends.png")

def plot_race_trends(df):
    counts = df['Race'].value_counts().sort_index()
    plt.figure(figsize=(8, 6))
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Race Trends", fontsize=14)
    plt.xlabel("Race", fontsize=12)
    plt.ylabel("Number of Visits", fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("race_trends.png", dpi=300)
    plt.close()
    print("✅ Saved: race_trends.png")

def plot_ethnicity_trends(df):
    counts = df['Ethnicity'].value_counts().sort_index()
    plt.figure(figsize=(8, 6))
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Ethnicity Trends", fontsize=14)
    plt.xlabel("Ethnicity", fontsize=12)
    plt.ylabel("Number of Visits", fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("ethnicity_trends.png", dpi=300)
    plt.close()
    print("✅ Saved: ethnicity_trends.png")

def plot_age_trends(df):
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 18, 35, 50, 65, 100],
                            labels=["0-18", "19-35", "36-50", "51-65", "66+"])
    counts = df['AgeGroup'].value_counts().sort_index()
    plt.figure(figsize=(8, 6))
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Age Trends", fontsize=14)
    plt.xlabel("Age Group", fontsize=12)
    plt.ylabel("Number of Visits", fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("age_trends.png", dpi=300)
    plt.close()
    print("✅ Saved: age_trends.png")

def plot_insurance_trends(df):
    counts = df['Insurance'].value_counts().sort_index()
    plt.figure(figsize=(8, 6))
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Insurance Trends", fontsize=14)
    plt.xlabel("Insurance", fontsize=12)
    plt.ylabel("Number of Visits", fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("insurance_trends.png", dpi=300)
    plt.close()
    print("✅ Saved: insurance_trends.png")

def generate_statistics(file_path):
    """Main function to generate all bar chart plots for management reports."""
    df = load_patient_data(file_path)
    if df is None:
        return

    plot_gender_trends(df)
    plot_race_trends(df)
    plot_ethnicity_trends(df)
    plot_age_trends(df)
    plot_insurance_trends(df)
