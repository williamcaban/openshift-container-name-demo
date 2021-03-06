[![Docker Repository on Quay](https://quay.io/repository/redhat/wcabanba/status "Docker Repository on Quay")](https://quay.io/repository/redhat/wcabanba)

# Simple Demo Application Used to Showcase OpenShift Concepts

This repository provides a sample Python web application implemented using the Flask web framework. It is intended to be used to demonstrate deployment of Python web applications to OpenShift 3.x

To test this apps you will need an OpenShift or OKD environment.

# Using the application

The application understand the following environment variables
- APP_VERSION
- APP_MESSAGE

The values are displayed as the application version value and a text message.

Using the basic funcitonalities of the demo app:

| ROUTE PATH 	|                                     FUNCTIONALITY                                    	|                                USE CASES                                	|
|:----------:	|:------------------------------------------------------------------------------------:	|:-----------------------------------------------------------------------:	|
|   /           | Display a simple web interface with the name of the Pod, ``APP_VERSION`` and ``APP_MESSAGE`` information. | This can be used to demo from a browser |
|   /hello   	| Return a single liner text version of the Pod name and ``APP_VERSION``.                  	| This can be used to demo from a ``curl`` command or similar             	|
| /_health   	| Return a JSON formatted status of the app, the container name and container version. 	| This can be used for health checks or pod readiness checks              	|
| /_net      	| Return a JSON formatted list of the network interfaces seen by the pod.              	| This can be used to demo Multus/OpenShift Multinetwork functionalities.	|
| /_net/\<ifname>      	| Return a JSON formatted list of IPv4 addresses of *ifname* Pod interface.              	| This can be used to demo Multus/OpenShift Multinetwork functionalities.	|

## Implementation Notes

This sample Python application relies on the support provided by the default S2I builder for deploying a WSGI application using the ``gunicorn`` WSGI server. The requirements which need to be satisfied for this to work are:

* The WSGI application code file needs to be named ``wsgi.py``.
* The WSGI application entry point within the code file needs to be named ``application``.
* The ``gunicorn`` package must be listed in the ``requirements.txt`` file for ``pip``.

In addition, the ``.s2i/environment`` file has been created to allow environment variables to be set to override the behaviour of the default S2I builder for Python.

The environment variable ``APP_CONFIG`` has been set to declare the name of the config file for ``gunicorn`` .


## Using a Minishift Environment

If using Red Hat CDK you can start OpenShift (Minishift) with the following command:
```
$ minishift start
oc login -u developer
```

Some additional Minishft commands if considering the use of privileged containers.

**NOTE**: THESE ARE NOT REQUIRED FOR THIS DEMO BUT GOOD TO KEEP IN MIND
```
oc adm policy add-scc-to-group anyuid system:authenticated
$ minishift addons enable anyuid
$ minishift addons enable admin-user
$ minishift start --ocp-tag v3.11.16
```

To explore additional Minishift addons
```
$ minishift addons list
```

Additional details about Minishift can be found at
- https://docs.okd.io/latest/minishift/using/basic-usage.html

# Demo and Lab Steps

To deploy this sample Python web application from the OpenShift web console, you should select ``python:2.7``, ``python:3.3``, ``python:3.4`` or ``python:latest``, when using _Add to project_. Use of ``python:latest`` is the same as having selected the most up to date Python version available, which at this time is ``python:3.4``.

The HTTPS URL of this code repository which should be supplied to the _Git Repository URL_ field when using _Add to project_ is:

* https://github.com/williamcaban/openshift-container-name-demo.git

If using the ``oc`` command line tool instead of the OpenShift web console, to deploy this sample Python web application, you can run:

```
oc new-project demo-app --display-name='My Demo App'
```

To deploy it from git run the following command

* NOTE: Since this demo repo contains a ``Dockerfile``, by default, OpenShift will try to use the ``docker build strategy``. By specifying the *strategy* flag we force OpenShift to use ``s2i build strategy``.

```
oc new-app https://github.com/williamcaban/openshift-container-name-demo.git --name=myapp1 --strategy=source
```


To create a URL route
```
oc expose svc/myapp1 --name=myroute

oc get route
```

To get the text output displaying the name use the /hello path. Run the following command in another terminal:
```
$ while sleep 1; do curl http://$(oc get route myroute --template='{{ .spec.host }}'/hello); echo; done
```

Scale to 3 replicas and validate pods have been created
```
oc get pods -l app=myapp1

oc scale --replicas=3 dc/myapp1

oc get pods -l app=myapp1
```

Destroy one of the Pods and watch the system remediate.
```
oc get pods -l app=myapp1

oc delete po/<name-of-pod>

oc get pods -l app=myapp1
```

Deploy another version of the app using ``Docker`` strategy
```
oc new-app https://github.com/williamcaban/openshift-container-name-demo.git --name=myapp2 --strategy=docker APP_VERSION=v2
```

To deploy from local source code using ``Docker`` strategy
```
oc new-app </path/to/code> --name=<app-name> --strategy=docker APP_VERSION=v3

oc new-app ./ --name=myapp3 --strategy=docker APP_VERSION=v3
```

Split traffic among the different versions and monitor the load balancing displayed in the terminal running the ``curl`` command
```
oc get route myroute

# Update for 50-25-25 distribution

oc set route-backends myroute myapp1=50% myapp2=25% myapp3=25%

oc get route

# Update for equal traffic distribution

oc set route-backends myroute --equal

oc get route

# Remove ~10% of the traffic from version 3 and watch
# the resulting balancing distribution. The difference
# between requested vs actual is due to weight distribution.

oc set route-backends myroute --adjust myapp3=-10%

oc get route

```

More information about advanced deployment strategies visit: https://docs.openshift.com/container-platform/3.11/dev_guide/deployments/advanced_deployment_strategies.html


## Simulating webhooks rebuild events

Display the BuildConfig to identify the "Webhook Generic" URL
```
oc describe bc/myapp1
```

The <secret> in the URL will be the output of this command
```
oc get bc -o json | jq '.items[0] .spec.triggers[].generic.secret' | grep -v null
```

You can also find the correct URL over the console at the configuration tab of the build config:

https://<your-okd-path>/console/project/demo-app/browse/builds/myapp1?tab=configuration

Simulating a generic Webhook event:
```
curl -X POST -k https://<your-okd-path>/apis/build.openshift.io/v1/namespaces/demo-app/buildconfigs/myapp1/webhooks/<secret>/generic
```

## Notes about Build Strategies

In the previous example, when using the *``--strategy=source``* since no language type was specified, OpenShift will determine the language by inspecting the code repository. Because the code repository contains a ``requirements.txt``, it will subsequently be interpreted as including a Python application. When such automatic detection is used, ``python:latest`` will be used.

If needing to select a specific Python version, lets say python 2.7, when using ``oc new-app``, you should instead use the syntax:

```
oc new-app python:2.7~https://github.com/williamcaban/openshift-container-name-demo.git --name=myapp1
```
