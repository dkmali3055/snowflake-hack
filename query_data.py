import pandas as pd
from snowflake_connect import get_snowflake_connection

def fetch_festival_data(state):
    conn = get_snowflake_connection()
    query = f"""
        SELECT
    event_id,
    event_name AS event_name,
    year,
    state,
    city,
    start_date AS start_date,
    end_date AS end_date,
    attendees,
    event_type AS event_type
FROM festival_data
WHERE state = '{state}'
ORDER BY start_date
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_tourism_data(state):
    conn = get_snowflake_connection()
    query = f"""
        SELECT year, month, visitors_domestic, visitors_foreign
        FROM tourism_data
        WHERE state = '{state}'
        ORDER BY year, month
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    state = "Rajasthan"
    festivals = fetch_festival_data(state)
    tourism = fetch_tourism_data(state)
    print(festivals.head())
    print(tourism.head())
