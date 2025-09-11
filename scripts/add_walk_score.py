# this script queries the walk score API to get walk score for a given latitude and longitude
# the script takes in a csv file with latitude and longitude and returns the walk score for each location
# the script writes the output to a csv file

import requests
import pandas as pd

# function to get walk score for a given latitude and longitude
def get_walk_score(lat, lon):
    # set the API key
    api_key = "88f7b3d9d15049cc647ba74651545545"
    # set the API url
    url = "http://api.walkscore.com/score?format=json&lat=" + str(lat) + "&lon=" + str(lon) + "&wsapikey=" + api_key
    # make the API call
    response = requests.get(url)
    # parse the response
    data = response.json()
    print(data)
    
    if data['status'] != 1:
        print('Error: ', data['status'])
        return [0, 'not found']
    else:
        # get the walk score
        walk_score = data['walkscore']
        description = data['description']
        return [walk_score, description]

def get_transit_score(lat, lon, city):
    print(city)
    # set the API key
    api_key = "88f7b3d9d15049cc647ba74651545545"
    # set the API url
    url = "https://transit.walkscore.com/?lat=" + str(lat) + "&lon=" + str(lon) + "&city=" + str(city) + "&state=VT" + "&wsapikey=" + api_key
    # make the API call
    response = requests.get(url)
    
    try:
        # parse the response
        data = response.json()
        # get the walk score
        transit_score = data['transit_score']
        description = data['description']
        return [transit_score, description]
        
    except:
        print('Error: ', response)
        return [0, 'not found']
    
    
    

# load the input csv file
df = pd.read_csv('public/data/tdm.csv')

# create a new column to store the walk score
df['walk_score'] = 0
df['transit_score'] = 0
df['transit_description'] = ''
# create column wor walk description
df['walk_description'] = ''

city_col = 'MUNICIPALITY (alphabetical by county)'

# iterate through the rows of the dataframe
for index, row in df.iterrows():
    # get the latitude and longitude
    lat = row['LAT']
    lon = row['LON']
    # get the walk score
    # walk_scores = get_walk_score(lat, lon)
    
    # update the walk score in the dataframe
    # df.at[index, 'walk_score'] = walk_scores[0]
    # df.at[index, 'walk_description'] = walk_scores[1]
    print(row[city_col])
    # get transit score
    transit = get_transit_score(lat, lon, row[city_col])
    df.at[index, 'walk_score'] = transit[0]
    
# write the output to a csv file
df.to_csv('data/tdm_transits.csv', index=False)