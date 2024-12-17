from pydantic import BaseModel
import json
import logging
# Define the Pydantic model

logger = logging.getLogger()

class NameModel(BaseModel):
    name: str


def hello(event, context):
    logger.info("Received event: %s", event)  # Log the incoming event
    try:
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        logger.info("Parsed body: %s", body)  # Log the parsed body
        name_data = NameModel(**body)  # Validate using Pydantic model
        logger.info("Validated name data: %s", name_data)  # Log validated data

        response_body = {
            "message":
            f"Hello, {name_data.name}! Your function executed successfully!"
        }
        status_code = 200

    except Exception as e:
        # Handle validation or parsing errors
        logger.error("Error occurred: %s", str(e))  # Log the error
        response_body = {"error": str(e)}
        status_code = 400

    logger.info("Response: %s", response_body)  # Log the response
    return {"statusCode": status_code, "body": json.dumps(response_body)}
