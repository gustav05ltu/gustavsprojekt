import requests
import json
import pandas as pd

API_URL = "https://golf.se/api/golf/clubs"

SKRAP = ['Payex', 'GDF', 'SM-veckan', 'Proffstour', 
         'Lettländska', 'Estländska', 'Litauiska', 'SGF']

def get_all_courses():
    r = requests.get(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()
    clubs = data["clubs"]

    courses = []
    for club in clubs:
        addresses = club.get("Addresses", [])
        address = addresses[0] if addresses else {}
        emails = club.get("Emails", [])
        email = emails[0].get("EmailAddress") if emails else None

        courses.append({
            "name": club.get("Name"),
            "region": address.get("Region"),
            "city": address.get("PostalAddress"),
            "postal_code": address.get("PostalCode"),
            "country": address.get("Country", "Sverige"),
            "email": email,
            "id": club.get("id"),
        })

    df = pd.DataFrame(courses)

    # Filtrera till Sverige
    df = df[df['country'].isna() | df['country'].str.contains('Sverige', na=False)]

    # Ta bort administrativa poster
    mask = ~df['name'].str.contains('|'.join(SKRAP), na=False)
    df = df[mask].reset_index(drop=True)

    return df

if __name__ == "__main__":
    df = get_all_courses()
    df.to_csv("data/courses_clean.csv", index=False, encoding="utf-8")
    print(f"Sparade {len(df)} klubbar till data/courses_clean.csv")
    print(df[['name', 'city']].head(10).to_string())