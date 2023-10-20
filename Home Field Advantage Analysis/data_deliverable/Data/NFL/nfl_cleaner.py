import pandas as pd 
import numpy as np

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

teams_to_locations = {
    'Giants': 'New York, New York',
    'Bills': 'Buffalo, New York',
    'Bears': 'Chicago, Illinois',
    'Bengals': 'Cincinnati, Ohio',
    'Browns': 'Cleveland, Ohio',
    'Packers': 'Green Bay, Wisconsin',
    'Titans': 'Nashville, Tennessee',
    'Dolphins': 'Miami, Florida',
    'Commanders': 'Washington, D.C.',
    'Panthers': 'Charlotte, North Carolina',
    'Jaguars': 'Jacksonville, Florida',
    'Broncos': 'Denver, Colorado',
    'Raiders': 'Las Vegas, Nevada',
    'Buccaneers': 'Tampa Bay, Florida',
    'Texans': 'Houston, Texas',
    'Patriots': 'Foxborough, Massachusetts',
    'Falcons': 'Atlanta, Georgia',
    'Cowboys': 'Dallas, Texas',
    'Colts': 'Indianapolis, Indiana',
    'Chiefs': 'Kansas City, Missouri',
    'Saints': 'New Orleans, Louisiana',
    'Jets': 'New York, New York',
    'Ravens': 'Baltimore, Maryland',
    'Rams': 'Los Angeles, California',
    'Seahawks': 'Seattle, Washington',
    'Vikings': 'Minneapolis, Minnesota',
    'Chargers': 'Los Angeles, California',
    '49ers': 'San Francisco, California',
    'Steelers': 'Pittsburgh, Pennsylvania',
    'Eagles': 'Philadelphia, Pennsylvania',
    'Cardinals': 'Phoenix, Arizona',
    'Lions': 'Detroit, Michigan'
}

teams_to_full_name = {
    'Giants': 'New York Giants',
    'Bills': 'Buffalo Bills',
    'Bears': 'Chicago Bears',
    'Bengals': 'Cincinnati Bengals',
    'Browns': 'Cleveland Browns',
    'Packers': 'Green Bay Packers',
    'Titans': 'Tennessee Titans',
    'Dolphins': 'Miami Dolphins',
    'Commanders': 'Washington Commanders',
    'Panthers': 'Carolina Panthers',
    'Jaguars': 'Jacksonville Jaguars',
    'Broncos': 'Denver Broncos',
    'Raiders': 'Las Vegas Raiders',
    'Buccaneers': 'Tampa Bay Buccaneers',
    'Texans': 'Houston Texans',
    'Patriots': 'New England Patriots',
    'Falcons': 'Atlanta Falcons',
    'Cowboys': 'Dallas Cowboys',
    'Colts': 'Indianapolis Colts',
    'Chiefs': 'Kansas City Chiefs',
    'Saints': 'New Orleans Saints',
    'Jets': 'New York Jets',
    'Ravens': 'Baltimore Ravens',
    'Rams': 'Los Angeles Rams',
    'Seahawks': 'Seattle Seahawks',
    'Vikings': 'Minnesota Vikings',
    'Chargers': 'Los Angeles Chargers',
    '49ers': 'San Francisco 49ers',
    'Steelers': 'Pittsburgh Steelers',
    'Eagles': 'Philadelphia Eagles',
    'Cardinals': 'Arizona Cardinals',
    'Lions': 'Detroit Lions'
}

def to_state_full_name(x):
  city_state = x.split(", ")
  full_name = states[city_state[1]]
  return city_state[0] + ', ' + full_name

def team_to_city(team):
  return teams_to_locations[team]

def handle_team_changes(team, date, city):
  date_arr = date.split('-')
  if team == 'Raiders':
    if int(date_arr[0]) < 2020 or  (int(date_arr[0]) == 2020 and int(date_arr[1]) < 4):
      return 'Oakland, California'
    else:return city
  elif team == 'Chargers':
    if int(date_arr[0]) < 2017 or (int(date_arr[0]) == 2017 and int(date_arr[1]) < 4):
      return 'San Diego, California'
    else: return city
  elif team == 'Rams':
    if int(date_arr[0]) < 2016 or (int(date_arr[0]) == 2016 and int(date_arr[1]) < 4):
      return 'St. Louis, Missouri'
    else: return city
  else:
    return city
  
def handle_team_name_changes(team, city):
  if team == 'Raiders' and city == 'Oakland, California':
    return 'Oakland Raiders'
  elif team == 'Chargers' and city == 'San Diego, California':
    return 'San Diego Chargers'
  elif team == 'Rams' and city == 'St. Louis, Missouri':
    return 'St. Louis Rams'
  else: 
    return teams_to_full_name[team]
  
