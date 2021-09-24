# Demo CORD trains in R
This repository contains the minimal example in R to execute plot the age distribution.


## Execution as dockerfile
If you want to execute the train as a docker container, please build your train testing the code:
````shell
cd R
docker build -f Dockerfile_r . -t cord_demo_r:latest
docker run -v <path_to_project>/cord-pht-demo/R:/opt/pht_data:rw  cord_demo_r:latest 
````

This minimal example mounts the provided A2-1.csv file to ``script.R`` and allows the train to store ``result.csv`` and
``altersverteilung.pdf`` within the R directory.

## Next steps
Add more analysis functionality and provide FHIR queries with our Train-Lib instead of fhircracker.

## Missing requirements?
The base image is publicly available at ``harbor-pht.tada5hi.net/master/r/cord:latest`` if you want to modify it,
please clone the [train-container-library](https://github.com/PHT-EU/train-container-library) repository, modify the `requirements_r_cord.txt` file
and build the image with ``docker build -f docker_files/Dockerfile_cord -t new_cord_image:latest .``.

This newly build image (`new_cord_image:latest`) needs to be specified as base image within the ``Dockerfile_r``.