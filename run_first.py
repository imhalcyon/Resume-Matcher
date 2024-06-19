"""run_first."""

import json
import logging
import os

from scripts import JobDescriptionProcessor, ResumeProcessor
from scripts.utils import get_filenames_from_dir, init_logging_config

init_logging_config()

PROCESSED_RESUMES_PATH = "Data/Processed/Resumes"
PROCESSED_JOB_DESCRIPTIONS_PATH = "Data/Processed/JobDescription"


# Function to check if directory exists otherwise create it
def check_dir(directory):
    """:param directory: path to check :return: null."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_json(filename):
    """:param filename: path to json file :return: data from json file."""
    logging.info(f"Reading from {filename}")
    with open(filename) as f:
        data = json.load(f)
    return data


def remove_old_files(files_path):
    """:param files_path: path to folder containing files :return: null."""
    logging.info("Deleting old files from " + files_path)

    for filename in os.listdir(files_path):
        try:
            file_path = os.path.join(files_path, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logging.error(f"Error deleting {file_path}:\n{e}")

    logging.info("Deleted old files from " + files_path)


logging.info("Started to read from Data/Resumes")
try:
    # Check if there are resumes present or not.
    check_dir(PROCESSED_RESUMES_PATH)
    check_dir(PROCESSED_JOB_DESCRIPTIONS_PATH)

    # If present then parse it.
    remove_old_files(PROCESSED_RESUMES_PATH)

    file_names = get_filenames_from_dir("Data/Resumes")
    logging.info("Reading from Data/Resumes is now complete.")
except FileNotFoundError:
    # Exit the program if there are no resumes.
    logging.error("There are no resumes present in the specified folder.")
    logging.error("Exiting from the program.")
    logging.error("Add resumes in the Data/Resumes folder and try again.")
    exit(1)
except Exception as e:
    # Handle any other unexpected exceptions
    logging.error(f"An unexpected error occurred: {e}")
    logging.error("Exiting from the program.")
    exit(1)

# Now after getting the file_names parse the resumes into a JSON Format.
logging.info("Started parsing the resumes.")
for file in file_names:
    processor = ResumeProcessor(file)
    success = processor.process()
logging.info("Parsing of the resumes is now complete.")

logging.info("Started to read from Data/JobDescription")
try:
    # Check if there are resumes present or not.
    # If present then parse it.
    remove_old_files(PROCESSED_JOB_DESCRIPTIONS_PATH)

    file_names = get_filenames_from_dir("Data/JobDescription")
    logging.info("Reading from Data/JobDescription is now complete.")
except FileNotFoundError:
    # Exit the program if there are no job descriptions.
    logging.error("No job-description present in the specified folder.")
    logging.error("Exiting from the program.")
    logging.error("Add JD in Data/JobDescription folder and try again.")
    exit(1)
except Exception as e:
    # Handle any other unexpected exceptions
    logging.error(f"An unexpected error occurred: {e}")
    logging.error("Exiting from the program.")
    exit(1)

# Now after getting the file_names parse the resumes into a JSON Format.
logging.info("Started parsing the Job Descriptions.")
for file in file_names:
    processor = JobDescriptionProcessor(file)
    success = processor.process()
logging.info("Parsing of the Job Descriptions is now complete.")
logging.info("Success now run `streamlit run streamlit_second.py`")
