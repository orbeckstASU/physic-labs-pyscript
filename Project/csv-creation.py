import numpy as np
import csv

# This code will create a csv with time,position values of projectile motion

# Constants
g = -9.8   # acceleration due to gravity (m/s^2)
v0 = 20.0  # initial velocity (m/s)
y0 = 0.0   # initial position (m)

# I want to create 50 points of dats
t_final = 2 * v0 / -g  # time when projectile hits ground
time_points = np.linspace(0, t_final, 50)

# Position calculation
positions = y0 + v0 * time_points + 0.5 * g * time_points**2

# Save to CSV
with open('Project/projectile_motion.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['time (s)', 'position (m)'])
    for t, y in zip(time_points, positions):
        writer.writerow([t, y])

print("CSV file 'projectile_motion.csv' created successfully.")
