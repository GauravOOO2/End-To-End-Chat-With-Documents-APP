import unstructured_client
from unstructured_client.models import operations, shared

API_KEY = "BMBICOiwbTGku20LbKFHI6AbMP2Jsh"
SERVER_URL = "https://api.unstructuredapp.io"

def parse_document(file_path: str):
    client = unstructured_client.UnstructuredClient(api_key_auth=API_KEY, server_url=SERVER_URL)

    with open(file_path, "rb") as f:
        data = f.read()

    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=shared.Files(content=data, file_name=file_path),
            strategy=shared.Strategy.HI_RES,  # High-resolution parsing strategy
            languages=["eng"],  # Specify language
        ),
    )

    try:
        res = client.general.partition(request=req)
        print(res)  # Print the entire response to the terminal
        
        # Check the structure of res.elements, which is expected to be a list of elements
        parsed_text = " ".join([element.get('text', '') for element in res.elements])  # Safely extract 'text'
        metadata = [element.get('metadata', {}) for element in res.elements]  # Safely extract 'metadata'
        
        return {"parsed_content": parsed_text, "metadata": metadata}
    
    except Exception as e:
        raise Exception(f"Error parsing document: {str(e)}")
