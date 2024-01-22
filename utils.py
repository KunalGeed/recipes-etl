import pandas as pd

def read_dataset(filepath):
    """
    Read the dataset from the specified file path.

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
            df = pd.read_json(filepath)
        elif file_extension in ['csv', 'txt']:
            df = pd.read_csv(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except ValueError as ve:
        print(ve)
        return None
    except Exception as e:
        print(f"An error occurred while reading the dataset: {e}")
        return None