import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import time

geolocator = Nominatim(user_agent="tdm-transit-geocoder")

failed_lookup = []

def geocode_with_retry(geolocator, query, retries=1, delay=2):
    for attempt in range(retries):
        try:
            return geolocator.geocode(query, timeout=10)
        except GeocoderUnavailable:
            print(f"Geocoder unavailable. Retrying ({attempt + 1}/{retries})...")
            time.sleep(delay)
        except Exception as e:
            print(f"Error during geocoding attempt {attempt + 1}: {e}")
            time.sleep(delay)
    print(f"Failed to geocode after {retries} attempts: {query}")
    return None

# load the data
projects = pd.read_csv('data/tdm-data-20250911.csv', encoding='latin1')
# Filter out rows where 'ADDRESS OF PROJECT TO MAP' is missing or NaN
filtered_projects = projects[projects['ADDRESS OF PROJECT TO MAP'].notnull() & (projects['ADDRESS OF PROJECT TO MAP'].astype(str).str.strip() != '')].copy()

total_geocoded = 0
failed_geocoded = 0

# if value for "ADDRESS OF PROJECT TO MAP" is "NaN" or null or empty, then replace with "CITY"
projects['ADDRESS TO SEARCH'] = projects['ADDRESS OF PROJECT TO MAP'].fillna('CITY'+', VT, USA')


# for every value in failed_lookup, geocode the institution name
for idx, (index, row) in enumerate(filtered_projects.iterrows()):
    place = row['ADDRESS OF PROJECT TO MAP']
    try:
        location = geocode_with_retry(geolocator, place, retries=3, delay=2)
        if location:
            print(f"[{idx+1}/{len(filtered_projects)}] Geocoded: {place} -> Lat: {location.latitude}, Lon: {location.longitude}")
            filtered_projects.at[index, 'LON'] = location.longitude
            filtered_projects.at[index, 'LAT'] = location.latitude
            total_geocoded += 1
        else:
            print(f"[{idx+1}/{len(filtered_projects)}] {str(place)} not found.")
            failed_geocoded += 1
    except Exception as e:
        print(f"[{idx+1}/{len(filtered_projects)}] Error geocoding {str(place)}: {e}")
        failed_geocoded += 1
    # Rate limiting: wait 1 second between requests
    time.sleep(1)

print(f"Geocoded {total_geocoded} places")
print(f"Failed to geocode {failed_geocoded} places")
# Always save the updated survey dataframe to a new csv file
try:
    filtered_projects.to_csv('data/tdm-20250911-geocoded.csv', index=False, encoding='latin1')
    print("Geocoding complete. Updated survey data saved to 'data/tdm-20250911-geocoded.csv'.")
except Exception as e:
    print(f"Error saving CSV: {e}")
