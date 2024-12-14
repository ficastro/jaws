import pandas as pd

class DataFrame:
    def __init__(self, unfixed_dataframe):
        self.original = unfixed_dataframe
        self.fix = self.fix()

        print('Original shape: '+ str(self.original.shape[0]) +' x '+ str(self.original.shape[1]))

    def fix(self):
        fixed_dataframe = self.original

        fixed_dataframe['DATE'] = fixed_dataframe['DATE'].replace([0, '0', 'xx'], pd.NA)
        fixed_dataframe = fixed_dataframe.dropna(how='all')

        print('Fixed shape: '+ str(fixed_dataframe.shape[0]) +' x '+ str(self.original.shape[1]))

        return fixed_dataframe


class Variable:
    def __init__(self, column, values):
        self.name = str(column)
        self.values = values

    def quartiles(self):
        return

class DateVariable(Variable):
    def __init__(self, column, values):
        self.is_date = True

        super().__init__(column, values)

class Injury(Variable):
    def __init__(self, column, values):
        self.amount = 0

        super().__init__(column, values)

    def amputation(self, row_value):

        regexes = 'amput'
        if 'amput' in row_value:
            self.amount += 1



def correct_fatality_info(dataframe): # Transform to true or false?
    dataframe['FATALITY'] = dataframe['FATALITY'].replace(' N', 'N')
    dataframe['FATALITY'] = dataframe['FATALITY'].replace('N ', 'N')
    dataframe['FATALITY'] = dataframe['FATALITY'].replace('M', 'N')

    dataframe['FATALITY'] = dataframe['FATALITY'].replace('y', 'Y')

    # dataframe['FATALITY'] = dataframe['FATALITY'].replace('UNKNOWN', '') # O que fazer com os dados desconhecidos?
    dataframe['FATALITY'] = dataframe['FATALITY'].replace('2017', 'UNKNOWN')

    return dataframe



def main():
    print("Running main...")
    csv_dataframe = pd.read_csv(
        "csv/shark_attacks.csv",
        encoding='latin1',
        usecols=[
            'Case Number',
            'Year',
            'Type',
            'Country',
            'Area',
            'Location',
            'Activity',
            'Sex ',
            'Age',
            'Injury',
            'Fatal (Y/N)',
            'Time',
            'Species '
        ]
    ).rename(columns={
        'Case Number':  'DATE',
        'Year':         'YEAR',
        'Type':         'TYPE',
        'Country':      'COUNTRY',
        'Area':         'AREA',
        'Location':     'LOCATION',
        'Activity':     'ACTIVITY',
        'Sex ':         'SEX',
        'Age':          'AGE',
        'Injury':       'INJURY',
        'Fatal (Y/N)':  'FATALITY',
        'Time':         'TIME',
        'Species':      'SPECIES'
    })
    
    original_dataframe = DataFrame(csv_dataframe)
    
    fixed_dataframe = original_dataframe.fix
    

    # print(df['COUNTRY'].value_counts())
    # print(df['COUNTRY'].unique())

    # df = correct_fatality_info(df)
    # print(df['FATAL'].value_counts())
    # Calcular porcentagem de fatalidades

    for column, values in fixed_dataframe.items():
        print(column)
        if str(column) == 'DATE':
            variable = DateVariable(str(column), values)
        else:
            variable = Variable

        print(variable.name)
        print(variable.values)
        print(variable.is_date) if variable.is_date else None



        # variable_quartiles = variable.quartiles() # pra que

        break # Quick test


print("\nRunning...\n")
main()
# try:
#     main()
# except Exception as e:
#     print(e)