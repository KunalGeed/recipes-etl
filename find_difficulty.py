
import re
from typing import Union
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np

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

