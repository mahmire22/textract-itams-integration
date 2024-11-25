from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process-document', methods=['POST'])
def process_document():
    # Mock processing response
    data = request.json
    print(f"Received data: {data}")

    # Simulated response
    response = {
        "status": "success",
        "message": "Document processed successfully",
        "data": {
            "document_id": "12345",
            "summary": "Sample summary of the processed document",
            "metadata": {
                "author": "Mock User",
                "date_processed": "2024-11-25"
            }
        }
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port=5000)
