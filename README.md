
# Recipes ETL

## Overview

This Python script, `etl.py`, is designed to perform ETL (Extract, Transform, Load) operations on a dataset of Open Recipes. The script filters recipes based on the presence of the word "Chilies" in the ingredients and adds a "difficulty" field to each extracted recipe. The difficulty is determined based on the sum of prepTime and cookTime. The resulting dataset is saved as a CSV file.

## Prerequisites

- Python 3.x (specifically 3.10.5)
- Required Python packages are listed in `requirements.txt`. Install them using:

    ```
    pip install -r requirements.txt
    ```
- If unable to install using the above command, please install all using
      ```
      pip install {package_name} == {package_version}
      ```
## Set-Up

1. Clone the repository or download it from GitHub:

    ```bash
    git clone https://github.com/KunalGeed/recipes-etl.git
    ```

2. Navigate to the `recipes-etl` directory:

    ```bash
    cd recipes-etl
    ```
3.  If you want, create a virtual python environment via 
     ```bash
     py -m venv venv
     ```
     (or equivalent command on your device).

     Please also activate the virtual enviroment you create. This can be done using the command
     ```bash
     venv/Scripts/Activate.ps1
     ```

4. Install all the required packages as stated in `requirements.txt`. Install them using:

    ```
    pip install -r requirements.txt
    ```


7. View the output:

    The resulting CSV file, `test_output.csv`, will be generated in the same directory.

## Instructions

1. **Dataset Download:**
    - Download the [Open Recipes dataset](link-to-dataset) and save it as `dataset/recipes.json`. If the file is already there, then no need.

2. **Script Execution:**
    - The main script is `etl.py`. Open a terminal and navigate to the `recipes-etl` directory.
    - Run the script using the command `python etl.py`. 
    - You can open the file in your code editor and run the file that way, incase terminal in not working for you.
    - This will execute the script, extract recipes with "Chilies" as an ingredient, determine difficulty, and save the resulting dataset as `test_output.csv`. 
    - If you want to search for a different ingredient, please open etl.py. On line 48 you can edit the variable `target_word` to whatever you want.
    - Please note that if you already have an existing `test_output.csv` file in the folder, then it is possible of it raising a permission denied error. Please rename the csv and run the code to generate a new one.

3. **Output:**
    - The script will create a CSV file, `test_output.csv`, containing the filtered and processed recipes. The version generated on my local machine is in `local_output.csv.`
`
4. **Requirements:**
    - Ensure that the required Python packages are installed using the `pip install -r requirements.txt` command.

5. **Python Version:**
    - The script is designed to work with Python 3.x. (Specifically Python 3.10.5)

## Dependencies

- pandas
- fuzzywuzzy
- numpy


## File Structure and Functions

### etl.py

- **File Purpose:**
  - `etl.py` is the main script responsible for extracting, transforming, and loading the Open Recipes dataset.

- **Functions:**
  1. **`read_dataset(filepath, lines=True)`**: Reads the dataset from the specified file path, supporting both JSON and CSV formats.
  2. **Main Block:**
      - Loads the `recipes.json` file as a Pandas DataFrame.
      - Filters the DataFrame based on the 'ingredients' column and the target word 'chillies'.
      - Adds a 'difficulty' column to the filtered DataFrame.
      - Saves the resulting DataFrame to an output CSV file.

### filter_dataset.py

- **File Purpose:**
  - `filter_dataset.py` contains functions related to filtering a DataFrame based on a target word.

- **Functions:**
  1. **`has_target_word_single(string, target_word)`**: Checks if a string contains a target word with fuzzy matching.
  2. **`has_target_word_multiple(string, target_word)`**: Checks if a string contains multiple target words with fuzzy matching.
  3. **`filter_dataframe_by_word(df, column_name: str, target_word: str)`**: Filters a DataFrame based on a specific word in a specified column.

### find_difficulty.py

- **File Purpose:**
  - `find_difficulty.py` contains functions related to calculating the difficulty level based on total time.

- **Functions:**
  1. **`calculate_total_time(cookTime, prepTime)`**: Calculates the total time in minutes based on cookTime and prepTime.
  2. **`determine_difficulty(cookTime, prepTime)`**: Determines the difficulty level based on total time.
  3. **`add_difficulty(df)`**: Adds a 'difficulty' column to a DataFrame based on 'cookTime' and 'prepTime' columns.

## How It Works

### Task 1: Extract Recipes with "Chilies" as an Ingredient

- **Challenge:**
  - The requirement to account for misspellings and different variations of the word "Chilies" makes a simple word search approach impractical.

- **Approach:**
  - **Fuzzy Matching:**
    - Regular expressions are powerful but may not cover all variations and possible spelling mistakes.
    - Utilizing the `fuzzywuzzy` library in Python for fuzzy string matching provides a robust solution.
      - The `fuzz.ratio` function computes the similarity between two strings, allowing for variations and typos.
    - Key components of the approach include:
      - **Character Matching:**
        - The algorithm compares each character in the two strings, adding a score for matching characters.
      - **Positional Matching:**
        - Positions of matching characters are considered, with closer positions contributing more to the similarity score.
      - **Score Calculation:**
        - The similarity score is normalized to a percentage by dividing it by the total possible score.
    - For optimal performance, the target word is compared to each individual word in the string containing ingredients.

### Task 2: Calculate Difficulty Based on prepTime and cookTime

- **Data Format:**
  - The data in the `prepTime` and `cookTime` columns use the format PTxHyM, where x and y represent hours and minutes, respectively.

- **Parsing Strategy:**
  - We parse the string to extract the minutes and hours for both `prepTime` and `cookTime`.
  - In cases where BOTH `prepTime` and `cookTime` are null (missing), the recipe is classified as "Unknown" difficulty.

- **Difficulty Classification:**
  - Based on the total time calculated, we classify the difficulty as follows:
    - **Unknown:**
      - If both `prepTime` and `cookTime` are null.
    - **Easy:**
      - If the total time is less than 30 minutes.
    - **Medium:**
      - If the total time is between 30 minutes and 1 hour.
    - **Hard:**
      - If the total time is greater than 1 hour.





