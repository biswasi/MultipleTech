import os
from azure.cosmos import CosmosClient

def get_container():
    url = os.environ["COSMOS_ENDPOINT"]
    key = os.environ["COSMOS_KEY"]
    database_name = os.environ.get("COSMOS_DATABASE", "CustomerDB")
    container_name = os.environ.get("COSMOS_CONTAINER", "Customers")

    client = CosmosClient(url, credential=key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container
