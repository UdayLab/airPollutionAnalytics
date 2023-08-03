import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class DataImputer:
    def __init__(self, input_file, output_file):
        """
        Initialize the DataImputer class with input and output file paths.
        
        Parameters:
        - input_file (str): Path to the input CSV file.
        - output_file (str): Path to the output CSV file.
        """
        self.input_file = input_file
        self.output_file = output_file
        
    def load_data(self):
        """
        Load the data from the input CSV file.
        
        Returns:
        - data (pd.DataFrame): DataFrame containing the loaded data.
        """
        data = pd.read_csv(self.input_file)
        return data
        
    def replace_zeros_with_none(self, data):
        """
        Replace zeros with None in the DataFrame.
        
        Parameters:
        - data (pd.DataFrame): DataFrame to replace zeros in.
        
        Returns:
        - data (pd.DataFrame): DataFrame with zeros replaced by None.
        """
        # Replace zeros in all columns except the first column with None
        data = data.replace(0.0, None)
        return data
        
    def impute_missing_values(self, data):
        """
        Impute missing values in the DataFrame using linear regression.
        
        Parameters:
        - data (pd.DataFrame): DataFrame to impute missing values in.
        
        Returns:
        - imputed_data (pd.DataFrame): DataFrame with imputed missing values.
        """
        # Create a copy of the original data to avoid modifying it
        imputed_data = data.copy()
        
        # Get the column names of the DataFrame
        columns = imputed_data.columns

        # Iterate over each column except the first column
        for column in columns:
            # Find the indices where the values are missing
            missing_indices = imputed_data[column].isnull()
            
            # Find the indices where the values are not missing
            non_missing_indices = ~missing_indices

            # Create the feature matrix X using the non-missing indices
            X = np.where(non_missing_indices)[0].reshape(-1, 1)
            
            # Create the target vector y using the non-missing values
            y = np.array(imputed_data[column])[non_missing_indices]

            # Create a linear regression model
            regression_model = LinearRegression()
            
            # Fit the model using the feature matrix X and target vector y
            regression_model.fit(X, y)

            # Predict the missing values using the missing indices
            imputed_data.loc[missing_indices, column] = regression_model.predict(np.where(missing_indices)[0].reshape(-1, 1))

        return imputed_data
        
    def save_output(self, data):
        """
        Save the DataFrame to the output CSV file.
        
        Parameters:
        - data (pd.DataFrame): DataFrame to save.
        """
        # Save the DataFrame to the specified output file
        data.to_csv(self.output_file, index=False)
        
        # Print a success message
        print("Output saved")


