import os

from dotenv import load_dotenv

from google import genai


# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()


# --------------------------------
# Get Gemini API key
# --------------------------------

api_key = os.getenv(
    "GEMINI_API_KEY"
)


# --------------------------------
# Validate API key
# --------------------------------

if not api_key:

    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


# --------------------------------
# Create Gemini client
# --------------------------------

client = genai.Client(
    api_key=api_key
)


# --------------------------------
# Send test request
# --------------------------------

response = client.models.generate_content(

    model="gemini-3.5-flash",

    contents=(
        "Say hello in one short sentence "
        "and confirm that the Gemini API is working."
    )

)


# --------------------------------
# Display response
# --------------------------------

print(
    response.text
)