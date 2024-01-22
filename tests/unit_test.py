"""
Unit Tests for Recipe ETL Script

This file contains unit tests for the Python script that performs ETL (Extract, Transform, Load) on the Open Recipes dataset.
The script filters recipes containing "Chilies" (and variations) as ingredients, calculates the difficulty of each recipe,
and saves the resulting dataset as a CSV file.

Test coverage includes:
1. Downloading the dataset.
2. Filtering recipes based on ingredient "chillies".
3. Calculating difficulty values.
4. Verifying the structure of the output CSV file.
5. Ensuring correct handling of edge cases.
6. Checking script readability and comments.
"""

import unittest
import os
import pandas as pd