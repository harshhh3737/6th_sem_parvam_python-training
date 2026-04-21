import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.arange(1, 6)
y = np.array([10, 20, 15, 25, 30])

categories = ['A', 'B', 'C', 'D', 'E']
values = [5, 7, 3, 8, 6]

# Create a 2x3 grid of plots
plt.figure(figsize=(12, 8))

# 1. Line Plot
plt.subplot(2, 3, 1)
plt.plot(x, y, marker='o')
plt.title("Line Plot")

# 2. Bar Chart
plt.subplot(2, 3, 2)
plt.bar(categories, values)
plt.title("Bar Chart")

# 3. Scatter Plot
plt.subplot(2, 3, 3)
plt.scatter(x, y, color='red')
plt.title("Scatter Plot")

# 4. Histogram
plt.subplot(2, 3, 4)
data = np.random.randn(100)
plt.hist(data, bins=10)
plt.title("Histogram")

# 5. Pie Chart
plt.subplot(2, 3, 5)
plt.pie(values, labels=categories, autopct='%1.1f%%')
plt.title("Pie Chart")

# 6. Box Plot
plt.subplot(2, 3, 6)
data2 = [np.random.randn(100) for _ in range(3)]
plt.boxplot(data2)
plt.title("Box Plot")

plt.tight_layout()
plt.show()