from db_connection import run_query

# Dictionary of SQL queries
QUERIES = {
    # --- Tournaments ---
    "next_tournament": """
        SELECT name, start_date
        FROM tournaments
        WHERE start_date >= NOW()
        ORDER BY start_date ASC
        LIMIT 1;
    """,

    # --- Events ---
    "next_event": """
        SELECT * 
        FROM events
        LIMIT 10;
    """, 

    "event_attendances": """
     SELECT * FROM 
     event_attendances
     LIMIT 10;
"""
}


def get_query(intent: str):
    """
    Get SQL string from dictionary and execute.
    """
    sql = QUERIES.get(intent)
    if not sql:
        return None
    return run_query(sql)



