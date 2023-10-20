import pandas as pd
import numpy as np

df_matches_raw = pd.read_csv('./raw/matches.csv', 
                             usecols=['id', 'home', 'away', 'year', 'venue', 'home_score', 'away_score', 'attendance'])
df_teams_raw = pd.read_csv('./raw/teams.csv' )
# df_stadiums_raw = pd.read_csv('./raw/stadiums.csv')

#print(df_teams_raw[:20])
# print(df_stadiums_raw[:49])

df_filtered = df_matches_raw[df_matches_raw['year'] >= 2003] # from 2003 on 
df_filtered = df_filtered[df_filtered.home_score != df_filtered.away_score] # get rid of ties???
df_filtered['home_wins'] = df_filtered.apply(lambda row: 1 if row['home_score'] > row['away_score'] else 0, axis=1)

# # create home_pts column
# df_year_filtered['home_pts'] = df_year_filtered.apply(lambda row: 3 if row['home_score'] > row['away_score'] else 
#                                     1 if row['home_score'] == row['away_score'] else 0, axis=1)

# # create away_pts column
# df_year_filtered['away_pts'] = df_year_filtered.apply(lambda row: 3 if row['away_score'] > row['home_score'] else 
#                                     1 if row['away_score'] == row['home_score'] else 0, axis=1)

df_matches_cleaned = df_filtered[['id', 'home', 'away', 'year', 'venue', 'home_wins', 'attendance']] # choose columns 

df_null_filter = df_matches_cleaned.dropna(subset=["venue"]) # drop rows where venue is not included/unknown
stadium_filter_1 = df_null_filter.loc[df_matches_cleaned['venue'] != 'ESPN Wide World of Sports Complex'] # get rid of neutral venue
stadium_filter_1 = stadium_filter_1.loc[df_matches_cleaned['home'] != 'East All-Stars'] # get rid of all-star game


# clean/standardize stadium names to have format "stadium_name" instead of "stadium_name, city"
stadium_filter_1["venue"] = stadium_filter_1["venue"].str.replace(",.*", "", regex=True)

# standardize team names
stadium_filter_1['home'] = stadium_filter_1['home'].replace('Columbus Crew SC', 'Columbus Crew')
stadium_filter_1['away'] = stadium_filter_1['away'].replace('Columbus Crew SC', 'Columbus Crew')
stadium_filter_1['home'] = stadium_filter_1['home'].replace('D.C. United', 'DC United')
stadium_filter_1['away'] = stadium_filter_1['away'].replace('D.C. United', 'DC United')
stadium_filter_1['home'] = stadium_filter_1['home'].replace('Houston Dynamo', 'Houston Dynamo FC')
stadium_filter_1['away'] = stadium_filter_1['away'].replace('Houston Dynamo', 'Houston Dynamo FC')
stadium_filter_1['home'] = stadium_filter_1['home'].replace('Montreal Impact', 'CF Montréal')
stadium_filter_1['away'] = stadium_filter_1['away'].replace('Montreal Impact', 'CF Montréal')
stadium_filter_1['home'] = stadium_filter_1['home'].replace('New York City FC', 'NYCFC')
stadium_filter_1['away'] = stadium_filter_1['away'].replace('New York City FC', 'NYCFC')
stadium_filter_1['home'] = stadium_filter_1['home'].replace('Sporting Kansas City', 'Sporting KC')
stadium_filter_1['away'] = stadium_filter_1['away'].replace('Sporting Kansas City', 'Sporting KC')

# standardize stadium names
stadium_filter_1['venue'] = stadium_filter_1['venue'].replace('RFK Stadium', 'RFK Memorial Stadium')
stadium_filter_1['venue'] = stadium_filter_1['venue'].replace('R.F.K. Stadium', 'RFK Memorial Stadium')
stadium_filter_1['venue'] = stadium_filter_1['venue'].replace('RFK Memorial', 'RFK Memorial Stadium')
stadium_filter_1['venue'] = stadium_filter_1['venue'].replace('Stanford', 'Stanford Stadium')

# get rid of venues associated with home teams where the venue is not in or near the team's city 
stadium_filter_2 = stadium_filter_1.loc[~((stadium_filter_1['home'] == 'CF Montréal') & 
                                          (stadium_filter_1['venue'].isin(['DRV PNK Stadium',
                                                                            'Red Bull Arena',
                                                                           'Exploria Stadium'])))]
stadium_filter_3 = stadium_filter_2.loc[~((stadium_filter_2['home'] == 'Chicago Fire FC') & 
                                          (stadium_filter_2['venue'].isin(['Dignity Health Sports Park',
                                                                           'Cardinal Stadium',
                                                                           'Giants Stadium',
                                                                           'Sports Authority Field at Mile High'
                                                                           ])))]
stadium_filter_4 = stadium_filter_3.loc[~((stadium_filter_3['home'] == 'Colorado Rapids') & 
                                          (stadium_filter_3['venue'].isin(['BMO Field'])))]
stadium_filter_5 = stadium_filter_4.loc[~((stadium_filter_4['home'] == 'DC United') & 
                                          (stadium_filter_4['venue'].isin(['BMO Field'])))]
stadium_filter_6 = stadium_filter_5.loc[~((stadium_filter_5['home'] == 'New England Revolution') & 
                                          (stadium_filter_5['venue'].isin(['Pizza Hut Park', 'RFK Memorial Stadium'])))]
stadium_filter_7 = stadium_filter_6.loc[~((stadium_filter_6['home'] == 'NYCFC') & 
                                          (stadium_filter_6['venue'].isin(['Pratt & Whitney Stadium at Rentschler Field'])))]
