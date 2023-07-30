import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, csv_file, output_file):
        """
        Initialize the DataProcessor object with the given csv_file and output_file
        
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
        DataFrame: The DataFrame containing the data from the CSV file
        """
        df = pd.read_csv(self.csv_file)
        return df
    
    def remove_columns(self, df, column_numbers):
        """
        Remove specific columns from the DataFrame
        
        Args:
        df (DataFrame): The input DataFrame
        column_numbers (list): The list of column numbers to remove
        
        Returns:
        DataFrame: The DataFrame with the specified columns removed
        """
        df.drop(df.columns[column_numbers], axis=1, inplace=True)
        return df
    
    def fill_missing_values(self, df, missing_value):
        """
        Fill missing values in the DataFrame with the provided missing value
        
        Args:
        df (DataFrame): The input DataFrame
        missing_value: The value to fill in for missing values
        
        Returns:
        DataFrame: The DataFrame with missing values filled
        """
        df.fillna(missing_value, inplace=True)
        return df
    
    def apply_condition(self, df, conditional_operator, condition_value, new_value):
        """
        Apply a condition to the DataFrame and replace values based on the condition
        
        Args:
        df (DataFrame): The input DataFrame
        conditional_operator (str): The operator to use for the condition (e.g., '>', '<=', '==')
        condition_value: The value to use in the condition
        new_value: The value to replace in the DataFrame if the condition is True
        
        Returns:
        DataFrame: The DataFrame with values replaced based on the condition
        """
        condition_value = float(condition_value)  # Convert condition_value to float
        mask = eval(f"df.iloc[:, 1:].astype(float) {conditional_operator} condition_value")
        df.iloc[:, 1:] = np.where(mask, new_value, df.iloc[:, 1:])
        return df
    
    def replace_missing_point(self, df, missing_point):
        """
        Replace missing Latitude Longitude values in the DataFrame
        
        Args:
        df (DataFrame): The input DataFrame
        missing_point (str): The value to replace missing Latitude Longitude values
        
        Returns:
        DataFrame: The DataFrame with missing Latitude Longitude values replaced
        """
        f = lambda x: missing_point.format(int(x.split()[1])+1) if 'Unnamed' in x else x
        df = df.rename(columns=f)
        return df
    
    def save_to_csv(self, df):
        """
        Save the DataFrame to a CSV file
        
        Args:
        df (DataFrame): The DataFrame to be saved
        """
        df.to_csv(self.output_file, index=False)
        print("Saved")
    
    def process_data(self, column_numbers, missing_value, conditional_operator, condition_value, new_value, missing_point):
        """
        Process the data in the CSV file with the provided parameters
        
        Args:
        column_numbers (list): The list of column numbers to remove from the DataFrame
        missing_value: The value to fill in for missing values in the DataFrame
        conditional_operator (str): The operator to use for the condition (e.g., '>', '<=', '==')
        condition_value: The value to use in the condition
        new_value: The value to replace in the DataFrame if the condition is True
        missing_point (str): The value to replace missing Latitude Longitude values
        """
        df = self.read_csv()
        df = self.remove_columns(df, column_numbers)
        df = self.fill_missing_values(df, missing_value)
        df = self.apply_condition(df, conditional_operator, condition_value, new_value)
        df = self.replace_missing_point(df, missing_point)
        self.save_to_csv(df)


