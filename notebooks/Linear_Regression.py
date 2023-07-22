"""
This module provides functionality for data imputing using sklearn with the help of pandas and numpy.

The pandas library is imported as 'pd' to provide an easy-to-use data manipulation and analysis tool. It provides data structures like DataFrame and Series, which allow for efficient handling of tabular data.

The numpy library is imported as 'np' to provide support for numerical operations and array manipulation. It offers a wide range of mathematical functions and allows for efficient computation on large arrays of data.

The LinearRegression is imported from sklearn.linear_model. Scikit-learn (Sklearn) provides a selection of efficient tools for machine learning and statistical modeling including classification, regression, clustering and dimensionality reduction via a consistence interface in Python.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class DataImputer:
    """
    A class for imputing missing values in CSV file.

    This class provides methods to read a CSV file into a pandas DataFrame, convert zero into None value. 
    replace missing values with vales calculated through linear regeression.
    save output in another CSV file.
    """

    def __init__(self, input_file, output_file):
        """
        Initialize the DataImputer object with the given csv_file and output_file
        
        Args:
        input_file (str): The path to the input CSV file
        output_file (str): The path to the output CSV file
        """
        self.input_file = input_file
        self.output_file = output_file
        
    def load_data(self):
        """
        Read the CSV file into a DataFrame
        
        Returns:
        DataFrame: The DataFrame containing the data from the CSV file
        """
        data = pd.read_csv(self.input_file)
        return data
        
    def replace_zeros_with_none(self, data):
        """
        replace all zeros with None from the DataFrame
        
        Args:
        data (DataFrame): The input DataFrame
        
        Returns:
        DataFrame: The DataFrame with the zero replaced with None
        """
        data.iloc[:, 1:] = data.iloc[:, 1:].replace(0.0, None)
        return data
        
    def impute_missing_values(self, data):
        """
        impute missing vales with values calculated through linear regression

        args:
        data (DataFrame): The input Dataframe

        Returns:
        DataFrame: The DataFrame with imputed values through linear regression 
        """
        imputed_data = data.copy()
        columns = imputed_data.columns[1:]  # Exclude the first column (ID column)

        for column in columns:
            missing_indices = imputed_data[column].isnull()
            non_missing_indices = ~missing_indices

            X = np.where(non_missing_indices)[0].reshape(-1, 1)
            y = np.array(imputed_data[column])[non_missing_indices]

            regression_model = LinearRegression()
            regression_model.fit(X, y)

            imputed_data.loc[missing_indices, column] = regression_model.predict(np.where(missing_indices)[0].reshape(-1, 1))

        return imputed_data
        
    def save_output(self, data):
        """
        Save the DataFrame to a CSV file
        
        Args:
        data (DataFrame): The DataFrame to be saved
        """
        data.to_csv(self.output_file, index=False)
        print("Output saved in ", self.output_file)