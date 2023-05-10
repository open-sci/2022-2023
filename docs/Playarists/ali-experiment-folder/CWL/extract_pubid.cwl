cwlVersion: v1.0
class: CommandLineTool
id: extract-pubid

baseCommand: python

inputs:
  input_csv:
    type: File
    inputBinding:
      position: 1
  output_csv:
    type: string
    inputBinding:
      position: 2
  python_script:
    type: File
    inputBinding:
      position: 0

outputs:
  extracted_pubid:
    type: File
    outputBinding:
      glob: $(inputs.output_csv)