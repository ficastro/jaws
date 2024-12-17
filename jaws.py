import matplotlib
import pandas as pd
from collections import defaultdict

class Cleaning:
    def __init__(self, original_dataframe):
        print("\nCleaning...\n")
        self.original = original_dataframe
        self.clean = self.clean()

        print('\nOriginal shape: '+ str(self.original.shape[0]) +' x '+ str(self.original.shape[1]))
        print('Clean shape: '+ str(self.clean.shape[0]) +' x '+ str(self.clean.shape[1])+'\n') 

    def clean(self):
        print("Cleaning dataframe...")
        cleaning_df = self.original.copy()
        cleaning_df = self.clean_dates(cleaning_df)
        cleaning_df = self.clean_type(cleaning_df)
        cleaning_df = self.clean_countries(cleaning_df)
        cleaning_df = self.clean_locations(cleaning_df)
        cleaning_df = self.clean_activities(cleaning_df)
        cleaning_df = self.clean_injuries(cleaning_df)
        cleaning_df = self.clean_fatalities(cleaning_df)

        cleaning_df = cleaning_df.drop_duplicates()
        cleaning_df = cleaning_df.dropna(how='all')
        return cleaning_df
    
    def clean_dates(self, df_to_clean):
        print("Cleaning dates...")
        df_to_clean['DATE'] = df_to_clean['DATE'].replace([0, '0', 'xx'], pd.NA) # Datas preenchidas como 0 ou xx
        df_to_clean['DATE'] = df_to_clean['DATE'].replace(r'^ND', pd.NA, regex=True) # Datas preenchidas como "ND.0001"
        df_to_clean['DATE'] = df_to_clean['DATE'].replace(r'^0+', pd.NA, regex=True) # Datas preenchidas como "000.04.33" ou "0500.44.00"
        df_to_clean['DATE'] = df_to_clean['DATE'].replace(r'\.$', '', regex=True) # Datas terminadas em .

        # df_to_clean['DATE'] = df_to_clean['DATE'].replace(r'^((?:[^\.]*\.){3}).*$', r'\1', regex=True) # Engloba os três casos abaixo:
        df_to_clean['DATE'] = df_to_clean['DATE'].replace(r'\.\D+$', '', regex=True) # Datas terminadas em .R ou .a ou .b, etc.
        df_to_clean['DATE'] = df_to_clean['DATE'].replace(r'\.\D\d$', '', regex=True) # Datas terminadas em .R1 ou .R2, etc.
        df_to_clean['DATE'] = df_to_clean['DATE'].replace(r'\s.$', '', regex=True) # Datas terminadas em ' g' ou ' f', etc.

        df_to_clean['YEAR'] = df_to_clean['YEAR'].replace(r'^0+', pd.NA, regex=True)
        
        return df_to_clean
    
    def clean_type(self, df_to_clean):
        print("Cleaning types...")
        df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Boatomg', 'Boating')
        df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Boat', 'Boating')
        # df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Invalid', None)
        # df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Questionable', None)

        return df_to_clean
    
    def clean_countries(self, df_to_clean):
        print("Cleaning countries...")
        df_to_clean['COUNTRY'] = df_to_clean['COUNTRY'].str.strip()

        return df_to_clean
    
    def clean_area(self, df_to_clean):
        print("Cleaning areas...")
        df_to_clean['AREA'] = df_to_clean['AREA'].str.strip()
        df_to_clean['AREA'] = df_to_clean['AREA'].replace('"', '')

        return df_to_clean
    
    def clean_locations(self, df_to_clean):
        print("Cleaning locations...")
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'.*Recife.*', 'Recife', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'.*Piedade.*', 'Recife', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'.*Noronha.*', 'Fernando de Noronha', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'.*Estale.*', 'Balneário Camboriú', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'.*Escale.*', 'Balneário Camboriú', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'.*S.o Lui.', 'São Luis', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'.*Rio de Jan.*', 'Rio de Janeiro', regex=True)
        
        return df_to_clean
    
    def clean_activities(self, df_to_clean):
        print("Cleaning activities...")

        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace([
            '.',
            ' ',
            ''
        ], None)
        
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*wreck.*', 'Shipwreck involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*sea dis.*', 'Sea disaster', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*s[iu]nk.*', 'Sinking involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*days.*', 'Spending days in the ocean', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*rid.*shark.*', 'Riding shark', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*f[ae]ll.*', 'Falling in the water', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*horse.*', 'Riding horse', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*plane.*', 'Plane involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*boeing.*', 'Plane involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*(?<!\w)air(?!\w).*', 'Plane involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*submar.*', 'Submarine involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*freigh.*', 'Ship involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*ship.*', 'Ship involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*sail.*', 'Boat involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*boat.*', 'Boat involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*raft.*', 'Raft involved', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*kaya.*',
            r'(?i).*canoe.*',
            r'(?i).*board.*',
            r'(?i).*ski.*',
            r'(?i).*hik.*',
            r'(?i).*tread.*',
        ), 'Sports', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*swim.*',
            r'(?i).*floa.*',
            r'(?i).*jump.*',
        ), 'Swimming', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*bath.*',
            r'(?i).*lyi.*',
            r'(?i).*stand.*',
            r'(?i).*walk.*',
            r'(?i).*wading.*'
        ),'Bathing', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*fish.*', 'Fishing', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*surf.*', 'Surfing', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*diving.*', 'Diving', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*hunt.*', 'Hunting', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*snork.*', 'Snorkeling', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*accid.*', 'Accident', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*shark.*','Handling shark', regex=True)

        return df_to_clean

    def clean_injuries(self, df_to_clean):
        print("Cleaning injuries...")

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace(r'(?i).*drown.*', 'Drowned', regex=True)
        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace(r'(?i).*remain.*', 'Eaten', regex=True)
        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace(r'(?i).*no injury.*', 'No injury', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*severe.*',
            r'(?i).*serious.*',
            r'(?i).*major.*',
        ), 'Severe', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*hand.*',
            r'(?i).*finger.*',
            r'(?i).*finger.*',
        ), 'Hands', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*f[oe][oe]t.*',
            r'(?i).*ankle.*',
            r'(?i).*heel.*',
            r'(?i).*toe.*',
        ), 'Feet', regex=True)
        
        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*arm.*',
            r'(?i).*shoulder.*',
        ), 'Arms', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*leg.*',
            r'(?i).*thigh.*',
            r'(?i).*calf.*',
        ), 'Legs', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*bit.*',
            r'(?i).*lacer.*'
        ), 'Bites', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*no details.*',
            r'(?i).*unconfirm.*',
            r'(?i).*provoked.*',
            r'(?i).*survived.*',
            r'(?i).*not confirm.*',
        ), 'Other', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*minor.*',
            r'(?i).*abras.*',
            r'(?i).*recover.*',
            r'(?i).*injur.*',
            r'(?i).*bruis.*',
            r'(?i).*wounds.*',
            r'(?i).*punct.*',
            r'(?i).*stitch.*',
        ), 'Minor', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*fatal.*',
            r'(?i).*perish.*',
            r'(?i).*death.*',
            r'(?i).*dead.*',
            r'(?i).*killed.*',
        ), 'Fatal', regex=True)

        value_counts = df_to_clean['INJURY'].value_counts()
        df_to_clean['INJURY'] = df_to_clean['INJURY'].map(
            lambda injury: 'Other' if value_counts.get(injury, 0) < 5 else injury
            # lambda injury: print(injury) if value_counts.get(injury, 0) < 5  and pd.notna(injury) else injury // Print all 'Other injuries'
        )
        
        return df_to_clean

    def clean_fatalities(self, df_to_clean):
        print("Cleaning fatalities...")
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].astype(str)
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace(' N', 'N')
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace('N ', 'N')
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace('M', 'N')
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace('y', 'Y')
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace('2017', None)
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace('UNKNOWN', None)
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace('nan', None)
        df_to_clean['FATALITY'] = df_to_clean['FATALITY'].replace('<NA>', None)

        return df_to_clean

