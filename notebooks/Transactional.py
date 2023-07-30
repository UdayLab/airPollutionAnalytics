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

class denseDF2DB:
    def __init__(self, inputDF, condition, threshold):
        self.inputDF = inputDF
        self.condition = condition
        self.threshold = threshold
        self.tids = list(self.inputDF.index)
        self.items = list(self.inputDF.columns.values)
        self.outputFile = ' '

    def createTransactional(self, outputFile):
        self.outputFile = outputFile
        with open(outputFile, 'w') as f:
            if self.condition not in condition_operator:
                print('Condition error')
            else:
                for tid in self.tids:
                    transaction = [item for item in self.items[1:] if condition_operator[self.condition](self.inputDF.at[tid, item], self.threshold)]
                    if len(transaction) > 1:
                        f.write(f'{transaction[0]}')
                        for item in transaction[1:]:
                            f.write(f'\t{item}')
                    elif len(transaction) == 1:
                        f.write(f'{transaction[0]}')
                    else:
                        continue
                    f.write('\n')

    def getFileName(self):
        return self.outputFile