stadium_filter_8 = stadium_filter_7.loc[~((stadium_filter_7['home'] == 'New York Red Bulls') & 
                                          (stadium_filter_7['venue'].isin(['Dignity Health Sports Park'])))]
stadium_filter_9 = stadium_filter_8.loc[~((stadium_filter_8['home'] == 'Real Salt Lake') & 
                                          (stadium_filter_8['venue'].isin(['Qwest Field'])))]
stadium_filter_10 = stadium_filter_9.loc[~((stadium_filter_9['home'] == 'San Jose Earthquakes') & 
                                          (stadium_filter_9['venue'].isin(['Spartan Stadium' 
                                                                           ])))]
stadium_filter_11 = stadium_filter_10.loc[~((stadium_filter_10['home'] == 'Toronto FC') & 
                                          (stadium_filter_10['venue'].isin(['Sin confirmar', 
                                                                             'Pratt & Whitney Stadium at Rentschler Field',
                                                                             'Exploria Stadium'
                                                                           ])))]
stadium_filter_11 = stadium_filter_10.loc[~((stadium_filter_10['home'] == 'Vancouver Whitecaps') & 
                                          (stadium_filter_10['venue'].isin(['Providence Park', 
                                                                             'Rio Tinto Stadium'
                                                                           ])))]
df_matches_cleaned = stadium_filter_11

# teams = np.sort(stadium_filter_11['venue'].unique()) # unique teams
venues = stadium_filter_11.loc[stadium_filter_11['home'] == 'Chicago Fire FC', 'venue'].unique().tolist()
#print(venues)

# merge the teams table with the games table to add home_id column
df_matches_cleaned = df_matches_cleaned.merge(df_teams_raw[['team_id', 'team_name']], left_on='home', right_on='team_name')
df_matches_cleaned['home_id'] = df_matches_cleaned['team_id'] # add new column home_id to the games table with corresponding team_id values
df_matches_cleaned = df_matches_cleaned.rename(columns={'team_name': 'home_team_name'})
df_matches_cleaned = df_matches_cleaned.drop(['team_id'], axis=1)
#df_matches_cleaned = df_matches_cleaned.drop(['team_name', 'team_id'], axis=1) # drop the team_name and team_id columns from the games table 

# same with away teams 
df_matches_cleaned = df_matches_cleaned.merge(df_teams_raw[['team_id', 'team_name']], left_on='away', right_on='team_name') # add new column away_id to the games table with corresponding team_id values
df_matches_cleaned['away_id'] = df_matches_cleaned['team_id'] 
df_matches_cleaned = df_matches_cleaned.rename(columns={'team_name': 'away_team_name'})
df_matches_cleaned = df_matches_cleaned.drop(['team_id'], axis=1)
# df_matches_cleaned = df_matches_cleaned.drop(['team_name', 'team_id'], axis=1) # drop the team_name and team_id columns from the games table 

# # same process with stadiums and stadium id
# df_matches_cleaned = df_matches_cleaned.merge(df_stadiums_raw[['stadium_id', 'stadium_name']], left_on='venue', right_on='stadium_name')
# df_matches_cleaned['stadium_id'] = df_matches_cleaned['stadium_id']
# #df_matches_cleaned = df_matches_cleaned.drop(['stadium_name'], axis=1)

df_matches_cleaned = df_matches_cleaned.drop(['home', 'away'], axis=1) # drop home and away columns


df_matches_cleaned = df_matches_cleaned.rename(columns={'venue': 'stadium_name'})


#df_matches_cleaned = df_year_filtered[['id', 'home', 'away', 'year', 'venue', 'home_wins']]
df_matches_cleaned = df_matches_cleaned.rename(columns={'id': 'game_id'})
df_matches_cleaned = df_matches_cleaned[['game_id', 'home_team_name', 'home_id', 'away_team_name', 'away_id', 'home_wins', 'year', 'stadium_name', 'attendance']] # rearrange columns

# add stadium_capacity column 
# df_matches_cleaned = pd.merge(df_matches_cleaned, df_stadiums_raw, on='stadium_id')
# df_matches_cleaned = df_matches_cleaned.rename(columns={'stadium_name_x': 'stadium_name'})
# df_matches_cleaned = df_matches_cleaned.drop(['stadium_name_y'], axis=1)

# to add city
df_matches_cleaned = pd.merge(df_matches_cleaned, df_teams_raw, left_on='home_team_name', right_on='team_name')

df_matches_cleaned['capacity'] = np.nan 
df_matches_cleaned['league'] = 'MLS' # add sport column

df_games_cleaned = df_matches_cleaned[['home_team_name', 'away_team_name', 'home_wins', 'year', 'stadium_name', 'city', 'attendance', 'capacity', 'league']] 

df_games_clean_sample = df_games_cleaned.sample(n=100) # sample 100 games
# df_teams_clean_sample = df_teams_raw
# df_stadiums_clean_sample = df_stadiums_raw

df_games_cleaned.to_csv('./clean/full/games.csv', index=False)
df_games_clean_sample.to_csv('./clean/sample/games_sample.csv', index=False)

# df_teams_raw.to_csv('./clean/full/teams.csv', index=False) # raw teams is already cleaned 
# df_teams_clean_sample.to_csv('./clean/samples/teams_sample.csv', index=False)

# df_stadiums_raw.to_csv('./clean/full/stadiums.csv', index=False) # raw stadiums is already cleaned
# df_stadiums_clean_sample.to_csv('./clean/samples/stadiums_sample.csv', index=False)


print(df_games_cleaned[:20])

