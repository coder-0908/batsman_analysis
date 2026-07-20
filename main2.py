# USED THIS TO GENERATE THE WAGON WHEEL OF THE BOUNDARIES SCORED BY THE BATSMAN



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load the dataset
try:
    df = pd.read_csv('large_batsman_stats.csv')
except FileNotFoundError:
    print("Error: 'large_batsman_stats.csv' not found. Make sure you've run the updated generate_data.py first!")
    exit()

# Ensure the location columns exist
if 'Locations_4s' not in df.columns or 'Locations_6s' not in df.columns:
    print("Error: Location columns not found. Please run the updated generate_data.py to generate them.")
    exit()

# 2. Extract and flatten all 4s and 6s into simple lists
all_fours = []
for item in df['Locations_4s'].dropna():
    if item != 'None':
        # Split the comma-separated strings and remove extra spaces
        all_fours.extend([loc.strip() for loc in item.split(',')])

all_sixes = []
for item in df['Locations_6s'].dropna():
    if item != 'None':
        all_sixes.extend([loc.strip() for loc in item.split(',')])

# 3. Map fielding positions to angles (in degrees)
# Assuming a Right-Handed Batsman facing "North" (90 degrees)
# 0 degrees is East (Leg side), 180 degrees is West (Off side)
angles_map = {
    'Square Leg': 0,
    'Mid Wicket': 45,
    'Long On': 75,
    'Long Off': 105,
    'Extra Cover': 135,
    'Cover': 150,
    'Point': 180,
    'Third Man': 225,
    'Fine Leg': 315
}

# 4. Set up the Polar Plot
fig = plt.figure(figsize=(10, 10))
# Create polar axes and set the background color to a nice grass green
ax = fig.add_subplot(111, polar=True)
ax.set_facecolor('#a8e6cf') 
fig.patch.set_facecolor('#f4f4f9')

# 5. Draw the shots (Lines from the center)
# We add a slight random "jitter" to the angle and length so the lines don't perfectly overlap,
# making it look like a realistic cluster of shots.

# Plot Fours (Blue lines, ending near the boundary edge)
for loc in all_fours:
    if loc in angles_map:
        angle_rad = np.deg2rad(angles_map[loc] + np.random.uniform(-8, 8)) # +/- 8 degrees jitter
        length = np.random.uniform(0.85, 0.95) # Stops just inside/at the boundary
        ax.plot([0, angle_rad], [0, length], color='#1d3557', alpha=0.5, linewidth=1.5)

# Plot Sixes (Red lines, going over the boundary edge)
for loc in all_sixes:
    if loc in angles_map:
        angle_rad = np.deg2rad(angles_map[loc] + np.random.uniform(-8, 8))
        length = np.random.uniform(1.05, 1.15) # Goes past the boundary
        ax.plot([0, angle_rad], [0, length], color='#e63946', alpha=0.8, linewidth=2.5)

# 6. Beautify the Wagon Wheel
# Draw the boundary rope
boundary_circle = plt.Circle((0, 0), 1.0, transform=ax.transData._b, color='white', fill=False, linewidth=2, linestyle='--')
ax.add_artist(boundary_circle)

# Remove the default math grids and angles
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.grid(False)
ax.spines['polar'].set_visible(False)

# Add our own fielding position labels around the edge
for position, angle in angles_map.items():
    ax.text(np.deg2rad(angle), 1.25, position, ha='center', va='center', fontsize=11, fontweight='bold', color='#333333')

# 7. Add Legend and Title
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#1d3557', lw=2, label=f'Fours ({len(all_fours)})'),
    Line2D([0], [0], color='#e63946', lw=3, label=f'Sixes ({len(all_sixes)})')
]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.2, 1.1))

plt.title('Batsman Wagon Wheel: Career 4s and 6s', size=16, weight='bold', pad=30)
plt.tight_layout()
plt.show()