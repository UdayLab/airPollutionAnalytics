"""
This module provides functionality for finding frequent Patterns with thr help of Apriori, FPGrowth, and ECLAT.

The pandas library is imported as 'pd' to provide an easy-to-use data manipulation and analysis tool. It provides data structures like DataFrame and Series, which allow for efficient handling of tabular data.

The Apriori is imported as alg. Apriori is one of the fundamental algorithm to discover frequent patterns in a transactional database. This program employs apriori property (or downward closure property) to  reduce the search space effectively. This algorithm employs breadth-first search technique to find the complete set of frequent patterns in a transactional database.

FPGrowth is imported from PAMI.frequentPattern.basic as algo. FPGrowth is one of the fundamental algorithm to discover frequent patterns in a transactional database. It stores the database in compressed fp-tree decreasing the memory usage and extracts the patterns from tree.It employs employs downward closure property to  reduce the search space effectively.

ECLAT is imported from PAMI.frequentPattern.basic as algor. ECLAT is one of the fundamental algorithm to discover frequent patterns in a transactional database.

Plotly is imported as px. Plotly's Python graphing library makes interactive, publication-quality graphs. Examples of how to make line plots, scatter plots, area charts, bar charts, error bars, box plots, histograms, heatmaps, subplots, multiple-axes, polar charts, and bubble charts.
"""
import pandas as pd
import PAMI.frequentPattern.basic.Apriori as alg
from PAMI.frequentPattern.basic import FPGrowth as algo
from PAMI.frequentPattern.basic import ECLAT as algor
import plotly.express as px

class FrequentPatternAnalysis:
    """
    A class for analysing frequent patterns in a CSV file.

    This class provides methods to read a CSV file into a pandas DataFrame, convert zero into None value. 
    replace missing values with vales calculated through linear regeression.
    save output in another CSV file.
    """
    def __init__(self, input_file, min_sup_list, sep):
        """
        Initialize the FrequentPatternAnalysis object with the given csv_file and min_sup_list
        
        Args:
        input_file (str): The path to the input CSV file
        min_sup_list (str): The mimimum Support list
        sep (str): The seprator that is used in list
        """
        self.input_file = input_file
        self.min_sup_list = min_sup_list
        self.sep = sep
        self.result = pd.DataFrame(columns=['algorithm', 'minSup', 'pattern', 'runtime', 'memory'])

    @staticmethod
    def prepare_input_file(input_file, output_file, num_rows, num_columns):
        """
        Read the CSV file, Tranform data data into output file according to number of rows and columbs provided. 
        
        Args:
        input_file (str): The Path to the Input File 
        output_file (str): The Path to the Output File
        num_rows (int): Number of rows selected 
        num_columns (int): Number of Columns selected 
        """
        df = pd.read_csv(input_file)
        df_subset = df.iloc[:num_rows, :num_columns]
        df_subset.to_csv(output_file, index=False)

    def run_analysis(self):
        """
        Apply differnt algoritumns on the data provided and print the result  
        """
        algorithms = {
            'Apriori': alg.Apriori,
            'FPGrowth': algo.FPGrowth,
            'ECLAT': algor.ECLAT
        }
        
        for algorithm, algorithm_class in algorithms.items():
            for min_sup in self.min_sup_list:
                obj = algorithm_class(self.input_file, minSup=min_sup, sep=self.sep)
                obj.startMine()
                df = pd.DataFrame([algorithm, min_sup, len(obj.getPatterns()), obj.getRuntime(), obj.getMemoryRSS()], index=self.result.columns).T
                self.result = self.result._append(df, ignore_index=True)
        print(self.result)

    def plot_results(self):
        """
        plot the result on canvas using plotly module

        returns:
        A canvas with graph on it. 
        """
        fig_pattern = px.line(self.result, x='minSup', y='pattern', color='algorithm', markers=True)
        fig_pattern.show()

        fig_runtime = px.line(self.result, x='minSup', y='runtime', color='algorithm', markers=True)
        fig_runtime.show()

        fig_memory = px.line(self.result, x='minSup', y='memory', color='algorithm', markers=True)
        fig_memory.show()

