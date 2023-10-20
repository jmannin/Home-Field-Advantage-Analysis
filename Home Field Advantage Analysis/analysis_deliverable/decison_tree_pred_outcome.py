import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import random
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


def generate_team_name():
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(3))

# Loading data and cleaning
city_data = pd.read_csv('./data_deliverable/Data/full_data/city_data_final.csv')
stadiums = pd.read_csv('./data_deliverable/Data/full_data/stadiums_cleaned_final.csv')
team_win = pd.read_csv('./data_deliverable/Data/full_data/team_win_percentage.csv')
teams = pd.read_csv('./data_deliverable/Data/full_data/teams_cleaned_final.csv')

stadiums['capacity'] = stadiums['capacity'].str.replace(',', '').astype(float)


team_win = team_win.drop('team_id', axis=1)
team_win = team_win.merge(teams[['team_id', 'team_name']], on='team_name', how='left')
team_win = team_win.merge(city_data, on='city', how='left')

stadiums['team_id'] = teams['team_id']
team_win = team_win.merge(stadiums, on='team_id', how='left')

le = LabelEncoder()
team_win['league'] = le.fit_transform(team_win['league'])
team_win['city'] = le.fit_transform(team_win['city'])

team_win['capacity'] = pd.to_numeric(team_win['capacity'], errors='coerce')
team_win['capacity'] = team_win['capacity'].fillna(team_win['capacity'].mean())

X = team_win[['elevation (ft)', 'median household income ($)', 'league', 'capacity']]
y = team_win['home_win_pct']

# Making random teams
random_teams = []
for i in range(10):
    team = {}
    city_name = random.choice(city_data['city'].values)
    team['city'] = le.transform([city_name])[0]
    team['elevation (ft)'] = city_data.loc[city_data['city'] == city_name, 'elevation (ft)'].values[0]
    team['median household income ($)'] = city_data.loc[city_data['city'] == city_name, 'median household income ($)'].values[0]
    team['league'] = random.choice(team_win['league'].values)
    team['capacity'] = random.choice(stadiums.dropna(subset=['capacity'])['capacity'].values)
    random_teams.append(team)

team_names = [generate_team_name() for _ in range(10)]


# Training tree
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = DecisionTreeRegressor(max_depth=3)
clf.fit(X_train, y_train)

# Predicting home win %s
random_teams_df = pd.DataFrame(random_teams)
random_teams_df = random_teams_df.fillna(random_teams_df.mean())
random_teams_df = random_teams_df.drop('city', axis=1)

predicted_win_pct = clf.predict(random_teams_df)

# Playing the season out
scores = {i: 0 for i in range(10)}
for i in range(10):
    random_teams[i]['predicted_win_pct'] = predicted_win_pct[i]

## This parameter controls how much of the simulation results are random vs. the higher home % team winning
randomness = 0.05
## Parameter must be between 0 and 1. Closer to 0 is less random, 1 is more
## Note: this does not effect how home win % is predicted

for i in range(10):
    for j in range(i+1, 10):
        team_i_win_prob = random_teams[i]['predicted_win_pct']
        team_j_win_prob = random_teams[j]['predicted_win_pct']

        adj_i_win_prob = team_i_win_prob + randomness * (0.5 - team_i_win_prob)
        adj_j_win_prob = team_j_win_prob + randomness * (0.5 - team_j_win_prob)

        prob_i = adj_i_win_prob / (adj_i_win_prob + adj_j_win_prob)
        prob_j = adj_j_win_prob / (adj_i_win_prob + adj_j_win_prob)

        winner = random.choices([i, j], [prob_i, prob_j])[0]
        scores[winner] += 3

# Decision Tree
plt.figure(figsize=(14,9))
plot_tree(clf, filled=True, feature_names=X.columns, fontsize=7)

plt.title("Decision Tree Regression for Home Field Advantage", fontsize=14)
plt.savefig('./analysis_deliverable/visualizations/decision_tree_regression.png')

