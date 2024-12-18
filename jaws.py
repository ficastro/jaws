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
        cleaning_df = self.clean_ages(cleaning_df)
        cleaning_df = self.clean_injuries(cleaning_df)
        cleaning_df = self.clean_fatalities(cleaning_df)
        cleaning_df = self.clean_time(cleaning_df)
        cleaning_df = self.clean_species(cleaning_df)

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

        value_counts = df_to_clean['COUNTRY'].value_counts()
        df_to_clean['COUNTRY'] = df_to_clean['COUNTRY'].map(
            lambda country: 'Other' if value_counts.get(country, 0) < 10 else country
        )

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
        
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*wreck.*', 'Shipwreck', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*sea dis.*', 'Sea disaster', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*s[iu]nk.*', 'Sinking involved', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*days.*', 'Spent days in the ocean', regex=True)
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

    def clean_ages(self, df_to_clean):
        print("Cleaning ages...")
        df_to_clean['AGE'] = df_to_clean['AGE'].replace((
            r'(?i).*young.*',
            r'(?i).*month.*',
        ), 5, regex=True)

        df_to_clean['AGE'] = df_to_clean['AGE'].replace((
            r'(?i).*teen.*',
        ), 15, regex=True)

        df_to_clean['AGE'] = df_to_clean['AGE'].replace((
            r'(?i).*adul.*',
        ), 30, regex=True)

        df_to_clean['AGE'] = df_to_clean['AGE'].replace((
            r'(?i).*elder.*',
        ), 70, regex=True)

        df_to_clean['AGE'] = pd.to_numeric(df_to_clean['AGE'], errors='coerce').astype('Int64')

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

    def clean_time(self, df_to_clean):
        print("Cleaning times...")

        df_to_clean['TIME'] = df_to_clean['TIME'].replace((
            r'(?i)h.*',
            r'(?i)j.*',
            r'(?i)00',
            r'(?i)30',
        ), '', regex=True)

        df_to_clean['TIME'] = df_to_clean['TIME'].replace((
            r'(?i).*nig.*',
            r'(?i).*set.*',
            r'(?i).*dark.*',
            r'(?i).*evening.*',
            r'(?i).*dusk.*',
            r'(?i).*am.*',
            r'(?i).*A\.M\..*',
        ), 22, regex=True) # Night = 22h

        df_to_clean['TIME'] = df_to_clean['TIME'].replace((
            r'(?i).*after\s*no.*',
            r'(?i).*down.*',
            r'(?i).*day.*',
            r'(?i).*pm.*',
            r'(?i).*P\.M\..*',
        ), 15, regex=True) # Day = 15h

        df_to_clean['TIME'] = df_to_clean['TIME'].replace((
            r'(?i)mornin.*',
            r'(?i)noon.*',
            r'(?i)dawn.*',
        ), 10, regex=True) # Morning = 8h

        df_to_clean['TIME'] = df_to_clean['TIME'].replace((
            '',
            '--',
            '"',
            r'(?i).*betwe.*',
            r'(?i).*fatal.*',
            r'(?i).*before.*',
            r'(?i).*lunc.*',
            r'(?i).*after.*',
            r'(?i).*x.*',
            r'(?i).*s$',
            r'(?i).*[<>].*',
        ), None, regex=True)

        df_to_clean['TIME'] = df_to_clean['TIME'].replace((
            r'(?i)^0.*',
        ), '', regex=True)

        df_to_clean['TIME'] = pd.to_numeric(df_to_clean['TIME'], errors='coerce').astype('Int64')

        return df_to_clean
    
    def clean_species(self, df_to_clean):
        print("Cleaning species...")

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*white.*',
        ), 'White shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*nurse.*',
        ), 'Nurse shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*tiger.*',
        ), 'Tiger shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*bull.*',
        ), 'Bull shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*silver.*',
        ), 'Silvertip shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*hammer.*',
        ), 'Hammerhead shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*hammer.*',
        ), 'Whale shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*black.*',
        ), 'Blacktip shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*galapagos.*',
        ), 'Galapagos shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*spin.*',
        ), 'Spinner shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*mak.*',
        ), 'Mako shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*blu.*',
        ), 'Blue shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*gr[ae]y.*',
        ), 'Grey shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*sandbar.*',
        ), 'Sandbar shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*sand.*',
        ), 'Sand shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*reef.*',
            r'(?i).*carib.*',
        ), 'Reef shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*lemon.*',
        ), 'Lemon shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*wobb.*',
        ), 'Wobbegong shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*whaler.*',
            r'(?i).*copper.*',
            r'(?i).*bronze.*',
            r'(?i).*narrowtooth.*',
        ), 'Copper shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*whip.*',
            r'(?i).*thresh.*',
        ), 'Whiptail shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*zambes.*',
        ), 'Zambesi shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*barrac.*',
        ), 'Barracuda', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*smal.*',
            r'(?i).*dog.*',
            r'(?i).*little.*',
            r'(?i).*tiny.*',
            r'(?i).*juvenile.*',
            r'(?i).*young.*',
            r'(?i).*[0123]\.?.*m?.*',
        ), 'Small', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*big.*',
            r'(?i).*large.*',
            r'(?i).*long.*',
            r'(?i).*[456789]\.?.*m?.*',
        ), 'Big', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*invo.*',
            r'(?i).*unknown.*',
            r'(?i).*possib.*',
            r'(?i).*question.*',
            r'(?i).*not.*',
            r'(?i).*uniden.*',
            r'(?i).*inval.*',
            r'(?i).*doubt.*',
        ), None, regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*shark\'s.*',
            r'(?i).*pack.*',
            r'(?i).*school.*',
            r'(?i).*number.*',
        ), 'Multiple sharks', regex=True)

        value_counts = df_to_clean['SPECIES'].value_counts()
        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].map(
            lambda species: 'Other' if value_counts.get(species, 0) < 10 else species
        )

        return df_to_clean

