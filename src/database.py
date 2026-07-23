import os
import json

import streamlit as st
import psycopg2

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

def get_database_url():

    # --------------------------------------------------------
    # Streamlit Cloud
    # --------------------------------------------------------

    if "DATABASE_URL" in st.secrets:

        return st.secrets["DATABASE_URL"]


    # --------------------------------------------------------
    # Local Development
    # --------------------------------------------------------

    database_url = os.getenv(
        "DATABASE_URL"
    )


    if database_url:

        return database_url


    raise ValueError(

        "DATABASE_URL not found in "
        "Streamlit Secrets or .env file."

    )


# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_connection():

    database_url = get_database_url()

    return psycopg2.connect(
        database_url
    )


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """
        CREATE TABLE IF NOT EXISTS calls (

            id SERIAL PRIMARY KEY,

            advisor TEXT NOT NULL,

            team TEXT NOT NULL,

            audio_file TEXT NOT NULL,

            overall_score INTEGER,

            needs_discovery_score INTEGER,

            product_knowledge_score INTEGER,

            objection_handling_score INTEGER,

            compliance_score INTEGER,

            next_step_booking_score INTEGER,

            summary TEXT,

            strengths TEXT,

            issues TEXT,

            action_items TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """

    )

    connection.commit()

    cursor.close()

    connection.close()


# ============================================================
# SAVE CALL ANALYSIS
# ============================================================

def save_call_analysis(

    advisor,

    team,

    audio_file,

    analysis_result

):

    category_scores = (

        analysis_result.category_scores

    )


    strengths_json = json.dumps(

        analysis_result.strengths

    )


    issues_json = json.dumps(

        [

            issue.model_dump()

            for issue in analysis_result.issues

        ]

    )


    action_items_json = json.dumps(

        analysis_result.action_items

    )


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        INSERT INTO calls (

            advisor,

            team,

            audio_file,

            overall_score,

            needs_discovery_score,

            product_knowledge_score,

            objection_handling_score,

            compliance_score,

            next_step_booking_score,

            summary,

            strengths,

            issues,

            action_items

        )

        VALUES (

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s

        )

        """,

        (

            advisor,

            team,

            audio_file,

            analysis_result.overall_score,

            category_scores.needs_discovery,

            category_scores.product_knowledge,

            category_scores.objection_handling,

            category_scores.compliance,

            category_scores.next_step_booking,

            analysis_result.summary,

            strengths_json,

            issues_json,

            action_items_json

        )

    )


    connection.commit()

    cursor.close()

    connection.close()


# ============================================================
# GET ALL SAVED CALLS
# ============================================================

def get_all_calls():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT

            id,

            advisor,

            team,

            audio_file,

            overall_score,

            needs_discovery_score,

            product_knowledge_score,

            objection_handling_score,

            compliance_score,

            next_step_booking_score,

            summary,

            strengths,

            issues,

            action_items,

            created_at

        FROM calls

        ORDER BY created_at DESC

        """

    )


    rows = cursor.fetchall()


    cursor.close()

    connection.close()


    return rows


# ============================================================
# GET TOTAL NUMBER OF CALLS
# ============================================================

def get_total_calls():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT COUNT(*)

        FROM calls

        """

    )


    result = cursor.fetchone()


    cursor.close()

    connection.close()


    return result[0]


# ============================================================
# GET AVERAGE OVERALL SCORE
# ============================================================

def get_average_score():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT AVG(overall_score)

        FROM calls

        """

    )


    result = cursor.fetchone()


    cursor.close()

    connection.close()


    if result[0] is None:

        return 0


    return round(

        result[0],

        2

    )


# ============================================================
# GET BEST PERFORMING ADVISOR
# ============================================================

def get_best_advisor():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT

            advisor,

            AVG(overall_score) AS average_score

        FROM calls

        GROUP BY advisor

        ORDER BY average_score DESC

        LIMIT 1

        """

    )


    result = cursor.fetchone()


    cursor.close()

    connection.close()


    if result is None:

        return None


    return (

        result[0],

        round(

            result[1],

            2

        )

    )


# ============================================================
# GET AVERAGE CATEGORY SCORES
# ============================================================

def get_category_averages():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT

            AVG(needs_discovery_score),

            AVG(product_knowledge_score),

            AVG(objection_handling_score),

            AVG(compliance_score),

            AVG(next_step_booking_score)

        FROM calls

        """

    )


    result = cursor.fetchone()


    cursor.close()

    connection.close()


    if result is None:

        return {

            "needs_discovery": 0,

            "product_knowledge": 0,

            "objection_handling": 0,

            "compliance": 0,

            "next_step_booking": 0

        }


    return {

        "needs_discovery": round(

            result[0] or 0,

            2

        ),

        "product_knowledge": round(

            result[1] or 0,

            2

        ),

        "objection_handling": round(

            result[2] or 0,

            2

        ),

        "compliance": round(

            result[3] or 0,

            2

        ),

        "next_step_booking": round(

            result[4] or 0,

            2

        )

    }


# ============================================================
# GET ADVISOR PERFORMANCE
# ============================================================

def get_advisor_performance():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT

            advisor,

            AVG(overall_score),

            COUNT(*)

        FROM calls

        GROUP BY advisor

        ORDER BY AVG(overall_score) DESC

        """

    )


    rows = cursor.fetchall()


    cursor.close()

    connection.close()


    advisor_data = []


    for row in rows:

        advisor_data.append(

            {

                "advisor": row[0],

                "average_score": round(

                    row[1],

                    2

                ),

                "total_calls": row[2]

            }

        )


    return advisor_data


# ============================================================
# GET ALL ADVISORS
# ============================================================

def get_all_advisors():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT DISTINCT advisor

        FROM calls

        ORDER BY advisor

        """

    )


    rows = cursor.fetchall()


    cursor.close()

    connection.close()


    return [

        row[0]

        for row in rows

    ]


# ============================================================
# GET ALL TEAMS
# ============================================================

def get_all_teams():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        SELECT DISTINCT team

        FROM calls

        ORDER BY team

        """

    )


    rows = cursor.fetchall()


    cursor.close()

    connection.close()


    return [

        row[0]

        for row in rows

    ]


# ============================================================
# GET FILTERED CALLS
# ============================================================

def get_filtered_calls(

    advisor=None,

    team=None,

    min_score=0,

    max_score=100

):

    connection = get_connection()

    cursor = connection.cursor()


    query = """

        SELECT

            id,

            advisor,

            team,

            audio_file,

            overall_score,

            needs_discovery_score,

            product_knowledge_score,

            objection_handling_score,

            compliance_score,

            next_step_booking_score,

            summary,

            strengths,

            issues,

            action_items,

            created_at

        FROM calls

        WHERE overall_score BETWEEN %s AND %s

    """


    parameters = [

        min_score,

        max_score

    ]


    if advisor is not None:

        query += """

            AND advisor = %s

        """

        parameters.append(

            advisor

        )


    if team is not None:

        query += """

            AND team = %s

        """

        parameters.append(

            team

        )


    query += """

        ORDER BY created_at DESC

    """


    cursor.execute(

        query,

        parameters

    )


    rows = cursor.fetchall()


    cursor.close()

    connection.close()


    return rows


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

if __name__ == "__main__":

    initialize_database()

    print(

        "Database initialized successfully!"

    )