plt.show()

# League Table
team_ids = scores.keys()
points = scores.values()
teams = [team_names[id] for id in team_ids]
league_table = pd.DataFrame(list(zip(teams, points)), columns=["Team", "Points"])
league_table = league_table.sort_values(by="Points", ascending=False)
league_table['Wins'] = league_table['Points'] // 3
league_table['Losses'] = 9 - league_table['Wins']

fig, ax = plt.subplots(1, 1, figsize=(8, 6))

table_data = league_table.values.tolist()
column_labels = ["Team", "Points", "Wins", "Losses"]

row_labels = list(range(1, len(teams) + 1))
ax.axis('off')
table = ax.table(cellText=table_data,
                 colLabels=column_labels,
                 rowLabels=row_labels,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(13)
table.scale(0.55, 2.75)

for (row, col), cell in table.get_celld().items():
    if (row == 0) or (col == -1):
        cell.set_fontsize(15)
        cell.set_facecolor('#1890db')
        cell.set_text_props(color='white')

ax.set_title('Simulated League Table', fontsize=15, pad=25)

plt.savefig('./analysis_deliverable/visualizations/simulated_league_table.png')

plt.show()

# Standings bar graph
teams = [team_names[id] for id in team_ids]
points = scores.values()
league_table = pd.DataFrame(list(zip(teams, points)), columns=["Team", "Points"])
league_table = league_table.sort_values(by="Points", ascending=False)

plt.figure(figsize=(12,8))
sns.barplot(x="Points", y="Team", data=league_table, orient='h')
plt.title("Final League Table")
plt.savefig('./analysis_deliverable/visualizations/final_league_table.png')
plt.show()

#Team attributes graphs
def plot_team_attributes(random_teams, team_names, scores):
    winning_team = team_names[max(scores, key=scores.get)]

    attributes = ['elevation (ft)', 'median household income ($)', 'league', 'capacity']
    num_attributes = len(attributes)
    fig, axs = plt.subplots(num_attributes, 1, figsize=(13, num_attributes*2))

    for i, attr in enumerate(attributes):
        attribute_values = [team[attr] for team in random_teams]
        bar_colors = ['red' if team == winning_team else 'blue' for team in team_names]
        axs[i].bar(team_names, attribute_values, color=bar_colors)
        axs[i].set_title(f'{attr} by Team')
        axs[i].set_xlabel('Team')
        axs[i].set_ylabel(attr)

    plt.tight_layout()

    plt.savefig('./analysis_deliverable/visualizations/team_attributes.png')
    plt.show()

plot_team_attributes(random_teams, team_names, scores)

# Predicted win %s vs results
def plot_predicted_win_percentages(random_teams, team_names, scores):
    team_ranks = sorted(scores, key=scores.get, reverse=True)
    team_ranks = {team: rank+1 for rank, team in enumerate(team_ranks)}

    team_data = [(team['predicted_win_pct'], team_names[id], team_ranks[id]) for id, team in enumerate(random_teams)]
    team_data.sort(key=lambda x: x[0], reverse=False)
    predicted_win_percentages, team_names_sorted, ranks_sorted = zip(*team_data)

    team_labels = [f"{team} ({rank})" for team, rank in zip(team_names_sorted, ranks_sorted)]
    bar_colors = ['red' if rank == 1 else 'blue' for rank in ranks_sorted]

    plt.figure(figsize=(10, 6))
    plt.barh(team_labels, predicted_win_percentages, color=bar_colors)
    plt.xlabel("Predicted Home Win Percentage")
    plt.ylabel("Teams (Final Rank)")
    plt.title("Predicted Home Win Percentage by Team")

    plt.tight_layout()
    plt.savefig('./analysis_deliverable/visualizations/predicted_home_win_percentage.png')
    plt.show()

plot_predicted_win_percentages(random_teams, team_names, scores)
