import pandas as pd
import json
import os
import datetime
from dotenv import load_dotenv, find_dotenv

# todo remove
load_dotenv(find_dotenv())

DATA_PATH = os.getenv("TRAIN_DATA_PATH", "/opt/train_data/patients.json")
RESULTS_PATH = "/opt/pht_results/average_age.json"


def age_from_dob(dob):
    today = datetime.date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def parse_fhir_results():
    with open(DATA_PATH, "r") as input_file:
        fhir_response_dict = json.load(input_file)

    entries = fhir_response_dict.get("entry")

    birthdates = []
    # only extract the birthdate from the patient resources
    if entries:
        for entry in entries:
            birthdates.append(entry.get("resource").get("birthDate"))
    patients_df = pd.DataFrame()
    patients_df["birthdate"] = birthdates
    patients_df["birthdate"] = pd.to_datetime(patients_df["birthdate"])

    return patients_df


def calculate_local_average():
    results = parse_fhir_results()
    ages = results["birthdate"].apply(age_from_dob)
    local_average = ages.mean()
    return local_average


def load_previous_data():
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH, "r") as f:
            average_age_dict = json.load(f)

        return average_age_dict

    else:
        return None


def calculate_average_age():
    local_average = calculate_local_average()
    prev_results = load_previous_data()
    # previous results exist load them otherwise create a new dictionary containing the results
    if prev_results:
        prev_average = prev_results["average_age"]
        new_average = (prev_average + local_average) / 2 if prev_average else local_average
        prev_average["average_age"] = new_average
    else:
        new_average = local_average
        prev_results = {"average_age": new_average}

    # store the updated results
    with open(RESULTS_PATH, "w") as f:
        json.dump(prev_results, fp=f, indent=2)


if __name__ == '__main__':
    calculate_average_age()
