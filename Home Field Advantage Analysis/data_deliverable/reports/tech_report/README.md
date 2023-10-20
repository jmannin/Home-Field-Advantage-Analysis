# final-project-tjnz
final-project-tjnz created by GitHub Classroom

Note: the data spec is in the Data folder of the repository

# Technical Report 

## How many data points are there in total?

  Games table: 71,361 data points
  Teams table: 152 data points
  Stadiums table: 221 data points

  Given the enormous amount of game data we have for each league, we definitely think we have enough data to perform our analysis later on.

## What are the identifying attributes?
    More detail is given in our data spec but the identifying attributes for each table are:
      a. Games: game_id, home_team_id, away_team_id, home_wins, year, stadium_id, attendance, league
      b. Teams: team_id, team_name, city
      c. Stadiums: stadium_id, stadium_name, capacity

## Where is the data from? 

    We obtained most of our data through publicly available datasets found via Kaggle. These are fairly reputable as historical game data is well recorded, and the specific datasets we used were well-recieved on the platform. Because of the timeframes and nature of the datasets, we believe that it is very comprehensive and representative. Almost all games are recorded in the time frame, so it is very unlikely that we have forms of sampling bias. Overall, because of the very public and granular nature of our datasets, we are not particularly concerned about inaccuracies or skew. 

## How clean is the data? Does this data contain what you need in order to complete the project you proposed to do? (Each team will have to go about answering this question differently but use the following questions as a guide. Graphs and tables are highly encouraged if they allow you to answer these questions more succinctly.)

    We consider our data quite clean. We have a dataset which is clean enought to comprehensively answer most of our questions with basically all samples included. The one area where they may be issues is analyzing the relationship between stadium attendance, capacity and home advantage due to incomplete data, but this is only one part of our analysis. Overall, our data is now certainly organized in a way that home field advantage can easily be identified and compared across categores. 

  ### How did you check for the cleanliness of your data? What was your threshold reference?

    We ultimately did not check comprehensively for the cleanliess, though we feel this is justified give the nature of our cleaning. The changes we made were largely not due to innaccuracy, but specifics relating to the relationships we were exploring. For example, a game being played in a neutral venue should be removed because there should be no 'home field advantage' in that situation. This however mean we didn't exactly need specific thresholds in our cleaning. 

  ### Did you implement any mechanism to clean your data? If so, what did you do?

    Most of our cleaning involved going through the data and manually checking for certain attributes to fix or remove. For example, we removed all games with ties in the mls, removed data that was pre-2002, removed certain stadiums that were 'home teams' non-home stadiums, and checked edge cases and stadium and city switches. While those were manual checks, we also created a home wins column for most of the leagues. To fill it in, we had to check scores in individual games which was also an involved process/mechanism. To complete these tasks we simply used pandas and python operations including replace and conditionals.
      
  ### Are there any missing values? Do these occur in fields that are important for your project's goals?

      We are missing some values for capacity and attendance. We have attendance when we don't have capacity and vice-versa. Some games and stadiums are missing both attendance and capacity, respectively. We haven't yet decided how we want to treat this data. This issue is particularly important for our project's goals because we are trying to determine the relationships between the features of home stadiums and home field advantages. If data is missing, or if the data we have isn't consistent across games and sports, it may be difficult to find the true relationships, especially if capacity isn't a good proxy for attendance and visa-versa.

  
  ### Are there duplicates? Do these occur in fields that are important for your project's goals?

      We have cleaned the data so that there are no duplicates in any of the three tables.
  
  ### How is the data distributed? Is it uniform or skewed? Are there outliers? What are the min/max values? (focus on the fields that are most relevant to your project goals)

      From our data it is difficult to see the distribution. Because we want to compare home field advantage across a number of different factors, the most useful design is to not include rate summaries, instead just recording results. These results don't have a distribution that can easily be found, as they will simply favor better teams. 

  ### Are there any data type issues (e.g. words in fields that were supposed to be numeric)? Where are these coming from? (E.g. a bug in your scarper? User input?) How will you fix them?

      Some values for capacity are ints, and others are strings of the form ("xx,xxx"). This is the case for two reasons: Firstly, some of the initial datasets differ in the way that they represent this capacity figure. Additionally, we had to manually input some of the capacity data using excel, which lead to some discrepencies in the way in which capacity is represented. This should be an quick fix that consists of converting all the values in the "capacity" column to values of type int. 

      Other than that, we have not noticed any other data type issues (we made sure to eliminate all those we could detect these in our data cleaning/merging).

  ### Do you need to throw any data away? What data? Any reason this might affect the analyses you are able to run or the conclusions you are able to draw?

      As mentioned previously, we may need to discard the games in our game table in which we don't have data for attendance and capacity. This will lower the number of games we have and may be significant, but this approach may be a way to avoid more significant error in our analysis. Having capacity and attendence numbers be inconsistent may prevent us from drawing accurate relationships between stadium/game fan involvement and success on the field. We throw data away for games that are tied in soccer, because ties largely do not exist in any of the other sports leagues. This shouldn't be an issue as ties can be removed while still allowing the true effect of playing at home to be seen with wins and losses. 

## Summarize any challenges or observations you hav emade sing collecting your data. Then, discuss your next steps and how your data collection has impact the type of analysis your will perform.

      The main challenges were due to the inconsistencies across games and stadium data. Teams often moved stadiums or played games in other stadiums than their home ones due to renovations or playoffs. We had to adjust for these changes. Additionally, we had to often perform manual calculations or checks to get consistent data across leagues. This entailed deriving a home wins column by calculating scores, or checking where stadiums were located to determine if a team was actually in their home stadium. We still have the challenge of determining how to deal with inconsistent attendance and capacity data which was touched on earlier in the writeup, and this will be important for our analysis. Addressing these challenges will ultimately allow us to accurately find the relationships or lack of between home-field advantage and factors like city and fan involvement, because these attributes are accurately labeled in the data. Our next steps involve looking at the averages of home wins across time and factors like sport, attendance/capacity, and city, hopefully uncovering interesting relationships. 

  