class Analysis:
    def __init__(self, clean_dataframe):
        print("\nAnalysing...\n")
        self.dataframe = clean_dataframe
        
        self.year_analysis()
        self.type_analysis()
        self.country_analysis()
        self.activity_analysis()
        self.age_analysis()
        self.injury_analysis()
        self.fatality_analysis()
        self.time_analysis()
        self.species_analysis()

        # self.brazil_analysis()

        return print("\nAnalysis finished.\n")

    def year_analysis(self):
        print("Analysing years...")
        attacks_by_year = self.dataframe['YEAR'].value_counts().to_dict()

        # for value in self.dataframe['DATE'].values:
        #     print(value)

        # for year, count in self.dataframe['YEAR'].value_counts().items():
            # print(f'Year {year} - {count} shark attack(s) registered.')

        return attacks_by_year

    def type_analysis(self):
        print("Analysing types...")
        type_count = self.dataframe['TYPE'].value_counts().to_dict()

        return type_count

    def country_analysis(self):
        print("Analysing countries...")
        attacks_by_country = self.dataframe['COUNTRY'].value_counts().to_dict()

        return attacks_by_country

    def activity_analysis(self):
        print("Analysing activities...")
        activity_count = self.dataframe['ACTIVITY'].value_counts().to_dict()

        return activity_count

    def age_analysis(self):
        print("Analysing age...")

        # age_count = {
        #     'Under 15': 0,
        #     'Between 15 and 25': 0,
        #     'Between 25 and 60': 0,
        #     'Over 60': 0
        # }
        # for age, amount in self.dataframe['AGE'].value_counts().items():

        #     if int(age) > 0 and int(age) < 15:
        #         age_count['Under 15'] += amount

        #     elif int(age) > 15 and int(age) < 25:
        #         age_count["Between 15 and 25"] += amount

        #     elif int(age) > 25 and int(age) < 60:
        #         age_count["Between 25 and 60"] += amount

        #     elif int(age) > 60:
        #         age_count["Over 60"] += amount

        bins = [0, 15, 25, 60, float('inf')]
        labels = ['Under 15', 'Between 15 and 25', 'Between 25 and 60', 'Over 60']

        self.dataframe['AGE'] = pd.cut(self.dataframe['AGE'], bins=bins, labels=labels, right=False)

        age_count = self.dataframe['AGE'].value_counts().to_dict()
        
        return age_count

    def injury_analysis(self):
        print("Analysing injuries...")
        injury_count = self.dataframe['INJURY'].value_counts().to_dict()

        return injury_count

    def fatality_analysis(self):
        print("Analysing fatalities...")
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
        print("Analysing time...")

        bins = [0, 5, 12, 18, float('inf')]
        labels = ['Night', 'Morning', 'Afternoon', 'Evening']

        self.dataframe['TIME'] = pd.cut(self.dataframe['TIME'], bins=bins, labels=labels, right=False)

        time_analysis = self.dataframe['TIME'].value_counts().to_dict()
    
        return time_analysis

    def species_analysis(self):
        print("Analysing species...")
        species_count = self.dataframe['SPECIES'].value_counts().to_dict()
        
        return species_count
    
    def brazil_attacks_by_area(self):
        area_filter = self.dataframe['COUNTRY'] == 'BRAZIL'
        brazil_attacks = self.dataframe[area_filter]['AREA'].value_counts()

        return print(f'\n> Brazil shark attacks by area:\n{brazil_attacks}')
    
    def brazil_attacks_by_location(self):
        area_filter = self.dataframe['COUNTRY'] == 'BRAZIL'
        brazil_attacks = self.dataframe[area_filter]['LOCATION'].value_counts()

        return print(f'\n> Brazil shark attacks by location:\n{brazil_attacks}')
    
    def brazil_analysis(self):
        print("\nRunning Brazil analysis...")
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
    
    def attacks_by_area_by_countries(self):
        print("Analysing attacks by area and country...")
        attacks_by_area_by_countries = defaultdict(dict) # {'COUNTRY_A':{'area_1':74, 'area_2':11}, 'COUNTRY_B':{} }

        for country in Analysis(self.dataframe).country_analysis().keys():
            area_filter = self.dataframe['COUNTRY'] == str(country)

            attacks_by_area_by_countries[str(country)] = self.dataframe[area_filter]['AREA'].value_counts().to_dict()

        return attacks_by_area_by_countries
            

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
        'Species ':      'SPECIES'
    })
    
    dataframe = Cleaning(csv_dataframe)
    dataframe = dataframe.clean

    analysis = Analysis(dataframe)
    bivariate_analysis = BiAnalysis(dataframe)

    return print("\nJAWS FINISHED\n")

if __name__ == '__main__':
    main()