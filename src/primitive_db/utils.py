import json
import os


def load_metadata(filepath):
    """Load metadata from JSON file. Return empty dict if file not found."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Save metadata to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_table_data(table_name):
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]

        value = value_func()
        cache[key] = value
        return value

    return cache_result

