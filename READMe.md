# Python and Django container example - countdown to Christmas

This repository includes a Python and Django based container which outputs a countdown to Christmas to a URL.

## Container image build

To build an image based, run the following from the top level directory (the one with the Dockerfile in it):

~~~
podman build -t christmas_counter .
~~~

## Container deployment and testing

Then, deploy a container from that image:

~~~
podman run -p 8000:8000 localhost/christmas_counter
~~~

This will generate a countdown loop which updates every second to http://<IP or FQDN>:8000/days_until_christmas/.

To test that it is working, you request a response from that URL in a for loop which includes a 1 second sleep:

~~~
while true; do curl http://192.168.122.154:8000/days_until_christmas/; sleep 1; done
~~~

The output will loop something like the following:

~~~
There are 243 days, 11 hours, 40 minutes and 43 seconds until Christmas!
~~~
