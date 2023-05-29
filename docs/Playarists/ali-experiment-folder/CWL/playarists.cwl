cwlVersion: v1.0
class: CommandLineTool
baseCommand: python run_workflow.py
inputs:
  batch_size:
    type: int
    inputBinding:
      prefix: --batch_size
  max_workers:
    type: int
    inputBinding:
      prefix: --max_workers
  oc_meta:
    type: File
    inputBinding:
      prefix: --oc_meta
  erih_plus:
    type: File
    inputBinding:
      prefix: --erih_plus
  doaj:
    type: File
    inputBinding:
      prefix: --doaj
outputs:
  result:
    type: stdout
