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
    description="Run ingestion for the BYO-backend LLM Inference competition."
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

    from ingestion import Ingestion

    args = parser.parse_args()

    if not args.codabench:
        submission_dir = os.path.join(root_dir_name, "sample_code_submission")
        input_dir = os.path.join(root_dir_name, "input_data")
        output_dir = os.path.join(root_dir_name, "sample_result_submission")
    else:
        submission_dir = "/app/ingested_program"
        input_dir = "/app/input_data"
        output_dir = "/app/output"

    ingestion = Ingestion()
    ingestion.install_requirements(submission_dir)
    ingestion.load_submission(submission_dir)
    ingestion.load_prompts(input_dir)
    ingestion.run_inference()
    ingestion.save_predictions(output_dir)

    print("\n----------------------------------------------")
    print("[✔] Ingestion Program executed successfully!")
    print("----------------------------------------------\n\n")
