import pandas as pd
import numpy as np

def uniform_subset(df, col, nrows_cat, **kwargs):
    """
    Draw a subset with same number of rows from each category/bin of focused column.
        PARAMS:
            df (pd.DataFrame): 
            col (str): name of interested column that needing a balance distribution throughout all categories/bins
            nrow_cat (int): number of rows to draw from each category/bin
            **kwargs:
                num_bin (int): number of bins to cut the continuous column
                threshold (list): list of number as threshold for cutting continous column into bins. e.g. [-np.inf, 0, np.inf], [-3, 5, 10], ...
                right (bool): indicates whether `bins` includes the rightmost edge or not. If 'right == True', then the threshold [1, 2, 3] indicate (1,2], (2,3]. 
        RETURNS:
            df_sub (pd.Dataframe): A subset from original df.
    """
    num_bin = kwargs.get('num_bin', None)
    threshold = kwargs.get('threshold', None)
    right = kwargs.get('right', None)
    
    data = df.copy()
    data.dropna(subset=[col], inplace=True)
    df_sub = pd.DataFrame([])
    
    # determine if the interested column is continuous
    # remember to change the dtype of categorial data with number as label to 'o' or 'category'  
    # continuous column
    if data[col].dtype == 'int' or data[col].dtype == 'float':
        # cut column to bins
        data[col] = pd.cut(data[col], threshold, include_lowest=True, right=right)     
        
    # extract categories
    cat_names = set(data[col])
    for cat in cat_names:
        cat_sub = data[data[col]==cat].sample(n=nrows_cat, axis=0)
        df_sub = pd.concat([df_sub, cat_sub], axis=0)
        
    return df_sub.reset_index(drop=True)