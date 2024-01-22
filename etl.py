from utils import *
import numpy as np
from fuzzywuzzy import fuzz
import timeit
import re
from typing import Union
import pandas as pd

def read_dataset(filepath, lines=True):
    """
    Read the dataset from the specified file path. Added support for CSV.

    Parameters:
    - filepath (str): The path to the dataset file.

    Returns:
    - pd.DataFrame: The DataFrame containing the dataset.
    """
    try:
        # Extract the file extension
        file_extension = filepath.split('.')[-1].lower()

        # Check the file type and use the appropriate loading function
        if file_extension == 'json':
            df = pd.read_json(filepath, lines=True)
        elif file_extension in ['csv', 'txt']:
            df = pd.read_csv(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except ValueError as ve:
        print("Value Error", ve)
        return None
    except Exception as e:
        print(f"An error occurred while reading the dataset: {e}")
        return None
    
def calculate_total_time(cookTime,prepTime) -> Union[int, None]:
    total_time=0
    if (not cookTime or cookTime=="PT") and (not prepTime or prepTime=="PT"):
        return None
    
    if not cookTime or cookTime=="PT":
        cookmins=0
    else:
        minutes_match = re.search(r'(\d+)M', cookTime)
        hours_match =  re.search(r'(\d+)H', cookTime)
        hours = int(hours_match.group(1))*60 if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0                  
        cookmins=minutes+hours
    
    if not prepTime or prepTime=="PT":
        prepmins=0
    else:
        minutes_match = re.search(r'(\d+)M', prepTime)
        hours_match = re.search(r'(\d+)H', prepTime)
        hours = int(hours_match.group(1))*60 if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        prepmins=minutes+hours
    
    return cookmins+prepmins     

def determine_difficulty(cookTime,prepTime):
    total_time= calculate_total_time(cookTime,prepTime)
    if total_time is None:
        return 'Unknown'
    elif total_time > 60:
        return 'Hard'
    elif 30 <= total_time <=60:
        return 'Medium'
    else:
        return 'Easy'
    
def add_difficulty(df):
    #difficulty
    df['difficulty']= df.apply(lambda row: determine_difficulty(row['cookTime'], row['prepTime']), axis=1)
    return df
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



if __name__ == "__main__":
    #Loading recipies.json file as a Pandas DataFrame.
    filepath="dataset/recipes.json"
    df=read_dataset(filepath)
    col_name="ingredients"
    target_word="chillies"
    df_filtered=filter_dataframe_by_word(df,col_name, target_word)
    df_difficulty=add_difficulty(df_filtered)
    df_difficulty.to_csv('output_file.csv', index=False)

    


