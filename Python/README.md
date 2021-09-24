# Demo CORD trains
This repository contains the minimal requirements of an entrypoint.py to execute FHIR queries
and write demo analysis code in Python.


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
    "output_format": "raw",
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

### PyCharm IDE docker execution
You can simply specify the Interpreter in PyCharm based on the docker image. Therefore, add the interpreter with a public available
master image (e.g. ``harbor-pht.tada5hi.net/master/python/slim:latest``). If you run the train such, set the variable `DOCKER_IDE=True`.
Please specify as container settings `-v <local_path>/station-data:/opt/pht_results` to the run parameters.

### Execution as dockerfile
If you want to execute the train as a docker container, please build your train testing the code:
````shell
docker build -f Dockerfile . -t harbor-pht.tada5hi.net/cord_demo:latest
docker run --env-file ./.env  -v <path>/station-data:/opt/train_data/:rw harbor-pht.tada5hi.net/cord_demo:latest
````