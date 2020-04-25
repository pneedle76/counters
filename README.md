# A day in the life of a container

## Overview

This repository includes a 'day in the life of a container' demo/tutorial to help people (including myself!) really understand the end-to-end container lifecycle and how to readily manage each step in the process. This includes:

- Creating an example Python / Django program suitable for a container.
- Building that program into a container image based on the RHEL 8 Universal Base Image (ubi8/ubi), using podman on a RHEL 8 console node.
- Running a container based on that image, again using podman on RHEL 8.
- Testing the functionality of the deployed container and examining it for debugging purposes.
- Tagging the image for Quay, uploading it to [quay.io](https://quay.io) and publishing it.
- Importing the image from `quay.io` to an OpenShift Container Platform 4 internal registry.
- Deploying an application on OpenShift Container Platform using the imported image.
- Testing the program's continuation while scaling OpenShift Container Platform application pods, deleting the original one and then watching the Django server fail over to another replica.

The container image build pulls [Red Hat Universal Base Image 8](https://developers.redhat.com/blog/2019/10/09/what-is-red-hat-universal-base-image/) (ubi8/ubi) from [registry.redhat.io](https://registry.redhat.io) and then includes the dependencies required to run the Python / Django program as additional layers.

The Python / Django program itself outputs days, hours, minutes and seconds until Christmas, overwriting the output every second. This makes for a nice demo because you can use `curl` in a `for` loop to confirm that there are no service interruptions to the application as you remove replica pods in the OpenShift project.

Full steps detailing that container lifecycle are outlined in the following two documents:

- [Building the Christmas countdown Python / Django container image from scratch](python_django_tutorial.md).

- [Deploying the Christmas countdown image in an OpenShift environment](openshift_tutorial.md).

If you just want to build the image using podman on a RHEL 8 node and test it, follow the steps below.

## Build and test the image on RHEL 8

One a RHEL 8 console node, build an image based on the contents of this repository. Run the following from the top level directory of your local clone (the directory with the Dockerfile in it):

~~~
podman build -t christmas_counter .
~~~

Then, deploy a container from that image:

~~~
podman run -p 8000:8000 localhost/christmas_counter
~~~

This will generate a countdown loop which updates every second to *http://\<IP or FQDN\>:8000/days_until_christmas/*. To test that it is working, request a response from that URL using `curl` in a `for` loop that includes a one second sleep:

~~~
while true; do curl http://<IP or FQDN>:8000/days_until_christmas/; sleep 1; done
~~~

The output will be something like the following and it will be overwritten every second:

~~~
There are 243 days, 11 hours, 40 minutes and 43 seconds until Christmas!
~~~

## Pull an existing image based on the contents of this repository:

An image built from this repository using the `podman build` command outlined above is available at **quay.io/pneedle/christmas_counter-python-django:v1.0**.
