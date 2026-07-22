from src.llm_analysis import analyze_call_with_llm


# --------------------------------
# Sample Speaker-Labeled Transcript
# --------------------------------

sample_transcript = [

    {
        "start": 0.00,
        "end": 5.00,
        "speaker": "Advisor",
        "text": (
            "Hello, welcome to FitNova. "
            "How can I help you today?"
        )
    },

    {
        "start": 5.00,
        "end": 10.00,
        "speaker": "Customer",
        "text": (
            "I am looking for a weight loss program."
        )
    },

    {
        "start": 10.00,
        "end": 20.00,
        "speaker": "Advisor",
        "text": (
            "What is your main fitness goal? "
            "Have you tried any weight loss program before?"
        )
    },

    {
        "start": 20.00,
        "end": 30.00,
        "speaker": "Customer",
        "text": (
            "I want to lose around 12 kilos "
            "in the next 6 months."
        )
    },

    {
        "start": 30.00,
        "end": 40.00,
        "speaker": "Advisor",
        "text": (
            "We can help you with a personalized "
            "weight loss program."
        )
    }

]


# --------------------------------
# Call Gemini Analysis
# --------------------------------

print(
    "🤖 Sending transcript to Gemini..."
)


analysis_result = analyze_call_with_llm(

    sample_transcript

)


# --------------------------------
# Display Result
# --------------------------------

print(
    "\n✅ Gemini Analysis Completed!\n"
)


print(
    "Overall Score:",
    analysis_result.overall_score
)


print(
    "\nCategory Scores:"
)


print(
    "Needs Discovery:",
    analysis_result.category_scores.needs_discovery
)


print(
    "Product Knowledge:",
    analysis_result.category_scores.product_knowledge
)


print(
    "Objection Handling:",
    analysis_result.category_scores.objection_handling
)


print(
    "Compliance:",
    analysis_result.category_scores.compliance
)


print(
    "Next Step Booking:",
    analysis_result.category_scores.next_step_booking
)


print(
    "\nSummary:"
)


print(
    analysis_result.summary
)


print(
    "\nStrengths:"
)


for strength in analysis_result.strengths:

    print(
        "-",
        strength
    )


print(
    "\nIssues:"
)


for issue in analysis_result.issues:

    print(
        "-",
        issue.issue_type
    )


print(
    "\nAction Items:"
)


for action_item in analysis_result.action_items:

    print(
        "-",
        action_item
    )