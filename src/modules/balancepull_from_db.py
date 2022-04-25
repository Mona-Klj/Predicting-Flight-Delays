import psycopg2
import pandas as pd

def pull_balance_data_into_csv(table_name, balance_col, nrow_each_cat):
    """
    Given focused column, randomly pull given number of rows for each category/bin from given table in Postgres midterm database and export into a csv file.
        PARAMS:
            table_name (str): table name in database.
            balance_col (str): name of the column wanted a balance distribution.
            nrow_each_cat (int): number of rows to pull for each category in 'balance_col'.
        RETURNS:
            export a csv file of pulled data.
    """

    # Connect to mid-term database
    con = psycopg2.connect(database='mid_term_project',
                           user='lhl_student',
                           password='lhl_student',
                           host='mid-term-project.ca2jkepgjpne.us-east-2.rds.amazonaws.com',
                           port='5432')
    print("Database opened successfully")
    
    cur = con.cursor()

    # extract column names
    cur.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 0
        ;
        """)
    col_names = [desc[0] for desc in cur.description]
    
    # created an empty dataframe with headers
    df = pd.DataFrame([], columns=col_names)

    # extract percentage of given number to total number of rows in each category
    cur.execute(f"""
        SELECT {balance_col}, CAST(100.0*{nrow_each_cat}/COUNT(*) AS FLOAT)
        FROM {table_name}
        GROUP BY {balance_col}
        ;
        """)
    cat_pct = cur.fetchall()    
    
    # pull same number of rows for each category
    # append to df
    for cat, pct in cat_pct:
        # there is a easier way by using 'tablesample system_rows()', but will need superuser power
        # select rows with calculated percentage of total rows in each category
        cur.execute(f"""
            SELECT *
            FROM {table_name}
            TABLESAMPLE SYSTEM ({pct})
            WHERE {balance_col} = '{cat}'
            ;
            """)
        rows = cur.fetchall()
        df = pd.concat([df, pd.DataFrame(rows, columns=col_names)], axis=0)

    df.to_csv(f'{table_name}_{balance_col}_raw.csv')
    
    # Close the database connection
    con.close()