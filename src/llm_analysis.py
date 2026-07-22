import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from src.models import AnalysisResult


# --------------------------------
# Load Environment Variables
# --------------------------------

load_dotenv()


# --------------------------------
# Get Gemini API Key
# --------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )


# --------------------------------
# Create Gemini Client
# --------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# --------------------------------
# Analyze Call with Gemini
# --------------------------------

def analyze_call_with_llm(
    labeled_transcript
):

    """
    Analyze a speaker-labeled call transcript
    using Gemini 3.5 Flash.

    Returns:
        AnalysisResult
    """


    # --------------------------------
    # Convert Transcript to Text
    # --------------------------------

    transcript_text = ""


    for segment in labeled_transcript:

        start_time = segment.get(
            "start",
            0
        )

        end_time = segment.get(
            "end",
            0
        )

        speaker = segment.get(
            "speaker",
            "Unknown"
        )

        text = segment.get(
            "text",
            ""
        )


        transcript_text += (

            f"[{start_time:.2f}s - "
            f"{end_time:.2f}s] "

            f"{speaker}: "

            f"{text}\n"

        )


    # --------------------------------
    # Prompt
    # --------------------------------

    prompt = f"""

You are an expert AI sales call quality analyst.

Analyze the following speaker-labeled call transcript.

IMPORTANT:

Evaluate ONLY the Advisor's performance.

The Customer's statements should be used as context
to evaluate the Advisor.

Do not invent events that are not present
in the transcript.

If the call is incomplete, explicitly identify
the missing stages.

Evaluate the following categories:

1. Needs Discovery

- Did the Advisor understand the customer's needs?
- Did the Advisor ask relevant questions?
- Did the Advisor identify goals, pain points,
  preferences, or constraints?

2. Product Knowledge

- Did the Advisor explain the product or service?
- Did the Advisor explain relevant benefits?
- Did the Advisor provide accurate information?

3. Objection Handling

- Did the Advisor identify and respond to
  customer concerns, objections, or pain points?

4. Compliance

- Did the Advisor avoid unsupported claims,
  misleading promises, or inappropriate statements?

5. Next Step Booking

- Did the Advisor clearly propose or complete
  a next step such as a booking, consultation,
  follow-up, trial, or purchase?

Each category must be scored from 0 to 20.

The overall_score must be the sum of all five
category scores.

Therefore:

overall_score =
needs_discovery
+
product_knowledge
+
objection_handling
+
compliance
+
next_step_booking

The maximum overall score is 100.

For every detected issue, include:

- issue_type
- severity
- timestamp
- quote
- reason
- recommendation

Return ONLY valid JSON.

Do not use Markdown.

Use exactly this JSON structure:

{{
    "overall_score": 0,

    "category_scores": {{
        "needs_discovery": 0,
        "product_knowledge": 0,
        "objection_handling": 0,
        "compliance": 0,
        "next_step_booking": 0
    }},

    "summary": "",

    "strengths": [],

    "issues": [
        {{
            "issue_type": "",
            "severity": "",
            "timestamp": "",
            "quote": "",
            "reason": "",
            "recommendation": ""
        }}
    ],

    "action_items": []
}}

CALL TRANSCRIPT:

{transcript_text}

"""


    # --------------------------------
    # Gemini API Call with Retry Logic
    # --------------------------------

    max_retries = 3

    response = None


    for attempt in range(
        max_retries
    ):

        try:

            print(
                "Using Gemini model: "
                "gemini-3.5-flash"
            )


            response = (
                client.models.generate_content(

                    model="gemini-3.5-flash",

                    contents=prompt

                )
            )


            print(
                "Gemini analysis completed."
            )


            break


        except errors.ServerError as error:

            print(

                f"Gemini server error "
                f"(attempt {attempt + 1}/"
                f"{max_retries}): {error}"

            )


            if attempt < max_retries - 1:

                wait_time = 5 * (
                    attempt + 1
                )


                print(

                    f"Retrying in "
                    f"{wait_time} seconds..."

                )


                time.sleep(
                    wait_time
                )


            else:

                raise RuntimeError(

                    "Gemini is temporarily "
                    "unavailable after multiple "
                    "retry attempts. Please try "
                    "again later."

                )


        except Exception as error:

            raise RuntimeError(

                f"Gemini API error: {error}"

            ) from error


    # --------------------------------
    # Check Response
    # --------------------------------

    if response is None:

        raise RuntimeError(

            "No response received from Gemini."

        )


    # --------------------------------
    # Extract Response Text
    # --------------------------------

    response_text = response.text.strip()


    # --------------------------------
    # Remove Markdown Code Fences
    # --------------------------------

    if response_text.startswith(
        "```json"
    ):

        response_text = (

            response_text

            .replace(
                "```json",
                ""
            )

            .replace(
                "```",
                ""
            )

            .strip()

        )


    elif response_text.startswith(
        "```"
    ):

        response_text = (

            response_text

            .replace(
                "```",
                ""
            )

            .strip()

        )


    # --------------------------------
    # Convert JSON to Python Dictionary
    # --------------------------------

    try:

        analysis_data = json.loads(
            response_text
        )


    except json.JSONDecodeError as error:

        raise RuntimeError(

            "Gemini returned invalid JSON.\n\n"

            f"Response received:\n"
            f"{response_text}"

        ) from error


    # --------------------------------
    # Validate with Pydantic
    # --------------------------------

    try:

        analysis_result = AnalysisResult(
            **analysis_data
        )


    except Exception as error:

        raise RuntimeError(

            "Gemini response failed "
            "Pydantic validation.\n\n"

            f"Details: {error}"

        ) from error


    # --------------------------------
    # Return Validated Result
    # --------------------------------

    return analysis_result