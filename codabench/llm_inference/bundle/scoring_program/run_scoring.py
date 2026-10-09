# ------------------------------------------
# Imports
# ------------------------------------------
import os
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
    description="Run the scoring program for the LLM Inference competition."
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

    from score import Scoring

    args = parser.parse_args()

    if not args.codabench:
        # Local run: score the sample predictions against local reference data.
        prediction_dir = os.path.join(root_dir_name, "sample_result_submission")
        reference_dir = os.path.join(root_dir_name, "reference_data")
        output_dir = os.path.join(root_dir_name, "scoring_output")
    else:
        # Codabench paths: ingestion output is mounted at /app/input/res,
        # reference data at /app/input/ref.
        prediction_dir = "/app/input/res"
        reference_dir = "/app/input/ref"
        output_dir = "/app/output"

    scoring = Scoring()
    scoring.load_predictions(prediction_dir)
    scoring.load_reference(reference_dir)
    scoring.compute_scores()
    scoring.save_scores(output_dir)

    print("\n----------------------------------------------")
    print("[✔] Scoring Program executed successfully!")
    print("----------------------------------------------\n\n")
