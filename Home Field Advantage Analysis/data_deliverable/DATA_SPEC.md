# I. Where the MLB, MLS, NBA, NFL, and NHL data is from
The data for each league was collected from games data sources from Kaggle. The Kaggle dataset for the NBA data was collected from the official NBA stats website. The dataset for the MLB data was scraped from ESPNs website. The dataset for the MLS was collected from several sources, most notably scraped from the fbref website. The dataset for the NHL data was gathered from an NHL stats API. The datasets we used for NHL data were collected from various sources, most notably from ESPN. More details about where and how each dataset was created can be seen at the links provided below.

Here are the links to the data we used:
    MLB: https://www.kaggle.com/datasets/josephvm/mlb-game-data?select=games.csv	
    NBA: https://www.kaggle.com/datasets/nathanlauga/nba-games?resource=download&select=games.csv
    MLS: https://www.kaggle.com/datasets/nathanlauga/nba-games?resource=download&select=games.csv
    NHL: https://www.kaggle.com/datasets/martinellis/nhl-game-data
    NFL: https://www.kaggle.com/datasets/cviaxmiwnptr/nfl-team-stats-20022019-espn
         https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data



# II. Format of NBA data
Note that we have cleaned and joined our collected data into three tables: games, teams, and stadiums. All of the attributes of each table will be used/useful in some way for our analysis (that's why they have been kept after cleaning in the first place).

The full data can be accessed in the full_data folder within the larger Data folder and samples of the data can be accessed in the sample_data folder (again within the larger Data folder).

## games (aka games_cleaned_final)
Each row in the table contains data for one game 

    a. game_id - int - the unique id of the game
    b. home_team_id - int - the team id of the the home team
    c. away_team_id - int - the team id of the away team
    d. home_wins - bool - 1 (true) or 0 (false)
        If home_wins=1, then the home team won the game; otherwise, home_wins=0
    e. year - int - The year that the game was played. 
        The range is between 2003 and 2022 for the NBA and MLS, from 2003 to 2020 for the NHL, from 2016 to 2021 for the MLB, and from 2003 to 2023 for the NFL
    f. stadium_id - int - the id of the stadium/venue at which the game was played
    g. attendance - int - the attendance at the game 
        Some games or even leagues have no attendance data, in which case, the value is left as NaN
        Not a required value
    h. league - str - the name of the league in which the game was played
        Options are MLB, NHL, NFL, MLS, or NBA

## teams (aka teams_cleaned_final)
Each line of the file contains one NBA league team

    a. team_id - int - the unique id of the team
    b. team_name - str - the name of the team; these names are also unique across all 5 leagues
    c. city - str - the city in which the team resides

## stadiums (aka stadiums_cleaned_final)
    a. stadium_id - int - the unique id of the stadium
    b. stadium_name - str - the name of the stadium
    c. capacity - int - the capacity of the stadium



