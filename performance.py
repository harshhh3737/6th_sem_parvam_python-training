import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Create / Load Dataset
# -----------------------------
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Helen"],
    "Math": np.random.randint(50, 100, 8),
    "Science": np.random.randint(50, 100, 8),
    "English": np.random.randint(50, 100, 8)
}

df = pd.DataFrame(data)

# -----------------------------
# 2. Data Processing
# -----------------------------
df["Total"] = df[["Math", "Science", "English"]].sum(axis=1)
df["Average"] = df["Total"] / 3

# Grade assignment
def assign_grade(avg):
    if avg >= 85:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 50:
        return "C"
    else:
        return "D"

df["Grade"] = df["Average"].apply(assign_grade)

# -----------------------------
# 3. Display Data
# -----------------------------
print("\nStudent Data:\n")
print(df)

# Topper
topper = df.loc[df["Total"].idxmax()]
print("\nTopper:\n", topper["Name"], "-", topper["Total"])

# Subject averages
print("\nSubject Averages:\n")
print(df[["Math", "Science", "English"]].mean())

# -----------------------------
# 4. Visualization
# -----------------------------
plt.figure(figsize=(14, 8))

# 1. Bar Chart - Average per student
plt.subplot(2, 3, 1)
plt.bar(df["Name"], df["Average"], color='skyblue')
plt.xticks(rotation=45)
plt.title("Average Marks per Student")

# 2. Line Plot - Total marks
plt.subplot(2, 3, 2)
plt.plot(df["Name"], df["Total"], marker='o', color='green')
plt.xticks(rotation=45)
plt.title("Total Marks Trend")

# 3. Pie Chart - Grade distribution
plt.subplot(2, 3, 3)
grade_counts = df["Grade"].value_counts()
plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%')
plt.title("Grade Distribution")

# 4. Histogram - Math scores
plt.subplot(2, 3, 4)
plt.hist(df["Math"], bins=5, color='orange')
plt.title("Math Score Distribution")

# 5. Scatter Plot - Math vs Science
plt.subplot(2, 3, 5)
plt.scatter(df["Math"], df["Science"], color='red')
plt.xlabel("Math")
plt.ylabel("Science")
plt.title("Math vs Science")

# 6. Box Plot - Subject comparison
plt.subplot(2, 3, 6)
plt.boxplot([df["Math"], df["Science"], df["English"]],
            labels=["Math", "Science", "English"])
plt.title("Subject Comparison")

plt.tight_layout()
plt.show()