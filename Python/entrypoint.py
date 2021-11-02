import os
import asyncio
import json
import pandas as pd
import pathlib
import pickle
from dotenv import load_dotenv, find_dotenv
from train_lib.fhir import PHTFhirClient


DATA_PATH = os.getenv("TRAIN_DATA_PATH")
DOCKER_IDE = True

if DOCKER_IDE:
    # local testing with docker as interpreter in IDE
    MODEL_PATH = 'model.pkl'
    RESULT_PATH = 'results.pkl'
    QUERY_FILE = "cord_query.json"
    FHIR_PATH = "cord_results.json"
else:
    # for trains submitted via UI or build with dockerfile - docker_ide = False
    QUERY_FILE = "/opt/pht_train/cord_query.json"
    FHIR_PATH = "/opt/train_data/cord_query_results.json"
    MODEL_PATH = '/opt/pht_results/model.pkl'
    RESULT_PATH = '/opt/pht_results/results.pkl'


def main():
    """
    Main analysis function of the train - the CORD minimal demo, requires only result files and no models
    :return:
    """
    # parse the FHIR response and load previous results (if available)
    pat_df = parse_fhir_response()
    try:
        results = load_if_exists(RESULT_PATH)
    except FileNotFoundError:
        print("No file available")
    if results is None:
        results = {'analysis': {}, 'discovery': {}}
    print("Previous results: {}".format(results))

    # Write analysis code here
    # demo function to count occurence of variables
    occ = occurence_data(pat_df, 'gender')

    results['analysis']['analysis_exec_' + str(len(results['analysis']) + 1)] = occ

    print("Updated results: {}".format(results))

    save_results(results, RESULT_PATH)


def load_if_exists(model_path: str):
    """
    Load previous computed results, if available
    :param model_path: Path of models or results to load
    :return: model
    """
    p = pathlib.Path(model_path)
    if pathlib.Path.is_file(p):
        print("Loading previous results")
        with open(p, "rb") as model_file:
            model = pickle.load(model_file)
        return model
    else:
        return None


def save_results(results, result_path):
    dirPath = '/opt/pht_results'
    try:
        # Create target Directory
        os.mkdir(dirPath)
        print("Directory ", dirPath,  " Created (usually done by TB)")
    except FileExistsError:
        print("Directory ", dirPath,  " already exists (done by TB)")
    p = pathlib.Path(result_path)
    with open(p, 'wb') as results_file:
        return pickle.dump(results, results_file)


def parse_fhir_response() -> pd.DataFrame:
    with open(FHIR_PATH, "r") as f:
        results = json.load(f)
    parsed_resources = []
    for patient in results:
        resource = patient["resource"]
        parsed_resources.append(parse_resource(resource))

    df = pd.DataFrame(parsed_resources)
    return df


def parse_resource(resource):
    """
    Parse a FHIR resource returned from a FHIR server in a desired format

    :param resource:
    :return:
    """
    # TODO specify required resources here
    sequence_dict = {
        "givenName": resource['name'][0]['given'],
        "familyName": resource['name'][0]['family'],
        "birthDate": resource["birthDate"],
        "gender": resource["gender"]
    }
    return sequence_dict


def occurence_data(pat_df, column):
    """
    Return value counts of given dataframe columns
    :param pat_df: Dataframe
    :param column: Column included in Dataframe
    :return: Series of value occurences
    """

    return pat_df[column].value_counts()


def query():
    print("FHIR Client PHT Credentials")
    print(os.getenv("FHIR_SERVER_URL"))
    print(os.getenv("FHIR_TOKEN"))
    print(os.getenv("FHIR_USER"))
    print(os.getenv("FHIR_PW"))
    client = PHTFhirClient(server_url=os.getenv("FHIR_SERVER_URL"), token=os.getenv("FHIR_TOKEN"))
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(client.execute_query(QUERY_FILE))
    try:
        with open(FHIR_PATH, "w") as f:
            json.dump(result, f)
        print("FHIR data stored as json")
    except:
        print("Data not stored")


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    print(os.curdir)
    #query()  # executed by stations - just for testing purpose
    main()
