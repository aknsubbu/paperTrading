import json
from random import uniform
from datetime import datetime, timedelta

def generate_balance_records(num_records):
    records = []

    for i in range(1, num_records + 1):
        user_id = f"user_{str(i).zfill(3)}"
        balance = round(uniform(1000, 10000), 2)
        created_at = datetime.utcnow() - timedelta(days=i, hours=i)
        updated_at = created_at + timedelta(hours=i)

        record = {
            "user_id": user_id,
            "balance": balance,
            "created_at": created_at.isoformat() + "Z",
            "updated_at": updated_at.isoformat() + "Z",
        }

        records.append(record)

    return records

# Generate records
generated_records = generate_balance_records(100)

# Save records to a JSON file
with open("balance_records.json", "w") as json_file:
    json.dump(generated_records, json_file, indent=2)

print("Records generated and saved to balance_records.json")
