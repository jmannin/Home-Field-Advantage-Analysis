import pandas as pd 

# Load the individual games tables for each league
mlb_games = pd.read_csv('./MLB/clean/full/games.csv')
mls_games = pd.read_csv('./MLS/clean/full/games.csv')
nba_games = pd.read_csv('./NBA/clean/full/games.csv')
nfl_games = pd.read_csv('./NFL/clean/full/games.csv')
nhl_games = pd.read_csv('./NHL/clean/full/games.csv')

# Combine the games tables into a single df
games = pd.concat([mlb_games, mls_games, nba_games, nfl_games, nhl_games])

# Create a unique id for each team and stadium
teams = games[['home_team_name']].drop_duplicates().reset_index(drop=True).reset_index().rename(columns={'index': 'team_id', 'home_team_name': 'team_name'})
stadiums = games[['stadium_name']].drop_duplicates().reset_index(drop=True).reset_index().rename(columns={'index': 'stadium_id'})

# teams.to_csv('teams_1.csv', index=False)
# stadiums.to_csv('stadiums_1.csv', index=False)

# Join the teams and stadiums tables with the games table

# home id
games = games.merge(teams, how='left', left_on='home_team_name', right_on='team_name')
games = games.rename(columns={'team_id': 'home_team_id'})
games = games.drop(['team_name'], axis=1)
# away id
games = games.merge(teams, how='left', left_on='away_team_name', right_on='team_name')
games = games.rename(columns={'team_id': 'away_team_id'})
games = games.drop(['team_name'], axis=1)
# stadium id
games = games.merge(stadiums, how='left', on='stadium_name')
games = games.drop(['home_team_name', 'away_team_name', 'stadium_name'], axis=1)

# now add city to teams
teams = teams.merge(games[['home_team_id', 'city']], left_on='team_id', right_on='home_team_id').drop_duplicates()
teams = teams.drop(['home_team_id'], axis=1)

# add capacity to stadiums
stadiums = stadiums.merge(games[['stadium_id', 'capacity']], on='stadium_id').drop_duplicates()

# teams.to_csv('teams_2.csv', index=False)
# stadiums.to_csv('stadiums_2.csv', index=False)

# add game_id
games['game_id'] = games.reset_index().index

# Create the final tables
games_table = games[['game_id', 'home_team_id', 'away_team_id', 'home_wins', 'year', 'stadium_id', 'attendance', 'league']]
teams_table = teams[['team_id', 'team_name', 'city']]
stadiums_table = stadiums[['stadium_id', 'stadium_name', 'capacity']]

games_sample = games_table.sample(n=100)
teams_sample = teams_table.sample(n=100)
stadiums_sample = stadiums_table.sample(n=100)

# Save the tables as CSV files
games_table.to_csv('./full_data/games_cleaned_final.csv', index=False)
teams_table.to_csv('./full_data/teams_cleaned_final.csv', index=False)
stadiums_table.to_csv('./full_data/stadiums_cleaned_final.csv', index=False)

games_sample.to_csv('./sample_data/games_cleaned_sample.csv', index=False)
teams_sample.to_csv('./sample_data/teams_cleaned_sample.csv', index=False)
stadiums_sample.to_csv('./sample_data/stadiums_cleaned_sample.csv', index=False)

print(games_table[:5])
print(teams_table[:5])
print(stadiums_table[:5])