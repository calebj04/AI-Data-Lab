import pandas as pd

# Read the data
df = pd.read_csv('data/nfl_kick_attempts.csv')

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

# === Extra Point analysis: flag kicker seasons below league-average XP% ===

# Filter to just extra points (XP)
xp = df[df['kick_type'] == 'XP'].copy()

# Compute league XP% per season
league = (
    xp.groupby('season')
      .agg(made=('made', 'sum'), att=('made', 'size'))
)
league['league_xp_pct'] = league['made'] / league['att']
league_avg = league['league_xp_pct']  # Series indexed by season

# Compute each kicker’s XP% per season (and include team info if available)
group_cols = ['kicker_player_id', 'kicker_player_name', 'season']
if 'posteam' in xp.columns:
    group_cols.append('posteam')

kicker_xp = (
    xp.groupby(group_cols)
      .agg(made=('made', 'sum'), att=('made', 'size'))
      .reset_index()
)

kicker_xp['xp_pct'] = kicker_xp['made'] / kicker_xp['att']
kicker_xp['league_xp_pct'] = kicker_xp['season'].map(league_avg)

# Optional: ignore tiny samples
MIN_ATT = 1
kicker_xp['below_avg'] = (kicker_xp['att'] >= MIN_ATT) & (kicker_xp['xp_pct'] < kicker_xp['league_xp_pct'])

# Add triple dashes to below-average seasons
kicker_xp['season_label'] = kicker_xp['season'].astype(str) + np.where(kicker_xp['below_avg'], '---', '')

# Sort for output
kicker_xp.sort_values(['kicker_player_id', 'season'], inplace=True)

# === Add an empty row between different players ===

# Create a blank row for visual separation
blank_row = pd.Series({col: '' for col in kicker_xp.columns})

# Build a new DataFrame with blank lines inserted
output_rows = []
for pid, group in kicker_xp.groupby('kicker_player_id', sort=False):
    output_rows.append(group)
    output_rows.append(pd.DataFrame([blank_row]))

kicker_xp_formatted = pd.concat(output_rows, ignore_index=True)

# Save final formatted data
kicker_xp_formatted.to_csv('data/kicker_xp_by_season_formatted.csv', index=False)