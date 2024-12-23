import pandas as pd
goalscorers_df = pd.read_csv('goalscorers.csv')
results_df = pd.read_csv('results.csv')
shootouts_df = pd.read_csv('shootouts.csv')

#Cleaning Data
#Checking for duplicates
has_duplicates_goalscorers = goalscorers_df.duplicated().any()
has_duplicates_results = results_df.duplicated().any()
has_duplicates_shootouts = shootouts_df.duplicated().any()

print("Dataframes with duplicates are true.","Goalscorers: ",has_duplicates_goalscorers,", Results: ", has_duplicates_results, ", Shootouts: " , has_duplicates_shootouts)

# Adding a column to check which rows have duplicates in goalscorers
goalscorers_df['is_duplicated'] = goalscorers_df.duplicated(keep=False)
print("\n\n Goalscorers Table with Duplicated Column")
print(goalscorers_df)

#Removing duplicated results from goalscorers
goalscorers_df.drop_duplicates(inplace=True)

#Check if it still has any duplicates
has_duplicates_goalscorers = goalscorers_df.duplicated().any()
print("\n\nCheck if goalscorers still has any duplicates:",has_duplicates_goalscorers)

#Query 1
#Filters out the date then uses lambda to calculate the average goals per game from 1900-2000
target_years = results_df[(results_df['date'] >= '1900-01-01') & (results_df['date'] <= '2000-12-31')].assign(average_score = lambda x: x[['home_score', 'away_score']].mean(axis=1))
print("\n\n Query 1 Table, Average Number of Goals per Game Between 1900 and 2000")
print(target_years[['date','home_score','away_score','average_score']])

#Query 2
#Counts how many times each winner
shootout_wins = shootouts_df['winner'].value_counts().sort_index(ascending = True)
print("\n\n Query 2 Table, Counts The Number of Shootout Wins per Country In Alphabetic Order")
print(shootout_wins)

#Query 3
#Merges the date, home team, and away team because they're the same across all three datasets. Used inner to help ensure reliability of the key
merge_results_and_goalscorers = pd.merge(results_df,goalscorers_df, on=['date', 'home_team', 'away_team'], how='inner')
merge_final = pd.merge(merge_results_and_goalscorers, shootouts_df, on=['date', 'home_team', 'away_team'], how='inner')
print("\n\n Task 3, Create A Reliable Key For Joining All Three Tables")
print(merge_final)

#Query 4
#Using the the key from the previous query to make it easier
penalty_winner = merge_final[(merge_final['home_score'] == merge_final['away_score'])]
print("\n\n Query 4, Identify which teams won a penalty shootout after a 1-1 draw")
print(penalty_winner[['date', 'home_team', 'away_team', 'winner']])

#Query 5
# Counts the goal for each scorer in each tourney,
top_scorer = merge_final.groupby('tournament')['scorer'].value_counts().reset_index(name='score_count')
# Then it looks for the top scorer in each tourney,
top_scorer_per_tourney = top_scorer.loc[top_scorer.groupby('tournament')['score_count'].idxmax()]
# Calculates the total goals per tourney,
total_goals_by_tourney = merge_final.groupby('tournament')['scorer'].count().reset_index(name='total_goals')
# Merges total points with the top scorer's data,
top_scorer_with_total = pd.merge(top_scorer_per_tourney, total_goals_by_tourney, on='tournament')
# Used lambda to assign the percentage calculator,
top_scorer_with_total['percentage'] = top_scorer_with_total.apply(lambda row: (row['score_count'] / row['total_goals']) * 100, axis=1)
print("\n\n Query 5, Identify the top goal scorer per tournament and percantage of their goal compared to the rest of the goals in the tournament")
print(top_scorer_with_total[['tournament', 'scorer', 'score_count', 'total_goals', 'percentage']])
