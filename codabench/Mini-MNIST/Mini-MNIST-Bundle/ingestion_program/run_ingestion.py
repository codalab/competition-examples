# ------------------------------------------
# Imports
# ------------------------------------------
import os
import sys
import argparse

# ------------------------------------------
# Directories
# ------------------------------------------
module_dir = os.path.dirname(os.path.realpath(__file__))
root_dir_name = os.path.dirname(module_dir)

# ------------------------------------------
# Args
# ------------------------------------------
parser = argparse.ArgumentParser(
    description="This is script to run ingestion program for the competition"
)
parser.add_argument(
    "--codabench",
    help="True when running on Codabench",
    action="store_true",
)

# ------------------------------------------
# Main
# ------------------------------------------
if __name__ == "__main__":

    print("\n----------------------------------------------")
    print("Ingestion Program started!")
    print("----------------------------------------------\n\n")

    args = parser.parse_args()

    if not args.codabench:
        # DO NOT CHANGE THESE PATHS UNLESS YOU CHANGE THE FOLDER NAMES IN THE BUNDLE
        input_dir = os.path.join(root_dir_name, "input_data")
        output_dir = os.path.join(root_dir_name, "sample_result_submission")
        program_dir = os.path.join(root_dir_name, "ingestion_program")
        submission_dir = os.path.join(root_dir_name, "sample_code_submission")
    else:
        # DO NOT CHANGE THESE PATHS. THESE ARE USED ON THE CODABENCH PLATFORM
        input_dir = "/app/input_data"
        output_dir = "/app/output"
        program_dir = "/app/program"
        submission_dir = "/app/ingested_program"

    sys.path.append(input_dir)
    sys.path.append(output_dir)
    sys.path.append(program_dir)
    sys.path.append(submission_dir)

    # Import ingestion class
    from ingestion import Ingestion
    # Import model from submission dir
    from model import Model

    # Initialize Ingestions
    ingestion = Ingestion()

    # Start timer
    ingestion.start_timer()

    # Load train and test data
    ingestion.load_train_and_test_data(input_dir)

    # initialize submission
    ingestion.init_submission(Model)

    # fit submission
    ingestion.fit_submission()

    # predict submission
    ingestion.predict_submission()

    # save result
    ingestion.save_predictions(output_dir)

    # Stop timer
    ingestion.stop_timer()

    # Show duration
    print("\n------------------------------------")
    print(f"[✔] Total duration: {ingestion.get_duration()}")
    print("------------------------------------")

    print("\n----------------------------------------------")
    print("[✔] Ingestion Program executed successfully!")
    print("----------------------------------------------\n\n")
