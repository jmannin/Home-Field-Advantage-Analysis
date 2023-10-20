import pandas as pd 
import numpy as np

# GET STADIUM NAMES, FIND WHERE THEY WERE MARKED HOME BUT DIDN'T PLAY IN THEIR CITY AS DONE WITH MLS

df_games_raw = pd.read_csv('./raw/games.csv', 
                             usecols=['game_id', 'date_time_GMT', 'away_team_id', 'home_team_id', 'outcome', 'venue'])
df_teams_raw = pd.read_csv('./raw/team_info.csv', usecols=['team_id', 'shortName', 'teamName', 'city'])
df_arenas_raw = pd.read_csv('./raw/arenas.csv')


df_games_raw['date_time_GMT'] = df_games_raw['date_time_GMT'].apply(lambda x: pd.to_datetime(x).year)
df_games_raw = df_games_raw.rename(columns={'date_time_GMT': 'year'})
df_games_raw = df_games_raw[df_games_raw['year'] >= 2003] # from 2003 on 

# create new column home_wins based on outcome 
df_games_raw['home_wins'] = df_games_raw['outcome'].apply(lambda x: 1 if 'home win' in x else 0)
df_games_raw = df_games_raw[['game_id', 'home_team_id', 'away_team_id', 'home_wins', 'year', 'venue']]
df_games_raw = df_games_raw.rename(columns={'venue': 'stadium_name'})

# clean dirty venue names
df_games_raw.loc[df_games_raw['stadium_name'].str.contains("Centre Bell"), "stadium_name"] = "Centre Bell"
df_games_raw.loc[df_games_raw['stadium_name'].str.contains("Staples Center"), "stadium_name"] = "STAPLES Center"
df_games_raw.loc[df_games_raw['stadium_name'].str.contains("Bridgestone Arena"), "stadium_name"] = "Bridgestone Arena"
df_games_raw.loc[df_games_raw['stadium_name'].str.contains("Verizon Center"), "stadium_name"] = "Verizon Center"
df_games_raw.loc[df_games_raw['stadium_name'].str.contains("Rogers Arena"), "stadium_name"] = "Rogers Arena"
df_games_raw.loc[df_games_raw['stadium_name'].str.contains("Hartwall Areena"), "stadium_name"] = "Hartwall Arena"

# new team_name column in teams
df_teams_raw['team_name'] = df_teams_raw.apply(lambda x: x['shortName'] + ' ' + x['teamName'], axis=1)

df_games_raw = df_games_raw.merge(df_teams_raw[['team_id', 'team_name']], left_on='home_team_id', right_on='team_id')
df_games_raw = df_games_raw.rename(columns={'team_name': 'home_team_name'})

df_games_raw = df_games_raw.merge(df_teams_raw[['team_id', 'team_name']], left_on='away_team_id', right_on='team_id')
df_games_raw = df_games_raw.rename(columns={'team_name': 'away_team_name'})

df_games_raw = pd.merge(df_games_raw, df_teams_raw, left_on='home_team_id', right_on='team_id')
df_games_raw = df_games_raw.drop(['team_id', 'shortName', 'teamName', 'team_name'], axis=1)

stadium_names, stadium_ids = pd.factorize(df_games_raw['stadium_name']) # get unique stadium names and their corresponding indices

# Add a new column "stadium_id" to the "games" DataFrame, mapping each stadium name to its corresponding integer id
df_games_raw['stadium_id'] = stadium_names

# change column names
df_games_raw = df_games_raw.rename(columns={'home_team_id': 'home_id'})
df_games_raw = df_games_raw.rename(columns={'away_team_id': 'away_id'})


df_games_raw['attendance'] = np.nan

# Capacity: use this to get unique values and output to a table, which will help us construct the capacity table manually
# stadiums = pd.DataFrame(df_games_raw["stadium_name"].unique(), columns=["stadium_name"])
# stadiums["capacity"] = ""
# stadiums.to_csv("new_file.csv", index=False) # save to CSV file to manually input capacities

df_games_raw = df_games_raw.merge(df_arenas_raw, on='stadium_name') # merge w/ arenas table on stadium name

df_games_raw['league'] = 'NHL' # add sport column

df_games_cleaned = df_games_raw[['home_team_name',  'away_team_name', 
                             'home_wins', 'year', 'stadium_name', 'city', 'attendance', 'capacity', 'league']]



# df_games_cleaned = df_games_raw[['home_team_name', 'away_team_name', 
#                              'home_wins', 'year', 'stadium_name', 'capacity', 'league']]

df_games_cleaned_sample = df_games_cleaned.sample(n=100)
df_teams_cleaned = df_teams_raw

df_games_cleaned.to_csv('./clean/full/games.csv', index=False)
df_games_cleaned_sample.to_csv('./clean/sample/game_sample.csv', index=False)

print(df_games_cleaned[1000:1040])

