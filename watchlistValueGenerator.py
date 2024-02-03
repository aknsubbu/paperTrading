import json
from random import randint
from datetime import datetime, timedelta

def generate_watchlist_records(num_records=100):
    symbols = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB", "NVDA", "PYPL", "ADBE", "INTC"]

    watchlist_records = []

    for _ in range(num_records):
        user_id = f"user_{str(_).zfill(3)}"
        symbol = symbols[randint(0, len(symbols) - 1)]
        created_at = datetime.utcnow() - timedelta(days=randint(1, 365), hours=randint(1, 24))

        watchlist_item = {
            "user_id": user_id,
            "symbols": [symbol],
            "created_at": created_at.isoformat() + "Z"
        }

        watchlist_records.append(watchlist_item)

    return watchlist_records

# Example usage
watchlist_records = generate_watchlist_records( num_records=100)

# Save records to a JSON file
with open("watchlist_records.json", "w") as json_file:
    json.dump(watchlist_records, json_file, indent=2)

print("Watchlist records generated and saved to watchlist_records.json")
