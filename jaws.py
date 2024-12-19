import numpy as np
import pandas as pd
from collections import defaultdict
from matplotlib import pyplot

class Cleaning:
    def __init__(self, original_dataframe):
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
        cleaning_df = self.clean_area(cleaning_df)
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
        # df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Sea Disaster', 'Unprovoked')
        df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Boating', 'Unprovoked')
        df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Boatomg', 'Unprovoked')
        df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Boat', 'Unprovoked')
        df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Invalid', None)
        df_to_clean['TYPE'] = df_to_clean['TYPE'].replace('Questionable', None)

        return df_to_clean
    
    def clean_countries(self, df_to_clean):
        print("Cleaning countries...")
        df_to_clean['COUNTRY'] = df_to_clean['COUNTRY'].str.strip()

        df_to_clean['COUNTRY'] = df_to_clean['COUNTRY'].replace((
            r'.*SOUTH AFRICA.*'
        ), 'SOUTH\nAFRICA', regex=True)

        df_to_clean['COUNTRY'] = df_to_clean['COUNTRY'].replace((
            r'.*PAPUA NEW.*'
        ), 'PAPUA\nNEW GUINEA', regex=True)

        value_counts = df_to_clean['COUNTRY'].value_counts()
        df_to_clean['COUNTRY'] = df_to_clean['COUNTRY'].map(
            # lambda country: 'Other' if value_counts.get(country, 0) < 5 else country
            lambda country: None if value_counts.get(country, 0) < 5 else country
        )

        return df_to_clean
    
    def clean_area(self, df_to_clean):
        print("Cleaning areas...")
        df_to_clean['AREA'] = df_to_clean['AREA'].str.strip()
        df_to_clean['AREA'] = df_to_clean['AREA'].replace('"', '')

        df_to_clean['AREA'] = df_to_clean['AREA'].replace((
            r'(?i).*rio de.*',
        ), 'Rio\nde Janeiro', regex=True)

        df_to_clean['AREA'] = df_to_clean['AREA'].replace((
            r'(?i).*grande d[oe] n.*',
        ), 'Rio Grande\ndo Norte', regex=True)
    
        df_to_clean['AREA'] = df_to_clean['AREA'].replace((
            r'(?i).*grande d[oe] s.*',
        ), 'Rio Grande\ndo Sul', regex=True)

        df_to_clean['AREA'] = df_to_clean['AREA'].replace((
            r'(?i).*porto se.*',
        ), 'Bahia', regex=True)

        df_to_clean['AREA'] = df_to_clean['AREA'].replace((
            r'(?i).*catarina.*',
            r'(?i).*cambor.*',
        ), 'Santa\nCatarina', regex=True)

        df_to_clean['AREA'] = df_to_clean['AREA'].replace((
            r'(?i).*noron.*',
        ), 'Fernando\nde Noronha', regex=True)

        df_to_clean['AREA'] = df_to_clean['AREA'].replace((
            r'(?i).*vic?tor.*',
        ), 'Vitória', regex=True)

        return df_to_clean
    
    def clean_locations(self, df_to_clean):
        print("Cleaning locations...")
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'(?i).*recife.*', 'Recife', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'(?i).*piedade.*', 'Recife', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'(?i).*noronha.*', 'Fernando de Noronha', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'(?i).*estale.*', 'Balneário Camboriú', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'(?i).*escale.*', 'Balneário Camboriú', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'(?i).*s.o Lui.', 'São Luis', regex=True)
        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace(r'(?i).*rio de jan.*', 'Rio de Janeiro', regex=True)
        
        return df_to_clean
    
    def clean_activities(self, df_to_clean):
        print("Cleaning activities...")

        df_to_clean['LOCATION'] = df_to_clean['LOCATION'].replace([
            r'(?i)\.',
            r'(?i).*unknown.*',
            ' ',
            ''
        ], None, regex=True)
        
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*wreck.*', 'Shipwreck', regex=True)
        
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*sea dis.*',
            r'(?i).*desert.*',
            r'(?i).*burn.*',
            r'(?i).*tsuna.*',
            r'(?i).*hurric.*',
            r'(?i).*tidal.*',
        ), 'Sea disaster', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*s[aiu]nk.*',
            r'(?i).*founder.*',
        ), 'Sinking', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*days.*',
            r'(?i).*ashore.*',
            r'(?i).*aband.*',
            r'(?i).*adrift.*',
        ), 'Spent days in the ocean', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*rid.*shark.*', 'Riding shark', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*horse.*', 'Riding horse', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*plane.*',
            r'(?i).*aircraft.*',
            r'(?i).*air.*',
            r'(?i).*boeing.*',
        ), 'Plane involved', regex=True)
        
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*freigh.*',
            r'(?i).*ship.*',
            r'(?i).*cruis.*',
            r'(?i).*sail.*',
            r'(?i).*boat.*',
            r'(?i).*raft.*',
            r'(?i).*submar.*',
        ), 'Ship involved', regex=True)
    
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*kaya.*',
            r'(?i).*kak.*',
            r'(?i).*canoe.*',
            r'(?i).*board.*',
            r'(?i).*ski.*',
            r'(?i).*hik.*',
            r'(?i).*tread.*',
            r'(?i).*snork.*',
            r'(?i).*row.*',
            r'(?i).*paddl.*',
        ), 'Sports', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*swim.*',
            r'(?i).*floa.*',
            r'(?i).*jump.*',
            r'(?i).*scull.*',
        ), 'Swimming', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*bath.*',
            r'(?i).*lyi.*',
            r'(?i).*stand.*',
            r'(?i).*walk.*',
            r'(?i).*wading.*',
            r'(?i).*dangl.*',
            r'(?i).*sit.*',
            r'(?i).*shall.*',
            r'(?i).*play.*',
            r'(?i).*wash.*',
            r'(?i).*splash.*',
        ),'Bathing', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*feed.*',
            r'(?i).*fed.*',
        ), 'Fishing', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*fish.*',
            r'(?i).*net.*',
            r'(?i).*catch.*',
            r'(?i).*crab.*',
        ), 'Fishing', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*life.?saving.*',
            r'(?i).*drill.*',
            r'(?i).*rescue.*',
        ), 'Lifesaving', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*surf.*', 'Surfing', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*div.*', 'Diving', regex=True)
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*hunt.*', 'Hunting', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*murder.*',
        ), 'Murder', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*capsi.*',
            r'(?i).*accid.*',
            r'(?i).*colli.*',
            r'(?i).*f[ae]ll.*',
            r'(?i).*knock.*',
            r'(?i).*parach.*',
            r'(?i).*explo.*',
        ), 'Accident', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace((
            r'(?i).*photo.*',
            r'(?i).*film.*',
        ), 'Photography', regex=True)

        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].replace(r'(?i).*shark.*','Handling\nshark', regex=True)

        value_counts = df_to_clean['ACTIVITY'].value_counts()
        df_to_clean['ACTIVITY'] = df_to_clean['ACTIVITY'].map(
            # lambda activity: 'Other' if value_counts.get(activity, 0) < 5 else activity
            lambda activity: None if value_counts.get(activity, 0) < 5 else activity
        )

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

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace(r'(?i).*remain.*', 'Eaten', regex=True)
        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace(r'(?i).*no injury.*', 'No injury', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*severe.*',
            r'(?i).*serious.*',
            r'(?i).*major.*',
            # r'(?i).*lacer.*'
        ), 'Severe', regex=True)
        
        """
        Atenção: alternando a ordem dos quatro próximos (Arms, Legs, Hands e Feets), obtem-se resultados diferentes.
        O algoritmo deve reconhecer qual prevalece em cada caso.
        """
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
            r'(?i).*f[oe][oe]t.*',
            r'(?i).*ankle.*',
            r'(?i).*heel.*',
            r'(?i).*toe.*',
        ), 'Feet', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*hand.*',
            r'(?i).*finger.*',
        ), 'Hands', regex=True) # Hands vinha muito em primeiro lugar, então ficou por último entre Arms, Legs e Feet; 

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*no details.*',
            r'(?i).*unconfirm.*',
            r'(?i).*provoked.*',
            r'(?i).*survived.*',
            r'(?i).*not confirm.*',
        ), None, regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace(r'(?i).*drown.*', 'Drowned', regex=True)

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*minor.*',
            r'(?i).*abras.*',
            r'(?i).*recover.*',
            r'(?i).*injur.*',
            r'(?i).*bruis.*',
            r'(?i).*wound.*',
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

        df_to_clean['INJURY'] = df_to_clean['INJURY'].replace((
            r'(?i).*bit.*',
            r'(?i).*lacer.*',
        ), None, regex=True)

        value_counts = df_to_clean['INJURY'].value_counts()
        df_to_clean['INJURY'] = df_to_clean['INJURY'].map(
            # lambda injury: 'Other' if value_counts.get(injury, 0) < 5 else injury
            lambda injury: None if value_counts.get(injury, 0) < 5 else injury
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
        ), 'Hammerhead\nshark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*whale.*',
        ), 'Whale shark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*black.*',
        ), 'Blacktip\nshark', regex=True)

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
        ), 'Whiptail\nshark', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*zambes.*',
        ), 'Zambesi\nshark', regex=True)

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
            r'(?i).*[01]\.?.*m?.*',
        ), 'Smaller\nsharks', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*big.*',
            r'(?i).*large.*',
            r'(?i).*long.*',
            r'(?i).*[456789]\.?.*m?.*',
        ), 'Bigger\nsharks', regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*invo.*',
            r'(?i).*unknown.*',
            r'(?i).*possib.*',
            r'(?i).*question.*',
            r'(?i).*not.*',
            r'(?i).*uniden.*',
            r'(?i).*inval.*',
            r'(?i).*doubt.*',
            r'(?i).*[23].*',
        ), None, regex=True)

        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].replace((
            r'(?i).*shark\'s.*',
            r'(?i).*pack.*',
            r'(?i).*school.*',
            r'(?i).*number.*',
        ), 'Multiple\nsharks', regex=True)

        value_counts = df_to_clean['SPECIES'].value_counts()
        df_to_clean['SPECIES'] = df_to_clean['SPECIES'].map(
            # lambda species: 'Other' if value_counts.get(species, 0) < 10 else species
            lambda species: None if value_counts.get(species, 0) < 10 else species
        )

        return df_to_clean


