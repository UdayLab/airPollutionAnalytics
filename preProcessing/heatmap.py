import pandas as pd
"""
The pandas library provides data manipulation and analysis tools.

It is commonly used for handling and analyzing structured data, such as CSV files or database tables.
"""

import numpy as np
"""
The numpy library provides mathematical functions and tools for working with arrays and matrices.

It is commonly used for numerical computations and scientific computing tasks.
"""

import plotly.graph_objects as go
"""
The plotly.graph_objects module from the plotly library provides a high-level interface for creating interactive plots and visualizations.

It allows you to create a wide range of charts, maps, and other visualizations with customizable features.
"""

import re
"""
The re module provides regular expression matching operations for pattern searching and manipulation of strings.

It is commonly used for tasks such as string parsing, pattern matching, and text manipulation.
"""

class DataAnalyzer:
    def __init__(self, file_path):
        """
        Initialize an instance of the data analysis class.

        Args:
        - file_path (str): The path to the CSV file. This is a string representing the file path to the CSV file that will be analyzed.
        """
        self.file_path = file_path  # Store the file path as an instance variable
        self.condition = None  # Initialize the condition attribute to None
        self.threshold = None  # Initialize the threshold attribute to None
        self.df_coordinates = None  # Initialize the df_coordinates attribute to None

    def read_csv(self):
        """
        Read the CSV file and return a pandas DataFrame.

        Returns:
        - df (pd.DataFrame): The pandas DataFrame containing the data from the CSV file.
        """
        df = pd.read_csv(self.file_path)
        # Read the CSV file into a pandas DataFrame

        return df

    def select_columns(self, df, column_number):
        """
        Select the columns starting from the specified column number and return them as a list.

        Args:
        - df (pd.DataFrame): The pandas DataFrame. This is the DataFrame from which columns will be selected.
        - column_number (int): The starting column number. This is the column number from which the selection should start.

        Returns:
        - selected_columns (list): The list of selected column names excluding Timestamp. This is a list of column names starting from the specified column number, excluding the "Timestamp" column.
        """
        selected_columns = df.columns[column_number:]
        # Select the columns starting from the specified column number

        return selected_columns

    def convert_to_numpy(self, df, selected_columns):
        """
        Convert the selected columns of the DataFrame to a NumPy array and return it.

        Args:
        - df (pd.DataFrame): The pandas DataFrame. This is the DataFrame from which the selected columns will be converted to a NumPy array.
        - selected_columns (list): The list of selected column names. This is a list of column names that will be converted to a NumPy array.

        Returns:
        - data (np.ndarray): The selected columns as a NumPy array. This is a NumPy array containing the values of the selected columns from the DataFrame.
        """
        data = df[selected_columns].to_numpy()
        # Select the columns from the DataFrame and convert them to a NumPy array
        
        return data

    def count_rows_satisfying_condition(self, data, condition, threshold):
        """
        Count the number of rows in the data array that satisfy the given condition and threshold.

        Args:
        - data (np.ndarray): The data array. This is a numpy array containing the data to be analyzed.
        - condition (str): The condition to evaluate (e.g., '>', '<=', '=='). This is a string representing the condition to apply to the data.
        - threshold (int/float): The threshold value. This is the value against which the data will be compared.

        Returns:
        - counts (np.ndarray): The counts for each column that satisfy the condition. This is a numpy array containing the counts for each column that satisfies the given condition and threshold.
        """
        condition_met = eval(f"data {condition} {threshold}")
        # Evaluate the condition using the data array, condition, and threshold
        
        counts = np.sum(condition_met, axis=0)
        # Sum the rows that satisfy the condition along the specified axis (0 represents columns)

        return counts

    def create_hashmap(self, selected_columns, counts):
        """
        Create a hashmap by mapping the selected columns to their respective counts.

        Args:
        - selected_columns (list): The list of selected column names. This is a list of column names that will be used as keys in the hashmap.
        - counts (np.ndarray): The counts for each column. This is a NumPy array containing the counts for each column, in the same order as the selected_columns list.

        Returns:
        - hashmap (dict): The hashmap mapping column names to counts. This is a dictionary where the keys are the column names and the values are the corresponding counts.
        """
        hashmap = dict(zip(selected_columns, counts))
        # Create a hashmap by zipping the selected_columns list and the counts array
        return hashmap

    def analyze_data(self, condition, threshold, column_number):
        """
        Analyze the data by counting the number of rows that satisfy the given condition and threshold.

        Args:
        - condition (str): The condition to evaluate (e.g., '>', '<=', '==').
        - threshold (int/float): The threshold value.
        - column_number (int): The starting column number.

        Returns:
        - hashmap (dict): A hashmap mapping column names to counts.
        """
        self.condition = condition  # Set the condition attribute of the instance
        self.threshold = threshold  # Set the threshold attribute of the instance

        df = self.read_csv() # Read the CSV file
        
        selected_columns = self.select_columns(df, column_number)
        # Select the columns to analyze
        
        data = self.convert_to_numpy(df, selected_columns)
        # Convert the selected columns to a numpy array
        
        counts = self.count_rows_satisfying_condition(data, condition, threshold)
        # Count the rows satisfying the condition

        hashmap = self.create_hashmap(selected_columns, counts)
        # Create a hashmap mapping column names to counts

        return hashmap

    def extract_coordinates(self, condition, threshold, column_number):
        """
        Extract the latitude, longitude, and count from the data.

        Args:
        - condition (str): The condition to evaluate (e.g., '>', '<=', '==').
        - threshold (int/float): The threshold value.
        - column_number (int): The starting column number.

        Returns:
        - df_coordinates (pd.DataFrame): The DataFrame containing latitude, longitude, and count.
        """
        self.condition = condition  # Set the condition attribute of the instance
        self.threshold = threshold  # Set the threshold attribute of the instance
        df = self.read_csv()  # Read the CSV file into a pandas DataFrame

        data = {'latitude': [], 'longitude': [], 'count': []}
        # Initialize empty lists to store latitude, longitude, and count values

        for column_name in df.columns[1:]:
            # Iterate over the column names in the DataFrame, starting from the second column. This assumes that the first column does not contain coordinate data.

            matches = re.findall(r'\((.*?)\)', column_name)
            # Use a regular expression pattern to find all occurrences of latitude and longitude values enclosed in parentheses in the column name.
    
            if len(matches) > 0:
                longitude, latitude = map(float, matches[0].split())
                # Extract the latitude and longitude values from the matches list by splitting the string and converting them to float.

                data['latitude'].append(latitude)  # Append the latitude value to the latitude list
                data['longitude'].append(longitude)  # Append the longitude value to the longitude list

        data_array = self.convert_to_numpy(df, df.columns[column_number:])
        # Convert the selected columns from the DataFrame into a NumPy array using the convert_to_numpy method.

        counts = self.count_rows_satisfying_condition(data_array, self.condition, self.threshold)
        # Count the number of rows in the data array that satisfy the specified condition and threshold using the count_rows_satisfying_condition method.

        data['count'] = counts.tolist()
        # Convert the count values to a list and assign them to the 'count' key in the data dictionary.

        self.df_coordinates = pd.DataFrame(data)
        # Create a new DataFrame, df_coordinates, using the pd.DataFrame constructor from the pandas library. Pass the data dictionary as input to create the DataFrame.

        return self.df_coordinates
        # Return the df_coordinates DataFrame as the output of the method.
        
    def create_map(self):
        """
        Create a density map using latitude, longitude, and count data.

        Returns:
        - Map
        """

        # Filter the coordinates DataFrame to include only rows where the count is greater than 0.
        filtered_coordinates = self.df_coordinates[self.df_coordinates['count'] > 0]

        # Create the trace for the density map
        trace = go.Densitymapbox(
        lat=filtered_coordinates['latitude'],  # Latitude data
        lon=filtered_coordinates['longitude'],  # Longitude data
        z=filtered_coordinates['count'],  # Count data
        radius=10,  # Radius of each point
        colorscale='Viridis',  # Color scale for the map
        opacity=0.7,  # Opacity of each point
        hovertemplate='Latitude: %{lat}<br>Longitude: %{lon}<br>Count: %{z}<extra></extra>',  # Hover template for tooltip
        colorbar=dict(title='Count')  # Title for the colorbar
        )

        # Create the layout for the map
        layout = go.Layout(
        mapbox=dict(style='open-street-map'),  # Mapbox style
        margin=dict(l=0, r=0, t=0, b=0),  # Margin settings
        coloraxis_colorbar=dict(title='Count')  # Title for the color axis
        )

        # Create a Figure object with the trace and layout
        fig = go.Figure(data=[trace], layout=layout)

        # Display the figure in fullscreen mode
        fig.show(fullscreen=True)
        