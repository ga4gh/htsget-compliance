#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: htsget-compliance
hints:
    DockerRequirement:
        dockerPull: ga4gh/htsget-compliance:latest
inputs:
    orchestrator_url:
        type: string
        inputBinding:
            position: 1
outputs: []