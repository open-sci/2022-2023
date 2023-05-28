import os
import pandas as pd
import csv

def detect_delimiter(file_path): #this is to find that the csv has ; and not , as delimeter
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        dialect = csv.Sniffer().sniff(file.read(1024))
    return dialect.delimiter

delimiter = detect_delimiter('ERIHPLUSapprovedJournals.csv')
erih_plus_df = pd.read_csv('ERIHPLUSapprovedJournals.csv', sep=delimiter)

###

def process_meta_csv(file_path, e_df):
    meta_data = pd.read_csv(file_path)
    meta_data['venue'] = meta_data['venue'].astype(str)
    meta_data['issn'] = meta_data['venue'].str.extract(r'issn:(\d{4}-\d{3}[\dX])') # creating a cloumn for issn?
    # some lines don't have volume information + look at file organization
    # this regex just matches the numbers and not issn: part
    
    # Extract the identifier (OMID) from the 'id' column
    # THIS ACTUALLY CHANGES THE ID COLUMN CONTENT
    meta_data['id'] = meta_data['id'].str.extract(r'(meta:[^ ]*)')

    merged_data_print = e_df.merge(meta_data, left_on='Print ISSN', right_on='issn', how='inner') 
    merged_data_online = e_df.merge(meta_data, left_on='Online ISSN', right_on='issn', how='inner')
    merged_data = pd.concat([merged_data_print, merged_data_online], ignore_index=True)
    
    # Keep only the relevant columns for the mapping dataframe
    merged_data = merged_data[['id', 'issn', 'Journal ID', 'Print ISSN', 'Online ISSN']].rename(columns={'id': 'OC_OMID', 'issn': 'OC_ISSN', 'Journal ID': 'EP_ID', 'Print ISSN': 'EP_Print_ISSN', 'Online ISSN': 'EP_Online_ISSN'})
    
    # Create the 'EP_ISSN' column
    merged_data['EP_ISSN'] = merged_data['EP_Print_ISSN'].combine_first(merged_data['EP_Online_ISSN'])
    
    # Drop the 'EP_Print_ISSN' and 'EP_Online_ISSN' columns
    merged_data = merged_data.drop(columns=['EP_Print_ISSN', 'EP_Online_ISSN'])

    return merged_data

merged_data = process_meta_csv('0.csv', erih_plus_df)
print(merged_data)

###

csv_directory = ''
merged_data = pd.DataFrame()

for file_name in os.listdir(csv_directory):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_directory, file_name)
        merged_data_file = process_meta_csv(file_path, erih_plus_df)
        merged_data = pd.concat([merged_data, merged_data_file], ignore_index=True)

###

new_merged_data = merged_data.dropna(subset=['OC_ISSN']).reset_index(drop=True)

###

doaj_file_path = 'journalcsv__doaj.csv'
doaj_df = pd.read_csv(doaj_file_path, encoding="UTF-8")

###

new_doaj = doaj_df.iloc[1:, [5, 6, 10]]
new_doaj.columns

###
open_access_dict = {}

for index, row in new_doaj.iterrows():
    open_access_dict[row['Journal ISSN (print version)']] = True
    open_access_dict[row['Journal EISSN (online version)']] = True

###

# Merge Open Access information with the main dataframe
new_merged_data['Open Access'] = new_merged_data['OC_ISSN'].map(open_access_dict)

# Fill missing Open Access information with 'Unknown'
new_merged_data['Open Access'] = new_merged_data['Open Access'].fillna('Unknown')





