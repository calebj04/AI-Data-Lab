import pandas as pd

#hello

# Read the data
df = pd.read_csv('data/nfl_kick_attempts.csv')

# Select relevant columns
kicker_seasons = df[["kicker_player_id", "kicker_player_name", "season"]]

#git test
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