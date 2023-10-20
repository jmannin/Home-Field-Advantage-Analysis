import pandas as pd 

## EXTRA TEST IF WE HAVE TIME: MEASURES HOW THE PERFORMANCE OF THE TEAMS IN A LEAGUE CHANGE OVER TIME USING STANDARD DEVIATION
games = pd.read_csv(
    '../data_deliverable/Data/full_data/games_cleaned_final.csv',
    usecols=['game_id', 'home_team_id', 'home_wins', 'year', 'league'],
    low_memory=True
)

teams = pd.read_csv(
    '../data_deliverable/Data/full_data/teams_cleaned_final.csv',
    usecols=['team_id', 'team_name'],
    low_memory=True
)

# merge the games and teams tables
merged_data = games.merge(teams, left_on='home_team_id', right_on='team_id')

# calculate win percentage for each team per year/season
# transform: calculates the mean value of the "home_wins" for each group (team_id, year)
merged_data['win_percentage'] = merged_data.groupby(['team_id', 'year'])['home_wins'].transform('mean')

# print(merged_data.head(100))

# calculate stddev of win percentage for each team over time
std_deviation = merged_data.groupby('team_id')['win_percentage'].std()

# merge stddev with teams table
std_deviation = std_deviation.reset_index()
std_deviation = pd.merge(std_deviation, games[['home_team_id', 'league']], left_on='team_id', right_on='home_team_id')

# group teams by league, compute avg stddev
avg_std_deviation = std_deviation.groupby('league')['win_percentage'].mean()

result = pd.DataFrame({'league': avg_std_deviation.index, 'avg_standard_deviation': avg_std_deviation.values})

# Display the final table
print(result)



