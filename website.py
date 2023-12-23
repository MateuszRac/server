import matplotlib.pyplot as plt
import os

# Data for the linear plot
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Create a linear plot
plt.plot(x, y, label='Linear Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Linear Plot Example')
plt.legend()

# Save the plot to the specified location
output_path = '/var/www/html/plot.png'

# Ensure the directory exists
output_directory = os.path.dirname(output_path)
os.makedirs(output_directory, exist_ok=True)

# Save the plot
plt.savefig(output_path)

# Show the plot (optional)
plt.show()