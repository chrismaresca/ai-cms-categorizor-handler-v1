# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from dotenv import load_dotenv
import json
import logging

# Async imports
import asyncio
# Requests Imports
import requests

# Pydantic Imports
from pydantic import ValidationError
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel


# Modules Imports
from modules.utils import fetch_tags, format_system_prompt
from modules.constants import MODEL_NAME, USER_PROMPT_TEMPLATE
from modules.types import CategorizationAPIRequest, StructuredCategorizationAIResponse, StructuredCategorizationAPIResponse, CategorizationAIResponse, Tag, lambda_response


# -------------------------------------------------------------------------------- #
# Configuration
# -------------------------------------------------------------------------------- #

# Configure logger
logger = logging.getLogger()

logger.setLevel(logging.INFO)

# Ensure Lambda doesn't add duplicate handlers
if not logger.hasHandlers():
    handler = logging.StreamHandler()  # Output logs to stdout
    formatter = logging.Formatter('%(levelname)s: %(message)s\n\n')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# Load environment variables
load_dotenv()
logger.info("Loaded environment variables")


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #


async def categorize_content_async(event, context) -> StructuredCategorizationAPIResponse:
    logger.info(f"Received event: {event}")
    try:
        # Parse the request body
        try:
            body = json.loads(event.get("body", "{}"))
            logger.info(f"Parsed raw request body: {body}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON body: {e}")
            raise ValueError(f"Invalid JSON in request body. Missing {', '.join(k for k in ['brandId', 'content'] if k not in body)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise ValueError(f"Unexpected error: {e}")

        # Validate the request body
        try:
            request = CategorizationAPIRequest(**body)
            brand_id = request.brandId
            content = request.content

            logger.info(
                f"Validated data for brand ID: {brand_id} with content: {content}"
            )
        except ValidationError as e:
            logger.error(f"Request validation failed: {e}")
            raise ValueError(f"Request validation failed. {e}")

        # Fetch tags from CMS
        try:
            tags = fetch_tags(brand_id)
            if not tags:
                raise ValueError("No tags found for the given brand ID")
            logger.info(f"Fetched CMS data: {tags}")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch tags from CMS: {e}")
            raise ValueError("Failed to fetch category data")
        except ValueError as e:
            logger.error(f"Error processing CMS data: {e}")
            raise

        # Format the system prompt
        try:
            formatted_system_prompt = format_system_prompt(tags=tags)
        except Exception as e:
            logger.error(f"Failed to format system prompt: {e}")
            raise ValueError("Failed to prepare AI prompt")

        # Configure and run the agent
        try:
            MODEL = OpenAIModel(MODEL_NAME)

            agent = Agent(model=MODEL,
                          result_type=CategorizationAIResponse,
                          system_prompt=formatted_system_prompt)

            result = await agent.run(
                USER_PROMPT_TEMPLATE.format(content=content))

            logger.info(f"Successfully ran the agent")

            if not result or not result.data:
                raise ValueError("No result returned from AI query")

            # Get the tag name and code present from the result
            tag_name, code_present = result.data.category, result.data.code_present
            logger.info(f"Tag name: {tag_name}, Code present: {code_present}")
            # Get the tag from the tags dictionary
            if tag_name not in tags:
                raise ValueError(f"Invalid category returned: {tag_name}")

            tag = tags[tag_name]
            tag_obj = Tag(id=tag.id, category=tag.category)

            structured_response = StructuredCategorizationAIResponse(tag=tag_obj,
                                                                     code_present=code_present)

            handler_response = lambda_response(
                status_code=200,
                body=StructuredCategorizationAPIResponse(
                    status="Success",
                    message="Content successfully categorized",
                    data=structured_response,
                ).model_dump(exclude_none=True)
            )
            # return handler_response
        except Exception as e:
            logger.error(f"AI processing error: {e}")
            raise ValueError("Failed to process content")

    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        handler_response = lambda_response(
            status_code=400,
            body=StructuredCategorizationAPIResponse(
                status="Error",
                message=str(e),
                data=None,
            ).model_dump(exclude_none=True),
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        handler_response = lambda_response(
            status_code=500,
            body=StructuredCategorizationAPIResponse(
                status="Error",
                message=str(e),
                data=None,
            ).model_dump(exclude_none=True),
        )

    
    return handler_response


def categorize(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(categorize_content_async(event, context))
