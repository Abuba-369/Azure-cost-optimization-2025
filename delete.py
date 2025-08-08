# Azure Function: Delete old records from Cosmos DB after export

from azure.cosmos import CosmosClient, exceptions
import os
import json

# Cosmos DB configuration (same as before)
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
CONTAINER_NAME = os.environ["CONTAINER_NAME"]

def main(mytimer):
    # Assume 'moved_ids.json' blob holds a list of already exported record IDs
    # Alternatively, if using a queue, process dequeue here

    # For illustration, assume you have the moved_ids loaded:
    from azure.storage.blob import BlobServiceClient
    BLOB_CONN_STR = os.environ["BLOB_CONN_STR"]
    BLOB_CONTAINER = os.environ["BLOB_CONTAINER"]
    MOVED_IDS_BLOB = os.environ.get("MOVED_IDS_BLOB", "moved_ids.json")

    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    blob_container = blob_service.get_container_client(BLOB_CONTAINER)
    blob_client = blob_container.get_blob_client(MOVED_IDS_BLOB)
    moved_ids = json.loads(blob_client.download_blob().readall())

    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.get_database_client(DATABASE_NAME)
    container = db.get_container_client(CONTAINER_NAME)

    for record_id in moved_ids:
        try:
            # Use correct partition key if needed, e.g., partition_key=record_id or another field
            container.delete_item(item=record_id, partition_key=record_id)
        except exceptions.CosmosHttpResponseError as e:
            print(f"Failed to delete record {record_id}: {e}")
  