class Analysis:
    def __init__(self, clean_dataframe):
        print("\nAnalysing...\n")
        self.dataframe = clean_dataframe
        
        self.attacks_by_year()
        self.type_count()
        self.attacks_by_country()
        self.attacks_by_area_by_countries()
        self.activity_count()
        self.injury_analysis()
        self.fatality_analysis()

        # self.brazil_analysis()

        return print("\nAnalysis finished.\n")


    def attacks_by_year(self):
        attacks_by_year = self.dataframe['YEAR'].value_counts().to_dict()

        # for value in self.dataframe['DATE'].values:
        #     print(value)

        # for year, count in self.dataframe['YEAR'].value_counts().items():
            # print(f'Year {year} - {count} shark attack(s) registered.')

        return attacks_by_year

    def type_count(self):
        type_count = self.dataframe['TYPE'].value_counts().to_dict()

        return type_count

    def attacks_by_country(self):
        attacks_by_country = self.dataframe['COUNTRY'].value_counts().to_dict()

        return attacks_by_country
    
    def attacks_by_area_by_countries(self):
        attacks_by_area_by_countries = defaultdict(dict) # {'COUNTRY_A':{'area_1':74, 'Rio de area_2':11}, 'COUNTRY_B':{} }

        for country in self.attacks_by_country().keys():
            area_filter = self.dataframe['COUNTRY'] == str(country)

            attacks_by_area_by_countries[str(country)] = self.dataframe[area_filter]['AREA'].value_counts().to_dict()

        return attacks_by_area_by_countries

    def activity_count(self):
        activity_count = self.dataframe['ACTIVITY'].value_counts().to_dict()

        return activity_count

    def age_analysis(self):
        return

    def injury_analysis(self):
        print("Analysing injuries...")
        injuries_analysis = {}
        injuries_analysis['No injury'] = self.dataframe['INJURY'].str.contains(r'(?i).*no injury.*', regex=True).sum()
        injuries_analysis['Amputations'] = self.dataframe['INJURY'].str.contains(r'(?i).*amput.*', regex=True).sum()

        injuries_analysis['Legs'] = self.dataframe['INJURY'].str.contains(r'(?i).*leg.*', regex=True).sum()
        injuries_analysis['Hands'] = self.dataframe['INJURY'].str.contains(r'(?i).*hand.*', regex=True).sum()
        injuries_analysis['Arms'] = self.dataframe['INJURY'].str.contains(r'(?i).*arm.*', regex=True).sum()
        injuries_analysis['Feet'] = self.dataframe['INJURY'].str.contains(r'(?i).*f[oe][oe]t.*', regex=True).sum()

        injuries_analysis['Minor'] = self.dataframe['INJURY'].str.contains(r'(?i).*minor.*', regex=True).sum()

        injuries_analysis['Severe'] = self.dataframe['INJURY'].str.contains(r'(?i).*severe.*', regex=True).sum()
        injuries_analysis['Severe'] = self.dataframe['INJURY'].str.contains(r'(?i).*serious.*', regex=True).sum()

        injuries_analysis['Bites'] = self.dataframe['INJURY'].str.contains(r'(?i).*bit.*', regex=True).sum()
        injuries_analysis['Bites'] = self.dataframe['INJURY'].str.contains(r'(?i).*lacer.*', regex=True).sum()

        injuries_analysis['Other'] = self.dataframe['INJURY'].str.contains(r'(?i).*other.*', regex=True).sum()

        injuries_analysis = pd.Series(injuries_analysis).sort_values(ascending=False).to_dict()

        # return print(injuries_analysis)
        return print(injuries_analysis), print(self.dataframe['INJURY'].value_counts())

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

        # print(f'Total de ataques: {total_attacks}; sendo {fatalities} fatalidades, {non_fatalities} não-fatalidades e {missing_fatalities} valores faltantes')
        # print(f'> O que representa uma mortalidade de {fatality_percentage}%, desconsiderando os valores faltantes.')
        # print(f'> E uma mortalidade de {new_fatality_percentage}%, corrigindo os valores faltantes proprocionalmente.')

        fatality_analysis = {}
        fatality_analysis['Total attacks'] = total_attacks
        fatality_analysis['Fatalities'] = fatalities
        fatality_analysis['Non-fatalitiies'] =  non_fatalities
        fatality_analysis['Unkown'] = missing_fatalities
        fatality_analysis['Fatality percentage'] = (fatality_percentage + new_fatality_percentage) / 2

        return fatality_analysis

    def time_analysis(self):
        return

    def species_analysis(self):
        return
    
    def brazil_attacks_by_area(self):
        area_filter = self.dataframe['COUNTRY'] == 'BRAZIL'
        brazil_attacks = self.dataframe[area_filter]['AREA'].value_counts()

        return print(f'\n> Brazil shark attacks by area:\n{brazil_attacks}')
    
    def brazil_attacks_by_location(self):
        area_filter = self.dataframe['COUNTRY'] == 'BRAZIL'
        brazil_attacks = self.dataframe[area_filter]['LOCATION'].value_counts()

        return print(f'\n> Brazil shark attacks by location:\n{brazil_attacks}')
    
    def brazil_analysis(self):
        self.brazil_attacks_by_area()
        self.brazil_attacks_by_location()
    

