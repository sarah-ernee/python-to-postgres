from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://dev:sgtunnel2024@dev-gcp-tunnel.u0j98ms.mongodb.net/?retryWrites=true&w=majority&appName=dev-gcp-tunnel')
source_db = client['sample_tbm']  
source_col = source_db['rings_per_shift']  

new_db = client['sample_tbm']  
new_col = new_db['tbm_sg_shifts'] 

documents = source_col.find()

for doc in documents:
    transformed_doc_opeb = {
        "date": doc["date"],
        "tunnel_drive_id": 1,
        "timestamp": doc["endNs"],
        "shift": {
            "day": {
                "start_time": doc["startDs"],
                "end_time": doc["endDs"],
                "rings_built": doc["dayRb"],
            },
            "night": {
                "start_time": doc["startNs"],
                "end_time": doc["endNs"],
                "rings_built": doc["nightRb"],
            }
        }
    }

    transformed_doc_opwb = {
        "date": doc["date"],
        "tunnel_drive_id": 2,
        "timestamp": doc["endNs"],
        "shift": {
            "day": {
                "start_time": doc["startDs"],
                "end_time": doc["endDs"],
                "rings_built": doc["dayRb"],
            },
            "night": {
                "start_time": doc["startNs"],
                "end_time": doc["endNs"],
                "rings_built": doc["nightRb"],
            }
        }
    }

    insert_list = [transformed_doc_opeb, transformed_doc_opwb]
    new_col.insert_many(insert_list)
    print("Document inserted for OPEB OPWB for", doc["date"])

print("Data migration completed")
