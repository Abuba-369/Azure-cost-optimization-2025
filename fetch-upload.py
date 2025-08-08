# Azure Function: Export old records from Cosmos DB to Blob Storage

import os
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import json

# Cosmos DB configuration
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
CONTAINER_NAME = os.environ["CONTAINER_NAME"]

# Blob Storage configuration
BLOB_CONN_STR = os.environ["BLOB_CONN_STR"]
BLOB_CONTAINER = os.environ["BLOB_CONTAINER"]

def main(mytimer):
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.get_database_client(DATABASE_NAME)
    container = db.get_container_client(CONTAINER_NAME)

    # Query records older than cutoff date
    query = "SELECT * FROM c WHERE c.timestamp < @cutoff_date"
    params = [{"name": "@cutoff_date", "value": cutoff_date.isoformat() + "Z"}]
    records = list(container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))

    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    blob_container = blob_service.get_container_client(BLOB_CONTAINER)

    moved_ids = []
    for item in records:
        # Export each record as a separate blob (or batch them)
        blob_name = f"{item['id']}.json"
        blob_container.upload_blob(blob_name, json.dumps(item), overwrite=True)
        moved_ids.append(item['id'])

    # Optionally: Save moved_ids to another persistent store or queue for next process
