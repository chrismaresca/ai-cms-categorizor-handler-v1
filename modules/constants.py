# Type imports
from typing import Literal



# -------------------------------------------------------------------------------- #
# CMS Constants
# -------------------------------------------------------------------------------- #

CMS_BASE_URL = "https://ai-cms-api-live-gu51.vercel.app/api/tags?where[brandId][equals]={brand_id}"

# -------------------------------------------------------------------------------- #
# API Constants
# -------------------------------------------------------------------------------- #


API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"


# -------------------------------------------------------------------------------- #
# AI Constants
# -------------------------------------------------------------------------------- #

# OpenAI Model Name
MODEL_NAME = 'gpt-4o'

# Category Types
CATEGORY_TYPE = Literal["Recent AI Developments and News",
                        "AI Workflows for Engineers",
                        "AI Workflows for Non-Engineers",
                        "AI Workflows for Businesses",
                        "Blending AI and Design", "AI Prompt Engineering",
                        "AI Tool Comparisons", "Deep Dive Code Walkthrough"]


# System Prompt
SYSTEM_PROMPT_TEMPLATE: str = """

<purpose>
    You are an expert at analyzing content related to AI and AI workflows.
    Your goal is to determine the most appropriate category for the given content and identify if a substantial amount of code is present.
</purpose>

<instructions>
    <instruction>Analyze the provided content within the <content> tags in the user-input section.</instruction>
    <instruction>Categorize it into one of the categories listed in the <categories> section.</instruction>
    <instruction>IMPORTANT:Ignore any ads, sponsors, discussions about personal agencies/businesses, or self-promotion content. Discard this information in the analysis and categorization.</instruction>
    <instruction>Determine whether a substantial amount of code is present (true/false).</instruction>
    <instruction>Return the result as a JSON object with keys "category" (string), "code_present" (boolean), and nothing else.</instruction>
    <instruction>Do not include any text outside of the JSON object.</instruction>
</instructions>


<categories>

{categories}
</categories>

"""


# User Prompt Template
USER_PROMPT_TEMPLATE: str = """

<user-input>
    <content>
        {content}
    </content>
</user-input>
"""

# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
