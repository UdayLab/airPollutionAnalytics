import PAMI.extras.dbStats.transactionalDatabaseStats as stats
# Importing the transactionalDatabaseStats module
import pandas as pd
# Importing the pandas library for data manipulation
import re
# Importing the re module for regular expressions
import plotly.graph_objects as go
# Importing the plotly library for creating interactive visualizations

class HeatmapCreator:
    def __init__(self, csv_file):
        """
        Initializes the HeatmapCreator class.

        Parameters:
        - csv_file (str): The path to the CSV file containing the data.
        """
        self.csv_file = csv_file

    def extract_data(self):
        """
        Extracts the longitude, latitude, and count data from the CSV file.
        """
        pattern = r"Point\(([-\d.]+) ([-\d.]+)\)\s+(\d+)"  # Regular expression pattern to extract the data
        data = {
            'longitude': [],
            'latitude': [],
            'count': []
        }  # Dictionary to store the extracted data
        df = pd.read_csv(self.csv_file, header=None)  # Reading the CSV file into a pandas DataFrame
        for index, row in df.iterrows():
            row_str = ' '.join(row.astype(str))  # Converting the row to a string
            matches = re.findall(pattern, row_str)  # Finding all matches of the pattern in the row string
            for match in matches:
                longitude = float(match[0])  # Extracting the longitude from the match
                latitude = float(match[1])  # Extracting the latitude from the match
                count = int(match[2])  # Extracting the count from the match
                data['longitude'].append(longitude)
                data['latitude'].append(latitude)
                data['count'].append(count)
        self.filtered_coordinates = pd.DataFrame(data)  # Creating a DataFrame from the extracted data
        print(self.filtered_coordinates)

    def create_map(self):
        """
        Creates a heatmap using the extracted data and displays it.
        """
        self.extract_data()  # Extracting the data from the CSV file
        trace = go.Densitymapbox(
            lon=self.filtered_coordinates['longitude'],  # Setting the longitude values for the heatmap
            lat=self.filtered_coordinates['latitude'],  # Setting the latitude values for the heatmap
            z=self.filtered_coordinates['count'],  # Setting the count values for the heatmap
            radius=10,  # Setting the radius of each heatmap point
            colorscale='Viridis',  # Setting the colorscale for the heatmap
            opacity=0.7,  # Setting the opacity of the heatmap
            hovertemplate='longitude: %{lon}<br>latitude: %{lat}<br>Count: %{z}<extra></extra>',
            # Setting the hover template for the heatmap
            colorbar=dict(title='Count')  # Setting the title for the colorbar
        )
        layout = go.Layout(
            mapbox=dict(style='open-street-map'),  # Setting the style of the mapbox
            margin=dict(l=0, r=0, t=0, b=0),  # Setting the margins of the layout
            coloraxis_colorbar=dict(title='Count')  # Setting the title for the colorbar in the layout
        )
        fig = go.Figure(data=[trace], layout=layout)  # Creating the figure object
        fig.show(fullscreen=True)  # Displaying the figure in fullscreen

def save_item_frequencies(input_file, item_frequencies_output, transactionLength_output, sep):
    """
    Saves the item frequencies and transaction length distribution of a transactional database to CSV files.

    Parameters:
    - input_file (str): The path to the input CSV file.
    - item_frequencies_output (str): The path to save the item frequencies CSV file.
    - transactionLength_output (str): The path to save the transaction length distribution CSV file.
    - sep (str): The separator used in the input CSV file.
    """
    obj = stats.transactionalDatabaseStats(input_file, sep)
    # Creating an instance of the transactionalDatabaseStats class
    obj.run()  # Running the analysis on the input file
    item_frequencies = obj.getSortedListOfItemFrequencies()  # Getting the sorted list of item frequencies
    transactionLength = obj.getTransanctionalLengthDistribution()  # Getting the transaction length distribution

    obj.printStats()  # Printing the statistics
    obj.plotGraphs()  # Plotting the graphs
    obj.save(item_frequencies, item_frequencies_output)  # Saving the item frequencies to a CSV file
    obj.save(transactionLength, transactionLength_output)  # Saving the transaction length distribution to a CSV file


