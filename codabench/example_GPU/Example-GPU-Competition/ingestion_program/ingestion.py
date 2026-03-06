# ------------------------------------------
# Imports
# ------------------------------------------
import os
import json
import torch


class Ingestion:

    def check_gpu_availability(self):

        if torch.cuda.is_available():
            self.gpu_detected = True
            print("GPU is available!")
            print("Device name:", torch.cuda.get_device_name(0))
            print("Device count:", torch.cuda.device_count())
        else:
            self.gpu_detected = False
            print("GPU is not available.")

    def save_gpu_status(self, output_dir=None):
        json_to_save = os.path.join(output_dir, "gpu_status.json")
        with open(json_to_save, "w") as f:
            f.write(json.dumps({"gpu_detected": self.gpu_detected}, indent=4))
