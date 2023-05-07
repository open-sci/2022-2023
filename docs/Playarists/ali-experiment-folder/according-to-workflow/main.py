import os
import pandas as pd
import glob
import concurrent.futures
from tqdm import tqdm
from utils import detect_delimiter
from process import process_file, process_file_wrapper

def main():
    delimiter = detect_delimiter('ERIHPLUSapprovedJournals.csv')
    erih_plus_df = pd.read_csv('ERIHPLUSapprovedJournals.csv', sep=delimiter)

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
                results = executor.map(process_file_wrapper, [(f, erih_plus_df) for f in batch_files])
                all_results.extend(results)

            # Update the progress bar for each batch
            pbar.update(len(batch_files))

    # Create a dictionary to store the results
    results_dict = {filename: result for filename, result in all_results}

    print("expected output for part 1.1:")
    print(results_dict[next(iter(results_dict))].head(1))

if __name__ == '__main__':
    main()

