# Demo CORD trains in R
This repository contains the minimal example in R to plot the age distribution on synthetic CORD data.

If you want to submit the code using our demo live page, we suggest cloning this repository first.
You can either execute the train locally for development or within the UI.

## UI execution
Please submit the demo train file with the corresponding query. Please use for all R Codes, the default master image.

Demo train 1 does not need a fhir query specified. Train 2 and 3 have the corresponding query provided.


## Execution with a dockerfile
If you want to execute the train as a docker image, please build your train testing the code:

If you want to run demo-train-1, 2 or 3 locally, just change filename in the dockerfile (both: copy and run command). Change before in the corresponding
entrypoint file the results_path (train_data dir if local execution)
Afterwards you can create and execute the train locally using this command:

````shell
docker build -f Dockerfile_r . -t harbor-pht.tada5hi.net/cord_demo:latest
docker run -v PATH_TO_REPO/R:/opt/train_data/:rw harbor-pht.tada5hi.net/cord_demo:latest
````
PATH_TO_REPO is the path to the current repository.
The corresponding input data for demo train 1, 2 and 3 are provided.
The local execution with the R demo trains will throw currently an error by saving the results.