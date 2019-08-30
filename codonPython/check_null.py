import numpy
import pandas as pd

def check_null(dataframe: pd.DataFrame, columns_to_be_checked: list) -> bool:
    """
    Checks a pandas dataframe for null values

    This function takes a pandas dataframe supplied as an argument and returns a integer value representing any null values found within the columns to check

    Parameters
    ----------
    data : pandas.DataFrame
        Dataframe to read
    columns_to_be_checked: list
        Given dataframe columns to be checked for null values

    Returns
    -------
    out : int
        The number of null values found in the given columns

    Examples
    --------
    >>> check_null(dataframe = pd.DataFrame({'col1': [1,2], 'col2': [3,4]}), columns_to_check = ['col1'])
    0
    >>> check_null(dataframe = pd.DataFrame({'col1': [1,numpy.nan], 'col2': [3,4]}), columns_to_check = ['col1'])
    1
    """

    null_count = 0
    for eachColumn in columns_to_be_checked:
        prev_null_count = null_count
        null_count = prev_null_count + (len(dataframe) - dataframe[eachColumn].count())
        
    return null_count