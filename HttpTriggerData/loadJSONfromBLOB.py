from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import json

try:
    connect_str = "DefaultEndpointsProtocol=https;AccountName=snowflakecalculatordata;AccountKey=2QlRyOr9e9UQagpZGxzKam3lp4vpU+pokDKDdqt63EgbGP5dCrWQhVKaqGCZJRHd8whE4nBl1meV+ASt5nncdA==;EndpointSuffix=core.windows.net"
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = "snowflakedata"
    blob_name = "SnowflakeCloudData.json"

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(

        container=container_name, blob=blob_name)

    data = json.loads(blob_client.download_blob().readall())
    #correct JSON
    data = json.dumps(data, indent=4)
    data = '[' + data

    print(data)

except Exception as ex:
    print(ex)