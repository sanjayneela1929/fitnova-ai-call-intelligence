from src.models import AnalysisResult


def analyze_call(labeled_transcript):
    """
    Performs structured rule-based call analysis.

    The function returns a validated AnalysisResult
    Pydantic model.
    """

    # --------------------------------
    # Initialize Result Sections
    # --------------------------------

    issues = []

    strengths = []

    action_items = []


    # --------------------------------
    # Get Advisor Segments
    # --------------------------------

    advisor_segments = [

        segment

        for segment in labeled_transcript

        if segment.get("speaker") == "Advisor"

    ]


    # --------------------------------
    # Combine Advisor Speech
    # --------------------------------

    advisor_text = " ".join(

        segment.get(
            "text",
            ""
        )

        for segment in advisor_segments

    )


    text_lower = advisor_text.lower()


    # --------------------------------
    # Default Scores
    # --------------------------------

    needs_discovery_score = 15

    product_knowledge_score = 15

    objection_handling_score = 15

    compliance_score = 15

    next_step_booking_score = 15


    # --------------------------------
    # Needs Discovery Analysis
    # --------------------------------

    discovery_keywords = [

        "goal",

        "need",

        "looking for",

        "interested",

        "problem",

        "what are you looking for",

        "what is your goal",

        "requirement"

    ]


    discovery_found = any(

        keyword in text_lower

        for keyword in discovery_keywords

    )


    if discovery_found:

        needs_discovery_score = 20


        strengths.append(

            "The advisor explored or identified "
            "the customer's needs."

        )

    else:

        issues.append(

            {

                "issue_type": "Weak Needs Discovery",

                "severity": "Medium",

                "timestamp": "Not identified",

                "quote": "",

                "reason": (

                    "The advisor did not sufficiently "
                    "explore the customer's needs."

                ),

                "recommendation": (

                    "Ask open-ended questions about "
                    "the customer's goals and requirements."

                )

            }

        )


        action_items.append(

            "Improve needs discovery by asking "
            "more open-ended questions."

        )


    # --------------------------------
    # Product Knowledge Analysis
    # --------------------------------

    product_keywords = [

        "plan",

        "program",

        "service",

        "price",

        "features",

        "package",

        "membership",

        "cost"

    ]


    product_found = any(

        keyword in text_lower

        for keyword in product_keywords

    )


    if product_found:

        product_knowledge_score = 20


        strengths.append(

            "The advisor discussed the product "
            "or service."

        )

    else:

        issues.append(

            {

                "issue_type": "Limited Product Explanation",

                "severity": "Medium",

                "timestamp": "Not identified",

                "quote": "",

                "reason": (

                    "The advisor did not provide "
                    "enough product information."

                ),

                "recommendation": (

                    "Explain relevant product features "
                    "and benefits clearly."

                )

            }

        )


        action_items.append(

            "Improve product explanation "
            "during customer conversations."

        )


    # --------------------------------
    # Over-Promising Detection
    # --------------------------------

    overpromising_keywords = [

        "guaranteed",

        "definitely",

        "100%",

        "surely",

        "you will lose",

        "guarantee",

        "certainly"

    ]


    overpromising_detected = False


    for segment in advisor_segments:

        segment_text = segment.get(

            "text",

            ""

        )


        segment_lower = segment_text.lower()


        for keyword in overpromising_keywords:

            if keyword in segment_lower:

                issues.append(

                    {

                        "issue_type": (
                            "Potential Over-Promising"
                        ),

                        "severity": "High",

                        "timestamp": (

                            f"{segment.get('start', 0):.2f}s - "

                            f"{segment.get('end', 0):.2f}s"

                        ),

                        "quote": segment_text,

                        "reason": (

                            "The advisor may have made "
                            "an unrealistic or absolute "
                            "promise."

                        ),

                        "recommendation": (

                            "Use realistic, transparent, "
                            "and evidence-based language."

                        )

                    }

                )


                compliance_score = 5


                action_items.append(

                    "Avoid absolute guarantees "
                    "or unrealistic promises."

                )


                overpromising_detected = True


                break


        if overpromising_detected:

            break


    # --------------------------------
    # Calculate Overall Score
    # --------------------------------

    overall_score = round(

        (

            needs_discovery_score

            + product_knowledge_score

            + objection_handling_score

            + compliance_score

            + next_step_booking_score

        ) / 5

    )


    # --------------------------------
    # Generate Summary
    # --------------------------------

    if len(issues) == 0:

        summary = (

            "The call was handled well with no major "
            "issues detected by the initial analysis."

        )

    else:

        summary = (

            f"The analysis identified "

            f"{len(issues)} potential issue(s) "

            "that may require review."

        )


    # --------------------------------
    # Return Validated Pydantic Model
    # --------------------------------

    return AnalysisResult(

        overall_score=overall_score,

        category_scores={

            "needs_discovery": (
                needs_discovery_score
            ),

            "product_knowledge": (
                product_knowledge_score
            ),

            "objection_handling": (
                objection_handling_score
            ),

            "compliance": (
                compliance_score
            ),

            "next_step_booking": (
                next_step_booking_score
            )

        },

        summary=summary,

        strengths=strengths,

        issues=issues,

        action_items=action_items

    )