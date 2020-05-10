import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("data/shelter-2019.csv", index_col = 0)

# Set up the graph
barWidth = 0.25

# Load the two bars with their respective data
occupied = data["OCCUPANCY"][:100]
capacity = data["CAPACITY"][:100]

# Pos
r1 = np.arange(len(occupied))
r2 = [barWidth+ x for x in r1]

# Make the graph
plt.bar(r1, occupied, color='#7f6d5f', width=barWidth, edgecolor='white', label='Occupied')
plt.bar(r2, capacity, color='#557f2d', width=barWidth, edgecolor='white', label='Avaliable')

# Show
plt.legend()
plt.show()

print(occupied)