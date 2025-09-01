"""
Script to download and extract the Vosk English model
"""

import os
import requests
import zipfile
import argparse
from tqdm import tqdm
import sys

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
MODEL_PATH = "models/vosk-model-en-us-0.22"


def download_file(url, destination):
    """Download a file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(destination, 'wb') as file, tqdm(
            desc=destination,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def download_model():
    """Download and extract the Vosk model"""
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Check if model already exists
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at {MODEL_PATH}")
        return True

    # Download the model
    zip_path = "models/vosk-model-en-us-0.22.zip"
    print(f"Downloading Vosk model from {MODEL_URL}")

    try:
        download_file(MODEL_URL, zip_path)

        # Extract the model
        print("Extracting model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("models")

        # Clean up zip file
        os.remove(zip_path)

        print(f"Model successfully downloaded to {MODEL_PATH}")
        return True

    except Exception as e:
        print(f"Error downloading model: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Vosk model")
    parser.add_argument("--url", help="Custom model URL", default=MODEL_URL)
    args = parser.parse_args()

    success = download_model()
    sys.exit(0 if success else 1)