import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. USER INPUT SECTION
# -----------------------------
students = []

n = int(input("Enter number of students: "))

subjects = ["Math", "Science", "English", "Computer"]

for i in range(n):
    print(f"\nEnter details for Student {i+1}")
    name = input("Name: ")

    marks = []
    for subject in subjects:
        mark = float(input(f"{subject} marks: "))
        marks.append(mark)

    students.append([name] + marks)

# Create DataFrame
columns = ["Name"] + subjects
df = pd.DataFrame(students, columns=columns)

# -----------------------------
# 2. DATA ANALYSIS
# -----------------------------

# Total and Average using NumPy
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1)

# Pass/Fail condition
df["Result"] = np.where(df["Average"] >= 50, "Pass", "Fail")

# Grade system
def get_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 75:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    else:
        return "F"

df["Grade"] = df["Average"].apply(get_grade)

# -----------------------------
# 3. STATISTICS
# -----------------------------
print("\n📊 SUBJECT-WISE STATISTICS")
for subject in subjects:
    print(f"\n{subject}")
    print("Mean:", np.mean(df[subject]))
    print("Max :", np.max(df[subject]))
    print("Min :", np.min(df[subject]))

# Top performers
top_students = df.sort_values(by="Average", ascending=False)

# -----------------------------
# 4. EXPORT TO EXCEL
# -----------------------------
output_file = "student_performance_report.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Student Data", index=False)
    top_students.to_excel(writer, sheet_name="Ranked Students", index=False)

print(f"\n✅ Excel report generated: {output_file}")

# -----------------------------
# 5. VISUALIZATION
# -----------------------------

# Bar chart - student averages
plt.figure(figsize=(8,5))
plt.bar(df["Name"], df["Average"], color="skyblue")
plt.title("Student Average Scores")
plt.xlabel("Students")
plt.ylabel("Average")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Subject-wise average
plt.figure(figsize=(6,4))
df[subjects].mean().plot(kind="bar", color="orange")
plt.title("Subject-wise Average Performance")
plt.ylabel("Average Score")
plt.show()

# Pass/Fail Pie chart
plt.figure(figsize=(5,5))
df["Result"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    colors=["green", "red"]
)
plt.title("Pass vs Fail Distribution")
plt.ylabel("")
plt.show()