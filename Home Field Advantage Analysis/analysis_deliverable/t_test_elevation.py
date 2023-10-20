import pandas as pd
from scipy.stats import ttest_ind

def preprocessing():

    city_data =  pd.read_csv(
            '../data_deliverable/Data/full_data/city_data_final.csv',
            usecols=['city', 'elevation (ft)'],
            low_memory=True
        )

    team_win_pct =  pd.read_csv(
            '../data_deliverable/Data/full_data/team_win_percentage.csv',
            usecols=['team_id', 'home_win_pct', 'city'],
            low_memory=True
        )

    city_data = city_data.rename(columns={'elevation (ft)': 'elevation'})

    df = pd.merge(team_win_pct, city_data, on='city')

    df = df[['team_id', 'home_win_pct', 'elevation']]

    print(df.head(5))
    print('mean: ', df['elevation'].mean())

    elevation_threshold = 1000 # split teams at elevation = 1000 ft


    # Split the teams into higher and lower elevation groups
    lower_elevation_teams = df[df['elevation'] <= 1000]
    higher_elevation_teams = df[df['elevation'] > 4000]

    print(lower_elevation_teams.shape)
    print(higher_elevation_teams.shape)


    return lower_elevation_teams, higher_elevation_teams

def t_test(df_low, df_high):
    df_low_win_pct = df_low['home_win_pct']
    df_high_win_pct = df_high['home_win_pct']

    tstat, pvalue = ttest_ind(df_low_win_pct, df_high_win_pct)

    return tstat, pvalue

def main():
    alpha = 0.05  # significance level
    lower_elevation_teams, higher_elevation_teams = preprocessing()
    tstat, pvalue = t_test(lower_elevation_teams, higher_elevation_teams)
    print('t-test results:')
    print('t statistics: ', tstat)
    print('p value: ', pvalue)
    print()

    if pvalue < alpha:
      print("Reject the null hypothesis. There is evidence to suggest that teams playing in higher elevation regions have a higher home field win percentage.")
    else:
      print("Fail to reject the null hypothesis. There is not enough evidence to suggest that teams playing in higher elevation regions have a higher home field win percentage.")

if __name__ == '__main__':
    main()



