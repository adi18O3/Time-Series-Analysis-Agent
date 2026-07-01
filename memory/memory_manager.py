"""
Conversation memory manager.
"""

import json

from database.mysql import get_connection


def save_conversation(query, plan):
    """
    Save the user query and analysis plan.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_memory
        (user_query, analysis_plan)
        VALUES (%s, %s)
        """,
        (
            query,
            json.dumps(plan.model_dump())
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_last_conversation():
    """
    Return the most recent conversation.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM conversation_memory
        ORDER BY id DESC
        LIMIT 1
        """
    )

    conversation = cursor.fetchone()

    cursor.close()
    connection.close()

    return conversation