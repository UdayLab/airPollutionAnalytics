import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, csv_file, output_file):
        """
        Initialize the DataProcessor class with the input CSV file and the output file path.
        
        Parameters:
        - csv_file (str): The path to the input CSV file.
        - output_file (str): The path to the output file where the processed data will be saved.
        """
        self.csv_file = csv_file
        self.output_file = output_file
    
    def read_csv(self):
        """
        Read the CSV file and return a pandas DataFrame.
        
        Returns:
        - df (pandas.DataFrame): The DataFrame created from the CSV file.
        """
        df = pd.read_csv(self.csv_file)
        return df
    
    def remove_columns(self, df, column_number):
        """
        Remove columns from the DataFrame based on the given column numbers.
        
        Parameters:
        - df (pandas.DataFrame): The DataFrame from which columns will be removed.
        - column_number (list): A list of column numbers to be removed.
        
        Returns:
        - df (pandas.DataFrame): The DataFrame with the specified columns removed.
        """
        df.drop(df.columns[column_number], axis=1, inplace=True)
        return df
    
    def fill_missing_values(self, df, missing_value_replace):
        """
        Fill missing values in the DataFrame with the given value.
        
        Parameters:
        - df (pandas.DataFrame): The DataFrame in which missing values will be filled.
        - missing_value_replace (any): The value to be used for filling missing values.
        
        Returns:
        - df (pandas.DataFrame): The DataFrame with missing values filled.
        """
        df.fillna(missing_value_replace, inplace=True)
        return df
    
    def apply_condition(self, df, conditional_operator, condition_value, condition_value_replace):
        """
        Apply a condition to the DataFrame and replace values with a new value based on the condition.
        
        Parameters:
        - df (pandas.DataFrame): The DataFrame on which the condition will be applied.
        - conditional_operator (str): The operator to be used in the condition (e.g., '>', '<=', '==').
        - condition_value (any): The value to be used in the condition.
        - condition_value_replace (any): The value to replace the existing values that satisfy the condition.
        
        Returns:
        - df (pandas.DataFrame): The DataFrame with values replaced based on the condition.
        """
        # Create a mask based on the condition
        mask = df.iloc[:, 1:].apply(lambda x: eval(f'x {conditional_operator} {condition_value}'))
        # Replace values based on the mask
        df.iloc[:, 1:] = np.where(mask, condition_value_replace, df.iloc[:, 1:])
        return df
    
    def Removing_abnormal_values(self, df, thres_value, operator):
        """
        Remove abnormal values by replacing them with 0.

        Args:
        df (pd.DataFrame): Input DataFrame with numeric data.
        thres_value (float): Threshold value for comparison.
        operator (str): Comparison operator ("<", ">", "<=", ">=", "==", "!=").

        Returns:
        pd.DataFrame: DataFrame with abnormal values replaced by 0.
        """
        # Create a mask based on the condition
        mask = df.iloc[:, 1:].apply(lambda x: eval(f'x {operator} {thres_value}'))
        # Replace values based on the mask
        df.iloc[:, 1:] = np.where(mask,0, df.iloc[:, 1:])
        return df
    
    def delete_missing_point(self,df):
        """
        Deletes columns with 'Unnamed' in their names from the given DataFrame.
        
        Parameters:
        df (pandas.DataFrame): The DataFrame from which columns with 'Unnamed' in their names will be deleted.
        
        Returns:
        pandas.DataFrame: The DataFrame with 'Unnamed' columns removed.
        """
        sensorsWithPointInformation = [col for col in df if 'Unnamed' in col]
        df.drop(columns=sensorsWithPointInformation, inplace=True, axis=1)
        return df
    
    def filter_columns(self, df, value_check, threshold_per):
        """
        Filter columns based on the percentage of zero values in each column.
        
        Parameters:
        - df (pandas.DataFrame): The DataFrame from which columns will be filtered.
        - value_check (any): The value considered as zero.
        - threshold_per (float): The maximum percentage of zero values allowed.
        
        Returns:
        - df (pandas.DataFrame): The DataFrame with columns filtered based on zero value percentage.
        """
        # Calculate the number of zero rows for each column
        zero_rows = (df == value_check).sum()
        # Calculate the percentage of zero rows for each column
        zero_percentage = zero_rows / df.shape[0]
        # Get the columns that have zero below the threshold_per
        filtered_columns = df.columns[zero_percentage <= threshold_per]
        return df[filtered_columns]
    
    def save_to_csv(self, df):
        """
        Save the DataFrame to a CSV file.
        
        Parameters:
        - df (pandas.DataFrame): The DataFrame to be saved.
        """
        df.to_csv(self.output_file, index=False)
        print("Saved")
    
    
    def process_data(self, thres_value, operator, column_number, missing_value_replace, conditional_operator, condition_value, condition_value_replace, value_check, threshold_per):
        """
        Process the data by applying various transformations to the DataFrame.
        
        Parameters:
        - thres_value (any): The value to be used in the condition for replacing abnormal values with 0.
        - operator (str): The operator to be used in the condition for replacing abnormal value (e.g., '>', '<=', '==').
        - column_number: column number to be removed.
        - missing_value_replace (any): The value to be used for filling missing values.
        - conditional_operator (str): The operator to be used in the condition for applying values.
        - condition_value (any): The value to be used in the condition for applying values.
        - condition_value_replace (any): The value to replace the existing values that satisfy the condition.
        - value_check (any): The value considered as zero.
        - threshold_per (float): The maximum percentage of zero values allowed.
        """
        # Read the CSV file and obtain the initial DataFrame
        df = self.read_csv()
        # Remove specified columns from the DataFrame
        df = self.remove_columns(df, column_number)
        # Fill missing values in the DataFrame
        df = self.fill_missing_values(df, missing_value_replace)
        # Apply a condition to the DataFrame and replace values based on the condition
        df = self.apply_condition(df, conditional_operator, condition_value, condition_value_replace)
        # Replace abnormal values with 0
        df = self.Removing_abnormal_values(df, thres_value, operator)
        # Replace missing point column names in the DataFrame
        df = self.delete_missing_point(df)
        # Filter columns based on the percentage of zero values
        df = self.filter_columns(df, value_check, threshold_per)
        # Save the processed DataFrame to a CSV file
        self.save_to_csv(df)