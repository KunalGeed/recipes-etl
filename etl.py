from filter_dataset import *
from find_difficulty import *
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


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
    
if __name__ == "__main__":
    #Loading recipies.json file as a Pandas DataFrame.
    filepath="dataset/recipes.json"
    df=read_dataset(filepath)
    col_name="ingredients"
    target_word="chillies"
    df_filtered=filter_dataframe_by_word(df,col_name, target_word)
    df_difficulty=add_difficulty(df_filtered)
    df_difficulty.to_csv('output_file.csv', index=False)

    


