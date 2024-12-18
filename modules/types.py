# Type imports
from typing import List, Optional

# Pydantic imports
from pydantic import BaseModel, Field


# -------------------------------------------------------------------------------- #
# Base Types
# -------------------------------------------------------------------------------- #


class Tag(BaseModel):
    """Represents a tag with an ID and category."""
    id: str = Field(description="The ID of the tag")
    category: str = Field(description="The category of the tag")
    description: Optional[str] = Field(
        description="The description of the tag", default=None)

# -------------------------------------------------------------------------------- #
# AI Response Types
# -------------------------------------------------------------------------------- #


class CategorizationAIResponse(BaseModel):
    """Response from the AI categorization process."""
    category: str
    code_present: bool


class StructuredCategorizationAIResponse(BaseModel):
    """Response model for categorization API."""
    tag: Tag = Field(description="The tag that the content belongs to")
    code_present: bool = Field(description="Whether the content contains code")


# -------------------------------------------------------------------------------- #
# API Request Types
# -------------------------------------------------------------------------------- #

class CategorizationAPIRequest(BaseModel):
    """Request model for categorization API."""
    brandId: str = Field(description="The ID of the brand")
    content: str = Field(description="The content to categorize")

# -------------------------------------------------------------------------------- #
# API Response Types
# -------------------------------------------------------------------------------- #


class BaseAPIResponse(BaseModel):
    """Base response model for all API responses."""
    status: str = Field(description="The status of the response")
    message: Optional[str] = Field(description="The message of the response", default=None)


class StructuredCategorizationAPIResponse(BaseAPIResponse):
    """Response model for categorization API."""
    data: Optional[StructuredCategorizationAIResponse] = Field(description="The data of the response")


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
