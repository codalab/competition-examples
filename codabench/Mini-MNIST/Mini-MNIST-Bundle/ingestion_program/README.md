# Ingestion Program
- Ingestion program is responsible for loading Input Data(training data, training labels, and test data) from `input_data` directory. 
- It also loads a model from `sample_code_submission` directory which is used by ingestion for training and predictions. 
- Ingestion also saves the predictions in `sample_result_submission` directory

To run ingestion step locally, use the following commands

Go to the Competition Bundle directory
```
cd Competition_Bundle
```

Run Ingestion
```
python3 ingestion_program/run_ingestion.py
```

***


### ⚠️ NOTE:
- DO NOT change `metadata.yaml` file. This file is used by codabench to run your ingestion program
- DO NOT delete `metadata.yaml` file
- Directories names are different locally and on Codabench. Do not get confused by this. The bundle is setup in a way that you do not have to change the directories. Locally it will use local directories if you run ingestion without `--codabench` flag.
