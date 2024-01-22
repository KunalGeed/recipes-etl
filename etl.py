import pandas as pd
from filter_dataset import filter_dataframe_by_word
from find_difficulty import add_difficulty

# Disable the warning for chained assignments
pd.options.mode.chained_assignment = None

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
    # Loading recipes.json file as a Pandas DataFrame.
    filepath = "dataset/recipes.json"
    df = read_dataset(filepath)

    # Filtering DataFrame based on the 'ingredients' column and the target word 'chillies'.
    col_name = "ingredients"
    target_word = "chillies"
    df_filtered = filter_dataframe_by_word(df, col_name, target_word)

    # Adding a 'difficulty' column to the filtered DataFrame.
    df_difficulty = add_difficulty(df_filtered)

    # Saving the resulting DataFrame to an output CSV file.
    df_difficulty.to_csv('output_file.csv', index=False)
