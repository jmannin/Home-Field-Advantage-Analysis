# Home-Field-Advantage-Analysis

This was a final project for Brown University course cs1951A: Data Science taught by professor Lorenzo Di stefani.
<br />
The original group repository for this project is marked private. Thus for illustrative purposes, the contents have been imported to this repository.
<br />
<br />
In addition to myself, credit should be attributed to the following group members:
<br />
nicolasperez19
<br />
zaultavangar
<br />
typhamswann
<br />


Three hypotheses:
<br />
<br />
**Hypothesis**: There is a significant difference in the mean home win percentages between the five major US leagues—we expect the MLS to have the highest home win percentage.
<br />
**Method**: Our goal is calculate each team's home win percentage over all the data. Then we plan on using an ANOVA (Analysis of Variance) test to quantify and eventually visualize the variance in home win percentage across the five leagues. We deem this test is appropriate because it allows us to compare the means of a continuous variable (the home win percentage) across multiple groups (the leagues) simultaneously and determine if there are significant differences among them. 
<br>
**Result**: F-statistic: 11.4046, p-value: 4.2751e-08; reject the null hypothesis—there is evidence to suggest that the home field win percentages across the 5 leagues are significantly different. 
<br />
**Significance**: The f-statistic measures the ratio of the between-group variability to the within-group variability. A ratio of 11.4046 is quite large, suggesting there is a significant difference in the home win percentages across the 5 leagues. The p-value is the probability of observing such an f-statistic if the null hypothesis is true. As our p-value is very small, we can therefore conclude that there is evidence to suggest that the home win percentages across the 5 leagues are significantly different. For a visualization of this difference, please see the boxplot in our visualizations folder. 
<br>
<br>
**Hypothesis**: Teams that play in higher elevation regions have a higher home field win percentage.
<br />
**Method**: To test this hypotheis we plan on using a t-test. We plan on splitting the data based on a threshold (1000 ft) to produce one group that plays in higher elevation areas and another that plays in lower elevation areas. This makes the t-test appropriate given the two independent groups and our continuous variable (the home win percentage). The metric being tested will be the difference in home field win percentage betwen the two groups. If the t-test confirms statistical significance, we will reject the null hypothesis.
<br />
**Result**: t-statistic: 0.1082, p-value: 0.9139; accept the null hypothesis—there is not enough evidence to suggest that there is a significant difference in home field win percentages betwen teams playing in higher elevation areas and teams playing in lower elevation areas.
<br />
**Significance**: The t-statistic measures the difference in home win percentages betwen the high and low elevation groups, relative to the variability within each group. Our t-statistic, 0.1082, is close to zero, therefore suggesting that there is little difference in the home win percentages between teams playing in higher elevation areas and teams playing in lower elevation areas. The p-value, the probability of observing such a t-statistic if the null hypothesis were true, is very high, at 0.9139, suggesting that the observed difference in home win percentages between the two groups is not statistically significant. For the final deliverable, we plan on modifying this test by producing a more extreme split between the low and high elevation groups. With our current split, it doesn't make sense for a team that plays 1001ft and a team that plays at 999ft to be in different groups. Perhaps we can sacrifice data from some teams to create a larger elevation gap between the two groups (e.g. teams at elevations greater than 4000 ft and teams at elevations less than 2000ft). 
<br>
<br>
**Hypothesis**: Attendance is positively correlated with home field win percentage.
<br />
**Method**: To test this hypothesis we will look for correlation rather than difference between two groups. Therefore we deem a Pearson correlation test appropriate to check for statistical significance to reject the null hypothesis. Our plan is to take our entire dataset of games and attendance data for those games. Note that 3 of the leagues don't have attendance data, so we will only be using the games with attendance data from the MLS and the MLB (this is still more than enough data). 
<br>
**Result**: Pearson correlation coefficient: 0.1171, p-value: 1.8701e-44; reject the null hypothesis—there is evidence to suggest a positive, but very weak correlation between attendance and home field win percentage. 
<br>
**Significance**: The correlation coefficent measures the strength and direction of the linear relationship between the two variables. Our result of 0.1171 suggest a positive, but weak correlation between attendance and home field win percentage. Our very small p-value of 1.8701e-44 suggests that the observed correlation between attendance and home field win percentage is statistically significant. We can conclude that as attendance increases, there is a tendency for the home field win percentage to increase, but the strength of this relationship is not very strong. 
<br />
<br />
<br />
Machine Learning Components:
<br />
<br />
Clustering Analysis (KMeans)
<br/>
**Hypothesis**: Clustering major U.S sports teams based on home win percentage and environmental factors leads to high silhouette scores, and thus clearly distinguishable categorical groups.
<br/>
**Method**: To investigate this hypothesis, we tried to cluster the U.S major sports teams based on home win percentage and environmental factors (such as elevation and median regional income) using KMeans clustering. We iterated through different KMeans models using different k values and picked the optimal k value that would produce the maximal silhouette score. 
<br/>
**Result**:  By clustering the major sports teams into 5 different groups, we found that the silhouette score was 0.59
<br/> 
**Significance**: Since the silhouette score was between 0 and 1, this indicated that the major sports teams could be categorized into clearly distinguishable groups given home win percentage and environmental features.
<br />
<br />
Decision Trees
<br />
**Purpose**: Simulate results in a sports league of teams with randomly assigned stadium characteristics
<br />
**Reasoning**: Using decision trees for predicting game outcomes will help identify which factors are most important in determining the outcome of a game. We have a few variables we believe can impact a game in favor of the home field team. By studying the architecture of the decision tree we can determine which variables are the most impactful on league outcomes.
<br />
**Metric**: We will lean most heavily on F-score, as in, whether or not the prediction can hold up given real game data.
<br />
<br />
What challenges did you face evaluating the model?
<br />
<br />
Before evaluating our models, we expect to struggle with overfitting/underfitting or biased data, especially with our decision tree. We have difficulty with overfitting and/or underfitting from our decision tree machine learning model as the data we are using to predict home field wins may poorly capture the full effect of all possible variables on home field advantage. One important consideration is to train the model in such a way where it does not latch onto one variable as its main predictor.
<br />
<br />
Did you have to clean or restructure your data?
<br />
<br />
Our group has performed extensive cleaning and restructuring for our data. This included cleaning/restructuring on ‘02-’22 game data for each individual sports league included in the test. Some restructuring had to be done to join certain tables together (for example, joing the games and teams table based on where the home_team_id in games equals the team_id in teams). Additionally, specific variables such as stadium elevation and average regional income were scraped from alternative sources and packaged into table data for the current analysis. This was added for machine learning component purposes as we needed more variables to make useful predictions.
<br>
<br>
Did you find the results corresponded with your initial belief in the data? If yes/no, why do you think this was the case?
<br>
<br>
The main result, that the MLS offers the most significant home field advantage, correponded with our initial belief in the data. This may be because there is generally less of an away fan presence at MLS games, and these games are treated more like actual sports events than some of the entertainment-focused events in the NBA or NFL. However, we were expecting elevation and attendance to play a more major role in a team's success. 
<br>
<br>
Do you believe the tools for analysis that you chose were appropriate? If yes/no, why or what method could have been used?
<br>
<br>
Yes, we believe the tools for analysis that we chose were appropriate. Nevertheless, more attendance and elevation data may have made our last two tests more accurate.
<br>
<br>
Was the data adequate for your analysis? If not, what aspects of the data were problematic and how could you have remedied that?
<br>
<br>
Generally, yes, as we are dealing with a massive dataset of games across the five leagues. Although our project is specifically geared toward US teams and leagues, it would be interesting to perform the elevation and attendance tests with more teams from all around the world, to see if a pattern starts to form. 
