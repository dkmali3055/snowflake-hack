import snowflake.connector

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        account = 'XPUWXGA-UG65686',
user = 'DKMALI3055',
password = 'j2cQyEqahaBr8Gp',
role = 'ACCOUNTADMIN',
warehouse = 'COMPUTE_WH',
database = 'TOURISM_HACKATHON',
schema = 'PUBLIC'
    )
    return conn
