import boto3
import json
import urllib.parse
import requests

# Initialize AWS clients
s3_client = boto3.client('s3')
textract_client = boto3.client('textract')

def mock_itams_api(event):
    for record in event['Records']:
        # Extract bucket and file information
        bucket_name = record['s3']['bucket']['name']
        file_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        print(f"Processing file from bucket: {bucket_name}, key: {file_key}")

        # Trigger Textract to analyze the document
        response = textract_client.detect_document_text(
            Document={'S3Object': {'Bucket': bucket_name, 'Name': file_key}}
        )

        # Save Textract response back to S3
        output_bucket = bucket_name
        output_key = f"processed/{file_key.split('/')[-1]}.json"
        s3_client.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=json.dumps(response, indent=4)
        )
        print(f"Results saved to {output_bucket}/{output_key}")

        # Send the output to the Mock ITAMS API
        api_url = "http://127.0.0.1:5000/process-document"  # Replace with actual API endpoint if necessary
        api_payload = {
            "bucket": output_bucket,
            "key": output_key,
            "data": response
        }
        
        try:
            api_response = requests.post(api_url, json=api_payload)
            api_response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            print(f"Mock ITAMS API response: {api_response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to Mock ITAMS API: {e}")

# Example event payload for local testing (mocking SNS notification)
if __name__ == "__main__":
    event_payload = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "sales1-docuware-textract"},
                    "object": {"key": "incoming/test-document.pdf"}
                }
            }
        ]
    }

    mock_itams_api(event_payload)
