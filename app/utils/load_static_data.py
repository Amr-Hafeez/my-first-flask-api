import json


def load_static_data(language="en"):
    """Load static data from JSON files based on language"""
    # print("Logged to load static data")

    filename = f"app/data/static_data_{language}.json"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


static_arabic_data = load_static_data("ar")
static_english_data = load_static_data()
