cwlVersion: v1.0
class: CommandLineTool
id: extract-pubyear

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