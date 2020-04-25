# Deploying the Christmas countdown image in an OpenShift environment

This document provides steps to import the image `quay.io/pneedle/christmas_counter-python-django:v1.0` ([which was built from the a clone of this repository](python_django_tutorial.md)), into OpenShift Container Platform 4. The document then outlines how to deploy a new application in OpenShift Container Platform 4 based on that image and then scale the application to multiple replicas. Full details on testing the expected output is also included.

For the most part, I have left out the command prompt, except where I felt it was required for differentiation between a command and its output. Assume that commands are run from an external console which has access the `oc` command installed. For OpenShift Container Platform 4, `oc` is included in the `openshift-clients` RPM. 

Login to OpenShift using the `oc` command and then import the image from `quay.io` to the OpenShift internal registry:

~~~
oc login --server=https://<FQDN>:6443 -u <username> -p <password>
oc import-image quay.io/pneedle/christmas_counter-python-django:v1.0 --confirm
~~~

View the image in the internal registry:

~~~
# oc get images | grep -is 'christmas'
sha256:e37b359e3a6fcdbece98e0ba16244a26e40956126d9a90d683ec57617f74187b   quay.io/pneedle/christmas_counter-python-django@sha256:e37b359e3a6fcdbece98e0ba16244a26e40956126d9a90d683ec57617f74187b

# oc describe image sha256:e37b359e3a6fcdbece98e0ba16244a26e40956126d9a90d683ec57617f74187b
...
~~~

Create a new OpenShift project and a new application based on that image:

~~~
oc new-project christmas-counter
oc new-app quay.io/pneedle/christmas_counter-python-django:v1.0 --name christmas
~~~

Review the deployment log until it completes:

~~~
# oc logs dc/christmas
--> Scaling christmas-1 to 1
~~~

In another terminal window, run `oc get pods -o wide` continuously every second and observe the new application pod being created. Keep this command running while we create replicas and then delete the original application pod, so that we can continue to observe activity:

~~~
# watch -n1 -d 'oc get pods -o wide'
Every 1.0s: oc get pods -o wide                                                                         rhel81: Sat Apr 25 09:35:20 2020

NAME                 READY   STATUS	 RESTARTS   AGE   IP            NODE                  NOMINATED NODE   READINESS GATES
christmas-1-deploy   0/1     Completed   0          86s   10.128.2.60   master-3.ocp4.local   <none>           <none>
christmas-1-q6gnz    1/1     Running     0          78s   10.129.0.35   worker-2.ocp4.local   <none>           <none>
~~~

Add a route to the service so that it can be accessed externally to the cluster:

~~~
# oc expose svc/christmas
route.route.openshift.io/christmas exposed

# oc get svc
NAME        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
christmas   ClusterIP   172.30.209.50   <none>        8000/TCP   3m36s

# oc get route
NAME        HOST/PORT                                     PATH   SERVICES    PORT       TERMINATION   WILDCARD
christmas   christmas-christmas-counter.apps.ocp4.local          christmas   8000-tcp                 None
~~~

Test the URL in a browser:

~~~
$ firefox http://christmas-christmas-counter.apps.ocp4.local/days_until_christmas/ &
~~~

In another terminal window, test the URL from using `curl` in a `for` loop. Keep this running also, while we create replica pods and then delete the original pod, so that we can see if the Christmas countdown service continues unaffected:

~~~
$ while true; do curl http://christmas-christmas-counter.apps.ocp4.local/days_until_christmas/; sleep 1; done
There are 243 days, 10 hours, 17 minutes and 21 seconds until Christmas!
~~~

Scale replica pods so that we have five application pods in total:

~~~
# oc scale dc/christmas --replicas=5
deploymentconfig.apps.openshift.io/christmas scaled
~~~

Watch replica pods being created in the other window which still has the `watch` command running, until all five replicas are listed as `Running`:

~~~
# watch -n1 -d 'oc get pods -o wide'
Every 1.0s: oc get pods -o wide                                                                         rhel81: Sat Apr 25 09:51:03 2020

NAME                 READY   STATUS	 RESTARTS   AGE     IP            NODE                  NOMINATED NODE   READINESS GATES
christmas-1-deploy   0/1     Completed   0          17m     10.128.2.60   master-3.ocp4.local   <none>           <none>
christmas-1-ffvvw    1/1     Running     0          7m35s   10.130.0.26   worker-1.ocp4.local   <none>           <none>
christmas-1-q6gnz    1/1     Running     0          17m     10.129.0.35   worker-2.ocp4.local   <none>           <none>
christmas-1-r699j    1/1     Running     0          7m35s   10.131.0.56   master-2.ocp4.local   <none>           <none>
christmas-1-t9cc5    1/1     Running     0          7m35s   10.128.2.61   master-3.ocp4.local   <none>           <none>
christmas-1-w2jbg    1/1     Running     0          7m35s   10.128.0.54   master-1.ocp4.local   <none>           <none>
~~~

Delete the pod which was created before we scaled up, while reviewing whether the Christmas countdown `curl` loop continues seamlessly:

~~~
# oc delete pod christmas-1-q6gnz
pod "christmas-1-q6gnz" deleted
~~~

As the original pod terminates, observe the `oc get pods -o wide` and `curl` outputs looping in the other terminal windows. The Christmas countdown should continue to update every second uninterruptedly, as the Django server fails over to one of the replicas. We should also see another replica pod being spawned in place of the deleted one:

~~~
# watch -n1 -d 'oc get pods -o wide'
Every 1.0s: oc get pods -o wide                                                                         rhel81: Sat Apr 25 09:54:03 2020

NAME                 READY   STATUS	 RESTARTS   AGE    IP            NODE                  NOMINATED NODE   READINESS GATES
christmas-1-deploy   0/1     Completed   0          20m    10.128.2.60   master-3.ocp4.local   <none>           <none>
christmas-1-ffvvw    1/1     Running     0          10m    10.130.0.26   worker-1.ocp4.local   <none>           <none>
christmas-1-r699j    1/1     Running     0          10m    10.131.0.56   master-2.ocp4.local   <none>           <none>
christmas-1-t9cc5    1/1     Running     0          10m    10.128.2.61   master-3.ocp4.local   <none>           <none>
christmas-1-v2xts    1/1     Running     0          100s   10.129.0.36   worker-2.ocp4.local   <none>           <none>
christmas-1-w2jbg    1/1     Running     0          10m    10.128.0.54   master-1.ocp4.local   <none>           <none>
~~~
