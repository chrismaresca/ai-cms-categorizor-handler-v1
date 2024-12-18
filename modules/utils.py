# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Typing imports
from typing import Dict

# Requests import
import requests

# Constants import
from modules.constants import CMS_BASE_URL, SYSTEM_PROMPT_TEMPLATE

# Types import
from modules.types import Tag


# -------------------------------------------------------------------------------- #
# AI Utils
# -------------------------------------------------------------------------------- #


def format_category_section(tags: Dict[str, Tag]) -> str:
    """Dynamically format categories into the system prompt."""
    return "\n".join([
        f"    <category>\n        <name>{category}</name>\n        <description>{tag.description}</description>\n    </category>"
        for category, tag in tags.items()
    ])


def format_system_prompt(tags: Dict[str, Tag]) -> str:
    """Format the system prompt with the given brand ID."""

    return SYSTEM_PROMPT_TEMPLATE.format(
        categories=format_category_section(tags))


# -------------------------------------------------------------------------------- #
# Data Utils
# -------------------------------------------------------------------------------- #

def extract_tags(cms_data):
    """Helper function to extract tags from CMS data."""
    tags = []
    for tag in cms_data.get("docs", []):
        tag_info = {
            "name": tag["name"],
            "description": tag["aiDescription"]
        }
        tags.append(tag_info)
    return tags

# -------------------------------------------------------------------------------- #
# Requests Utils
# -------------------------------------------------------------------------------- #


def extract_tags(cms_data) -> Dict[str, Tag]:
    """Helper function to extract tags from CMS data and return a dictionary keyed by category name."""
    tags = {}
    for tag in cms_data.get("docs", []):
        tags[tag["name"]] = Tag(id=tag["id"],
                                category=tag["name"],
                                description=tag["aiDescription"])
    return tags


def fetch_tags(brand_id: str) -> Dict[str, Tag]:
    """Fetch CMS data for the given brand ID and return tags dictionary."""
    url = CMS_BASE_URL.format(brand_id=brand_id)
    # url = "https://ai-cms-api-live-gu51.vercel.app/api/tags?where[brandId][equals]=d42d5411-aac8-4cbd-aacb-05e946e78af5"
    response = requests.get(url)
    response.raise_for_status()

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch CMS data: {response.status_code}")

    cms_data = response.json()
    try:
        return extract_tags(cms_data)
    except Exception as e:
        raise ValueError(f"Failed to extract tags: {e}")


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #


