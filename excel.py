# छात्र प्रदर्शन विश्लेषण प्रणाली / Student Performance Analysis System

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Sample Data Creation
# -----------------------------
data = {
    'Student': ['Aman', 'Riya', 'Karan', 'Sneha', 'Arjun', 'Priya', 'Rahul', 'Neha'],
    'Math': [85, 78, 92, 88, 76, 95, 89, 84],
    'Science': [90, 82, 88, 91, 79, 94, 85, 87],
    'English': [75, 85, 80, 78, 88, 90, 84, 82]
}

df = pd.DataFrame(data)

# -----------------------------
# 2. Data Processing
# -----------------------------
df['Average'] = df[['Math', 'Science', 'English']].mean(axis=1)

# Grade Assignment Function
def assign_grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 75:
        return 'B'
    else:
        return 'C'

df['Grade'] = df['Average'].apply(assign_grade)

# -----------------------------
# 3. Statistical Analysis
# -----------------------------
class_avg = np.mean(df['Average'])
topper = df.loc[df['Average'].idxmax()]
lowest = df.loc[df['Average'].idxmin()]

# -----------------------------
# 4. Console Report
# -----------------------------
print("\n===== STUDENT PERFORMANCE REPORT =====")
print("\nFull Data:\n", df)

print("\nClass Average:", round(class_avg, 2))
print("\nTop Performer:\n", topper)
print("\nLowest Performer:\n", lowest)

# -----------------------------
# 5. Visualization
# -----------------------------

# Bar Chart - Average Scores
plt.figure(figsize=(8,5))
plt.bar(df['Student'], df['Average'], color='skyblue')
plt.title('Student Average Scores')
plt.xlabel('Students')
plt.ylabel('Average Marks')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_scores.png")
plt.show()

# Pie Chart - Grade Distribution
grade_counts = df['Grade'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Grade Distribution')
plt.savefig("grade_distribution.png")
plt.show()

# -----------------------------
# 6. Export to Excel
# -----------------------------
with pd.ExcelWriter("student_performance_report.xlsx") as writer:
    df.to_excel(writer, sheet_name='Performance Data', index=False)
    
    # Summary Sheet
    summary = pd.DataFrame({
        'Metric': ['Class Average'],
        'Value': [class_avg]
    })
    summary.to_excel(writer, sheet_name='Summary', index=False)

print("\nExcel report generated: student_performance_report.xlsx")