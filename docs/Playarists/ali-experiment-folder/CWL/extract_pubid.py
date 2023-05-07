import pandas as pd
import sys

input_csv = sys.argv[1]
output_csv = sys.argv[2]

df = pd.read_csv(input_csv)
#pubyear = df['PubYear']
pubid=df.iloc[:, 1]

pubid.to_csv(output_csv, index=False, header=True)
