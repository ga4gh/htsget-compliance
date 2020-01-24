#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: htsget-compliance
hints:
    DockerRequirement:
        dockerPull: ga4gh/htsget-compliance:latest
inputs:
    output_file:
        type: string?
        inputBinding:
            position: 1
            prefix: --file
    testbed_url:
        type: string?
        inputBinding:
            position: 2
            prefix: --testbed-url
    htsget_url:
        type: string
        inputBinding:
            position: 3
outputs: []