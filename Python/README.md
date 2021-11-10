# Demo CORD trains
This repository contains the minimal requirements of an entrypoint.py to execute FHIR queries
and write demo analysis code in Python.

If you want to submit the code using our demo live page, we suggest cloning this repository first.
You can either execute the train locally for development or within the UI.

## FHIR-queries
Synthethic data was uploaded to IBM, Blaze and HAPI FHIR Servers. These types are currently supported by our Train-Library.
The query is can search for multiple conditions. Therefore just adapt the ``query.json`` file.

If you want e.g. query only female subjects, a born after 1960 use this query file instead:

````json
{
  "query": {
    "resource": "Patient",
    "parameters": [
      {
        "variable": "birthdate",
        "condition": "gt1960"
      },
      {
        "variable": "gender",
        "condition": "female"
      }
    ]
  },
  "data": {
    "output_format": "json",
    "filename": "query_results.json"
  }
}
````
### Enviorment variables
To execute the FHIR queries certain parameters need to be specified. We currently support IBM, Blaze and Hapi FHIR Servers.
Our FHIR servers only contain synthethic data. Access to our resources can be requested by us (mailto:marius.herr@uni-tuebingen.de).
Copy the ``env_template`` file and adapt it:
```shell
cp .env_template .env
nano .env
```
## Analysis
The algorithm ``entrypoint.py`` requests over the train library the FHIR data at each station and performs the analysis
specified in this file. The minimal example is giving the value counts of a certain column. If you want to query and analze
different resources, adapt the `parse_resources()` function.

### Execution with a dockerfile
If you want to execute the train as a docker container, please build your train testing the code:

If you want to run demo-train-1 or 2 locally, just change filename in the dockerfile. Change before in the corresponding
entrypoint file the results_path (train_data dir if local execution)
Afterwards you can create and execute the train locally using this command:

````shell
docker build -f Dockerfile . -t harbor-pht.tada5hi.net/cord_demo:latest
docker run -v PATH_TO_REPO/Python:/opt/train_data/:rw harbor-pht.tada5hi.net/cord_demo:latest
````
PATH_TO_REPO is the path to the current repository.