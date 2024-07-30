from datetime import datetime, timedelta
import random
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://user:hihi123!@dev-gcp-tunnel.u0j98ms.mongodb.net/?retryWrites=true&w=majority&appName=dev-gcp-tunnel')
db = client['sample_tbm']  
collection = db['rings_per_shift']  

def generate_dummy_data(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Shift time 7am - 7pm
    start_of_ds = date_obj.replace(hour=7, minute=1, second=0)
    end_of_ds = date_obj.replace(hour=19, minute=0, second=0)

    # Shift time 7pm - 7am
    start_of_ns = date_obj.replace(hour=19, minute=1, second=0)
    end_of_ns = date_obj.replace(hour=7, minute=0, second=0)
    night_rb = random.randint(1, 10) 
    day_rb = random.randint(1, 10)
    return {
        "date": date_str,
        "startDs": start_of_ds,
        "endDs": end_of_ds,
        "startNs": start_of_ns,
        "endNs": end_of_ns,
        "nightRb": night_rb,
        "dayRb": day_rb
    }

# Generate dummy data for each day from January to May 2024
start_date = datetime(2024, 6, 1)
end_date = datetime(2025, 12, 31)
delta = timedelta(days=1)
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    dummy_data = generate_dummy_data(date_str)
    collection.insert_one(dummy_data)
    print("Insert 1 document")
    current_date += delta
    print(current_date)

print("Dummy data insertion complete.")
