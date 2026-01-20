import csv
import numpy as np
import matplotlib.pyplot as plt



# Read data.csv

with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    data_list = [list(map(float, row)) for row in reader]
data = np.array(data_list)

# Create average column (mean of each row, ignoring the first column)
average = np.mean(data[:, 1:], axis=1)
data = np.column_stack((data, average))
# Create stdev column (standard deviation of each row, ignoring the first column)
stdev = np.std(data[:, 1:-1], axis=1)
data = np.column_stack((data, stdev))

# Scatter plot of each column against the first column

# for i in range(1, 4):
#     plt.scatter(data[:, 0], data[:, i], label=f'Run {i} over time')

# Perform regression over the average data
coefficients = np.polyfit(data[:, 0], data[:, -2], 2)  # Quadratic fit
print(coefficients)
poly = np.poly1d(coefficients)
x_fit = np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 100)
y_fit = poly(x_fit)
plt.plot(x_fit, y_fit, color='red', label='Quadratic fit to average')

# Plot average w/ error bars
plt.errorbar(data[:, 0], data[:, -2], yerr=data[:, -1], fmt='o', color='black', label='Average with error bars')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.legend()
plt.show()
