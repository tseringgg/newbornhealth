import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="pdf_http_trigger", methods=["GET", "PUT"])
def pdf_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    method = req.method

    if method == 'GET':
        # Handle GET request
        return func.HttpResponse("This function was triggered by a GET request", status_code=200)
    elif method == 'PUT':
        # Handle PUT request
        return func.HttpResponse("This function was triggered by a PUT request", status_code=200)
    else:
        return func.HttpResponse("This function only supports GET and PUT requests", status_code=405)

# Get documents
@app.route(route="get_pdf", methods=["GET"])
def get_pdf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function to retrieve PDF processed a request.')

    blob_name = req.params.get('name')
    if not blob_name:
        return func.HttpResponse("Please pass the name of the PDF in the query string", status_code=400)

    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
        container_client = blob_service_client.get_container_client('pdf-container')
        blob_client = container_client.get_blob_client(blob_name)
        download_stream = blob_client.download_blob()

        return func.HttpResponse(
            download_stream.readall(),
            status_code=200,
            mimetype="application/pdf"
        )
    except Exception as e:
        logging.error(f"Error retrieving PDF: {e}")
        return func.HttpResponse("Error retrieving PDF", status_code=500)