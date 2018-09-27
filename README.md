# Flask Sample Application

This repository provides a sample Python web application implemented using the Flask web framework and hosted using ``gunicorn``. It is intended to be used to demonstrate deployment of Python web applications to OpenShift 3.

# Environment

To test this apps you will need an OpenShift or OKD environment.

If using Red Hat CDK you can start OpenShift (Minishift) 3.10.14 with the following command:
```
minishift start --ocp-tag 3.10.14
```

## Implementation Notes

This sample Python application relies on the support provided by the default S2I builder for deploying a WSGI application using the ``gunicorn`` WSGI server. The requirements which need to be satisfied for this to work are:

* The WSGI application code file needs to be named ``wsgi.py``.
* The WSGI application entry point within the code file needs to be named ``application``.
* The ``gunicorn`` package must be listed in the ``requirements.txt`` file for ``pip``.

In addition, the ``.s2i/environment`` file has been created to allow environment variables to be set to override the behaviour of the default S2I builder for Python.

* The environment variable ``APP_CONFIG`` has been set to declare the name of the config file for ``gunicorn``.

## Deployment Steps

To deploy this sample Python web application from the OpenShift web console, you should select ``python:2.7``, ``python:3.3``, ``python:3.4`` or ``python:latest``, when using _Add to project_. Use of ``python:latest`` is the same as having selected the most up to date Python version available, which at this time is ``python:3.4``.

The HTTPS URL of this code repository which should be supplied to the _Git Repository URL_ field when using _Add to project_ is:

* https://github.com/OpenShiftDemos/os-sample-python.git

If using the ``oc`` command line tool instead of the OpenShift web console, to deploy this sample Python web application, you can run:

```
oc new-project demo-python
```

To run it from git
```
oc new-app https://github.com/williamcaban/openshift-container-name-demo.git
```

To create a URL route
```
oc expose svc/openshift-container-name-demo
```

To get the text output displaying the name use the /hello path
```
while sleep 1; do curl http://$(oc get route openshift-container-name-demo --template='{{ .spec.host }}'/hello); echo; done
```

Scale to 3 replicas and validate pods have been created
```
oc scale --replicas=3 dc/openshift-container-name-demo

oc get pods
```

Destroy one of the Pods and watch the system remediate.
```
oc delete po/<name-of-pod>
```

## Simulating webhooks rebuild events

Display the BuildConfig to identify the "Webhook Generic" URL
```
oc describe bc/openshift-container-name-demo
```

The <secret> in the URL will be the output of this command
```
oc get bc -o json | jq '.items[0] .spec.triggers[].generic.secret' | grep -v null
```

You can also find the correct URL over the console at the configuration tab of the build config:

https://<your-okd-path>/console/project/demo-python/browse/builds/openshift-container-name-demo?tab=configuration

Simulating a generic Webhook event:
```
curl -X POST -k https://<your-okd-path>/apis/build.openshift.io/v1/namespaces/demo-python/buildconfigs/openshift-container-name-demo/webhooks/<secret>/generic
```

## Notes

In the previous example, because no language type was specified, OpenShift will determine the language by inspecting the code repository. Because the code repository contains a ``requirements.txt``, it will subsequently be interpreted as including a Python application. When such automatic detection is used, ``python:latest`` will be used.

If needing to select a specific Python version, lets say python 2.7, when using ``oc new-app``, you should instead use the syntax:

```
oc new-app python:2.7~https://github.com/williamcaban/openshift-container-name-demo.git
```