class UnivariateAnalysis:
    def __init__(self, clean_dataframe):
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

        self.brazil_analysis()

        pyplot.close()

        return print("\nAnalysis finished.\n")

    def year_analysis(self):
        print("Analysing years...")
        attacks_by_year = self.dataframe['YEAR'].value_counts().to_dict()

        return attacks_by_year

    def type_analysis(self):
        print("Analysing types...")
        type_count = self.dataframe['TYPE'].value_counts().to_dict()

        type_percentage = type_count
        for key, value in type_percentage.items():
            type_percentage[key] = ( value / sum(type_percentage.values()) ) * 100

        type_percentage = pd.Series(type_percentage).head(10).sort_values(ascending=False).to_dict()

        names = type_percentage.keys()
        count = type_percentage.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.bar(names, count, width=0.6)
        pyplot.title("Rate of shark attacks by type")
        pyplot.ylabel("Rate of shark attacks (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)
        
        pyplot.savefig('views/attacks_by_type.png', dpi=300, bbox_inches='tight')
        

        return type_count

    def country_analysis(self):
        print("Analysing countries...")
        # attacks_by_country = self.dataframe['COUNTRY'].value_counts().index[:20]
        attacks_by_country = self.dataframe['COUNTRY'].value_counts().to_dict()

        country_percentage = attacks_by_country
        for key, value in country_percentage.items():
            country_percentage[key] = ( value / sum(country_percentage.values()) ) * 100

        country_percentage = pd.Series(country_percentage).head(10).sort_values(ascending=False).to_dict()

        names = country_percentage.keys()
        count = country_percentage.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.bar(names, count, width=0.6)
        pyplot.title("Rate of shark attacks by country")
        pyplot.ylabel("Rate of shark attacks (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)
        
        pyplot.savefig('views/attacks_by_country.png', dpi=300, bbox_inches='tight')
        

        return attacks_by_country

    def activity_analysis(self):
        print("Analysing activities...")
        activity_count = self.dataframe['ACTIVITY'].value_counts().to_dict()

        activity_percentage = activity_count
        for key, value in activity_percentage.items():
            activity_percentage[key] = ( value / sum(activity_percentage.values()) ) * 100

        activity_percentage = pd.Series(activity_percentage).head(10).sort_values(ascending=False).to_dict()

        names = activity_percentage.keys()
        count = activity_percentage.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.bar(names, count, width=0.6)
        pyplot.title("Rate of shark attacks by activity")
        pyplot.ylabel("Rate of shark attacks (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)
        
        pyplot.savefig('views/attacks_by_activity.png', dpi=300, bbox_inches='tight')
        

        return activity_count

    def age_analysis(self):
        print("Analysing age...")
        bins = [0, 15, 25, 60, float('inf')]
        labels = ['Under 15', 'Between 15 and 25', 'Between 25 and 60', 'Over 60']

        self.dataframe['AGE'] = pd.cut(self.dataframe['AGE'], bins=bins, labels=labels, right=False)

        age_count = self.dataframe['AGE'].value_counts().to_dict()
        
        return age_count

    def injury_analysis(self):
        print("Analysing injuries...")
        injury_count = self.dataframe['INJURY'].value_counts().to_dict()

        injury_percentage = injury_count
        for key, value in injury_percentage.items():
            injury_percentage[key] = ( value / sum(injury_percentage.values()) ) * 100

        injury_percentage = pd.Series(injury_percentage).head(10).sort_values(ascending=False).to_dict()
        del injury_percentage['Fatal']

        names = injury_percentage.keys()
        count = injury_percentage.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.bar(names, count, width=0.6)
        pyplot.title("Rate of injuries by shark attacks")
        pyplot.ylabel("Rate of injuries (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)
        
        pyplot.savefig('views/attacks_by_injury.png', dpi=300, bbox_inches='tight')
        

        return injury_count

    def fatality_analysis(self):
        print("Analysing fatalities...")
        total_attacks = len(self.dataframe['FATALITY']) # 6302
        total_registers = self.dataframe['FATALITY'].count() # não conta None # 5691
        fatalities = self.dataframe['FATALITY'].value_counts().get('Y') # 1389
        non_fatalities = self.dataframe['FATALITY'].value_counts().get('N') # 4302
        missing_fatalities = self.dataframe['FATALITY'].isna().sum() # 611

        fatality_percentage = round( (fatalities / total_registers) * 100)
        missing_positives_proportion = round(missing_fatalities * fatality_percentage/100)
        missing_negatives_proportion = missing_fatalities - missing_positives_proportion

        fatalities += missing_positives_proportion
        non_fatalities += missing_negatives_proportion

        # new_fatality_percentage = round((fatalities / total_registers) * 100)

        fatality_analysis = {}
        fatality_analysis['Fatalities'] = fatalities
        fatality_analysis['Non-fatalitiies'] =  non_fatalities

        # fatality_analysis['Total attacks'] = total_attacks
        # fatality_analysis['Unkown'] = missing_fatalities
        # fatality_analysis['Fatality percentage'] = (fatality_percentage + new_fatality_percentage) / 2
        # fatality_percentage = fatality_analysis
        # for key, value in fatality_percentage.items():
        #     fatality_percentage[key] = ( value / sum(fatality_percentage.values()) ) * 100
        # names = fatality_percentage.keys()
        # count = fatality_percentage.values()
        # pyplot.figure(figsize=(13, 9))
        # pyplot.bar(names, count, width=0.6)
        # pyplot.title("Rate of fatality by shark attacks")
        # pyplot.ylabel("Rate of fatality (%)")
        # pyplot.xticks(range(len(names)), names, fontsize=12)
        # pyplot.savefig('views/attacks_by_fatality.png', dpi=300, bbox_inches='tight')
        # 

        names = fatality_analysis.keys()
        count = fatality_analysis.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.pie(
            count,
            labels=names,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12}
        )
        pyplot.title("Rate of fatality by shark attacks", fontsize=16)
        pyplot.savefig('views/attacks_by_fatality_pie.png', dpi=300, bbox_inches='tight')
        

        return fatality_analysis

    def time_analysis(self):
        print("Analysing time...")

        bins = [0, 5, 12, 18, float('inf')]
        labels = ['Night', 'Morning', 'Afternoon', 'Evening']

        self.dataframe['TIME'] = pd.cut(self.dataframe['TIME'], bins=bins, labels=labels, right=False)

        time_analysis_unordered = self.dataframe['TIME'].value_counts().to_dict()

        time_analysis = {}
        time_analysis['Morning'] = time_analysis_unordered['Morning']
        time_analysis['Afternoon'] = time_analysis_unordered['Afternoon']
        time_analysis['Evening'] = time_analysis_unordered['Evening']
        time_analysis['Night'] = time_analysis_unordered['Night']

        time_analysis_percentage = time_analysis
        for key, value in time_analysis_percentage.items():
            time_analysis_percentage[key] = ( value / sum(time_analysis.values()) ) * 100

        time_analysis_percentage = pd.Series(time_analysis_percentage).head(10).to_dict()

        names = time_analysis_percentage.keys()
        count = time_analysis_percentage.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.plot(names, count, linestyle='solid', linewidth=3)
        pyplot.title("Rate of shark attacks by time of the day")
        pyplot.ylabel("Rate of shark attacks (%)")
        
        pyplot.savefig('views/attacks_by_time.png', dpi=300, bbox_inches='tight')
        

        return time_analysis

    def species_analysis(self):
        print("Analysing species...")
        species_count = self.dataframe['SPECIES'].value_counts().to_dict()

        species_percentage = species_count
        for key, value in species_percentage.items():
            species_percentage[key] = ( value / sum(species_percentage.values()) ) * 100

        species_percentage = pd.Series(species_percentage).head(10).sort_values(ascending=False).to_dict()

        names = species_percentage.keys()
        count = species_percentage.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.bar(names, count, width=0.6)
        pyplot.title("Rate of shark attacks by species")
        pyplot.ylabel("Rate of shark attacks (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)
        
        pyplot.savefig('views/attacks_by_species.png', dpi=300, bbox_inches='tight')
        
        
        return species_count
    
    def brazil_attacks_by_area(self):
        area_filter = self.dataframe['COUNTRY'] == 'BRAZIL'
        brazil_attacks = self.dataframe[area_filter]['AREA'].value_counts().to_dict()

        names = brazil_attacks.keys()
        count = brazil_attacks.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.bar(names, count, width=0.4)
        pyplot.title("Number of shark attacks by area in Brazil")
        pyplot.ylabel("Number of attacks")
        pyplot.xticks(range(len(names)), names, fontsize=9)
        
        pyplot.savefig('views/brazil_attacks_by_area.png', dpi=300, bbox_inches='tight')
        

        return brazil_attacks
    
    def brazil_attacks_by_location(self):
        area_filter = self.dataframe['COUNTRY'] == 'BRAZIL'
        brazil_attacks = self.dataframe[area_filter]['LOCATION'].value_counts().to_dict()

        names = brazil_attacks.keys()
        count = brazil_attacks.values()
        pyplot.figure(figsize=(13, 9))
        pyplot.bar(names, count, width=0.4)
        pyplot.title("Number of attacks by location in Brazil")
        pyplot.ylabel("Number of attacks")
        pyplot.xticks(range(len(names)), names, fontsize=9)
        
        pyplot.savefig('views/brazil_attacks_by_location.png', dpi=300, bbox_inches='tight')
        

        return brazil_attacks
    
    def brazil_analysis(self):
        print("\nRunning Brazil analysis...")
        self.brazil_attacks_by_area()
        self.brazil_attacks_by_location()


class BivariateAnalysis(UnivariateAnalysis):
    def __init__(self, clean_dataframe):
        super().__init__(clean_dataframe)

        self.fatality_by_type()
        self.fatality_by_activity() # 'Murder' key should not be further considered because of its redundancy, but suggests that the algorithm is correct (as it has 100% of fatalities)
        self.fatality_by_country()
        self.fatality_by_injury()
        self.fatality_by_species()

        self.attacks_by_species_by_country()
        self.attacks_by_species_by_country()

        pyplot.close()

    def fatality_by_type(self):
        print("Analysing fatality by type...") # Chance of death by type
        all_types = self.dataframe['TYPE'].value_counts().index.to_list()

        type_fatality_percentage = {}
        attacks_by_type = self.type_analysis()

        for type in all_types:

            type_fatal_attacks = self.dataframe[(self.dataframe['TYPE'] == type) & (self.dataframe['FATALITY'] == 'Y')]
            type_unfatal_attacks = self.dataframe[(self.dataframe['TYPE'] == type) & (self.dataframe['FATALITY'] == 'N')]

            other_types = [type for type in all_types if type != type]
            other_fatal_attacks = self.dataframe[(self.dataframe['TYPE'].isin(other_types)) & (self.dataframe['FATALITY'] == 'Y')]
            other_unfatal_attacks = self.dataframe[(self.dataframe['TYPE'].isin(other_types)) & (self.dataframe['FATALITY'] == 'N')]

            all_attacks_count = int(
                len(type_fatal_attacks)
                + len(type_unfatal_attacks)
                + len(other_fatal_attacks)
                + len(other_unfatal_attacks)
            )

            type_modifier = ( attacks_by_type[type] / sum(attacks_by_type.values()) ) * 100

            if len(type_fatal_attacks) != 0:
                type_fatality_proportion = round( ((len(type_fatal_attacks) / all_attacks_count) * 100) * type_modifier )
                type_fatality_percentage[type] = type_fatality_proportion

        for key, value in type_fatality_percentage.items():
            type_fatality_percentage[key] = ( value / sum(type_fatality_percentage.values()) ) * 100

        type_fatality_percentage = pd.Series(type_fatality_percentage).head(10).sort_values(ascending=False).to_dict()

        names = type_fatality_percentage.keys()
        fatalities_count = type_fatality_percentage.values()
        pyplot.figure(figsize=(13, 9)) 
        pyplot.bar(names, fatalities_count, width=0.6, color='darkred')
        pyplot.title("Fatality rate of shark attacks by type")
        pyplot.ylabel("Fatality rate (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)

        pyplot.savefig('views/fatality_by_type.png', dpi=300, bbox_inches='tight')
        

        return type_fatality_percentage

    def fatality_by_activity(self):
        print("Analysing fatality by activity...") # Chance of death by activity
        all_activities = self.dataframe['ACTIVITY'].value_counts().index.to_list()
        all_activities.remove('Murder')

        activity_fatality_percentage = {}
        attacks_by_activity = self.activity_analysis()

        for activity in all_activities:

            activity_fatal_attacks = self.dataframe[(self.dataframe['ACTIVITY'] == activity) & (self.dataframe['FATALITY'] == 'Y')]
            activity_unfatal_attacks = self.dataframe[(self.dataframe['ACTIVITY'] == activity) & (self.dataframe['FATALITY'] == 'N')]

            other_activities = [activity for activity in all_activities if activity != activity]
            other_fatal_attacks = self.dataframe[(self.dataframe['ACTIVITY'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'Y')]
            other_unfatal_attacks = self.dataframe[(self.dataframe['ACTIVITY'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'N')]

            all_attacks_count = int(
                len(activity_fatal_attacks)
                + len(activity_unfatal_attacks)
                + len(other_fatal_attacks)
                + len(other_unfatal_attacks)
            )

            activity_modifier = ( attacks_by_activity[activity] / sum(attacks_by_activity.values()) ) * 100
            
            if len(activity_fatal_attacks) != 0:
                activity_fatality_proportion = round( ((len(activity_fatal_attacks) / all_attacks_count) * 100) * activity_modifier)
                activity_fatality_percentage[activity] = activity_fatality_proportion

        for key, value in activity_fatality_percentage.items():
            activity_fatality_percentage[key] = ( value / sum(activity_fatality_percentage.values()) ) * 100

        activity_fatality_percentage = pd.Series(activity_fatality_percentage).head(10).sort_values(ascending=False).to_dict()

        names = activity_fatality_percentage.keys()
        fatalities_count = activity_fatality_percentage.values()
        pyplot.figure(figsize=(13, 9)) 
        pyplot.bar(names, fatalities_count, width=0.6, color='darkred')
        pyplot.title("Fatality rate of shark attacks by activity")
        pyplot.ylabel("Fatality rate (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)

        pyplot.savefig('views/fatality_by_activity.png', dpi=300, bbox_inches='tight')
        

        return activity_fatality_percentage
    
    def fatality_by_country(self):
        print("Analysing fatality by country...")
        all_countries = self.dataframe['COUNTRY'].value_counts().index.to_list()

        country_fatality_percentage = {}
        attacks_by_country = self.country_analysis()

        for country in all_countries:

            country_fatal_attacks = self.dataframe[(self.dataframe['COUNTRY'] == country) & (self.dataframe['FATALITY'] == 'Y')]
            country_unfatal_attacks = self.dataframe[(self.dataframe['COUNTRY'] == country) & (self.dataframe['FATALITY'] == 'N')]

            other_activities = [country for country in all_countries if country != country]
            other_fatal_attacks = self.dataframe[(self.dataframe['COUNTRY'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'Y')]
            other_unfatal_attacks = self.dataframe[(self.dataframe['COUNTRY'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'N')]

            all_attacks_count = int(
                len(country_fatal_attacks)
                + len(country_unfatal_attacks)
                + len(other_fatal_attacks)
                + len(other_unfatal_attacks)
            )

            country_modifier = ( attacks_by_country[country] / sum(attacks_by_country.values()) ) * 100

            if len(country_fatal_attacks) != 0:
                country_fatality_proportion = round( ((len(country_fatal_attacks) / all_attacks_count) * 100) * country_modifier )
                country_fatality_percentage[country] = country_fatality_proportion

        for key, value in country_fatality_percentage.items():
            country_fatality_percentage[key] = ( value / sum(country_fatality_percentage.values()) ) * 100

        country_fatality_percentage = pd.Series(country_fatality_percentage).head(10).sort_values(ascending=False).to_dict()
            
        names = country_fatality_percentage.keys()
        fatalities_count = country_fatality_percentage.values()
        pyplot.figure(figsize=(13, 9)) 
        pyplot.bar(names, fatalities_count, width=0.6, color='darkred')
        pyplot.title("Fatality rate of shark attacks by country")
        pyplot.ylabel("Fatality rate (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)

        pyplot.savefig('views/fatality_by_country.png', dpi=300, bbox_inches='tight')
        

        return country_fatality_percentage

    def fatality_by_injury(self):
        print("Analysing fatality by injury...") # Chance of death by each injury
        all_injuries = self.dataframe['INJURY'].value_counts().index.to_list()
        all_injuries.remove('Fatal')
        all_injuries.remove('Eaten')
        all_injuries.remove('Drowned')

        injury_fatality_percentage = {}
        attacks_by_injury = self.injury_analysis()

        for injury in all_injuries:

            injury_fatal_attacks = self.dataframe[(self.dataframe['INJURY'] == injury) & (self.dataframe['FATALITY'] == 'Y')]
            injury_unfatal_attacks = self.dataframe[(self.dataframe['INJURY'] == injury) & (self.dataframe['FATALITY'] == 'N')]

            other_activities = [injury for injury in all_injuries if injury != injury]
            other_fatal_attacks = self.dataframe[(self.dataframe['INJURY'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'Y')]
            other_unfatal_attacks = self.dataframe[(self.dataframe['INJURY'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'N')]

            all_attacks_count = int(
                len(injury_fatal_attacks)
                + len(injury_unfatal_attacks)
                + len(other_fatal_attacks)
                + len(other_unfatal_attacks)
            )

            injury_modifier = ( attacks_by_injury[injury] / sum(attacks_by_injury.values()) ) * 100

            if len(injury_fatal_attacks) != 0:
                injury_fatality_proportion = round( ((len(injury_fatal_attacks) / all_attacks_count) * 100) * injury_modifier )
                injury_fatality_percentage[injury] = injury_fatality_proportion

        for key, value in injury_fatality_percentage.items():
            injury_fatality_percentage[key] = ( value / sum(injury_fatality_percentage.values()) ) * 100

        injury_fatality_percentage = pd.Series(injury_fatality_percentage).head(10).sort_values(ascending=False).to_dict()

        names = injury_fatality_percentage.keys()
        fatalities_count = injury_fatality_percentage.values()
        pyplot.figure(figsize=(13, 9)) 
        pyplot.bar(names, fatalities_count, width=0.6, color='darkred')
        pyplot.title("Fatality rate of shark attacks based on injury")
        pyplot.ylabel("Fatality rate (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)

        pyplot.savefig('views/fatality_by_injury.png', dpi=300, bbox_inches='tight')
        

        return injury_fatality_percentage

    def fatality_by_species(self):
        print("Analysing fatality by species...") # Chance of death by each species
        all_species = self.dataframe['SPECIES'].value_counts().index.to_list()

        species_fatality_percentage = {}
        attacks_by_species = self.species_analysis()

        for species in all_species:

            species_fatal_attacks = self.dataframe[(self.dataframe['SPECIES'] == species) & (self.dataframe['FATALITY'] == 'Y')]
            species_unfatal_attacks = self.dataframe[(self.dataframe['SPECIES'] == species) & (self.dataframe['FATALITY'] == 'N')]

            other_activities = [species for species in all_species if species != species]
            other_fatal_attacks = self.dataframe[(self.dataframe['SPECIES'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'Y')]
            other_unfatal_attacks = self.dataframe[(self.dataframe['SPECIES'].isin(other_activities)) & (self.dataframe['FATALITY'] == 'N')]

            all_attacks_count = int(
                len(species_fatal_attacks)
                + len(species_unfatal_attacks)
                + len(other_fatal_attacks)
                + len(other_unfatal_attacks)
            )

            species_modifier = ( attacks_by_species[species] / sum(attacks_by_species.values()) ) * 100

            if len(species_fatal_attacks) != 0:
                species_fatality_proportion = round( ((len(species_fatal_attacks) / all_attacks_count) * 100) * species_modifier )
                species_fatality_percentage[species] = species_fatality_proportion

        for key, value in species_fatality_percentage.items():
            species_fatality_percentage[key] = ( value / sum(species_fatality_percentage.values()) ) * 100
            
        species_fatality_percentage = pd.Series(species_fatality_percentage).head(10).sort_values(ascending=False).to_dict()

        names = species_fatality_percentage.keys()
        fatalities_count = species_fatality_percentage.values()
        pyplot.figure(figsize=(13, 9)) 
        pyplot.bar(names, fatalities_count, width=0.6, color='darkred')
        pyplot.title("Fatality rate of shark attacks by species")
        pyplot.ylabel("Fatality rate (%)")
        pyplot.xticks(range(len(names)), names, fontsize=9)

        pyplot.savefig('views/fatality_by_species.png', dpi=300, bbox_inches='tight')
        

        return species_fatality_percentage

    def attacks_by_area_by_country(self):
        print("Analysing attacks by area and country...")
        attacks_by_area_by_countries = defaultdict(dict) # {'COUNTRY_A':{'area_1':74, 'area_2':11}, 'COUNTRY_B':{} }

        for country in self.dataframe.country_analysis().keys():
            area_filter = self.dataframe['COUNTRY'] == str(country)

            attacks_by_area_by_countries[str(country)] = self.dataframe[area_filter]['AREA'].value_counts().to_dict()

        return attacks_by_area_by_countries
    
    def attacks_by_species_by_country(self):
        all_countries = self.dataframe['COUNTRY'].value_counts().head(10).to_dict()
        all_activities = self.dataframe['SPECIES'].value_counts().head(10).to_dict() # All species
        # del all_countries['BAHAMAS']
        # del all_countries['FIJI']
        # del all_countries['ITALY']

        attacks_by_country = self.country_analysis()

        activity_fatality_by_country = {}

        for country in all_countries:
            fatality_by_activity = {}

            for activity in all_activities:

                activity_fatal_attacks = self.dataframe[(self.dataframe['SPECIES'] == activity) & (self.dataframe['COUNTRY'] == country)]
                activity_nonfatal_attacks = self.dataframe[(self.dataframe['SPECIES'] == activity) & (self.dataframe['COUNTRY'] == country)]

                # country_modifier = ( attacks_by_country[country] / sum(attacks_by_country.values()) ) * 100
                country_modifier = 1

                if len(activity_fatal_attacks) != 0:
                    activity_fatality = round((len(activity_fatal_attacks) / (len(activity_fatal_attacks) + len(activity_nonfatal_attacks)) ) * 100) * country_modifier
                    fatality_by_activity[activity] = activity_fatality

                for key, value in fatality_by_activity.items():
                    fatality_by_activity[key] = ( value / sum(fatality_by_activity.values()) ) * 100

            activity_fatality_by_country[country] = fatality_by_activity

        countries = list(activity_fatality_by_country.keys())
        activities = list(activity_fatality_by_country[countries[0]].keys())

        values = {activity: [activity_fatality_by_country[country].get(activity, 0) for country in countries] for activity in activities}

        x = np.arange(len(countries))
        width = 0.1
        fig, ax = pyplot.subplots(figsize=(15, 11))

        for i, activity in enumerate(activities):
            ax.bar(x + i * width, values[activity], width, label=activity)

        ax.set_ylabel("Rate (%)", fontsize=12)
        ax.set_title("Rate of shark attacks by species and country")
        tick_positions = x + (width * (len(activities) - 1) / 2)
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(countries, fontsize=12)
        ax.legend(title="Species", fontsize=12)

        pyplot.tight_layout()
        pyplot.savefig('views/attacks_by_species_by_country.png', dpi=300, bbox_inches='tight')
        
        return activity_fatality_by_country


class MultivariateAnalysis(BivariateAnalysis):
    def __init__(self, clean_dataframe):
        super().__init__(clean_dataframe)

        self.activity_fatality_by_country()
        self.species_fatality_by_country()

        pyplot.close()

    def activity_fatality_by_country(self):
        all_countries = self.dataframe['COUNTRY'].value_counts().head(10).to_dict()
        all_activities = self.dataframe['ACTIVITY'].value_counts().head(10).to_dict()
        del all_activities['Plane involved']
        del all_activities['Ship involved']
        del all_activities['Sinking']

        attacks_by_country = self.country_analysis()

        activity_fatality_by_country = {}

        for country in all_countries:
            fatality_by_activity = {}

            for activity in all_activities:

                activity_fatal_attacks = self.dataframe[(self.dataframe['ACTIVITY'] == activity) & (self.dataframe['FATALITY'] == 'Y') & (self.dataframe['COUNTRY'] == country)]
                activity_nonfatal_attacks = self.dataframe[(self.dataframe['ACTIVITY'] == activity) & (self.dataframe['FATALITY'] == 'N') & (self.dataframe['COUNTRY'] == country)]

                country_modifier = ( attacks_by_country[country] / sum(attacks_by_country.values()) ) * 100

                if len(activity_fatal_attacks) != 0:
                    activity_fatality = round((len(activity_fatal_attacks) / (len(activity_fatal_attacks) + len(activity_nonfatal_attacks)) ) * 100) * country_modifier
                    fatality_by_activity[activity] = activity_fatality

                for key, value in fatality_by_activity.items():
                    fatality_by_activity[key] = ( value / sum(fatality_by_activity.values()) ) * 100

            activity_fatality_by_country[country] = fatality_by_activity

        countries = list(activity_fatality_by_country.keys())
        activities = list(activity_fatality_by_country[countries[0]].keys())

        values = {activity: [activity_fatality_by_country[country].get(activity, 0) for country in countries] for activity in activities}

        x = np.arange(len(countries))
        width = 0.1
        fig, ax = pyplot.subplots(figsize=(15, 11))

        for i, activity in enumerate(activities):
            ax.bar(x + i * width, values[activity], width, label=activity)

        ax.set_ylabel("Fatality rate (%)", fontsize=12)
        ax.set_title("Shark attacks fatality rate by activity and country")
        tick_positions = x + (width * (len(activities) - 1) / 2)
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(countries, fontsize=12)
        ax.legend(title="Activities", fontsize=12)

        pyplot.tight_layout()
        pyplot.savefig('views/fatality_by_activity_and_country.png', dpi=300, bbox_inches='tight')
        

        return activity_fatality_by_country
    
    def species_fatality_by_country(self):
        all_countries = self.dataframe['COUNTRY'].value_counts().head(10).to_dict()
        all_activities = self.dataframe['SPECIES'].value_counts().head(10).to_dict()
        del all_countries['BAHAMAS']
        del all_countries['FIJI']
        del all_countries['ITALY']

        attacks_by_country = self.country_analysis()

        activity_fatality_by_country = {}

        for country in all_countries:
            fatality_by_activity = {}

            for activity in all_activities:

                activity_fatal_attacks = self.dataframe[(self.dataframe['SPECIES'] == activity) & (self.dataframe['FATALITY'] == 'Y') & (self.dataframe['COUNTRY'] == country)]
                activity_nonfatal_attacks = self.dataframe[(self.dataframe['SPECIES'] == activity) & (self.dataframe['FATALITY'] == 'N') & (self.dataframe['COUNTRY'] == country)]

                country_modifier = ( attacks_by_country[country] / sum(attacks_by_country.values()) ) * 100

                if len(activity_fatal_attacks) != 0:
                    activity_fatality = round((len(activity_fatal_attacks) / (len(activity_fatal_attacks) + len(activity_nonfatal_attacks)) ) * 100) * country_modifier
                    fatality_by_activity[activity] = activity_fatality

                for key, value in fatality_by_activity.items():
                    fatality_by_activity[key] = ( value / sum(fatality_by_activity.values()) ) * 100

            activity_fatality_by_country[country] = fatality_by_activity

        countries = list(activity_fatality_by_country.keys())
        activities = list(activity_fatality_by_country[countries[0]].keys())

        values = {activity: [activity_fatality_by_country[country].get(activity, 0) for country in countries] for activity in activities}

        x = np.arange(len(countries))
        width = 0.1
        fig, ax = pyplot.subplots(figsize=(15, 11))

        for i, activity in enumerate(activities):
            ax.bar(x + i * width, values[activity], width, label=activity)

        ax.set_ylabel("Fatality rate (%)", fontsize=12)
        ax.set_title("Shark attacks fatality rate by species and country")
        tick_positions = x + (width * (len(activities) - 1) / 2)
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(countries, fontsize=12)
        ax.legend(title="Species", fontsize=12)

        pyplot.tight_layout()
        pyplot.savefig('views/fatality_by_species and.png', dpi=300, bbox_inches='tight')
        

        return activity_fatality_by_country


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

    # univariate_analysis = UnivariateAnalysis(dataframe)
    # bivariate_analysis = BivariateAnalysis(dataframe)
    multivariate_analysis = MultivariateAnalysis(dataframe)

    return print("\nJAWS FINISHED\n")

if __name__ == '__main__':
    main()