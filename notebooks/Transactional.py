import pandas as pd
from PAMI.extras.DF2DB import denseDF2DB as pro

# Define a class for converting DataFrame to a Transactional Database
class DataFrameToTransactionalDB:
    def __init__(self, df, operator, threshold, output_filename):
        # Constructor to initialize class variables
        self.df = df
        self.operator = operator
        self.threshold = threshold
        self.output_filename = output_filename
        self.transactional_db = None

    def create_transactional_db(self):
        # Create an instance of the denseDF2DB class with DataFrame, operator, and threshold as arguments
        obj = pro.denseDF2DB(self.df, self.operator, self.threshold)

        # Call the createTransactional method of the denseDF2DB class to create the transactional database
        # The output will be saved to the specified output_filename
        obj.createTransactional(self.output_filename)

        # Store the name of the generated transactional database in the instance variable
        self.transactional_db = obj.getFileName()

