import pandas as pd

def merge_cities_teams():
    # Read the cities and teams CSV files into pandas DataFrames
    cities_df = pd.read_csv('./cities.csv')
    teams_df = pd.read_csv('../data_deliverable/Data/full_data/teams_cleaned_final.csv')

    # Merge the DataFrames based on the team's city
    merged_df = pd.merge(teams_df, cities_df, left_on='city', right_on='city', how='left')

    merged_df = merged_df.drop_duplicates()

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv('../data_deliverable/Data/full_data/full_city_final_data.csv', index=False)


def main():
    # Call the function to merge the cities and teams data
    merge_cities_teams()


if __name__ == '__main__':
    main()