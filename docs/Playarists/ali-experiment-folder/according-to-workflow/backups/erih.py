import os
import pandas as pd
import csv
import glob
import concurrent.futures
from tqdm import tqdm

def detect_delimiter(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        dialect = csv.Sniffer().sniff(file.read(1024))
    return dialect.delimiter

delimiter = detect_delimiter('ERIHPLUSapprovedJournals.csv')
erih_plus_df = pd.read_csv('ERIHPLUSapprovedJournals.csv', sep=delimiter)

def process_meta_csv(chunk, erih_plus_df):
    meta_data = chunk
    meta_data['venue'] = meta_data['venue'].astype(str)
    meta_data['issn'] = meta_data['venue'].str.extract(r'issn:(\d{4}-\d{3}[\dX])')
    
    # Extract the identifier (OMID) from the 'id' column
    meta_data['id'] = meta_data['id'].str.extract(r'(meta:[^\s]*)')
    
    merged_data_print = erih_plus_df.merge(meta_data, left_on='Print ISSN', right_on='issn', how='inner')
    merged_data_online = erih_plus_df.merge(meta_data, left_on='Online ISSN', right_on='issn', how='inner')
    merged_data = pd.concat([merged_data_print, merged_data_online], ignore_index=True)
    
    # Keep only the relevant columns for the mapping dataframe
    merged_data = merged_data[['id', 'issn', 'Journal ID', 'Print ISSN', 'Online ISSN']].rename(columns={'id': 'OC_OMID', 'issn': 'OC_ISSN', 'Journal ID': 'EP_ID', 'Print ISSN': 'EP_Print_ISSN', 'Online ISSN': 'EP_Online_ISSN'})
    
    # Create the 'EP_ISSN' column
    merged_data['EP_ISSN'] = merged_data['EP_Print_ISSN'].combine_first(merged_data['EP_Online_ISSN'])
    
    # Drop the 'EP_Print_ISSN' and 'EP_Online_ISSN' columns
    merged_data = merged_data.drop(columns=['EP_Print_ISSN', 'EP_Online_ISSN'])
    
    # Drop rows with NaN values in the 'OC_ISSN' column
    merged_data = merged_data.dropna(subset=['OC_ISSN']).reset_index(drop=True)

    return merged_data


def process_file(input_file, erih_plus_df):
    chunksize = 5 * 10 ** 3
    processed_chunks = []
    
    # Read the input_file in chunks and process each chunk
    with pd.read_csv(input_file, chunksize=chunksize) as reader:
        for chunk in reader:
            processed_chunk = process_meta_csv(chunk, erih_plus_df)
            processed_chunks.append(processed_chunk)

    # Combine the processed chunks into a single DataFrame
    return pd.concat(processed_chunks, ignore_index=True)

input_directory = "I:\\open-sci\\dump-files\\opencitations-meta\\partial_dump"
files = glob.glob(os.path.join(input_directory, "*.csv"))

# Number of files to process at once
batch_size = 100

all_results = []

# Initialize a progress bar to visualize the progress of processing batches of files
with tqdm(total=len(files), desc="Batches") as pbar:
    # Process files in batches
    for i in range(0, len(files), batch_size):
        # Get the current batch of files
        batch_files = files[i:i + batch_size]

        # Process the current batch of files using a ProcessPoolExecutor for parallelism
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            results = executor.map(process_file, batch_files, [erih_plus_df] * len(batch_files))
            all_results.extend(results)
        
        # Update the progress bar for each batch
        pbar.update(len(batch_files))

# Combine the results from all batches into a single DataFrame
final_df = pd.concat(all_results, ignore_index=True)

print("eat it!")
print(final_df.head(1))
