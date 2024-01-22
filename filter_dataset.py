import numpy as np
from fuzzywuzzy import fuzz
import pandas as pd



def has_target_word_single(string, target_word):
    split_strings=string.split("\n")
    tokens = [token for string in split_strings for token in string.split()]
    return np.any(np.vectorize(lambda x: fuzz.ratio(target_word, x.lower()) >= 80)(tokens))

def has_target_word_multiple(string, target_word):
    tokens=string.split("\n")
    return np.any(np.vectorize(lambda x: fuzz.ratio(target_word, x.lower()) >= 80)(tokens))

def filter_dataframe_by_word(df, column_name:str, target_word:str):
    """
    Filter a DataFrame based on a specific word in a specified column.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - column_name (str): The name of the column to search.
    - target_word (str): The word to search for.

    Returns:
    - pd.DataFrame: A new DataFrame containing only the rows with the specified word.
    Raises:
    - ValueError: If the target word is empty, the specified column does not exist,
                  or the DataFrame is empty.
    """
    # Check if the target word is empty (ie 0 words given or an empty string was submitted)
    if len(target_word.split())==0:
        raise ValueError("Target word is empty.")

    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("DataFrame is empty.")
    
    if len(target_word.split())>=2:
        filtered_df = df[df[column_name].apply(lambda x: has_target_word_multiple(x, target_word))]
        return filtered_df
    else:
        filtered_df = df[df[column_name].apply(lambda x: has_target_word_single(x, target_word))]
        return filtered_df