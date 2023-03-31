cwlVersion: v1.0
class: CommandLineTool
id: extract-pubyear

requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: extract_pubyear.py
        entry: |
          ${
            var script = ' 
                import pandas as pd
                import sys

                input_csv = sys.argv[1]
                output_csv = sys.argv[2]

                df = pd.read_csv(input_csv)
                pubyear = df['PubYear']

                pubyear.to_csv(output_csv, index=False, header=True)'
            return script;
           }

baseCommand: python

arguments:
  - valueFrom: extract_pubyear.py

inputs:
  input_csv:
    type: File
    inputBinding:
      position: 1
  output_csv:
    type: string
    inputBinding:
      position: 2

outputs:
  extracted_pubyear:
    type: File
    outputBinding:
      glob: $(inputs.output_csv)