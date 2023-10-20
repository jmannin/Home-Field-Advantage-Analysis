import pandas as pd
from scipy.stats import pearsonr

def preprocessing():
    
    games = pd.read_csv(
        '../data_deliverable/Data/full_data/games_cleaned_final.csv',
        usecols=['game_id', 'home_team_id', 'home_wins','stadium_id', 'attendance', 'league'],
        low_memory=True
    )

    games = games.rename(columns= {'home_team_id': 'team_id'})

    print('games')
    print(games.head(5))

    teams = pd.read_csv(
        '../data_deliverable/Data/full_data/teams_cleaned_final.csv',
        usecols=['team_id', 'team_name'],
        low_memory=True
    )

    stadiums = pd.read_csv(
        '../data_deliverable/Data/full_data/stadiums_cleaned_final.csv',
        usecols=['stadium_id', 'capacity'],
        low_memory=True
    )

    merged_df = pd.merge(games, teams, on='team_id')

    merged_df = merged_df.dropna(subset=['attendance'])
    merged_df['attendance'] = merged_df['attendance'].str.replace(',', '').astype(float)

    home_win_pct = merged_df.groupby('team_id')['home_wins'].mean()

    result = merged_df[['game_id', 'team_id', 'attendance']]
    result = result.merge(home_win_pct, on='team_id')
    result = result.rename(columns={'home_wins': 'home_win_pct'})

    print(result.shape)

    # merged_df = pd.merge(merged_df, stadiums, on='stadium_id', how='left')

    # # create the capacity_attendance column based on conditions
    # merged_df['capacity_attendance'] = merged_df.apply(
    #     lambda row: row['attendance'] if row['league'] in ['MLB', 'MLS'] else row['capacity'],
    #     axis=1
    # )

    # # remove rows with NaN values 
    # merged_df = merged_df.dropna(subset=['capacity_attendance'])

    # # convert all strings to floats
    # merged_df['capacity_attendance'] = merged_df['capacity_attendance'].str.replace(',', '').astype(float)

    # # get home win percentage
    # home_win_pct = merged_df.groupby('team_id')['home_wins'].mean()

    # result = merged_df[['game_id', 'team_id', 'capacity_attendance']]
    # result = result.merge(home_win_pct, on='team_id')
    # result = result.rename(columns={'home_wins': 'home_win_pct'})

    # print(result.head(10))

    return result

def calculate_pearson_coef(df):
   corr_coef, pvalue = pearsonr(df['attendance'], df['home_win_pct'])
    # corr_coef, pvalue = pearsonr(df['capacity_attendance'], df['home_win_pct'])
   return corr_coef, pvalue

  
def main():
  df = preprocessing()
  corr_coef, pvalue = calculate_pearson_coef(df)
  print("Pearson Correlation Coefficient:", corr_coef)
  print('p value: ' , pvalue)

if __name__ == '__main__':
    main()

