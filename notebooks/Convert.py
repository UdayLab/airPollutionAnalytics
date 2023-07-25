import pandas as pd
import operator

condition_operator = {
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne
}

class DenseDF2DB:
    def __init__(self, input_df, condition, threshold_value):
        self.input_df = input_df.iloc[:, :]
        self.condition = condition
        self.threshold_value = threshold_value
        self.output_file = ''

    def create_transactional(self, output_file):
        self.output_file = output_file
        if self.condition not in condition_operator:
            raise ValueError('Condition error')
        selected_columns = self.input_df.columns[
            condition_operator[self.condition](self.input_df.values, self.threshold_value).any(axis=0)
        ]
        selected_rows = self.input_df.index[
            condition_operator[self.condition](self.input_df.values, self.threshold_value).any(axis=1)
        ]
        selected_df = self.input_df.loc[selected_rows, selected_columns]
        selected_df.to_csv(output_file, sep=',', header=False, index=False)

    def get_file_name(self):
        return self.output_file