class BiAnalysis:
    def __init__(self, clean_dataframe):
        self.dataframe = clean_dataframe

        self.type_activity_analysis()

    def type_activity_analysis(self):
        types = self.dataframe['TYPE'].value_counts()

        activity_by_type = defaultdict(list)

        for type, count in types.items():
            type_filter = self.dataframe['TYPE'] == type
            # print(self.dataframe[type_filter]['ACTIVITY'])

            # for correspondent_activity in (self.dataframe[type_filter]['ACTIVITY']).values:
            #     if correspondent_activity not in activity_by_type[type]:
            #         activity_by_type[type] = correspondent_activity

        return print(activity_by_type)
            

    def provoked_attacks_proportion(self):
        pass

    def species_fatality_analysis(self):
        pass

    def top_20_countries(self):
        # top_20_countries = self.dataframe.sort_values('COUNTRY').head(20)
        pass



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
        'Age':          'AGE',
        'Injury':       'INJURY',
        'Fatal (Y/N)':  'FATALITY',
        'Time':         'TIME',
        'Species':      'SPECIES'
    })
    
    dataframe = Cleaning(csv_dataframe)
    dataframe = dataframe.clean

    analysis = Analysis(dataframe)
    # bivariate_analysis = BiAnalysis(dataframe)

    return print("\nJAWS FINISHED\n")

if __name__ == '__main__':
    main()