def handle_stadium_changes(row):
  team = row['home_team_name']
  date = row['date']
  date_arr = date.split('-')
  if team == 'Atlanta Falcons':
    if int(date_arr[0]) < 2017 or (int(date_arr[0]) == 2017 and int(date_arr[1]) < 4):
      row['stadium_name'] = 'Georgia Dome'
      row['capacity'] = "71,250"
    return row
  elif team == 'Dallas Cowboys':
    if int(date_arr[0]) < 2009 or (int(date_arr[0]) == 2009 and int(date_arr[1]) < 4):
      row['stadium_name'] = 'Texas Stadium'
      row['capacity'] = "65,675"
    return row
  elif team == 'Indianapolis Colts':
    if int(date_arr[0]) < 2008 or (int(date_arr[0]) == 2008 and int(date_arr[1]) < 4):
      row['stadium_name'] = 'RCA Dome'
      row['capacity'] = "65,675"
    return row
  elif team == 'San Francisco 49ers':
    if int(date_arr[0]) < 2014 or (int(date_arr[0]) == 2014 and int(date_arr[1]) < 4):
      row['stadium_name'] = 'Candlestick Park'
      row['capacity'] = "69,732"
    return row
  elif team == 'Los Angeles Chargers':
    if int(date_arr[0]) < 2020 or (int(date_arr[0]) == 2020 and int(date_arr[1]) < 4):
      row['stadium_name'] = 'StubHub Center'
      row['capacity'] = "27,000"
    return row
  elif team == 'Minnesota Vikings':
    if int(date_arr[0]) < 2016 or (int(date_arr[0]) == 2016 and int(date_arr[1]) < 4):
      row['stadium_name'] = 'Mall of America Field'
      row['capacity'] = "64,111"
    return row
  else:
    return row

# RAIDERS (2020 fall), CHARGERS (2017 fall), RAMS (2016 fall)

df_games_raw = pd.read_csv('./raw/games.csv', usecols=['date', 'away', 'home', 'score_away', 'score_home'])
df_stadiums_raw = pd.read_csv('./raw/stadiums.csv', usecols=['stadium_name', 'stadium_location', 'stadium_open',
                                                           'stadium_close', 'stadium_capacity'], encoding='ISO-8859-1')
df_stadiums_raw2 = pd.read_csv('./raw/stadium_info_cleaned.csv')

# drop rows where stadium_open and stadium_close are both NaN
df_stadiums = df_stadiums_raw.dropna(subset=['stadium_open', 'stadium_close'], how='all')

# drop rows where stadium_close < 2003
condition = (df_stadiums['stadium_close'] >= 2003) | (df_stadiums['stadium_close'].isna())
df_stadiums = df_stadiums[condition]

condition = (df_stadiums['stadium_location'] == 'London, UK') | (df_stadiums['stadium_location'] == 'Mexico City, Mexico')
df_stadiums = df_stadiums[~condition]

df_stadiums['stadium_location'] = df_stadiums['stadium_location'].apply(to_state_full_name)
df_stadiums = df_stadiums.rename(columns={'stadium_location': 'city'})

df_games_raw['city'] = df_games_raw['home'].apply(team_to_city)


  
df_games_raw['city'] = df_games_raw.apply(lambda row: handle_team_changes(row['home'], 
                  row['date'], row['city']), axis=1) # handle team location changes (edge cases)
df_games_raw['home'] = df_games_raw.apply(lambda row: handle_team_name_changes(row['home'],
                  row['city']), axis=1) # change to full team name
df_games_raw['away'] = df_games_raw.apply(lambda row: handle_team_name_changes(row['away'],
                  row['city']), axis=1) # chantg to full team name


# new table stadium names
# stadium_names = pd.DataFrame(df_stadiums[['stadium_name', 'stadium_open', 'stadium_close']])
# for manual cleaning
# stadium_names.to_csv('stadium_names.csv', index=False)

df_stadiums2 = df_stadiums_raw2.merge(df_stadiums[['stadium_capacity', 'stadium_name']], on='stadium_name')

# update missing capacities
df_stadiums2.loc[df_stadiums2['stadium_name']== 'Edward Jones Dome', 'stadium_capacity'] = 66965


df_games_raw['home_wins'] = df_games_raw.apply(lambda row: 1 if row['score_home'] > row['score_away'] else 0, axis=1)
df_games = df_games_raw.merge(df_stadiums2[['team_name', 'stadium_name', 'stadium_capacity']], 
                                  left_on='home', right_on='team_name')
df_games = df_games.rename(columns={'home': 'home_team_name', 'stadium_capacity': 'capacity', 'away': 'away_team_name'})
df_games = df_games.drop(['team_name', 'score_away', 'score_home'], axis=1)

df_games.loc[df_games['stadium_name']== 'Edward Jones Dome', 'stadium_capacity'] = 66965

df_games['attendance'] = np.nan 
df_games['league'] = 'NFL' # add sport column

df_games[['date', 'home_team_name', 'stadium_name', 'capacity']] = df_games[['date', 'home_team_name', 'stadium_name', 'capacity']].apply(lambda row: handle_stadium_changes(row), axis=1)

# change from year-month-day to just year 
df_games['date'] = df_games["date"].str.replace("-.*", "", regex=True)
df_games = df_games.rename(columns={'date': 'year'})


df_games_cleaned = df_games[['home_team_name', 'away_team_name', 'home_wins', 'year', 'stadium_name', 'city', 'attendance', 'capacity', 'league']] 
df_games_cleaned_sample = df_games_cleaned.sample(n=100)

df_games_cleaned.to_csv('./clean/full/games.csv', index=False)
df_games_cleaned_sample.to_csv('./clean/sample/games_sample.csv', index=False)

print(df_games_cleaned[:10])

