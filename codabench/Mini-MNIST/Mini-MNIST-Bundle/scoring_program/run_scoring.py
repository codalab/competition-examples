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
    description="This is script to generate data for the HEP competition."
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
    print("Scoring Program started!")
    print("----------------------------------------------\n\n")

    args = parser.parse_args()

    if not args.codabench:
        # DO NOT CHANGE THESE PATHS UNLESS YOU CHANGE THE FOLDER NAMES IN THE BUNDLE
        prediction_dir = os.path.join(root_dir_name, "sample_result_submission")
        reference_dir = os.path.join(root_dir_name, "reference_data")
        output_dir = os.path.join(root_dir_name, "scoring_output")
    else:
        # DO NOT CHANGE THESE PATHS. THESE ARE USED ON THE CODABENCH PLATFORM
        prediction_dir = "/app/input/res"
        reference_dir = "/app/input/ref"
        output_dir = "/app/output"

    sys.path.append(prediction_dir)
    sys.path.append(reference_dir)
    sys.path.append(output_dir)

    # Import scoring class
    from score import Scoring

    # Initialize Scoring program
    scoring = Scoring()

    # Start timer
    scoring.start_timer()

    # Load reference data
    scoring.load_reference_data(reference_dir)

    # Load ingestion result
    scoring.load_ingestion_result(prediction_dir)

    # Compute Scores
    scoring.compute_scores()

    # Write scores
    scoring.write_scores(output_dir)

    # Stop timer
    scoring.stop_timer()

    # Show duration
    print("\n---------------------------------")
    print(f"[✔] Total duration: {scoring.get_duration()}")
    print("---------------------------------")

    print("\n----------------------------------------------")
    print("[✔] Scoring Program executed successfully!")
    print("----------------------------------------------\n\n")
