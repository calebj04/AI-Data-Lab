import pandas as pd
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler

#test
# Read the data
df = pd.read_csv('data/nfl_kick_attempts.csv')

# Clean player names by removing spaces
df['kicker_player_name'] = df['kicker_player_name'].str.replace(" ", "")

# Select relevant columns
kicker_seasons = df[["kicker_player_id", "kicker_player_name", "season"]]

# Count number of kicks per player per season
kicker_season_counts = (
    kicker_seasons
    .groupby(["kicker_player_id", "kicker_player_name", "season"])
    .size()
    .reset_index(name="kicks_in_season")
)

# Sort by player and season
kicker_season_counts.sort_values(by=["kicker_player_id", "season"], inplace=True)

# Save to CSV
kicker_season_counts.to_csv('data/kicker_seasons.csv', index=False)