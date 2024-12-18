# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
from modules.types import LambdaResponse, StructuredCategorizationAPIResponse

# -------------------------------------------------------------------------------- #
# Lambda Response Helper
# -------------------------------------------------------------------------------- #

def create_lambda_response(status_code: int, message: str, data: StructuredCategorizationAPIResponse = None) -> LambdaResponse:
    """Helper function to create a standardized Lambda response."""
    return LambdaResponse(
        statusCode=status_code,
        body=StructuredCategorizationAPIResponse(
            status="Success" if status_code == 200 else "Error",
            message=message,
            data=data,
        ).model_dump(exclude_none=True)
    ).model_dump_json() 