import pandas as pd
import numpy as np

# USE THIS CLEANER AS OPPOSED TO OTHER ONE

def get_state(city):
    if city == 'Atlanta':
        return 'Georgia'
    elif city == 'Boston':
        return 'Massachusetts'
    elif city== 'New Orleans':
        return 'Louisiana'
    elif city == 'Chicago':
        return 'Illinois'
    elif city == 'Dallas':
        return 'Texas'
    elif city == 'Denver':
        return 'Colorado'
    elif city == "Houston" or city == 'San Antonio':
        return 'Texas'
    elif city == 'Los Angeles' or city == 'Sacramento' or city == 'San Francisco':
        return 'California'
    elif city == 'Miami' or city == 'Orlando':
        return 'Florida'
    elif city == 'Milwaukee':
        return 'Wisconsin'
    elif city == 'New York':
        return 'New York'
    elif city == 'Philadelphia':
        return 'Pennsylvania'
    elif city == 'Phoenix':
        return 'Arizona'
    elif city == 'Oklahoma City':
        return 'Oklahoma'
    elif city == 'Toronto':
        return 'Ontario'
    elif city == 'Memphis':
        return 'Tennessee'
    elif city == 'Washington':
        return 'D.C.'
    elif city == 'Detroit':
        return 'Michigan'
    elif city == 'Cleveland':
        return 'Ohio'
    elif city == 'Portland':
        return 'Oregon'
    elif city == 'Indianapolis':
        return 'Indiana'
    elif city == 'Salt Lake City':
        return 'Utah'
    elif city == 'Minneapolis':
        return 'Minnesota'
    elif city == 'Charlotte':
        return 'North Carolina'

# imports the CSVs
df_games_raw = pd.read_csv('./raw/games.csv')
df_teams_raw = pd.read_csv('./raw/teams.csv')

# selects only the necessary columns from the game df, then renames the columns
df_games_clean = df_games_raw[['GAME_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'HOME_TEAM_WINS', 'SEASON']]
df_games_clean = df_games_clean.rename(columns={'GAME_ID': 'game_id', 'HOME_TEAM_ID': 'home_id', 'VISITOR_TEAM_ID': 'away_id', 'HOME_TEAM_WINS': 'home_wins', 'SEASON':'year'})

# selects only the necessary columns from the teams df, then renames the columns
df_teams_clean = df_teams_raw[['TEAM_ID', 'NICKNAME', 'CITY', 'ARENA', 'ARENACAPACITY']]
df_teams_clean = df_teams_clean.rename(columns={'TEAM_ID': 'team_id', 'NICKNAME': 'team_name', 'CITY': 'city', 'ARENA': 'stadium_name', 'ARENACAPACITY': 'capacity'})

# change team_name to full name
df_teams_clean['team_name'] = df_teams_clean.apply(lambda x: x['city'] + ' ' + x['team_name'], axis=1)


df_teams_clean['city'] = df_teams_clean['city'].replace('Brooklyn', 'New York')
df_teams_clean['city'] = df_teams_clean['city'].replace('Indiana', 'Indianapolis')
df_teams_clean['city'] = df_teams_clean['city'].replace('Utah', 'Salt Lake City')
df_teams_clean['city'] = df_teams_clean['city'].replace('Golden State', 'San Francisco')
df_teams_clean['city'] = df_teams_clean['city'].replace('Minnesota', 'Minneapolis')
df_teams_clean['city'] = df_teams_clean['city'] + ', ' + df_teams_clean['city'].apply(get_state)

# add missing capacities
df_teams_clean.loc[df_teams_clean['stadium_name'] == 'Smoothie King Center', 'capacity'] = 17791
df_teams_clean.loc[df_teams_clean['stadium_name'] == 'Barclays Center', 'capacity'] = 19000
df_teams_clean.loc[df_teams_clean['stadium_name'] == 'Wells Fargo Center', 'capacity'] = 21000
df_teams_clean.loc[df_teams_clean['stadium_name'] == 'Talking Stick Resort Arena', 'capacity'] = 18442
df_teams_clean.loc[df_teams_clean['stadium_name'] == 'Amway Center', 'capacity'] = 20000


df_games_clean = df_games_clean.merge(df_teams_clean, left_on='home_id', right_on='team_id')
df_games_clean = df_games_clean.rename(columns={'team_name': 'home_team_name'})
df_games_clean = df_games_clean.drop(['team_id'], axis=1)

df_games_clean = df_games_clean.merge(df_teams_clean[['team_id', 'team_name']], left_on='away_id', right_on='team_id')
df_games_clean = df_games_clean.rename(columns={'team_name': 'away_team_name'})
df_games_clean = df_games_clean.drop(['team_id'], axis=1)

df_games_clean['attendance'] = np.nan
df_games_clean['league'] = 'NBA' # add sport column
df_games_clean = df_games_clean[['home_team_name', 'away_team_name', 
                             'home_wins', 'year', 'stadium_name', 'city', 'attendance', 'capacity', 'league']]

df_games_clean_sample = df_games_clean.sample(n=100)
df_games_clean.to_csv('./clean/full/games.csv', index=False)
df_games_clean_sample.to_csv('./clean/sample/games_sample.csv', index=False)

# df_teams_clean.drop('state', axis=1, inplace=True)

# # samples only 100 games, because there were 26k games in total
# df_games_clean_sample = df_games_clean.sample(n=100)
# # didn't need to sample, because there were only 26 teams in total
# df_teams_clean_sample = df_teams_clean

# # saves games df to CSV
# df_games_clean.to_csv('./clean/full/games.csv', index=False)
# df_games_clean_sample.to_csv('./clean/samples/games_sample.csv', index=False)

# # saves teams df to CSV
# df_teams_clean.to_csv('./clean/full/teams.csv', index=False)
# df_teams_clean_sample.to_csv('./clean/samples/teams_sample.csv', index=False)

print(df_teams_clean[:15])
print(df_games_clean[:10])