"""
This module provides functionality for data analysis using pandas.

The pandas library is imported as 'pd' to provide an easy-to-use data manipulation and analysis tool. It provides data structures like DataFrame and Series, which allow for efficient handling of tabular data.

"""
import pandas as pd

class DataAnalyzer:
    """
    A class for analyzing data from a CSV file.

    This class provides methods to read a CSV file into a pandas DataFrame, select columns to be analyzed,
    convert the DataFrame to a numpy array, count the number of rows satisfying a condition for each column,
    remove the columns which are not satisfing the threshold value.
    """

    def __init__(self, csv_file, output_file):
        """
        Initialize the DataAnalyzer object with the given csv_file and output_file
        
        Args:
        csv_file (str): The path to the input CSV file
        output_file (str): The path to the output CSV file
        """
        self.csv_file = csv_file
        self.output_file = output_file
    
    def read_csv(self):
        """
        Read the CSV file into a DataFrame
        
        Returns:
        df (DataFrame): The DataFrame containing the data from the CSV file
        """
        self.df = pd.read_csv(self.csv_file)
        return self.df

    def filter_columns(self, zero_value, threshold):
        """
        filter the columns on which will be analizing 

        Args:
        zero_value: value that will be replaced
        threshold: threshold vlaue 

        Returns:
        filtered_columns: columns satisfying threshold condition     
        """
        total_rows = self.df.shape[0]
        zero_rows = (self.df == zero_value).sum()
        filtered_columns = self.df.columns[(zero_rows / total_rows) <= threshold]
        return filtered_columns

    def apply_condition(self, find_value, operator):
        """
        apply the condition given in argument 

        Agrs:
        find_value: on which the condition will apply
        operator: operator that is used 
        """        
        condition = f"self.df.iloc[:, 1:].apply(lambda x: any(x {operator} {find_value}))"
        columns_to_drop = self.df.columns[1:][eval(condition)]
        self.df = self.df.drop(columns=columns_to_drop)

    def save_to_csv(self):
        """
        Save the DataFrame to a CSV file
        """
        self.df.to_csv(self.output_file, index=False)
        print("Saved in ",self.output_file)

    def process_csv(self, find_value, operator, zero_value, threshold):
        """
        process the csv file according to condition given in arguments. and call sav_to_csv Function and save the file.

        Args:
        find_value: value on which contion will apply
        operator: operator that will be used 
        zero_value: value that will be replaced
        threshold: threshold vlaue

        """
        self.read_csv()
        filtered_cols = self.filter_columns(zero_value, threshold)
        self.df = self.df[filtered_cols]
        self.apply_condition(find_value, operator)
        self.save_to_csv()
        
        



