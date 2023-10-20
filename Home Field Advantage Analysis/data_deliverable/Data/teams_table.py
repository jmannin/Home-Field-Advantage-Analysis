import pandas as pd

teams_df = pd.read_csv('./full_data/teams_cleaned_final.csv')

unique_cities = teams_df['city'].unique() # Get a list of unique cities
print(unique_cities)

data = {'city': unique_cities, 'elevation (ft)': None, 'median household income ($)': None}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('city_data.csv', index=False)

# Median household income:  2017-2021 (generalizing back to 2003 because it doesn't change much), data from census.gov 
# Elevation: using wolfram alpha 

# cities_df = pd.DataFrame({'city': unique_cities}) # Create a new df with "city" column; fill with unique cities

# # Add columns for elevation and gdp (set to None for now)
# cities_df['elevation (ft)'] = None


# # Print the new DataFrame
# print(cities_df)
