import requests
import json
import pandas as pd

API_URL = "https://golf.se/api/golf/clubs"

def get_all_courses():
    r = requests.get(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()
    clubs = data["clubs"]

    courses = []
    for club in clubs:
        # Hämta adress om den finns
        addresses = club.get("Addresses", [])
        address = addresses[0] if addresses else {}

        # Hämta email om den finns
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

    return courses

if __name__ == "__main__":
    courses = get_all_courses()

    # Spara som JSON
    with open("data/courses_raw.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    # Spara som CSV också
    df = pd.DataFrame(courses)
    df.to_csv("data/courses_clean.csv", index=False, encoding="utf-8")

    print(f"Sparade {len(courses)} klubbar")
    print(df.head())