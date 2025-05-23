"""
Snowflake integration utilities for Cultural Tourism Dashboard
"""

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class SnowflakeConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to Snowflake"""
        try:
            print(f"before connection")
            self.connection = snowflake.connector.connect(
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA'),
                role=os.getenv('SNOWFLAKE_ROLE')
            )
            self.cursor = self.connection.cursor()
            print(f"after connection")
            return True
        except Exception as e:
            st.error(f"Failed to connect to Snowflake: {str(e)}")
            return False
    
    def disconnect(self):
        """Close Snowflake connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query):
        """Execute SQL query and return results as DataFrame"""
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            df = pd.read_sql(query, self.connection)
            return df
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
            return None
    
    def load_cultural_data(self, filters=None):
        print("inside function")
        """Load cultural tourism data from Snowflake"""
        base_query = """
        SELECT 
            DATE,
            STATE,
            EVENT,
            ART_FORM,
            VISITORS,
            TOURISM_LEVEL,
            REVENUE_INR,
            LOCAL_EMPLOYMENT,
            MONTH(DATE) as MONTH,
            YEAR(DATE) as YEAR,
            QUARTER(DATE) as QUARTER,
            REGION
        FROM CULTURAL_TOURISM_EVENTS
        """
        
        # Add filters if provided
        where_conditions = []
        if filters:
            if filters.get('state') and filters['state'] != 'All':
                where_conditions.append(f"STATE = '{filters['state']}'")
            if filters.get('year') and filters['year'] != 'All':
                where_conditions.append(f"YEAR = {filters['year']}")
            if filters.get('event') and filters['event'] != 'All':
                where_conditions.append(f"EVENT = '{filters['event']}'")
            if filters.get('art_form') and filters['art_form'] != 'All':
                where_conditions.append(f"ART_FORM = '{filters['art_form']}'")
            if filters.get('tourism_level') and filters['tourism_level'] != 'All':
                where_conditions.append(f"TOURISM_LEVEL = '{filters['tourism_level']}'")
            if filters.get('region') and filters['region'] != 'All':
                where_conditions.append(f"REGION = '{filters['region']}'")
            if filters.get('quarter') and filters['quarter'] != 'All':
                where_conditions.append(f"QUARTER = {filters['quarter']}")
            if filters.get('month') and filters['month'] != 'All':
                where_conditions.append(f"MONTH = {filters['month']}")
        
        # Add WHERE clause if filters exist
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        # Add ORDER BY clause
        base_query += " ORDER BY DATE DESC"
        vr = self.execute_query(base_query)
        print(vr)
        return vr
    
    def get_unique_values(self, column_name):
        """Get unique values for a specific column from the cultural tourism data"""
        query = f"""
        SELECT DISTINCT {column_name}
        FROM CULTURAL_TOURISM_EVENTS
        ORDER BY {column_name}
        """
        return self.execute_query(query)
    
    def get_summary_statistics(self, filters=None):
        """Get summary statistics for the cultural tourism data"""
        base_query = """
        SELECT 
            COUNT(*) as total_events,
            SUM(VISITORS) as total_visitors,
            SUM(REVENUE_INR) as total_revenue,
            SUM(LOCAL_EMPLOYMENT) as total_employment,
            AVG(VISITORS) as avg_visitors_per_event,
            AVG(REVENUE_INR) as avg_revenue_per_event
        FROM CULTURAL_TOURISM_EVENTS
        """
        
        # Add filters if provided
        where_conditions = []
        if filters:
            if filters.get('state') and filters['state'] != 'All':
                where_conditions.append(f"STATE = '{filters['state']}'")
            if filters.get('year') and filters['year'] != 'All':
                where_conditions.append(f"YEAR = {filters['year']}")
            if filters.get('event') and filters['event'] != 'All':
                where_conditions.append(f"EVENT = '{filters['event']}'")
            if filters.get('art_form') and filters['art_form'] != 'All':
                where_conditions.append(f"ART_FORM = '{filters['art_form']}'")
            if filters.get('tourism_level') and filters['tourism_level'] != 'All':
                where_conditions.append(f"TOURISM_LEVEL = '{filters['tourism_level']}'")
            if filters.get('region') and filters['region'] != 'All':
                where_conditions.append(f"REGION = '{filters['region']}'")
            if filters.get('quarter') and filters['quarter'] != 'All':
                where_conditions.append(f"QUARTER = {filters['quarter']}")
            if filters.get('month') and filters['month'] != 'All':
                where_conditions.append(f"MONTH = {filters['month']}")
        
        # Add WHERE clause if filters exist
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        return self.execute_query(base_query)