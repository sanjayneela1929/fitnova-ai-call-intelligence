import os

from dotenv import load_dotenv

from openai import OpenAI


# Load variables from .env
load_dotenv()


# Read API key
api_key = os.getenv(
    "OPENAI_API_KEY"
)


# Check whether API key exists
if not api_key:

    raise ValueError(
        "OPENAI_API_KEY was not found."
    )


# Create OpenAI client
client = OpenAI(
    api_key=api_key
)


# Send a simple test request
response = client.responses.create(

    model="gpt-5-mini",

    input="Say hello in one short sentence."

)


# Display response
print(
    response.output_text
)