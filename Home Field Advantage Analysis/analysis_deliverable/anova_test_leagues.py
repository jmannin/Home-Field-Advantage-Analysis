import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import f_classif
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

def get_dataset():
    games = pd.read_csv(
        '../data_deliverable/Data/full_data/games_cleaned_final.csv',
        usecols=['game_id', 'home_team_id', 'home_wins','league'],
        low_memory=True
    )

    teams = pd.read_csv(
        '../data_deliverable/Data/full_data/teams_cleaned_final.csv',
        usecols=['team_id', 'team_name', 'city'],
        low_memory=True
    )

    # calculate home win percentage
    home_win_pct = games.groupby('home_team_id')['home_wins'].mean().reset_index()
    home_win_pct = home_win_pct.rename(columns={'home_team_id': 'team_id', 'home_wins': 'home_win_pct'})

    # add league to teams table
    teams = pd.merge(teams, games[['home_team_id', 'league']], left_on='team_id', right_on='home_team_id')
    teams = teams.drop(columns=['home_team_id']) 

    # merge with teams table 
    result = pd.merge(home_win_pct, teams[['team_id', 'team_name', 'city', 'league']], on='team_id')
    result = result.drop_duplicates(subset='team_id') 

    # get percentage
    result['home_win_pct'] = result['home_win_pct'].apply(lambda x: x * 100)

    result = result.reset_index(drop=True)

    print(result.head(10))

    result.to_csv('../data_deliverable/Data/full_data/team_win_percentage.csv', index=False)

    return result

def anova_test(df, grouping_variable):
    # Group the DataFrame by "league"
    grouped = df.groupby(grouping_variable)

    # Perform ANOVA test using f_oneway
    anova_result = f_oneway(*[group['home_win_pct'] for name, group in grouped])
    f_value = anova_result.statistic
    p_value = anova_result.pvalue

    return f_value, p_value

def plot_boxplot_by_league(df, grouping_variable):
    # Group the DataFrame by "league"
    leagues_grouped = df.groupby(grouping_variable)

    data = [group['home_win_pct'] for name, group in leagues_grouped]

    labels = [name for name, group in leagues_grouped]
    
    # Create the boxplot using matplotlib
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.boxplot(data, labels=labels)
    ax.set_title(f'Boxplot of Home Win Percentage by {grouping_variable.title()}', fontweight='bold')
    ax.set_xlabel('League', fontweight='bold')
    ax.set_ylabel('Home Win Percentage (%)', fontweight='bold')
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis tick labels

    plt.savefig(f'./visualizations/boxplot_win_pct_by_{grouping_variable}.png') 

    plt.show()


def main():
    df = get_dataset()
    df = pd.read_csv('../data_deliverable/Data/full_data/team_win_percentage.csv')

    f_value, p_value = anova_test(df, 'league')
    print("ANOVA Results:")
    print("F-statistic:",f_value)
    print("p-value:", p_value)

    plot_boxplot_by_league(df, 'league')


if __name__ == '__main__':
    main()