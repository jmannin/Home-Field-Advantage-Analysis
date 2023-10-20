import pandas as pd
import numpy as np

# GET STADIUM NAMES, FIND WHERE THEY WERE MARKED HOME BUT DIDN'T PLAY IN THEIR CITY AS DONE WITH MLS

df_games_raw = pd.read_csv('./raw/games.csv', usecols=['Game', 'away', 'home', 'away-score', 'home-score', 'Stadium', 'Date', 'Location', 
                                                       'Attendance', 'Capacity'])
df_games_raw = df_games_raw.rename(columns={'Game': 'game_id'})
df_games_raw = df_games_raw.rename(columns={'away': 'away_team_name'})
df_games_raw = df_games_raw.rename(columns={'home': 'home_team_name'})
df_games_raw = df_games_raw.rename(columns={'Stadium': 'stadium_name', 'Location': 'city', 'Date': 'date', 'Attendance': 'attendance', 'Capacity': 'capacity'})

condition = df_games_raw['home_team_name'].str.contains('NL')
df_games_raw= df_games_raw[~condition] # get rid of AL NL game
condition = df_games_raw['away_team_name'].str.contains('NL')
df_games_raw= df_games_raw[~condition] # get rid of AL NL game

df_games_raw['stadium_name'] = df_games_raw['stadium_name'].str.replace(r'\n|\t', '', regex=True)
df_games_raw['stadium_name'] = df_games_raw['stadium_name'].str.replace("Coverage.*", "", regex=True)
df_games_raw['city'] = df_games_raw['city'].str.replace(r'\n|\t', '', regex=True)
df_games_raw['city'] = df_games_raw['city'].str.replace('\d+', '', regex=True)
df_games_raw['city'] = df_games_raw['city'].replace('Washington, District of Columbia', 'Washington, D.C.')


df_games_raw['date'] = df_games_raw['date'].apply(lambda x: pd.to_datetime(x).year)
df_games_raw = df_games_raw.rename(columns={'date': 'year'})

df_games_raw['home_wins'] = df_games_raw.apply(lambda row: 1 if row['home-score'] > row['away-score'] else 0, axis=1)
df_games_raw['capacity'] = np.nan 
df_games_raw['league'] = 'MLB' # add sport column

df_games_cleaned= df_games_raw[['home_team_name', 'away_team_name',  'home_wins', 'year', 'stadium_name', 'city', 'attendance', 'capacity', 'league']]

unique_teams = df_games_cleaned['home_team_name'].unique().tolist()
print(unique_teams)
for team in unique_teams:
    cities = df_games_cleaned.loc[df_games_cleaned['home_team_name'] == team, 'city'].unique().tolist()
    df_games_cleaned = df_games_cleaned.loc[~((df_games_cleaned['home_team_name'] == team) & (df_games_cleaned['city'].isin(cities[1:])))]

print(len(df_games_cleaned['city'].unique().tolist()))

cities = df_games_cleaned.loc[df_games_cleaned['home_team_name'] == 'PIT', 'city'].unique().tolist()
print(cities)

# venues = df_games_cleaned.loc[df_games_cleaned['home_team_name'] == 'PIT', 'stadium_name'].unique().tolist()
# print('venues: ', venues)

df_games_cleaned.to_csv('./clean/full/games.csv', index=False)
df_games_cleaned.to_csv('./clean/sample/games_sample.csv')

print(df_games_cleaned[:5])