# ------------------------------------------
# Imports
# ------------------------------------------
import argparse
import os


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

    from score import Scoring

    args = parser.parse_args()

    if not args.codabench:
        prediction_dir = os.path.join(root_dir_name, "sample_result_submission")
        output_dir = os.path.join(root_dir_name, "scoring_output")
    else:
        prediction_dir = "/app/input/res"
        output_dir = "/app/output"

    scoring = Scoring()
    scoring.load_ingestion_output(prediction_dir)
    scoring.save_leaderboard_result(output_dir)

    print("\n----------------------------------------------")
    print("[✔] Scoring Program executed successfully!")
    print("----------------------------------------------\n\n")
