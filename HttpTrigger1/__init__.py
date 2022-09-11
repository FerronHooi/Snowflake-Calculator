import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response. XXX",
             status_code=200
        )

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

    print("\nUploading to Azure Storage as blob:\n\t" + blob_client.blob_name)

    # # Upload the created file
    # with open("../Datafiles/snowflakeData.json", "rb") as data:
    #     blob_client.upload_blob(data, overwrite=True)

    blob_client.upload_blob({'test':'test'}, overwrite=True)

    # # Clean up
    # print("\nPress the Enter key to begin clean up")
    # input()
    #
    # print("Deleting blob container...")
    # container_client.delete_container()

    print("Done")

