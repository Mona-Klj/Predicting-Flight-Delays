import psycopg2
import pandas as pd

def pull_data_into_csv(table_name, pct):
    """
    Randomly pull given percentage of data from Postgres midterm database and export into a csv file.
        PARAMS:
            table_name (str): table name in database
            pct (float): the percentage of interest of rows in dataset
        RETURNS:
            export a csv file of pulled data.
    """

    # Connect to mid-term database
    # Replace the database information with your own info 
    con = psycopg2.connect(database='database',
                           user='username',
                           password='pwd',
                           host='host',
                           port='port')
    print("Database opened successfully")
    
    cur = con.cursor()
    
    # select rows with given percentage of total rows
    cur.execute(f"""
        SELECT *
        FROM {table_name}
        TABLESAMPLE SYSTEM ({pct})
        ;
        """)
    rows = cur.fetchall()

    # extract column names
    cur.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 0
        ;
        """)
    col_names = [desc[0] for desc in cur.description]
    
    df = pd.DataFrame(rows, columns=col_names)
    df.to_csv(f'{table_name}_raw.csv')
    
    # Close the database connection
    con.close()
