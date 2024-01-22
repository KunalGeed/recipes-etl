import re
from typing import Union
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np

def calculate_total_time(cookTime, prepTime) -> Union[int, None]:
    """
    Calculate the total time in minutes based on cookTime and prepTime.

    Parameters:
    - cookTime (str): The cooking time in ISO 8601 duration format.
    - prepTime (str): The preparation time in ISO 8601 duration format.

    Returns:
    - Union[int, None]: Total time in minutes or None if both cookTime and prepTime are empty.
    """
    total_time = 0

    # Check if both cookTime and prepTime are empty
    if (not cookTime or cookTime == "PT") and (not prepTime or prepTime == "PT"):
        return None

    # Calculate cooking time in minutes
    if not cookTime or cookTime == "PT":
        cookmins = 0
    else:
        minutes_match = re.search(r'(\d+)M', cookTime)
        hours_match = re.search(r'(\d+)H', cookTime)
        hours = int(hours_match.group(1)) * 60 if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        cookmins = minutes + hours

    # Calculate preparation time in minutes
    if not prepTime or prepTime == "PT":
        prepmins = 0
    else:
        minutes_match = re.search(r'(\d+)M', prepTime)
        hours_match = re.search(r'(\d+)H', prepTime)
        hours = int(hours_match.group(1)) * 60 if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        prepmins = minutes + hours

    return cookmins + prepmins

def determine_difficulty(cookTime, prepTime):
    """
    Determine the difficulty level based on total time.

    Parameters:
    - cookTime (str): The cooking time from recipies.json.
    - prepTime (str): The preparation time recipies.json.

    Returns:
    - str: Difficulty level ('Unknown', 'Easy', 'Medium', 'Hard').
    """
    total_time = calculate_total_time(cookTime, prepTime)

    # Determine difficulty level
    if total_time is None:
        return 'Unknown'
    elif total_time > 60:
        return 'Hard'
    elif 30 <= total_time <= 60:
        return 'Medium'
    else:
        return 'Easy'

def add_difficulty(df):
    """
    Add a 'difficulty' column to a DataFrame based on 'cookTime' and 'prepTime' columns.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: DataFrame with an added 'difficulty' column.
    """
    # Check if the DataFrame is empty
    if df.empty:
        return df  # Return the empty DataFrame
    # Add 'difficulty' column using determine_difficulty function
    df['difficulty'] = df.apply(lambda row: determine_difficulty(row['cookTime'], row['prepTime']), axis=1)
    return df
