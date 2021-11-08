# Demo CORD trains in R
This repository contains the minimal example in R to plot the age distribution on synthetic CORD data.

If you want to submit the code using our demo live page, we suggest cloning this repository first.
You can either execute the train locally for development or within the UI.

## UI execution
The R demo `script_fhir_import.R` counts and plots the age distribution
``altersverteilung.pdf`` if you submit the code via the UI.

Nothing more needs to be modified here.

## Local execution
### Build and execution as dockerfile
If you want to execute the train as a docker container, please build your train testing the code:
````shell
cd R
docker build -f Dockerfile_r . -t cord_demo_r:latest
docker run -v <path_to_project>/cord-pht-demo/R:/opt/pht_data:rw  cord_demo_r:latest 
````
If you run the trains locally, you need to provide the train with the input data in your defined format.


The R demo `script_fhir_import.R` counts and plots the age distribution
``altersverteilung.pdf`` if you submit the code via the UI.

### Next steps
You can customize and share your code within this repository.

### Missing requirements?
The master image is publicly available at [development harbor registry](https://harbor-pht.tada5hi.net/master/r/cord:latest) if you want to modify it,
please clone the [train-container-library](https://github.com/PHT-EU/train-container-library) repository, modify the `requirements_r_cord.txt` file
and build the image with ``docker build -f docker_files/Dockerfile_cord -t new_cord_image:latest .``.

This newly build image (`new_cord_image:latest`) needs to be specified as base image within the ``Dockerfile_r``.