import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

def download_image(url: str, filename: str) -> None:
    """
    Downloads an image from the specified URL and saves it to a file.

    Args:
        url (str): The URL of the image to download.
        filename (str): The name of the file to save the image to.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading image: {e}")
        return

    # Save the response content in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "wb") as f:
        f.write(response.content)
    logging.info(f"Image downloaded and saved to: {file_path}")

def main() -> None:
    """
    The main function that runs the script:
    """
    url = os.getenv("URL")
    filename = os.getenv("FILENAME")

    download_image(url, filename)

if __name__ == "__main__":
    main()