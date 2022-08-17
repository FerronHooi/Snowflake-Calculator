#link to blob: https://snowflakecalculatordata.blob.core.windows.net/snowflakedata/SnowflakeCloudData.json

import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


def write_to_blob():
    try:
        connect_str = "DefaultEndpointsProtocol=https;AccountName=snowflakecalculatordata;AccountKey=2QlRyOr9e9UQagpZGxzKam3lp4vpU+pokDKDdqt63EgbGP5dCrWQhVKaqGCZJRHd8whE4nBl1meV+ASt5nncdA==;EndpointSuffix=core.windows.net"
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the container
        container_name = "snowflakedata"
        blob_name = "SnowflakeCloudData.json"

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        print("\nUploading to Azure Storage as blob:\n\t" + blob_client.blob_name)

        # Upload the created file
        with open("SnowflakeCloudData.json", "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # # Clean up
        # print("\nPress the Enter key to begin clean up")
        # input()
        #
        # print("Deleting blob container...")
        # container_client.delete_container()

        print("Done")

    except Exception as ex:
        print('Exception:')
        print(ex)

write_to_blob()