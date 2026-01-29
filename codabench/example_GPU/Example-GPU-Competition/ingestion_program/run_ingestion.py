# ------------------------------------------
# Imports
# ------------------------------------------
import sys
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

    from ingestion import Ingestion

    args = parser.parse_args()

    if not args.codabench:
        output_dir = os.path.join(root_dir_name, "sample_result_submission")
        program_dir = os.path.join(root_dir_name, "ingestion_program")
    else:
        output_dir = "/app/output"
        program_dir = "/app/program"

    sys.path.append(program_dir)

    ingestion = Ingestion()
    ingestion.check_gpu_availability()
    ingestion.save_gpu_status(output_dir)

    print("\n----------------------------------------------")
    print("[✔] Ingestion Program executed successfully!")
    print("----------------------------------------------\n\n")
