import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

df = pd.read_csv("data/courses_clean.csv")

geolocator = Nominatim(user_agent="golf-dashboard")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_coords(row):
    query = f"{row['name']}, {row['city']}, Sverige"
    try:
        location = geocode(query)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        pass
    return pd.Series([None, None])

print("Hämtar koordinater... (tar några minuter)")
df[['lat', 'lng']] = df.apply(get_coords, axis=1)

df.to_csv("data/courses_with_coords.csv", index=False, encoding="utf-8")
print(f"Klart! {df['lat'].notna().sum()} av {len(df)} klubbar fick koordinater")