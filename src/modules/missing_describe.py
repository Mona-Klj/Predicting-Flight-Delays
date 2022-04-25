import pandas as pd

def md(data):
    """
    Returns a pandas dataframe containing information about missing values in columns. 
        PARAMS:
            data (pd.DataFrame): pandas dataframe to look into
        RETURNS:
            missing (): contains number, count, dtype and percentage of missing values in each column    
    """
    # number of missing values in each column
    num_missing = data.isnull().sum()
    # percentage of missing values in each column
    pct_missing = num_missing/data.shape[0]
    # concat info into one dataframe and sorted by num_missing in descending order
    missing = pd.concat([data.dtypes, num_missing, pct_missing], 
                        axis=1,
                        keys = ['dtype', 'missing_count', 'missing_percent']
                       ).sort_values('missing_count', ascending=False)
    return missing