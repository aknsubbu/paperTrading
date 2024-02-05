import json
from random import randint, uniform
from datetime import datetime, timedelta

def generate_records():
    records = []
    symbols = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB", "NVDA", "PYPL", "ADBE", "INTC", "CSCO", "NFLX", "CMCSA", "PEP", "COST", "TMUS", "AVGO", "TXN", "QCOM", "SBUX" ]

    for i in range(1, 101):
        user_id = f"user_{str(i).zfill(3)}"
        symbol = symbols[randint(0, len(symbols) - 1)]
        qty = randint(5, 30)
        avg_price = round(uniform(100, 3000), 2)
        created_at = datetime.utcnow() - timedelta(days=randint(1, 365), hours=randint(1, 24))
        updated_at = created_at + timedelta(hours=randint(1, 24))
        delete_at = None  # Assuming initially records are not deleted

        record = {
            "user_id": user_id,
            "stocks": [
                {
                    "symbol": symbol,
                    "quantity": qty,
                    "avg_price": avg_price,
                    "created_at": created_at.isoformat() + "Z",
                    "updated_at": updated_at.isoformat() + "Z",
                    "delete_at": delete_at,
                    "sold?": False
                }
            ]
        }

        records.append(record)

    return records

# Generate records
generated_records = generate_records()

# Save records to a JSON file
with open("stock_records.json", "w") as json_file:
    json.dump(generated_records, json_file, indent=2)

print("Records generated and saved to stock_records.json")
