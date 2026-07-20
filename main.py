# USED THIS TO GENERATE THE BAR CHART AND HEAT MAP OF HOW THE BATSMAN WAS DISMISSED




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset
df = pd.read_csv('large_batsman_stats.csv')

# Filter out 'Not Out' so we only look at actual wickets
dismissals = df[df['Dismissal_Type'] != 'Not Out']

# --- VISUALIZATION 1: BAR CHART ---
# Create a new plotting window
plt.figure(figsize=(8, 5))

# Create a count plot (bar chart) sorted by frequency
sns.countplot(
    data=dismissals, 
    x='Dismissal_Type', 
    order=dismissals['Dismissal_Type'].value_counts().index
)

plt.title('Frequency of Dismissal Types')
plt.xlabel('Dismissal Type')
plt.ylabel('Number of Times Out')
plt.tight_layout()
plt.show() # This opens a window showing the graph


# --- VISUALIZATION 2: HEATMAP ---
# Create a pivot table counting how often each bowler got him out by each dismissal type
bowler_dismissal_matrix = pd.crosstab(dismissals['Bowler'], dismissals['Dismissal_Type'])

plt.figure(figsize=(10, 6))

# Generate the heatmap
sns.heatmap(
    bowler_dismissal_matrix, 
    annot=True,     # Shows the actual numbers inside the cells
    cmap='YlGnBu',  # Beautiful yellow-green-blue color palette
    cbar=True       # Shows the color scale bar on the side
)

plt.title('Heatmap: Bowler vs. Dismissal Type')
plt.xlabel('Dismissal Type')
plt.ylabel('Bowler Name')
plt.tight_layout()
plt.show() # This opens the heatmap window