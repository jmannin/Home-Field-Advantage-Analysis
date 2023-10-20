import pandas as pd

# THIS IS THE ORIGINAL CLEANER, USE THE OTHER ONE

# imports the CSVs
df_games_raw = pd.read_csv('./raw/games.csv')
df_teams_raw = pd.read_csv('./raw/teams.csv')

# selects only the necessary columns from the game df, then renames the columns
df_games_clean = df_games_raw[['HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'HOME_TEAM_WINS', 'SEASON']]
df_games_clean = df_games_clean.rename(columns={'HOME_TEAM_ID': 'home_id', 'VISITOR_TEAM_ID': 'away_id', 'HOME_TEAM_WINS': 'home_wins', 'SEASON':'year'})

# add NBA as sport
df_games_clean['league'] = 'NBA'

# selects only the necessary columns from the teams df, then renames the columns
df_teams_clean = df_teams_raw[['TEAM_ID', 'NICKNAME', 'CITY']]
df_teams_clean = df_teams_clean.rename(columns={'TEAM_ID': 'team_id', 'NICKNAME': 'team_name', 'CITY': 'city',})

# selects only the necessary columns from the teams df to get the stadium data, then renames the columns
df_stadiums_clean = df_teams_raw[['ARENA', 'CITY', 'ARENACAPACITY']]
df_stadiums_clean = df_stadiums_clean.rename(columns={'ARENA': 'stadium_name', 'CITY': 'city', 'ARENACAPACITY': 'capacity'})

# samples only 100 games, because there were 26k games in total
df_games_clean_sample = df_games_clean.sample(n=100)
# didn't need to sample, because there were only 26 teams in total
df_teams_clean_sample = df_teams_clean
# didn't need to sample, because there were only 26 stadiums in total
df_stadiums_clean_sample = df_stadiums_clean

# saves games df to CSV
df_games_clean.to_csv('./clean/full/games.csv', index=False)
df_games_clean_sample.to_csv('./clean/samples/games_sample.csv', index=False)

# saves teams df to CSV
df_teams_clean.to_csv('./clean/full/teams.csv', index=False)
df_teams_clean_sample.to_csv('./clean/samples/teams_sample.csv', index=False)

df_stadiums_clean.to_csv('./clean/full/stadiums.csv', index=False)
df_stadiums_clean_sample.to_csv('./clean/samples/stadiums_sample.csv', index=False)