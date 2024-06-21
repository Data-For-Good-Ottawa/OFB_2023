import os
from typing import Optional, Union
from Lib.console import print_warn, print_error

# Attempt to import csv
try:
    import csv
except ImportError:
    csv = None
    print_warn("Warning: csv module is not available. CSV file handling will not be supported.")

# Attempt to import pandas
try:
    import pandas as pd
except ImportError:
    pd = None
    print_warn("Warning: pandas library is not available. Data frame functionality will not be supported.")

# Attempt to import numpy
try:
    import numpy as np
except ImportError:
    np = None
    print_warn("numpy library is not available. NumPy array functionality will not be supported.")


# Define functions using imported libraries, checking for None before usage
def get_data_as_pandas_data_frame(file_path: str):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The loaded DataFrame, or an empty DataFrame if loading fails.
    """
    if pd is None:
        print_error("pandas library is not available.")
        return None

    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"'{file_path}' is not a valid file path.")

        if not file_path.endswith('.csv'):
            raise ValueError(f"'{file_path}' does not point to a CSV file.")

        df = pd.read_csv(file_path, encoding='utf-8')
        return df

    except Exception as e:
        print_error(f"An error occurred while loading the CSV file: {e}")
        return pd.DataFrame()


def get_data_as_numpy_array(file_path: str):
    """
    Load data from a text file into a NumPy array.

    Parameters:
    file_path (str): The path to the text file.

    Returns:
    np.ndarray: The loaded NumPy array, or an empty array if loading fails.
    """
    if np is None:
        print_error("numpy library is not available.")
        return None

    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Error: '{file_path}' is not a valid file path.")

        # Example assuming data is space-delimited
        data = np.loadtxt(file_path)
        return data

    except Exception as e:
        print_error(f"An error occurred while loading the data: {e}")
        return np.array([])


def get_csv_reader(file_path: str):
    """
    Load data from a CSV file and return a CSV reader object.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    csv.reader: A CSV reader object. Returns an empty reader if loading fails.
    """
    if csv is None:
        print_error("csv library is not available.")
        return None
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"'{file_path}' is not a valid file path.")

        # Open the CSV file and return the CSV reader object
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            return reader

    except Exception as e:
        print_error(f"An error occurred while loading the CSV file: {e}")
        # Return an empty CSV reader if an exception occurs
        return csv.reader([])  # Return an empty iterable (empty CSV reader)
