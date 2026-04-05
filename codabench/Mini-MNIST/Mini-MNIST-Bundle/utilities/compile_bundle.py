"""
Utility script to compile the Codabench competition bundle.

This script packages the necessary files and directories within the 
Competition_Bundle into a zip file that can be directly uploaded to Codabench.
It specifically structures the zip file and excludes unnecessary files like
development utilities, cache folders, and hidden system files.
"""

import os
import zipfile


def zip_competition_bundle() -> None:
    """
    Creates a zip archive "Mini-MNIST-Bundle.zip" containing the competition bundle.

    The archive is saved in the directory above the Competition_Bundle folder.
    It intentionally excludes:
    - The 'utilities' directory itself
    - System or cache files like .DS_Store or __pycache__
    """
    # Define paths: The script is in utilities/, so the bundle root is one level up
    utilities_dir = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(utilities_dir, '..'))

    # Define the output zip file name and location
    bundle_name = 'Mini-MNIST-Bundle.zip'
    bundle_path = os.path.join(folder_path, bundle_name)

    # Configuration for inclusion and exclusion
    exclude_files = set()  # Files to strictly avoid globally
    include_files = {'logo.png', 'competition.yaml'}  # Specific files in the root
    exclude_folders = {'utilities'}  # Folders to skip
    exclude_patterns = {'.DS_Store', '__pycache__'}  # Glob patterns to skip

    print(f"[*] Packaging competition bundle from: {folder_path}")
    print(f"[*] Target archive: {bundle_path}")

    # Create the zip file
    with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            rel_path = os.path.relpath(root, folder_path)

            # Handle the root directory of the bundle
            if rel_path == '.':
                for file in files:
                    if file in include_files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zipf.write(file_path, arcname=arcname)

            # Handle the subdirectories of the bundle
            elif all(exclude not in rel_path for exclude in exclude_folders):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Check if file has an excluded pattern or is specifically excluded
                    has_excluded_pattern = any(pattern in file for pattern in exclude_patterns)

                    if file not in exclude_files and not has_excluded_pattern:
                        arcname = os.path.relpath(file_path, folder_path)
                        zipf.write(file_path, arcname=arcname)

    print("[✔] Bundle compiled successfully.")


if __name__ == "__main__":
    zip_competition_bundle()
