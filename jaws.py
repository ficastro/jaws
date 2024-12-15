import pandas as pd

class Cleaning:
    def __init__(self, original_dataframe):
        self.original = original_dataframe
        self.fixed = self.fix()

        print('\nOriginal shape: '+ str(self.original.shape[0]) +' x '+ str(self.original.shape[1]))
        print('Fixed shape: '+ str(self.fixed.shape[0]) +' x '+ str(self.fixed.shape[1])+'\n')
    
    def fix(self):
        print("\nFixing dataframe register issues..")
        fixing_df = self.original.copy()
        fixing_df = self.fix_dates(fixing_df)
        fixing_df = self.fix_fatality(fixing_df)

        fixing_df = self.remove_empty(fixing_df)
        return fixing_df
    
    def fix_dates(self, dataframe):
        print("Fixing dates...")
        dataframe['DATE'] = dataframe['DATE'].replace([0, '0', 'xx'], pd.NA) # Datas preenchidas como 0 ou xx
        dataframe['DATE'] = dataframe['DATE'].replace(r'^ND', pd.NA, regex=True) # Datas preenchidas como "ND.0001"
        dataframe['DATE'] = dataframe['DATE'].replace(r'^0+', pd.NA, regex=True) # Datas preenchidas como "000.04.33" ou "0500.44.00"
        dataframe['DATE'] = dataframe['DATE'].replace(r'\.$', '', regex=True) # Datas terminadas em .

        # dataframe['DATE'] = dataframe['DATE'].replace(r'^((?:[^\.]*\.){3}).*$', r'\1', regex=True) # Engloba os três casos abaixo:
        dataframe['DATE'] = dataframe['DATE'].replace(r'\.\D+$', '', regex=True) # Datas terminadas em .R ou .a ou .b, etc.
        dataframe['DATE'] = dataframe['DATE'].replace(r'\.\D\d$', '', regex=True) # Datas terminadas em .R1 ou .R2, etc.
        dataframe['DATE'] = dataframe['DATE'].replace(r'\s.$', '', regex=True) # Datas terminadas em ' g' ou ' f', etc.

        dataframe['YEAR'] = dataframe['YEAR'].replace(r'^0+', pd.NA, regex=True)
        
        return dataframe

    def fix_fatality(self, dataframe):
        print("Fixing fatalities...")
        dataframe['FATALITY'] = dataframe['FATALITY'].astype(str)
        dataframe['FATALITY'] = dataframe['FATALITY'].replace(' N', 'N')
        dataframe['FATALITY'] = dataframe['FATALITY'].replace('N ', 'N')
        dataframe['FATALITY'] = dataframe['FATALITY'].replace('M', 'N')
        dataframe['FATALITY'] = dataframe['FATALITY'].replace('y', 'Y')
        dataframe['FATALITY'] = dataframe['FATALITY'].replace('2017', None)
        dataframe['FATALITY'] = dataframe['FATALITY'].replace('UNKNOWN', None)
        dataframe['FATALITY'] = dataframe['FATALITY'].replace('nan', None)
        dataframe['FATALITY'] = dataframe['FATALITY'].replace('<NA>', None)

        return dataframe
    
    def remove_empty(self, complete_df):
        print("Removing empty rows...")
        sliced_df = complete_df.dropna(how='all')
        return sliced_df
    


class Analysis:
    def __init__(self, fixed_dataframe):
        self.dataframe = fixed_dataframe
        
        # self.date_analysis()
        # self.country_analysis()
        self.fatality_analysis()

    def date_analysis(self):
        attacks_by_year = self.dataframe['YEAR'].value_counts().to_dict()

        for value in self.dataframe['DATE'].values:
            print(value)

        for year, count in self.dataframe['YEAR'].value_counts().items():
            print(f'Year {year} - {count} shark attack(s) registered.')

    def country_analysis(self):
        attacks_by_country = self.dataframe['COUNTRY'].value_counts().to_dict()

    def fatality_analysis(self):
        total_attacks = len(self.dataframe['FATALITY']) # 6302
        total_registers = self.dataframe['FATALITY'].count() # não conta None # 5691
        fatalities = self.dataframe['FATALITY'].value_counts().get('Y') # 1389
        non_fatalities = self.dataframe['FATALITY'].value_counts().get('N') # 4302
        
        missing_fatalities = self.dataframe['FATALITY'].isna().sum() # 611

        fatality_percentage = round((fatalities / total_registers) * 100)
        missing_positives_proportion = round(missing_fatalities * fatality_percentage/100)
        missing_negatives_proportion = missing_fatalities - missing_positives_proportion

        fatalities += missing_positives_proportion
        non_fatalities += missing_negatives_proportion

        new_fatality_percentage = round((fatalities / total_registers) * 100)

        print(f'Total de ataques: {total_attacks}; sendo {fatalities} fatalidades, {non_fatalities} não-fatalidades e {missing_fatalities} valores faltantes')
        print(f'-> O que representa uma mortalidade de {fatality_percentage}%, desconsiderando os valores faltantes.')
        print(f'-> E uma porcentagem de {new_fatality_percentage}% corrigindo os valores faltantes proprocionalmente.')

        return 


def main():
    print("\nRunning main...\n")

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
    
    dataframe = Cleaning(csv_dataframe)
    dataframe = dataframe.fixed

    analysis = Analysis(dataframe)



if __name__ == '__main__':
    main()



#     def simplify(self):
#         simplifying_df = self.fixed
#         simplifying_df = self.simplify_years(simplifying_df)

#         simplifying_df = self.remove_empty(simplifying_df)
#         return simplifying_df

#     def simplify_years(self, complex_df):
#         simplifying_df = complex_df
#         simplifying_df['YEAR'] = simplifying_df['YEAR'].fillna(0).astype(int)
#         simplified_df = simplifying_df[simplifying_df['YEAR'] > 1975]
        
#         return print(simplified_df)