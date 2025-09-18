# Data is in 1/60 second intervals, as we're measuring at 60 Hz
# Each entry is the position in cm, starting at 0 seconds
data = tuple(((i + 1)/60, pos) for i, pos in enumerate([0, 1, 1.8, 3.2, 4.8, 6.5, 8.8, 11.1, 13.7, 16.7, 19.8, 23.3, 27, 31.1, 35.3, 39.9, 44.7, 49.9, 55.2, 60.8, 66.7, 72.9, 79.4, 86.1]))

otherData = [11.403, 0.1153, 0.0144]
otherDataTwo = [9.6624, 0.368, -0.0006]
otherDataThree = [9.9388, 0.2109, 0.054]
otherDataFour = [8.9152, 0.4102, -0.0034]

# There were further points that we chose to leave out, as there was a jump in the data, and we could not be confident of the timing of the fall past 86.1 cm

# Convert data to meters
data = tuple((t, p / 100) for t, p in data)

print(data)

# Fit a quadratic to the data
import numpy as np
coeffs = np.polyfit(*zip(*data), 2)
# Double a coeff
coeffs = (2 * coeffs[0], coeffs[1], coeffs[2])
print("Fitted coefficients (a, b, c) for ax^2 + bx + c:", coeffs)

# Calculate avg and stdev for our coeffs and other data
import statistics
all_coeffs = [coeffs, otherData, otherDataTwo, otherDataThree, otherDataFour]
a_values = [c[0] for c in all_coeffs]
b_values = [c[1] for c in all_coeffs]
c_values = [c[2] for c in all_coeffs]

avg_coeffs = [statistics.mean(a_values), statistics.mean(b_values), statistics.mean(c_values)]
stdev_coeffs = [statistics.stdev(a_values), statistics.stdev(b_values), statistics.stdev(c_values)]
print("Average coefficients (a, b, c):", avg_coeffs)
print("Standard deviation of coefficients (a, b, c):", stdev_coeffs)

avg_coeffs_for_graphing = (avg_coeffs[0] / 2, avg_coeffs[1], avg_coeffs[2])

# Graph the data
import matplotlib.pyplot as plt
plt.scatter(*zip(*data))
plt.plot(np.linspace(0, max(t for t, p in data), 100), np.polyval(avg_coeffs_for_graphing, np.linspace(0, max(t for t, p in data), 100)), color='red')

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position vs Time")
plt.show()