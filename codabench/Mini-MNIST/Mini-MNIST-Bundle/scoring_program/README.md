# Scoring Program
- Scoring program is responsible for loading Reference Data(test labels) from `reference_data` directory. 

- It also loads ingestion result from `sample_result_submission` directory.
- Scoring program computes score and saves to  also saves to `scoring_output` directory

To run scoring step locally, use the following commands

Go to the Competition Bundle directory
```
cd Competition_Bundle
```

Run Scoring
```
python3 scoring_program/run_scoring.py
```

***


### ⚠️ NOTE:
- DO NOT change `metadata.yaml` file. This file is used by codabench to run your ingestion program
- DO NOT delete `metadata.yaml` file
- Directories names are different locally and on Codabench. Do not get confused by this. The bundle is setup in a way that you do not have to change the directories. Locally it will use local directories if you run scoring without `--codabench` flag.
