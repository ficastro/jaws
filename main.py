import pandas as pd

class DataFrame:
    def __init__(self, unfixed_dataframe):
        self.original = unfixed_dataframe
        self.fixed = self.fixed_dataframe()

        print('Original shape: '+ str(self.original.shape[0]) +' x '+ str(self.original.shape[1]))

    def fixed_dataframe(self):
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


def correct_fatality_info(dataframe): # Transform to true or false?
    dataframe['FATAL'] = dataframe['FATAL'].replace(' N', 'N')
    dataframe['FATAL'] = dataframe['FATAL'].replace('N ', 'N')
    dataframe['FATAL'] = dataframe['FATAL'].replace('M', 'N')

    dataframe['FATAL'] = dataframe['FATAL'].replace('y', 'Y')

    # dataframe['FATAL'] = dataframe['FATAL'].replace('UNKNOWN', '') # O que fazer com os dados desconhecidos?
    dataframe['FATAL'] = dataframe['FATAL'].replace('2017', 'UNKNOWN')

    return dataframe



def main():
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
        'Fatal (Y/N)':  'FATAL',
        'Time':         'TIME',
        'Species':      'SPECIES'
    })
    
    unfixed_dataframe = DataFrame(csv_dataframe)
    
    fixed_dataframe = unfixed_dataframe.fixed
    

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

        # variable_quartiles = variable.quartiles()

        break # Para testar apenas com uma variável


print("\nRunning...\n")
main()
# try:
#     main()
# except Exception as e:
#     print(e)