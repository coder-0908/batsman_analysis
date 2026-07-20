# USED THIS TO GENERATE THE DATASET OF 500 INNINGS PLAYED BY AN IMAGINARY BATSMAN


import pandas as pd
import numpy as np

print("Generating 500 innings of cricket data...")

# Total number of innings to generate
num_innings = 500

# 1. Match IDs and Dates
# NumPy's arange instantly creates an array of numbers from 1 to 500
match_ids = np.arange(1, num_innings + 1)
dates = pd.date_range(start='2020-01-01', periods=num_innings, freq='D')

# 2. Runs
# We use a Gamma distribution in NumPy to simulate cricket scores realistically:
# Lots of low scores (0-30), fewer medium scores (50s), and rare high scores (100+)
runs = np.random.gamma(shape=1.5, scale=25, size=num_innings).astype(int)

# 3. Balls Faced
# Simulate strike rates between 80 (0.8) and 180 (1.8)
strike_rates = np.random.uniform(0.8, 1.8, size=num_innings)
# NumPy instantly calculates balls faced for all 500 rows at once (vectorization!)
balls_faced = np.where(runs == 0, np.random.randint(1, 6, size=num_innings), (runs / strike_rates).astype(int) + 1)

# 4. Boundaries (4s and 6s)
fours = (runs * np.random.uniform(0.2, 0.5, size=num_innings) // 4).astype(int)
sixes = (runs * np.random.uniform(0.0, 0.2, size=num_innings) // 6).astype(int)

# --- NEW: Generate Boundary Locations ---
# Common fielding positions for boundaries
fielding_positions = ['Cover', 'Point', 'Mid Wicket', 'Square Leg', 'Long On', 'Long Off', 'Fine Leg', 'Third Man', 'Extra Cover']

locations_4s = []
locations_6s = []

# Loop through the counts of boundaries and generate random locations for each one
for f, s in zip(fours, sixes):
    # If the batsman hit fours, pick 'f' random positions and join them with commas
    locs_4 = ", ".join(np.random.choice(fielding_positions, size=f)) if f > 0 else "None"
    locations_4s.append(locs_4)
    
    # If the batsman hit sixes, pick 's' random positions and join them with commas
    locs_6 = ", ".join(np.random.choice(fielding_positions, size=s)) if s > 0 else "None"
    locations_6s.append(locs_6)
# ----------------------------------------

# 5. Dismissal Types
# Assign weighted probabilities so 'Caught' happens more often than 'Stumped'
dismissal_types = ['Caught', 'Bowled', 'LBW', 'Not Out', 'Run Out', 'Stumped']
probs = [0.50, 0.20, 0.10, 0.10, 0.05, 0.05]
dismissals = np.random.choice(dismissal_types, size=num_innings, p=probs)

# 6. Bowlers
bowler_names = ['Bumrah', 'Rashid Khan', 'Cummins', 'Starc', 'Chahal', 'Rabada', 'Boult', 'Hazlewood']
bowlers = np.random.choice(bowler_names, size=num_innings)

# If the batsman is 'Not Out' or 'Run Out', a bowler doesn't get the wicket credit
bowlers = np.where((dismissals == 'Not Out') | (dismissals == 'Run Out'), 'N/A', bowlers)

# 7. Combine everything into a Pandas DataFrame
# Adding the new location columns right next to the boundary counts
df_large = pd.DataFrame({
    'Match_ID': match_ids,
    'Date': dates,
    'Runs': runs,
    'Balls_Faced': balls_faced,
    'Boundaries_4s': fours,
    'Locations_4s': locations_4s,
    'Sixes_6s': sixes,
    'Locations_6s': locations_6s,
    'Dismissal_Type': dismissals,
    'Bowler': bowlers
})

# 8. Export to a new CSV file
file_name = 'large_batsman_stats.csv'
df_large.to_csv(file_name, index=False)

print(f"Success! {num_innings} innings have been generated and saved to '{file_name}'.")