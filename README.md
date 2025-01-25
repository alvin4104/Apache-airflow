# Apache-airflow
What is Airflow®?
Apache Airflow® is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. Airflow’s extensible Python framework enables you to build workflows connecting with virtually any technology. A web interface helps manage the state of your workflows. Airflow is deployable in many ways, varying from a single process on your laptop to a distributed setup to support even the biggest workflows.

Workflows as code
The main characteristic of Airflow workflows is that all workflows are defined in Python code. “Workflows as code” serves several purposes:

Dynamic: Airflow pipelines are configured as Python code, allowing for dynamic pipeline generation.

Extensible: The Airflow® framework contains operators to connect with numerous technologies. All Airflow components are extensible to easily adjust to your environment.

Flexible: Workflow parameterization is built-in leveraging the Jinja templating engine.

Take a look at the following snippet of code:

from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo", start_date=datetime(2022, 1, 1), schedule="0 0 * * *") as dag:
    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow():
        print("airflow")

    # Set dependencies between tasks
    hello >> airflow()
Here you see:

A DAG named “demo”, starting on Jan 1st 2022 and running once a day. A DAG is Airflow’s representation of a workflow.

Two tasks, a BashOperator running a Bash script and a Python function defined using the @task decorator

>> between the tasks defines a dependency and controls in which order the tasks will be executed

Airflow evaluates this script and executes the tasks at the set interval and in the defined order. The status of the “demo” DAG is visible in the web interface:
![image](https://github.com/user-attachments/assets/b1ea4af0-6865-4813-a0b0-520b3bdcd113)

Demo DAG in the Graph View, showing the status of one DAG run
This example demonstrates a simple Bash and Python script, but these tasks can run any arbitrary code. Think of running a Spark job, moving data between two buckets, or sending an email. The same structure can also be seen running over time:
![image](https://github.com/user-attachments/assets/6525bd65-9466-45f0-90b7-08063591a583)

Demo DAG in the Grid View, showing the status of all DAG runs
Each column represents one DAG run. These are two of the most used views in Airflow, but there are several other views which allow you to deep dive into the state of your workflows.

Why Airflow®?
Airflow® is a batch workflow orchestration platform. The Airflow framework contains operators to connect with many technologies and is easily extensible to connect with a new technology. If your workflows have a clear start and end, and run at regular intervals, they can be programmed as an Airflow DAG.

If you prefer coding over clicking, Airflow is the tool for you. Workflows are defined as Python code which means:

Workflows can be stored in version control so that you can roll back to previous versions

Workflows can be developed by multiple people simultaneously

Tests can be written to validate functionality

Components are extensible and you can build on a wide collection of existing components

Rich scheduling and execution semantics enable you to easily define complex pipelines, running at regular intervals. Backfilling allows you to (re-)run pipelines on historical data after making changes to your logic. And the ability to rerun partial pipelines after resolving an error helps maximize efficiency.

Airflow’s user interface provides:

In-depth views of two things:

Pipelines

Tasks

Overview of your pipelines over time

From the interface, you can inspect logs and manage tasks, for example retrying a task in case of failure.

The open-source nature of Airflow ensures you work on components developed, tested, and used by many other companies around the world. In the active community you can find plenty of helpful resources in the form of blog posts, articles, conferences, books, and more. You can connect with other peers via several channels such as Slack and mailing lists.

Airflow as a Platform is highly customizable. By utilizing Public Interface of Airflow you can extend and customize almost every aspect of Airflow.

Why not Airflow®?
Airflow® was built for finite batch workflows. While the CLI and REST API do allow triggering workflows, Airflow was not built for infinitely running event-based workflows. Airflow is not a streaming solution. However, a streaming system such as Apache Kafka is often seen working together with Apache Airflow. Kafka can be used for ingestion and processing in real-time, event data is written to a storage location, and Airflow periodically starts a workflow processing a batch of data.

If you prefer clicking over coding, Airflow is probably not the right solution. The web interface aims to make managing workflows as easy as possible and the Airflow framework is continuously improved to make the developer experience as smooth as possible. However, the philosophy of Airflow is to define workflows as code so coding will always be required.

Quick Start
This quick start guide will help you bootstrap an Airflow standalone instance on your local machine.

Note

Successful installation requires a Python 3 environment. Starting with Airflow 2.7.0, Airflow supports Python 3.8, 3.9, 3.10, 3.11 and 3.12.

Only pip installation is currently officially supported.

While there have been successes with using other tools like poetry or pip-tools, they do not share the same workflow as pip - especially when it comes to constraint vs. requirements management. Installing via Poetry or pip-tools is not currently supported.

There are known issues with bazel that might lead to circular dependencies when using it to install Airflow. Please switch to pip if you encounter such problems. Bazel community works on fixing the problem in this PR so it might be that newer versions of bazel will handle it.

If you wish to install Airflow using those tools you should use the constraint files and convert them to appropriate format and workflow that your tool requires.

The installation of Airflow is straightforward if you follow the instructions below. Airflow uses constraint files to enable reproducible installation, so using pip and constraint files is recommended.

Set Airflow Home (optional):

Airflow requires a home directory, and uses ~/airflow by default, but you can set a different location if you prefer. The AIRFLOW_HOME environment variable is used to inform Airflow of the desired location. This step of setting the environment variable should be done before installing Airflow so that the installation process knows where to store the necessary files.

export AIRFLOW_HOME=~/airflow
Install Airflow using the constraints file, which is determined based on the URL we pass:

AIRFLOW_VERSION=2.10.4

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.10.4 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.8.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
Run Airflow Standalone:

The airflow standalone command initializes the database, creates a user, and starts all components.

airflow standalone
Access the Airflow UI:

Visit localhost:8080 in your browser and log in with the admin account details shown in the terminal. Enable the example_bash_operator DAG in the home page.

Upon running these commands, Airflow will create the $AIRFLOW_HOME folder and create the “airflow.cfg” file with defaults that will get you going fast. You can override defaults using environment variables, see Configuration Reference. You can inspect the file either in $AIRFLOW_HOME/airflow.cfg, or through the UI in the Admin->Configuration menu. The PID file for the webserver will be stored in $AIRFLOW_HOME/airflow-webserver.pid or in /run/airflow/webserver.pid if started by systemd.

Out of the box, Airflow uses a SQLite database, which you should outgrow fairly quickly since no parallelization is possible using this database backend. It works in conjunction with the SequentialExecutor which will only run task instances sequentially. While this is very limiting, it allows you to get up and running quickly and take a tour of the UI and the command line utilities.

As you grow and deploy Airflow to production, you will also want to move away from the standalone command we use here to running the components separately. You can read more in Production Deployment.

Here are a few commands that will trigger a few task instances. You should be able to see the status of the jobs change in the example_bash_operator DAG as you run the commands below.

# run your first task instance
airflow tasks test example_bash_operator runme_0 2015-01-01
# run a backfill over 2 days
airflow dags backfill example_bash_operator \
    --start-date 2015-01-01 \
    --end-date 2015-01-02
If you want to run the individual parts of Airflow manually rather than using the all-in-one standalone command, you can instead run:

airflow db migrate

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

airflow webserver --port 8080

airflow scheduler
What’s Next?
From this point, you can head to the Tutorials section for further examples or the How-to Guides section if you’re ready to get your hands dirty.

Installation of Airflow®
Using released sources

Using PyPI

Using Production Docker Images

Using Official Airflow Helm Chart

Using Managed Airflow Services

Using 3rd-party images, charts, deployments

Notes about minimum requirements

This page describes installations options that you might use when considering how to install Airflow®. Airflow consists of many components, often distributed among many physical or virtual machines, therefore installation of Airflow might be quite complex, depending on the options you choose.

You should also check-out the Prerequisites that must be fulfilled when installing Airflow as well as Supported versions to know what are the policies for supporting Airflow, Python and Kubernetes.

Airflow requires additional Dependencies to be installed - which can be done via extras and providers.

When you install Airflow, you need to setup the database which must also be kept updated when Airflow is upgraded.

Warning

As of June 2021 Airflow 1.10 is end-of-life and is not going to receive any fixes even critical security fixes. Follow the Upgrading from 1.10 to 2 to learn how to upgrade the end-of-life 1.10 to Airflow 2.

Using released sources
More details: Installing from Sources

When this option works best

This option is best if you expect to build all your software from sources.

Apache Airflow is one of the projects that belong to the Apache Software Foundation. It is a requirement for all ASF projects that they can be installed using official sources released via Official Apache Downloads.

This is the best choice if you have a strong need to verify the integrity and provenance of the software

Intended users

Users who are familiar with installing and building software from sources and are conscious about integrity and provenance of the software they use down to the lowest level possible.

What are you expected to handle

You are expected to build and install airflow and its components on your own.

You should develop and handle the deployment for all components of Airflow.

You are responsible for setting up database, creating and managing database schema with airflow db commands, automated startup and recovery, maintenance, cleanup and upgrades of Airflow and the Airflow Providers.

You need to setup monitoring of your system allowing you to observe resources and react to problems.

You are expected to configure and manage appropriate resources for the installation (memory, CPU, etc) based on the monitoring of your installation and feedback loop. See the notes about requirements.

What Apache Airflow Community provides for that method

You have instructions on how to build the software but due to various environments and tools you might want to use, you might expect that there will be problems which are specific to your deployment and environment you will have to diagnose and solve.

Where to ask for help

The #user-troubleshooting channel on slack can be used for quick general troubleshooting questions. The GitHub discussions if you look for longer discussion and have more information to share.

The #user-best-practices channel on slack can be used to ask for and share best practices on using and deploying airflow.

If you can provide description of a reproducible problem with Airflow software, you can open issue at GitHub issues

If you want to contribute back to Airflow, the #contributors slack channel for building the Airflow itself

Using PyPI
More details: Installation from PyPI

When this option works best

This installation method is useful when you are not familiar with Containers and Docker and want to install Apache Airflow on physical or virtual machines and you are used to installing and running software using custom deployment mechanism.

The only officially supported mechanism of installation is via pip using constraint mechanisms. The constraint files are managed by Apache Airflow release managers to make sure that you can repeatably install Airflow from PyPI with all Providers and required dependencies.

In case of PyPI installation you could also verify integrity and provenance of the packages downloaded from PyPI as described at the installation page, but software you download from PyPI is pre-built for you so that you can install it without building, and you do not build the software from sources.

Intended users

Users who are familiar with installing and configuring Python applications, managing Python environments, dependencies and running software with their custom deployment mechanisms.

What are you expected to handle

You are expected to install Airflow - all components of it - on your own.

You should develop and handle the deployment for all components of Airflow.

You are responsible for setting up database, creating and managing database schema with airflow db commands, automated startup and recovery, maintenance, cleanup and upgrades of Airflow and Airflow Providers.

You need to setup monitoring of your system allowing you to observe resources and react to problems.

You are expected to configure and manage appropriate resources for the installation (memory, CPU, etc) based on the monitoring of your installation and feedback loop.

What Apache Airflow Community provides for that method

You have Installation from PyPI on how to install the software but due to various environments and tools you might want to use, you might expect that there will be problems which are specific to your deployment and environment you will have to diagnose and solve.

You have Quick Start where you can see an example of Quick Start with running Airflow locally which you can use to start Airflow quickly for local testing and development. However, this is just for inspiration. Do not expect Quick Start is ready for production installation, you need to build your own production-ready deployment if you follow this approach.

Where to ask for help

The #user-troubleshooting channel on Airflow Slack for quick general troubleshooting questions. The GitHub discussions if you look for longer discussion and have more information to share.

The #user-best-practices channel on slack can be used to ask for and share best practices on using and deploying airflow.

If you can provide description of a reproducible problem with Airflow software, you can open issue at GitHub issues

Using Production Docker Images
More details: Docker Image for Apache Airflow

When this option works best

This installation method is useful when you are familiar with Container/Docker stack. It provides a capability of running Airflow components in isolation from other software running on the same physical or virtual machines with easy maintenance of dependencies.

The images are built by Apache Airflow release managers and they use officially released packages from PyPI and official constraint files- same that are used for installing Airflow from PyPI.

Intended users

Users who are familiar with Containers and Docker stack and understand how to build their own container images.

Users who understand how to install providers and dependencies from PyPI with constraints if they want to extend or customize the image.

Users who know how to create deployments using Docker by linking together multiple Docker containers and maintaining such deployments.

What are you expected to handle

You are expected to be able to customize or extend Container/Docker images if you want to add extra dependencies. You are expected to put together a deployment built of several containers (for example using docker-compose) and to make sure that they are linked together.

You are responsible for setting up database, creating and managing database schema with airflow db commands, automated startup and recovery, maintenance, cleanup and upgrades of Airflow and the Airflow Providers.

You are responsible to manage your own customizations and extensions for your custom dependencies. With the Official Airflow Docker Images, upgrades of Airflow and Airflow Providers which are part of the reference image are handled by the community - you need to make sure to pick up those changes when released by upgrading the base image. However, you are responsible in creating a pipeline of building your own custom images with your own added dependencies and Providers and need to repeat the customization step and building your own image when new version of Airflow image is released.

You should choose the right deployment mechanism. There a number of available options of deployments of containers. You can use your own custom mechanism, custom Kubernetes deployments, custom Docker Compose, custom Helm charts etc., and you should choose it based on your experience and expectations.

You need to setup monitoring of your system allowing you to observe resources and react to problems.

You are expected to configure and manage appropriate resources for the installation (memory, CPU, etc) based on the monitoring of your installation and feedback loop.

What Apache Airflow Community provides for that method

You have instructions: Building the image on how to build and customize your image.

You have Running Airflow in Docker where you can see an example of Quick Start which you can use to start Airflow quickly for local testing and development. However, this is just for inspiration. Do not expect to use this docker-compose.yml file for production installation, you need to get familiar with Docker Compose and its capabilities and build your own production-ready deployment with it if you choose Docker Compose for your deployment.

The Docker Image is managed by the same people who build Airflow, and they are committed to keep it updated whenever new features and capabilities of Airflow are released.

Where to ask for help

For quick questions with the Official Docker Image there is the #production-docker-image channel in Airflow Slack.

The #user-troubleshooting channel on Airflow Slack for quick general troubleshooting questions. The GitHub discussions if you look for longer discussion and have more information to share.

The #user-best-practices channel on slack can be used to ask for and share best practices on using and deploying airflow.

If you can provide description of a reproducible problem with Airflow software, you can open issue at GitHub issues

Using Official Airflow Helm Chart
More details: Helm Chart for Apache Airflow

When this option works best

This installation method is useful when you are not only familiar with Container/Docker stack but also when you use Kubernetes and want to install and maintain Airflow using the community-managed Kubernetes installation mechanism via Helm chart.

It provides not only a capability of running Airflow components in isolation from other software running on the same physical or virtual machines and managing dependencies, but also it provides capabilities of easier maintaining, configuring and upgrading Airflow in the way that is standardized and will be maintained by the community.

The Chart uses the Official Airflow Production Docker Images to run Airflow.

Intended users

Users who are familiar with Containers and Docker stack and understand how to build their own container images.

Users who understand how to install providers and dependencies from PyPI with constraints if they want to extend or customize the image.

Users who manage their infrastructure using Kubernetes and manage their applications on Kubernetes using Helm Charts.

What are you expected to handle

You are expected to be able to customize or extend Container/Docker images if you want to add extra dependencies. You are expected to put together a deployment built of several containers (for example using Docker Compose) and to make sure that they are linked together.

You are responsible for setting up database.

The Helm Chart manages your database schema, automates startup, recovery and restarts of the components of the application and linking them together, so you do not have to worry about that.

You are responsible to manage your own customizations and extensions for your custom dependencies. With the Official Airflow Docker Images, upgrades of Airflow and Airflow Providers which are part of the reference image are handled by the community - you need to make sure to pick up those changes when released by upgrading the base image. However, you are responsible in creating a pipeline of building your own custom images with your own added dependencies and Providers and need to repeat the customization step and building your own image when new version of Airflow image is released.

You need to setup monitoring of your system allowing you to observe resources and react to problems.

You are expected to configure and manage appropriate resources for the installation (memory, CPU, etc) based on the monitoring of your installation and feedback loop.

What Apache Airflow Community provides for that method

You have instructions: Building the image on how to build and customize your image.

You have Helm Chart for Apache Airflow - full documentation on how to configure and install the Helm Chart.

The Helm Chart is managed by the same people who build Airflow, and they are committed to keep it updated whenever new features and capabilities of Airflow are released.

Where to ask for help

For quick questions with the Official Docker Image there is the #production-docker-image channel in Airflow Slack.

For quick questions with the official Helm Chart there is the #helm-chart-official channel in Slack.

The #user-troubleshooting channel on Airflow Slack for quick general troubleshooting questions. The GitHub discussions if you look for longer discussion and have more information to share.

The #user-best-practices channel on slack can be used to ask for and share best practices on using and deploying airflow.

If you can provide description of a reproducible problem with Airflow software, you can open issue at GitHub issues

Using Managed Airflow Services
Follow the Ecosystem page to find all Managed Services for Airflow.

When this option works best

When you prefer to have someone else manage Airflow installation for you, there are Managed Airflow Services that you can use.

Intended users

Users who prefer to get Airflow managed for them and want to pay for it.

What are you expected to handle

The Managed Services usually provide everything you need to run Airflow. Please refer to documentation of the Managed Services for details.

What Apache Airflow Community provides for that method

Airflow Community does not provide any specific documentation for managed services. Please refer to the documentation of the Managed Services for details.

Where to ask for help

Your first choice should be support that is provided by the Managed services. There are a few channels in the Apache Airflow Slack that are dedicated to different groups of users and if you have come to conclusion the question is more related to Airflow than the managed service, you can use those channels.

Using 3rd-party images, charts, deployments
Follow the Ecosystem page to find all 3rd-party deployment options.

When this option works best

Those installation methods are useful in case none of the official methods mentioned before work for you, or you have historically used those. It is recommended though that whenever you consider any change, you should consider switching to one of the methods that are officially supported by the Apache Airflow Community or Managed Services.

Intended users

Users who historically used other installation methods or find the official methods not sufficient for other reasons.

What are you expected to handle

Depends on what the 3rd-party provides. Look at the documentation of the 3rd-party.

What Apache Airflow Community provides for that method

Airflow Community does not provide any specific documentation for 3rd-party methods. Please refer to the documentation of the Managed Services for details.

Where to ask for help

Depends on what the 3rd-party provides. Look at the documentation of the 3rd-party deployment you use.

Notes about minimum requirements
There are often questions about minimum requirements for Airflow for production systems, but it is not possible to give a simple answer to that question.

The requirements that Airflow might need depend on many factors, including (but not limited to):
The deployment your Airflow is installed with (see above ways of installing Airflow)

The requirements of the deployment environment (for example Kubernetes, Docker, Helm, etc.) that are completely independent from Airflow (for example DNS resources, sharing the nodes/resources) with more (or less) pods and containers that are needed that might depend on particular choice of the technology/cloud/integration of monitoring etc.

Technical details of database, hardware, network, etc. that your deployment is running on

The complexity of the code you add to your DAGS, configuration, plugins, settings etc. (note, that Airflow runs the code that DAG author and Deployment Manager provide)

The number and choice of providers you install and use (Airflow has more than 80 providers) that can be installed by choice of the Deployment Manager and using them might require more resources.

The choice of parameters that you use when tuning Airflow. Airflow has many configuration parameters that can fine-tuned to your needs

The number of DagRuns and tasks instances you run with parallel instances of each in consideration

How complex are the tasks you run

The above “DAG” characteristics will change over time and even will change depending on the time of the day or week, so you have to be prepared to continuously monitor the system and adjust the parameters to make it works smoothly.

While we can provide some specific minimum requirements for some development “quick start” - such as in case of our Running Airflow in Docker quick-start guide, it is not possible to provide any minimum requirements for production systems.

The best way to think of resource allocation for Airflow instance is to think of it in terms of process control theory - where there are two types of systems:

Fully predictable, with few knobs and variables, where you can reliably set the values for the knobs and have an easy way to determine the behaviour of the system

Complex systems with multiple variables, that are hard to predict and where you need to monitor the system and adjust the knobs continuously to make sure the system is running smoothly.

Airflow (and generally any modern system running usually on cloud services, with multiple layers responsible for resources as well multiple parameters to control their behaviour) is a complex system and they fall much more in the second category. If you decide to run Airflow in production on your own, you should be prepared for the monitor/observe/adjust feedback loop to make sure the system is running smoothly.

Having a good monitoring system that will allow you to monitor the system and adjust the parameters is a must to put that in practice.

There are few guidelines that you can use for optimizing your resource usage as well. The Fine-tuning your Scheduler performance is a good starting point to fine-tune your scheduler, you can also follow the Best Practices guide to make sure you are using Airflow in the most efficient way.

Also, one of the important things that Managed Services for Airflow provide is that they make a lot of opinionated choices and fine-tune the system for you, so you don’t have to worry about it too much. With such managed services, there are usually far less number of knobs to turn and choices to make and one of the things you pay for is that the Managed Service provider manages the system for you and provides paid support and allows you to scale the system as needed and allocate the right resources - following the choices made there when it comes to the kinds of deployment you might have.

Prerequisites
Airflow® is tested with:

Python: 3.8, 3.9, 3.10, 3.11, 3.12

Databases:

PostgreSQL: 12, 13, 14, 15, 16

MySQL: 8.0, Innovation

SQLite: 3.15.0+

Kubernetes: 1.26, 1.27, 1.28, 1.29, 1.30

The minimum memory required we recommend Airflow to run with is 4GB, but the actual requirements depend wildly on the deployment options you have

Warning

Despite significant similarities between MariaDB and MySQL, we DO NOT support MariaDB as a backend for Airflow. There are known problems (for example index handling) between MariaDB and MySQL and we do not test our migration scripts nor application execution on Maria DB. We know there were people who used MariaDB for Airflow and that cause a lot of operational headache for them so we strongly discourage attempts to use MariaDB as a backend and users cannot expect any community support for it because the number of users who tried to use MariaDB for Airflow is very small.

Warning

SQLite is used in Airflow tests. Do not use it in production. We recommend using the latest stable version of SQLite for local development.

Warning

Airflow® currently can be run on POSIX-compliant Operating Systems. For development it is regularly tested on fairly modern Linux Distros that our contributors use and recent versions of MacOS. On Windows you can run it via WSL2 (Windows Subsystem for Linux 2) or via Linux Containers. The work to add Windows support is tracked via #10388 but it is not a high priority. You should only use Linux-based distros as “Production” execution environment as this is the only environment that is supported. The only distro that is used in our CI tests and that is used in the Community managed DockerHub image is Debian Bookworm.

Dependencies
Airflow extra dependencies
The apache-airflow PyPI basic package only installs what’s needed to get started. Additional packages can be installed depending on what will be useful in your environment. For instance, if you don’t need connectivity with Postgres, you won’t have to go through the trouble of installing the postgres-devel yum package, or whatever equivalent applies on the distribution you are using.

Most of the extra dependencies are linked to a corresponding provider package. For example “amazon” extra has a corresponding apache-airflow-providers-amazon provider package to be installed. When you install Airflow with such extras, the necessary provider packages are installed automatically (latest versions from PyPI for those packages). However, you can freely upgrade and install provider packages independently from the main Airflow installation.

For the list of the extras and what they enable, see: Reference for package extras.

Provider packages
Unlike Apache Airflow 1.10, the Airflow 2.0 is delivered in multiple, separate, but connected packages. The core of Airflow scheduling system is delivered as apache-airflow package and there are around 60 provider packages which can be installed separately as so called Airflow Provider packages. The default Airflow installation doesn’t have many integrations and you have to install them yourself.

You can even develop and install your own providers for Airflow. For more information, see: Provider packages

For the list of the provider packages and what they enable, see: Providers packages reference.

Differences between extras and providers
Just to prevent confusion of extras versus provider packages: Extras and providers are different things, though many extras are leading to installing providers.

Extras are standard Python setuptools feature that allows to add additional set of dependencies as optional features to “core” Apache Airflow. One of the type of such optional features are providers packages, but not all optional features of Apache Airflow have corresponding providers.

We are using the extras setuptools features to also install provider packages. Most of the extras are also linked (same name) with provider packages - for example adding [google] extra also adds apache-airflow-providers-google as dependency. However, there are some extras that do not install providers (examples github_enterprise, kerberos, async - they add some extra dependencies which are needed for those extra features of Airflow mentioned. The three examples above add respectively GitHub Enterprise OAuth authentication, Kerberos integration or asynchronous workers for Gunicorn. None of those have providers, they are just extending Apache Airflow “core” package with new functionalities.

System dependencies
You need certain system level requirements in order to install Airflow. Those are requirements that are known to be needed for Linux Debian distributions:

Debian Bookworm (12)
Debian Bookworm is our platform of choice for development and testing. It is the most up-to-date Debian distribution and it is the one we use for our CI/CD system. It is also the one we recommend for development and testing as well as production use.

sudo apt install -y --no-install-recommends apt-utils ca-certificates \
  curl dumb-init freetds-bin krb5-user libgeos-dev \
  ldap-utils libsasl2-2 libsasl2-modules libxmlsec1 locales libffi8 libldap-2.5-0 libssl3 netcat-openbsd \
  lsb-release openssh-client python3-selinux rsync sasl2-bin sqlite3 sudo unixodbc


  Supported versions
Version Life Cycle
Apache Airflow® version life cycle:

Version

Current Patch/Minor

State

First Release

Limited Support

EOL/Terminated

2

2.10.4

Supported

Dec 17, 2020

TBD

TBD

1.10

1.10.15

EOL

Aug 27, 2018

Dec 17, 2020

June 17, 2021

1.9

1.9.0

EOL

Jan 03, 2018

Aug 27, 2018

Aug 27, 2018

1.8

1.8.2

EOL

Mar 19, 2017

Jan 03, 2018

Jan 03, 2018

1.7

1.7.1.2

EOL

Mar 28, 2016

Mar 19, 2017

Mar 19, 2017

Limited support versions will be supported with security and critical bug fix only. EOL versions will not get any fixes nor support. We highly recommend installing the latest Airflow release which has richer features.

Support for Python and Kubernetes versions
As of Airflow 2.0 we agreed to certain rules we follow for Python and Kubernetes support. They are based on the official release schedule of Python and Kubernetes, nicely summarized in the Python Developer’s Guide and Kubernetes version skew policy.

We drop support for Python and Kubernetes versions when they reach EOL. We drop support for those EOL versions in main right after EOL date, and it is effectively removed when we release the first new MINOR (Or MAJOR if there is no new MINOR version) of Airflow For example for Python 3.6 it means that we drop support in main right after 23.12.2021, and the first MAJOR or MINOR version of Airflow released after will not have it.

The “oldest” supported version of Python/Kubernetes is the default one. “Default” is only meaningful in terms of “smoke tests” in CI PRs which are run using this default version and default reference image available in DockerHub. Currently the apache/airflow:latest and apache/airflow:2.5.2 images are Python 3.8 images, however, in the first MINOR/MAJOR release of Airflow released after 14.09.2023, they will become Python 3.9 images.

We support a new version of Python/Kubernetes in main after they are officially released, as soon as we make them work in our CI pipeline (which might not be immediate due to dependencies catching up with new versions of Python mostly) we release a new images/support in Airflow based on the working CI setup.

Installing from Sources
Released packages
This page describes downloading and verifying Airflow® version 2.10.4 using officially released packages. You can also install Apache Airflow - as most Python packages - via PyPI. You can choose different version of Airflow by selecting different version from the drop-down at the top-left of the page.

The source, sdist and whl packages released are the “official” sources of installation that you can use if you want to verify the origin of the packages and want to verify checksums and signatures of the packages. The packages are available via the Official Apache Software Foundations Downloads

As of version 2.8 Airflow follows PEP 517/518 and uses pyproject.toml file to define build dependencies and build process and it requires relatively modern versions of packaging tools to get airflow built from local sources or sdist packages, as PEP 517 compliant build hooks are used to determine dynamic build dependencies. In case of pip it means that at least version 22.1.0 is needed (released at the beginning of 2022) to build or install Airflow from sources. This does not affect the ability of installing Airflow from released wheel packages.

The 2.10.4 downloads of Airflow® are available at:

Sources package (asc, sha512)

Sdist package (asc, sha512)

Whl package (asc, sha512)

If you want to install from the source code, you can download from the sources link above, it will contain a INSTALL file containing details on how you can build and install Airflow.

Release integrity
PGP signatures KEYS

It is essential that you verify the integrity of the downloaded files using the PGP or SHA signatures. The PGP signatures can be verified using GPG or PGP. Please download the KEYS as well as the asc signature files for relevant distribution. It is recommended to get these files from the main distribution directory and not from the mirrors.

gpg -i KEYS
or

pgpk -a KEYS
or

pgp -ka KEYS
To verify the binaries/sources you can download the relevant asc files for it from main distribution directory and follow the below guide.

gpg --verify apache-airflow-********.asc apache-airflow-*********
or

pgpv apache-airflow-********.asc
or

pgp apache-airflow-********.asc
Example:

$ gpg --verify apache-airflow-2.10.4-source.tar.gz.asc apache-airflow-2.10.4-source.tar.gz
  gpg: Signature made Sat 11 Sep 12:49:54 2021 BST
  gpg:                using RSA key CDE15C6E4D3A8EC4ECF4BA4B6674E08AD7DE406F
  gpg:                issuer "kaxilnaik@apache.org"
  gpg: Good signature from "Kaxil Naik <kaxilnaik@apache.org>" [unknown]
  gpg:                 aka "Kaxil Naik <kaxilnaik@gmail.com>" [unknown]
  gpg: WARNING: The key's User ID is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: CDE1 5C6E 4D3A 8EC4 ECF4  BA4B 6674 E08A D7DE 406F
The “Good signature from …” is indication that the signatures are correct. Do not worry about the “not certified with a trusted signature” warning. Most of the certificates used by release managers are self signed, that’s why you get this warning. By importing the server in the previous step and importing it via ID from KEYS page, you know that this is a valid Key already.

For SHA512 sum check, download the relevant sha512 and run the following:

shasum -a 512 apache-airflow--********  | diff - apache-airflow--********.sha512
The SHASUM of the file should match the one provided in .sha512 file.

Example:

shasum -a 512 apache-airflow-2.10.4-source.tar.gz  | diff - apache-airflow-2.10.4-source.tar.gz.sha512
Verifying PyPI releases
You can verify the Airflow .whl packages from PyPI by locally downloading the package and signature and SHA sum files with the script below:

#!/bin/bash
AIRFLOW_VERSION="2.10.4"
airflow_download_dir="$(mktemp -d)"
pip download --no-deps "apache-airflow==${AIRFLOW_VERSION}" --dest "${airflow_download_dir}"
curl "https://downloads.apache.org/airflow/${AIRFLOW_VERSION}/apache_airflow-${AIRFLOW_VERSION}-py3-none-any.whl.asc" \
    -L -o "${airflow_download_dir}/apache_airflow-${AIRFLOW_VERSION}-py3-none-any.whl.asc"
curl "https://downloads.apache.org/airflow/${AIRFLOW_VERSION}/apache_airflow-${AIRFLOW_VERSION}-py3-none-any.whl.sha512" \
    -L -o "${airflow_download_dir}/apache_airflow-${AIRFLOW_VERSION}-py3-none-any.whl.sha512"
echo
echo "Please verify files downloaded to ${airflow_download_dir}"
ls -la "${airflow_download_dir}"
echo
Once you verify the files following the instructions from previous chapter you can remove the temporary folder created.

Installation from PyPI
This page describes installations using the apache-airflow package published in PyPI.

Installation tools
Only pip installation is currently officially supported.

Note

While there are some successes with using other tools like poetry or pip-tools, they do not share the same workflow as pip - especially when it comes to constraint vs. requirements management. Installing via Poetry or pip-tools is not currently supported. If you wish to install airflow using those tools you should use the constraints and convert them to appropriate format and workflow that your tool requires.

There are known issues with bazel that might lead to circular dependencies when using it to install Airflow. Please switch to pip if you encounter such problems. Bazel community works on fixing the problem in this PR so it might be that newer versions of bazel will handle it.

Typical command to install airflow from scratch in a reproducible way from PyPI looks like below:

pip install "apache-airflow[celery]==2.10.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.8.txt"
Typically, you can add other dependencies and providers as separate command after the reproducible installation - this way you can upgrade or downgrade the dependencies as you see fit, without limiting them to constraints. Good practice for those is to extend such pip install command with the apache-airflow pinned to the version you have already installed to make sure it is not accidentally upgraded or downgraded by pip.

pip install "apache-airflow==2.10.4" apache-airflow-providers-google==10.1.0
Those are just examples, see further for more explanation why those are the best practices.

Note

Generally speaking, Python community established practice is to perform application installation in a virtualenv created with virtualenv or venv tools. You can also use pipx to install Airflow® in a application dedicated virtual environment created for you. There are also other tools that can be used to manage your virtualenv installation and you are free to choose how you are managing the environments. Airflow has no limitation regarding to the tool of your choice when it comes to virtual environment.

The only exception where you might consider not using virtualenv is when you are building a container image with only Airflow installed - this is for example how Airflow is installed in the official Container image.

Constraints files
Why we need constraints
Airflow® installation can be tricky because Airflow is both a library and an application.

Libraries usually keep their dependencies open and applications usually pin them, but we should do neither and both at the same time. We decided to keep our dependencies as open as possible (in pyproject.toml) so users can install different version of libraries if needed. This means that from time to time plain pip install apache-airflow will not work or will produce an unusable Airflow installation.

Reproducible Airflow installation
In order to have a reproducible installation, we also keep a set of constraint files in the constraints-main, constraints-2-0, constraints-2-1 etc. orphan branches and then we create a tag for each released version e.g. constraints-2.10.4.

This way, we keep a tested set of dependencies at the moment of release. This provides you with the ability of having the exact same installation of airflow + providers + dependencies as was known to be working at the moment of release - frozen set of dependencies for that version of Airflow. There is a separate constraints file for each version of Python that Airflow supports.

You can create the URL to the file substituting the variables in the template below.

https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt
where:

AIRFLOW_VERSION - Airflow version (e.g. 2.10.4) or main, 2-0, for latest development version

PYTHON_VERSION Python version e.g. 3.8, 3.9

The examples below assume that you want to use install airflow in a reproducible way with the celery extra, but you can pick your own set of extras and providers to install.

pip install "apache-airflow[celery]==2.10.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.8.txt"
Note

The reproducible installation guarantees that this initial installation steps will always work for you - providing that you use the right Python version and that you have appropriate Operating System dependencies installed for the providers to be installed. Some of the providers require additional OS dependencies to be installed such as build-essential in order to compile libraries, or for example database client libraries in case you install a database provider, etc.. You need to figure out which system dependencies you need when your installation fails and install them before retrying the installation.

Upgrading and installing dependencies (including providers)
The reproducible installation above should not prevent you from being able to upgrade or downgrade providers and other dependencies to other versions

You can, for example, install new versions of providers and dependencies after the release to use the latest version and up-to-date with latest security fixes - even if you do not want upgrade airflow core version. Or you can downgrade some dependencies or providers if you want to keep previous versions for compatibility reasons. Installing such dependencies should be done without constraints as a separate pip command.

When you do such an upgrade, you should make sure to also add the apache-airflow package to the list of packages to install and pin it to the version that you have, otherwise you might end up with a different version of Airflow than you expect because pip can upgrade/downgrade it automatically when performing dependency resolution.

pip install "apache-airflow[celery]==2.10.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.8.txt"
pip install "apache-airflow==2.10.4" apache-airflow-providers-google==10.1.1
You can also downgrade or upgrade other dependencies this way - even if they are not compatible with those dependencies that are stored in the original constraints file:

pip install "apache-airflow[celery]==2.10.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.8.txt"
pip install "apache-airflow[celery]==2.10.4" dbt-core==0.20.0
Warning

Not all dependencies can be installed this way - you might have dependencies conflicting with basic requirements of Airflow or other dependencies installed in your system. However, by skipping constraints when you install or upgrade dependencies, you give pip a chance to resolve the conflicts for you, while keeping dependencies within the limits that Apache Airflow, providers and other dependencies require. The resulting combination of those dependencies and the set of dependencies that come with the constraints might not be tested before, but it should work in most cases as we usually add requirements, when Airflow depends on particular versions of some dependencies. In cases you cannot install some dependencies in the same environment as Airflow - you can attempt to use other approaches. See best practices for handling conflicting/complex Python dependencies

Verifying installed dependencies
You can also always run the pip check command to test if the set of your Python packages is consistent and not conflicting.

> pip check
No broken requirements found.
When you see such message and the exit code from pip check is 0, you can be sure, that there are no conflicting dependencies in your environment.

Using your own constraints
When you decide to install your own dependencies, or want to upgrade or downgrade providers, you might want to continue being able to keep reproducible installation of Airflow and those dependencies via a single command. In order to do that, you can produce your own constraints file and use it to install Airflow instead of the one provided by the community.

pip install "apache-airflow[celery]==2.10.4" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.8.txt"
pip install "apache-airflow==2.10.4" dbt-core==0.20.0
pip freeze > my-constraints.txt
Then you can use it to create reproducible installations of your environment in a single operation via a local constraints file:

pip install "apache-airflow[celery]==2.10.4" --constraint "my-constraints.txt"
Similarly as in case of Airflow original constraints, you can also host your constraints at your own repository or server and use it remotely from there.

Fixing Constraints at release time
The released “versioned” constraints are mostly fixed when we release Airflow version and we only update them in exceptional circumstances. For example when we find out that the released constraints might prevent Airflow from being installed consistently from the scratch.

In normal circumstances, the constraint files are not going to change if new version of Airflow dependencies are released - not even when those versions contain critical security fixes. The process of Airflow releases is designed around upgrading dependencies automatically where applicable but only when we release a new version of Airflow, not for already released versions.

Between the releases you can upgrade dependencies on your own and you can keep your own constraints updated as described in the previous section.

The easiest way to keep-up with the latest released dependencies is to upgrade to the latest released Airflow version. Whenever we release a new version of Airflow, we upgrade all dependencies to the latest applicable versions and test them together, so if you want to keep up with those tests - staying up-to-date with latest version of Airflow is the easiest way to update those dependencies.

Installation and upgrade scenarios
In order to simplify the installation, we have prepared examples of how to upgrade Airflow and providers.

Installing Airflow® with extras and providers
If you need to install extra dependencies of Airflow®, you can use the script below to make an installation a one-liner (the example below installs Postgres and Google providers, as well as async extra).

AIRFLOW_VERSION=2.10.4
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[async,postgres,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
Note, that it will install the versions of providers that were available at the moment this version of Airflow has been released. You need to run separate pip commands without constraints, if you want to upgrade provider packages in case they were released afterwards.

Upgrading Airflow together with providers
You can upgrade airflow together with extras (providers available at the time of the release of Airflow being installed. This will bring apache-airflow and all providers to the versions that were released and tested together when the version of Airflow you are installing was released.

AIRFLOW_VERSION=2.10.4
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[postgres,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
Managing providers separately from Airflow core
In order to add new features, implement bug-fixes or simply maintain backwards compatibility, you might need to install, upgrade or downgrade any of the providers - separately from the Airflow Core package. We release providers independently from the core of Airflow, so often new versions of providers are released before Airflow is, also if you do not want yet to upgrade Airflow to the latest version, you might want to install just some (or all) newly released providers separately.

As you saw above, when installing the providers separately, you should not use any constraint files.

If you build your environment automatically, You should run provider’s installation as a separate command after Airflow has been installed (usually with constraints). Constraints are only effective during the pip install command they were used with.

It is the best practice to install apache-airflow in the same version as the one that comes from the original image. This way you can be sure that pip will not try to downgrade or upgrade apache airflow while installing other requirements, which might happen in case you try to add a dependency that conflicts with the version of apache-airflow that you are using:

pip install "apache-airflow==2.10.4" "apache-airflow-providers-google==8.0.0"
Note

Installing, upgrading, downgrading providers separately is not guaranteed to work with all Airflow versions or other providers. Some providers have minimum-required version of Airflow and some versions of providers might have limits on dependencies that are conflicting with limits of other providers or other dependencies installed. For example google provider before 10.1.0 version had limit of protobuf library <=3.20.0 while for example google-ads library that is supported by google has requirement for protobuf library >=4. In such cases installing those two dependencies alongside in a single environment will not work. In such cases you can attempt to use other approaches. See best practices for handling conflicting/complex Python dependencies

Managing just Airflow core without providers
If you don’t want to install any providers you have, just install or upgrade Apache Airflow, you can simply install airflow in the version you need. You can use the special constraints-no-providers constraints file, which is smaller and limits the dependencies to the core of Airflow only, however this can lead to conflicts if your environment already has some of the dependencies installed in different versions and in case you have other providers installed. This command, however, gives you the latest versions of dependencies compatible with just airflow core at the moment Airflow was released.

AIRFLOW_VERSION=2.10.4
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
# For example: 3.8
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-no-providers-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-no-providers-3.8.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
Note

Airflow uses Scarf to collect basic usage data during operation. Check the Usage data collection FAQ for more information about the data collected and how to opt-out.

Troubleshooting
This section describes how to troubleshoot installation issues with PyPI installation.

The ‘airflow’ command is not recognized
If the airflow command is not getting recognized (can happen on Windows when using WSL), then ensure that ~/.local/bin is in your PATH environment variable, and add it in if necessary:

PATH=$PATH:~/.local/bin
You can also start airflow with python -m airflow

Symbol not found: _Py_GetArgcArgv
If you see Symbol not found: _Py_GetArgcArgv while starting or importing airflow, this may mean that you are using an incompatible version of Python. For a homebrew installed version of Python, this is generally caused by using Python in /usr/local/opt/bin rather than the Frameworks installation (e.g. for python 3.8: /usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8).

The crux of the issue is that a library Airflow depends on, setproctitle, uses a non-public Python API which is not available from the standard installation /usr/local/opt/ (which symlinks to a path under /usr/local/Cellar).

An easy fix is just to ensure you use a version of Python that has a dylib of the Python library available. For example:

# Note: these instructions are for python3.8 but can be loosely modified for other versions
brew install python@3.8
virtualenv -p /usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/bin/python3 .toy-venv
source .toy-venv/bin/activate
pip install apache-airflow
python
>>> import setproctitle
# Success!
Alternatively, you can download and install Python directly from the Python website.

Setting up the database
Apache Airflow® requires a database. If you’re just experimenting and learning Airflow, you can stick with the default SQLite option. If you don’t want to use SQLite, then take a look at Set up a Database Backend to setup a different database.

Usually, you need to run airflow db migrate in order to create the database schema if it does not exist or migrate to the latest version if it does. You should make sure that Airflow components are not running while the database migration is being executed.

Note

Prior to Airflow version 2.7.0, airflow db upgrade was used to apply migrations, however, it has been deprecated in favor of airflow db migrate.

In some deployments, such as Helm Chart for Apache Airflow, both initializing and running the database migration is executed automatically when Airflow is upgraded.

Sometimes, after the upgrade, you are also supposed to do some post-migration actions. See Upgrading Airflow® to a newer version for more details about upgrading and doing post-migration actions.

Upgrading Airflow® to a newer version
Why you need to upgrade
Newer Airflow versions can contain database migrations so you must run airflow db migrate to migrate your database with the schema changes in the Airflow version you are upgrading to. Don’t worry, it’s safe to run even if there are no migrations to perform.

What are the changes between Airflow version x and y?
The release notes lists the changes that were included in any given Airflow release.

Upgrade preparation - make a backup of DB
It is highly recommended to make a backup of your metadata DB before any migration. If you do not have a “hot backup” capability for your DB, you should do it after shutting down your Airflow instances, so that the backup of your database will be consistent. If you did not make a backup and your migration fails, you might end-up in a half-migrated state and restoring DB from backup and repeating the migration might be the only easy way out. This can for example be caused by a broken network connection between your CLI and the database while the migration happens, so taking a backup is an important precaution to avoid problems like this.

When you need to upgrade
If you have a custom deployment based on virtualenv or Docker Containers, you usually need to run the DB migrate manually as part of the upgrade process.

In some cases the upgrade happens automatically - it depends if in your deployment, the upgrade is built-in as post-install action. For example when you are using Helm Chart for Apache Airflow with post-upgrade hooks enabled, the database upgrade happens automatically right after the new software is installed. Similarly all Airflow-As-A-Service solutions perform the upgrade automatically for you, when you choose to upgrade airflow via their UI.

How to upgrade
Reinstall Apache Airflow®, specifying the desired new version.

To upgrade a bootstrapped local instance, you can set the AIRFLOW_VERSION environment variable to the intended version prior to rerunning the installation command. Upgrade incrementally by patch version: e.g., if upgrading from version 2.8.2 to 2.8.4, upgrade first to 2.8.3. For more detailed guidance, see Quick Start.

To upgrade a PyPI package, rerun the pip install command in your environment using the desired version as a constraint. For more detailed guidance, see Installation from PyPI.

In order to manually migrate the database you should run the airflow db migrate command in your environment. It can be run either in your virtual environment or in the containers that give you access to Airflow CLI Using the Command Line Interface and the database.

Offline SQL migration scripts
If you want to run the upgrade script offline, you can use the -s or --show-sql-only flag to get the SQL statements that would be executed. You may also specify the starting airflow version with the --from-version flag and the ending airflow version with the -n or --to-version flag. This feature is supported in Postgres and MySQL from Airflow 2.0.0 onward.

Sample usage for Airflow version 2.7.0 or greater:
airflow db migrate -s --from-version "2.4.3" -n "2.7.3" airflow db migrate --show-sql-only --from-version "2.4.3" --to-version "2.7.3"

Note

airflow db upgrade has been replaced by airflow db migrate since Airflow version 2.7.0 and former has been deprecated.

Handling migration problems
Wrong Encoding in MySQL database
If you are using old Airflow 1.10 as a database created initially either manually or with previous version of MySQL, depending on the original character set of your database, you might have problems with migrating to a newer version of Airflow and your migration might fail with strange errors (“key size too big”, “missing indexes” etc). The next chapter describes how to fix the problem manually.

Why you might get the error? The recommended character set/collation for MySQL 8 database is utf8mb4 and utf8mb4_bin respectively. However, this has been changing in different versions of MySQL and you could have custom created database with a different character set. If your database was created with an old version of Airflow or MySQL, the encoding could have been wrong when the database was created or broken during migration.

Unfortunately, MySQL limits the index key size and with utf8mb4, Airflow index key sizes might be too big for MySQL to handle. Therefore in Airflow we force all the “ID” keys to use utf8 character set (which is equivalent to utf8mb3 in MySQL 8). This limits the size of indexes so that MySQL can handle them.

Here are the steps you can follow to fix it BEFORE you attempt to migrate (but you might also choose to do it your way if you know what you are doing).

Get familiar with the internal Database structure of Airflow which you might find at ERD Schema of the Database and list of migrations that you might find in Reference for Database Migrations.

Make a backup of your database so that you can restore it in case of a mistake.

Check which of the tables of yours need fixing. Look at those tables:

SHOW CREATE TABLE task_reschedule;
SHOW CREATE TABLE xcom;
SHOW CREATE TABLE task_fail;
SHOW CREATE TABLE rendered_task_instance_fields;
SHOW CREATE TABLE task_instance;
Make sure to copy the output. You will need it in the last step. Your dag_id, run_id, task_id and key columns should have utf8 or utf8mb3 character set set explicitly, similar to:

``task_id`` varchar(250) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,  # correct
or

``task_id`` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,  # correct
The problem is if your fields have no encoding:

``task_id`` varchar(250),  # wrong !!
or just collation set to utf8mb4:

``task_id`` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,  # wrong !!
or character set and collation set to utf8mb4

``task_id`` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,  # wrong !!
You need to fix those fields that have wrong character set/collation set.

3. Drop foreign key indexes for tables you need to modify (you do not need to drop all of them - do it just for those tables that you need to modify). You will need to recreate them in the last step (that’s why you need to keep the SHOW CREATE TABLE output from step 2.

ALTER TABLE task_reschedule DROP FOREIGN KEY task_reschedule_ti_fkey;
ALTER TABLE xcom DROP FOREIGN KEY xcom_task_instance_fkey;
ALTER TABLE task_fail DROP FOREIGN KEY task_fail_ti_fkey;
ALTER TABLE rendered_task_instance_fields DROP FOREIGN KEY rtif_ti_fkey;
4. Modify your ID fields to have correct character set/encoding. Only do that for fields that have wrong encoding (here are all potential commands you might need to use):

ALTER TABLE task_instance MODIFY task_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE task_reschedule MODIFY task_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;

ALTER TABLE rendered_task_instance_fields MODIFY task_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE rendered_task_instance_fields MODIFY dag_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;

ALTER TABLE task_fail MODIFY task_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE task_fail MODIFY dag_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;

ALTER TABLE sla_miss MODIFY task_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE sla_miss MODIFY dag_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;

ALTER TABLE task_map MODIFY task_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE task_map MODIFY dag_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE task_map MODIFY run_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;

ALTER TABLE xcom MODIFY task_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE xcom MODIFY dag_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE xcom MODIFY run_id VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
ALTER TABLE xcom MODIFY key VARCHAR(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;
Recreate the foreign keys dropped in step 3.

Repeat this one for all the indexes you dropped. Note that depending on the version of Airflow you Have, the indexes might be slightly different (for example map_index was added in 2.3.0) but if you keep the SHOW CREATE TABLE output prepared in step 2., you will find the right CONSTRAINT_NAME and CONSTRAINT to use.

# Here you have to copy the statements from SHOW CREATE TABLE output
ALTER TABLE <TABLE> ADD CONSTRAINT `<CONSTRAINT_NAME>` <CONSTRAINT>
This should bring the database to the state where you will be able to run the migration to the new Airflow version.

Post-upgrade warnings
Typically you just need to successfully run airflow db migrate command and this is all. However, in some cases, the migration might find some old, stale and probably wrong data in your database and moves it aside to a separate table. In this case you might get warning in your webserver UI about the data found.

Typical message that you might see:

Airflow found incompatible data in the <original table> table in the metadatabase, and has moved them to <new table> during the database migration to upgrade. Please inspect the moved data to decide whether you need to keep them, and manually drop the <new table> table to dismiss this warning.

When you see such message, it means that some of your data was corrupted and you should inspect it to determine whether you would like to keep or delete some of that data. Most likely the data was corrupted and left-over from some bugs and can be safely deleted - because this data would not be anyhow visible and useful in Airflow. However, if you have particular need for auditing or historical reasons you might choose to store it somewhere. Unless you have specific reasons to keep the data most likely deleting it is your best option.

There are various ways you can inspect and delete the data - if you have direct access to the database using your own tools (often graphical tools showing the database objects), you can drop such table or rename it or move it to another database using those tools. If you don’t have such tools you can use the airflow db shell command - this will drop you in the db shell tool for your database and you will be able to both inspect and delete the table.

How to drop the table using Kubernetes:

Exec into any of the Airflow pods - webserver or scheduler: kubectl exec -it <your-webserver-pod> python

Run the following commands in the python shell:

from airflow.settings import Session

session = Session()
session.execute("DROP TABLE _airflow_moved__2_2__task_instance")
session.commit()
Please replace <table> in the examples with the actual table name as printed in the warning message.

Inspecting a table:

SELECT * FROM <table>;
Deleting a table:

DROP TABLE <table>;
Migration best practices
Depending on the size of your database and the actual migration it might take quite some time to migrate it, so if you have long history and big database, it is recommended to make a copy of the database first and perform a test migration to assess how long the migration will take. Typically “Major” upgrades might take longer as adding new features require sometimes restructuring of the database.

Security
This section of the documentation covers security-related topics.

Make sure to get familiar with the Airflow Security Model if you want to understand the different user types of Apache Airflow®, what they have access to, and the role Deployment Managers have in deploying Airflow in a secure way.

Also, if you want to understand how Airflow releases security patches and what to expect from them, head over to Releasing security patches.

Follow the below topics as well to understand other aspects of Airflow security:

API
Audit Logs in Airflow
Flower
Kerberos
Releasing security patches
SBOM
Airflow Security Model
Webserver
Workload
Secrets

API
API Authentication
The API authentication is handled by the auth manager. For more information about API authentication, please refer to the auth manager documentation used by your environment. By default Airflow uses the FAB auth manager, if you did not specify any other auth manager, please look at API Authentication.

Enabling CORS
Cross-origin resource sharing (CORS) is a browser security feature that restricts HTTP requests that are initiated from scripts running in the browser.

Access-Control-Allow-Headers, Access-Control-Allow-Methods, and Access-Control-Allow-Origin headers can be added by setting values for access_control_allow_headers, access_control_allow_methods, and access_control_allow_origins options in the [api] section of the airflow.cfg file.

[api]
access_control_allow_headers = origin, content-type, accept
access_control_allow_methods = POST, GET, OPTIONS, DELETE
access_control_allow_origins = https://exampleclientapp1.com https://exampleclientapp2.com
Page size limit
To protect against requests that may lead to application instability, the stable API has a limit of items in response. The default is 100 items, but you can change it using maximum_page_limit option in [api] section in the airflow.cfg file.

Audit Logs in Airflow
Overview
Audit logs are a critical component of any system that needs to maintain a high level of security and compliance. They provide a way to track user actions and system events, which can be used to troubleshoot issues, detect security breaches, and ensure regulatory compliance.

In Airflow, audit logs are used to track user actions and system events that occur during the execution of DAGs and tasks. They are stored in a database and can be accessed through the Airflow UI.

To be able to see audit logs, a user needs to have the Audit Logs.can_read permission. Such user will be able to see all audit logs, independently of the DAGs permissions applied.

Level of Audit Logs
Audit logs exist at the task level and the user level.

Task Level: At the task level, audit logs capture information related to the execution of a task, such as the start time, end time, and status of the task.

User Level: At the user level, audit logs capture information related to user actions, such as creating, modifying, or deleting a DAG or task.

Location of Audit Logs
Audit logs can be accessed through the Airflow UI. They are located under the “Browse” tab, and can be viewed by selecting “Audit Logs” from the dropdown menu.

Types of Events
Airflow provides a set of predefined events that can be tracked in audit logs. These events include, but aren’t limited to:

trigger: Triggering a DAG

[variable,connection].create: A user created a Connection or Variable

[variable,connection].edit: A user modified a Connection or Variable

[variable,connection].delete: A user deleted a Connection or Variable

delete: A user deleted a DAG or task

failed: Airflow or a user set a task as failed

success: Airflow or a user set a task as success

retry: Airflow or a user retried a task instance

clear: A user cleared a task’s state

cli_task_run: Airflow triggered a task instance

In addition to these predefined events, Airflow allows you to define custom events that can be tracked in audit logs. This can be done by calling the log method of the TaskInstance object.

Flower
Flower is a web based tool for monitoring and administrating Celery clusters. This topic describes how to configure Airflow to secure your flower instance.

This is an optional component that is disabled by default in Community deployments and you need to configure it on your own if you want to use it.

Flower Authentication
Basic authentication for Celery Flower is supported.

You can specify the details either as an optional argument in the Flower process launching command, or as a configuration item in your airflow.cfg. For both cases, please provide user:password pairs separated by a comma.

airflow celery flower --basic-auth=user1:password1,user2:password2
[celery]
flower_basic_auth = user1:password1,user2:password2
Flower URL Prefix
Enables deploying Celery Flower on non-root URL

For example to access Flower on http://example.com/flower run it with:

airflow celery flower --url-prefix=flower
[celery]
flower_url_prefix = flower
NOTE: The old nginx rewrite is no longer needed

Kerberos
Airflow has initial support for Kerberos. This means that Airflow can renew Kerberos tickets for itself and store it in the ticket cache. The hooks and DAGs can make use of ticket to authenticate against kerberized services.

Limitations
Please note that at this time, not all hooks have been adjusted to make use of this functionality. Also it does not integrate Kerberos into the web interface and you will have to rely on network level security for now to make sure your service remains secure.

Celery integration has not been tried and tested yet. However, if you generate a key tab for every host and launch a ticket renewer next to every worker it will most likely work.

Enabling Kerberos
Airflow
To enable Kerberos you will need to generate a (service) key tab.

# in the kadmin.local or kadmin shell, create the airflow principal
kadmin:  addprinc -randkey airflow/fully.qualified.domain.name@YOUR-REALM.COM

# Create the airflow keytab file that will contain the airflow principal
kadmin:  xst -norandkey -k airflow.keytab airflow/fully.qualified.domain.name
Now store this file in a location where the airflow user can read it (chmod 600). And then add the following to your airflow.cfg

[core]
security = kerberos

[kerberos]
keytab = /etc/airflow/airflow.keytab
reinit_frequency = 3600
principal = airflow
In case you are using Airflow in a docker container based environment, you can set the below environment variables in the Dockerfile instead of modifying airflow.cfg

ENV AIRFLOW__CORE__SECURITY kerberos
ENV AIRFLOW__KERBEROS__KEYTAB /etc/airflow/airflow.keytab
ENV AIRFLOW__KERBEROS__INCLUDE_IP False
If you need more granular options for your Kerberos ticket the following options are available with the following default values:

[kerberos]
# Location of your ccache file once kinit has been performed
ccache = /tmp/airflow_krb5_ccache
# principal gets augmented with fqdn
principal = airflow
reinit_frequency = 3600
kinit_path = kinit
keytab = airflow.keytab

# Allow kerberos token to be flag forwardable or not
forwardable = True

# Allow to include or remove local IP from kerberos token.
# This is particularly useful if you use Airflow inside a VM NATted behind host system IP.
include_ip = True
Keep in mind that Kerberos ticket are generated via kinit and will your use your local krb5.conf by default.

Launch the ticket renewer by

# run ticket renewer
airflow kerberos
To support more advanced deployment models for using kerberos in standard or one-time fashion, you can specify the mode while running the airflow kerberos by using the --one-time flag.

a) standard: The airflow kerberos command will run endlessly. The ticket renewer process runs continuously every few seconds and refreshes the ticket if it has expired. b) one-time: The airflow kerberos will run once and exit. In case of failure the main task won’t spin up.

The default mode is standard.

Example usages:

For standard mode:

airflow kerberos
For one time mode:

airflow kerberos --one-time
Hadoop
If want to use impersonation this needs to be enabled in core-site.xml of your hadoop config.

<property>
  <name>hadoop.proxyuser.airflow.groups</name>
  <value>*</value>
</property>

<property>
  <name>hadoop.proxyuser.airflow.users</name>
  <value>*</value>
</property>

<property>
  <name>hadoop.proxyuser.airflow.hosts</name>
  <value>*</value>
</property>
Of course if you need to tighten your security replace the asterisk with something more appropriate.

Using Kerberos authentication
The Hive hook has been updated to take advantage of Kerberos authentication. To allow your DAGs to use it, simply update the connection details with, for example:

{ "use_beeline": true, "principal": "hive/_HOST@EXAMPLE.COM"}
Adjust the principal to your settings. The _HOST part will be replaced by the fully qualified domain name of the server.

You can specify if you would like to use the DAG owner as the user for the connection or the user specified in the login section of the connection. For the login user, specify the following as extra:

{ "use_beeline": true, "principal": "hive/_HOST@EXAMPLE.COM", "proxy_user": "login"}
For the DAG owner use:

{ "use_beeline": true, "principal": "hive/_HOST@EXAMPLE.COM", "proxy_user": "owner"}
and in your DAG, when initializing the HiveOperator, specify:

run_as_owner=True
To use kerberos authentication, you must install Airflow with the kerberos extras group:

pip install 'apache-airflow[kerberos]'
You can read about some production aspects of Kerberos deployment at Kerberos-authenticated workers

Releasing security patches
Apache Airflow® uses a consistent and predictable approach for releasing security patches - both for the Apache Airflow package and Apache Airflow providers (security patches in providers are treated separately from security patches in Airflow core package).

Releasing Airflow with security patches
Apache Airflow uses a strict SemVer versioning policy, which means that we strive for any release of a given MAJOR Version (version “2” currently) to be backwards compatible. When we release a MINOR version, the development continues in the main branch where we prepare the next MINOR version, but we release PATCHLEVEL releases with selected bugfixes (including security bugfixes) cherry-picked to the latest released MINOR line of Apache Airflow. At the moment, when we release a new MINOR version, we stop releasing PATCHLEVEL releases for the previous MINOR version.

For example, once we released 2.6.0 version on April 30, 2023 all the security patches will be cherry-picked and released in 2.6.* versions until we release 2.7.0 version. There will be no 2.5.* versions released after 2.6.0 has been released.

This means that in order to apply security fixes in Apache Airflow, you MUST upgrade to the latest MINOR and PATCHLEVEL version of Airflow.

Releasing Airflow providers with security patches
Similarly to Airflow, providers uses a strict SemVer versioning policy, and the same policies apply for providers as for Airflow itself. This means that you need to upgrade to the latest MINOR and PATCHLEVEL version of the provider to get the latest security fixes. Airflow providers are released independently from Airflow itself and the information about vulnerabilities is published separately. You can upgrade providers independently from Airflow itself, following the instructions found in Managing providers separately from Airflow core.

SBOM
Software Bill Of Materials (SBOM) files are critical assets used for transparency, providing a clear inventory of all the components used in Apache Airflow (name, version, supplier and transitive dependencies). They are an exhaustive representation of the software dependencies.

The general use case for such files is to help assess and manage risks. For instance a quick lookup against your SBOM files can help identify if a CVE (Common Vulnerabilities and Exposures) in a library is affecting you.

By default, Apache Airflow SBOM files are generated for airflow core with all providers. In the near future we aim at generating SBOM files per provider and also provide them for docker standard images.

Each airflow version has its own SBOM files, one for each supported python version. You can find them here.

Airflow Security Model
This document describes Airflow’s security model from the perspective of the Airflow user. It is intended to help users understand the security model and make informed decisions about how to deploy and manage Airflow.

If you would like to know how to report security vulnerabilities and how security reports are handled by the security team of Airflow, head to Airflow’s Security Policy.

Airflow security model - user types
The Airflow security model involves different types of users with varying access and capabilities:

While - in smaller installations - all the actions related to Airflow can be performed by a single user, in larger installations it is apparent that there different responsibilities, roles and capabilities that need to be separated.

This is why Airflow has the following user types:

Deployment Managers - overall responsible for the Airflow installation, security and configuration

Authenticated UI users - users that can access Airflow UI and API and interact with it

DAG Authors - responsible for creating DAGs and submitting them to Airflow

You can see more on how the user types influence Airflow’s architecture in Architecture Overview, including, seeing the diagrams of less and more complex deployments.

Deployment Managers
They have the highest level of access and control. They install and configure Airflow, and make decisions about technologies and permissions. They can potentially delete the entire installation and have access to all credentials. Deployment Managers can also decide to keep audits, backups and copies of information outside of Airflow, which are not covered by Airflow’s security model.

DAG Authors
They can create, modify, and delete DAG files. The code in DAG files is executed on workers and in the DAG File Processor. Note that in the simple deployment configuration, parsing DAGs is executed as a subprocess of the Scheduler process, but with Standalone DAG File Processor deployment managers might separate parsing DAGs from the Scheduler process. Therefore, DAG authors can create and change code executed on workers and the DAG File Processor and potentially access the credentials that the DAG code uses to access external systems. DAG Authors have full access to the metadata database.

Authenticated UI users
They have access to the UI and API. See below for more details on the capabilities authenticated UI users may have.

Non-authenticated UI users
Airflow doesn’t support unauthenticated users by default. If allowed, potential vulnerabilities must be assessed and addressed by the Deployment Manager. However, there are exceptions to this. The /health endpoint responsible to get health check updates should be publicly accessible. This is because other systems would want to retrieve that information. Another exception is the /login endpoint, as the users are expected to be unauthenticated to use it.

Capabilities of authenticated UI users
The capabilities of Authenticated UI users can vary depending on what roles have been configured by the Deployment Manager or Admin users as well as what permissions those roles have. Permissions on roles can be scoped as tightly as a single DAG, for example, or as broad as Admin. Below are four general categories to help conceptualize some of the capabilities authenticated users may have:

Admin users
They manage and grant permissions to other users, with full access to all UI capabilities. They can potentially execute code on workers by configuring connections and need to be trusted not to abuse these privileges. They have access to sensitive credentials and can modify them. By default, they don’t have access to system-level configuration. They should be trusted not to misuse sensitive information accessible through connection configuration. They also have the ability to create a Webserver Denial of Service situation and should be trusted not to misuse this capability.

Only admin users have access to audit logs.

Operations users
The primary difference between an operator and admin is the ability to manage and grant permissions to other users, and access audit logs - only admins are able to do this. Otherwise assume they have the same access as an admin.

Connection configuration users
They configure connections and potentially execute code on workers during DAG execution. Trust is required to prevent misuse of these privileges. They have full access to sensitive credentials stored in connections and can modify them. Access to sensitive information through connection configuration should be trusted not to be abused. They also have the ability to configure connections wrongly that might create a Webserver Denial of Service situations and specify insecure connection options which might create situations where executing DAGs will lead to arbitrary Remote Code Execution for some providers - either community released or custom ones.

Those users should be highly trusted not to misuse this capability.

Audit log users
They can view audit events for the whole Airflow installation.

Regular users
They can view and interact with the UI and API. They are able to view and edit DAGs, task instances, and DAG runs, and view task logs.

Viewer users
They can view information related to DAGs, in a read only fashion, task logs, and other relevant details. This role is suitable for users who require read-only access without the ability to trigger or modify DAGs.

Viewers also do not have permission to access audit logs.

For more information on the capabilities of authenticated UI users, see Access Control.

Capabilities of DAG Authors
DAG authors are able to submit code - via Python files placed in the DAGS_FOLDER - that will be executed in a number of circumstances. The code to execute is neither verified, checked nor sand-boxed by Airflow (that would be very difficult if not impossible to do), so effectively DAG authors can execute arbitrary code on the workers (part of Celery Workers for Celery Executor, local processes run by scheduler in case of Local Executor, Task Kubernetes POD in case of Kubernetes Executor), in the DAG File Processor (which can be either executed as standalone process or can be part of the Scheduler) and in the Triggerer.

There are several consequences of this model chosen by Airflow, that deployment managers need to be aware of:

Local executor and built-in DAG File Processor
In case of Local Executor and DAG File Processor running as part of the Scheduler, DAG authors can execute arbitrary code on the machine where scheduler is running. This means that they can affect the scheduler process itself, and potentially affect the whole Airflow installation - including modifying cluster-wide policies and changing Airflow configuration. If you are running Airflow with one of those settings, the Deployment Manager must trust the DAG authors not to abuse this capability.

Celery Executor
In case of Celery Executor, DAG authors can execute arbitrary code on the Celery Workers. This means that they can potentially influence all the tasks executed on the same worker. If you are running Airflow with Celery Executor, the Deployment Manager must trust the DAG authors not to abuse this capability and unless Deployment Manager separates task execution by queues by Cluster Policies, they should assume, there is no isolation between tasks.

Kubernetes Executor
In case of Kubernetes Executor, DAG authors can execute arbitrary code on the Kubernetes POD they run. Each task is executed in a separate POD, so there is already isolation between tasks as generally speaking Kubernetes provides isolation between PODs.

Triggerer
In case of Triggerer, DAG authors can execute arbitrary code in Triggerer. Currently there are no enforcement mechanisms that would allow to isolate tasks that are using deferrable functionality from each other and arbitrary code from various tasks can be executed in the same process/machine. Deployment Manager must trust that DAG authors will not abuse this capability.

DAG files not needed for Scheduler and Webserver
The Deployment Manager might isolate the code execution provided by DAG authors - particularly in Scheduler and Webserver by making sure that the Scheduler and Webserver don’t even have access to the DAG Files (that requires standalone DAG File Processor to be deployed). Generally speaking - no DAG author provided code should ever be executed in the Scheduler or Webserver process.

Allowing DAG authors to execute selected code in Scheduler and Webserver
There are a number of functionalities that allow the DAG author to use pre-registered custom code to be executed in scheduler or webserver process - for example they can choose custom Timetables, UI plugins, Connection UI Fields, Operator extra links, macros, listeners - all of those functionalities allow the DAG author to choose the code that will be executed in the scheduler or webserver process. However this should not be arbitrary code that DAG author can add in DAG folder. All those functionalities are only available via plugins and providers mechanisms where the code that is executed can only be provided by installed packages (or in case of plugins it can also be added to PLUGINS folder where DAG authors should not have write access to). PLUGINS_FOLDER is a legacy mechanism coming from Airflow 1.10 - but we recommend using entrypoint mechanism that allows the Deployment Manager to - effectively - choose and register the code that will be executed in those contexts. DAG Author has no access to install or modify packages installed in Webserver and Scheduler, and this is the way to prevent the DAG Author to execute arbitrary code in those processes.

Additionally, if you decide to utilize and configure the PLUGINS_FOLDER, it is essential for the Deployment Manager to ensure that the DAG author does not have write access to this folder.

The Deployment Manager might decide to introduce additional control mechanisms to prevent DAG authors from executing arbitrary code. This is all fully in hands of the Deployment Manager and it is discussed in the following chapter.

Access to All DAGs
All DAG authors have access to all DAGs in the airflow deployment. This means that they can view, modify, and update any DAG without restrictions at any time.

Responsibilities of Deployment Managers
As a Deployment Manager, you should be aware of the capabilities of DAG authors and make sure that you trust them not to abuse the capabilities they have. You should also make sure that you have properly configured the Airflow installation to prevent DAG authors from executing arbitrary code in the Scheduler and Webserver processes.

Deploying and protecting Airflow installation
Deployment Managers are also responsible for deploying airflow and make it accessible to the users in the way that follows best practices of secure deployment applicable to the organization where Airflow is deployed. This includes but is not limited to:

protecting communication using TLS/VPC and whatever network security is required by the organization that is deploying Airflow

applying rate-limiting and other forms of protections that is usually applied to web applications

applying authentication and authorization to the web application so that only known and authorized users can have access to Airflow

any kind of detection of unusual activity and protection against it

choosing the right session backend and configuring it properly including timeouts for the session

Limiting DAG Author capabilities
The Deployment Manager might also use additional mechanisms to prevent DAG authors from executing arbitrary code - for example they might introduce tooling around DAG submission that would allow to review the code before it is deployed, statically-check it and add other ways to prevent malicious code to be submitted. The way how submitting code to DAG folder is done and protected is completely up to the Deployment Manager - Airflow does not provide any tooling or mechanisms around it and it expects that the Deployment Manager will provide the tooling to protect access to the DAG folder and make sure that only trusted code is submitted there.

Airflow does not implement any of those feature natively, and delegates it to the deployment managers to deploy all the necessary infrastructure to protect the deployment - as external infrastructure components.

Limiting access for authenticated UI users
Deployment Managers also determine access levels and must understand the potential damage users can cause. Some Deployment Managers may further limit access through fine-grained privileges for the Authenticated UI users. However, these limitations are outside the basic Airflow’s security model and are at the discretion of Deployment Managers.

Examples of fine-grained access control include (but are not limited to):

Limiting login permissions: Restricting the accounts that users can log in with, allowing only specific accounts or roles belonging to access the Airflow system.

Access restrictions to views or DAGs: Controlling user access to certain views or specific DAGs, ensuring that users can only view or interact with authorized components.

Future: multi-tenancy isolation
These examples showcase ways in which Deployment Managers can refine and limit user privileges within Airflow, providing tighter control and ensuring that users have access only to the necessary components and functionalities based on their roles and responsibilities. However, fine-grained access control does not provide full isolation and separation of access to allow isolation of different user groups in a multi-tenant fashion yet. In future versions of Airflow, some fine-grained access control features could become part of the Airflow security model, as the Airflow community is working on a multi-tenant model currently.

Webserver
This topic describes how to configure Airflow to secure your webserver.

Rendering Airflow UI in a Web Frame from another site
Using Airflow in a web frame is enabled by default. To disable this (and prevent click jacking attacks) set the below:

[webserver]
x_frame_enabled = False
Disable Deployment Exposure Warning
Airflow warns when recent requests are made to /robots.txt. To disable this warning set warn_deployment_exposure to False as below:

[webserver]
warn_deployment_exposure = False
Sensitive Variable fields
Variable values that are deemed “sensitive” based on the variable name will be masked in the UI automatically. See Masking sensitive data for more details.

Web Authentication
The webserver authentication is handled by the auth manager. For more information about webserver authentication, please refer to the auth manager documentation used by your environment. By default Airflow uses the FAB auth manager, if you did not specify any other auth manager, please look at Webserver authentication.

SSL
SSL can be enabled by providing a certificate and key. Once enabled, be sure to use “https://” in your browser.

[webserver]
web_server_ssl_cert = <path to cert>
web_server_ssl_key = <path to key>
Enabling SSL will not automatically change the web server port. If you want to use the standard port 443, you’ll need to configure that too. Be aware that super user privileges (or cap_net_bind_service on Linux) are required to listen on port 443.

# Optionally, set the server to listen on the standard SSL port.
web_server_port = 443
base_url = http://<hostname or IP>:443
Enable CeleryExecutor with SSL. Ensure you properly generate client and server certs and keys.

[celery]
ssl_active = True
ssl_key = <path to key>
ssl_cert = <path to cert>
ssl_cacert = <path to cacert>
Rate limiting
Airflow can be configured to limit the number of authentication requests in a given time window. We are using Flask-Limiter to achieve that and by default Airflow uses per-webserver default limit of 5 requests per 40 second fixed window. By default no common storage for rate limits is used between the gunicorn processes you run so rate-limit is applied separately for each process, so assuming random distribution of the requests by gunicorn with single webserver instance and default 4 gunicorn workers, the effective rate limit is 5 x 4 = 20 requests per 40 second window (more or less). However you can configure the rate limit to be shared between the processes by using rate limit storage via setting the RATELIMIT_* configuration settings in webserver_config.py. For example, to use Redis as a rate limit storage you can use the following configuration (you need to set redis_host to your Redis instance)

RATELIMIT_STORAGE_URI = "redis://redis_host:6379/0"
You can also configure other rate limit settings in webserver_config.py - for more details, see the Flask Limiter rate limit configuration.

Workload
This topic describes how to configure Airflow to secure your workload.

Impersonation
Airflow has the ability to impersonate a unix user while running task instances based on the task’s run_as_user parameter, which takes a user’s name.

NOTE: For impersonations to work, Airflow requires sudo as subtasks are run with sudo -u and permissions of files are changed. Furthermore, the unix user needs to exist on the worker. Here is what a simple sudoers file entry could look like to achieve this, assuming airflow is running as the airflow user. This means the airflow user must be trusted and treated the same way as the root user.

airflow ALL=(ALL) NOPASSWD: ALL
Subtasks with impersonation will still log to the same folder, except that the files they log to will have permissions changed such that only the unix user can write to it.

Default Impersonation
To prevent tasks that don’t use impersonation to be run with sudo privileges, you can set the core:default_impersonation config which sets a default user impersonate if run_as_user is not set.

[core]
default_impersonation = airflow

Secrets
During Airflow operation, variables or configurations are used that contain particularly sensitive information. This guide provides ways to protect this data.

The following are particularly protected:

Variables. See the Variables Concepts documentation for more information.

Connections. See the Connections Concepts documentation for more information.

Further reading:

Encryption at rest
Using external Secret stores
Masking sensitive data
Fernet
Airflow uses Fernet to encrypt passwords in the connection configuration and the variable configuration. It guarantees that a password encrypted using it cannot be manipulated or read without the key. Fernet is an implementation of symmetric (also known as “secret key”) authenticated cryptography.

The first time Airflow is started, the airflow.cfg file is generated with the default configuration and the unique Fernet key. The key is saved to option fernet_key of section [core].

You can also configure a fernet key using environment variables. This will overwrite the value from the airflow.cfg file

# Note the double underscores
export AIRFLOW__CORE__FERNET_KEY=your_fernet_key
Generating Fernet key
If you need to generate a new fernet key you can use the following code snippet.

from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())  # your fernet_key, keep it in secured place!
Rotating encryption keys
Once connection credentials and variables have been encrypted using a fernet key, changing the key will cause decryption of existing credentials to fail. To rotate the fernet key without invalidating existing encrypted values, prepend the new key to the fernet_key setting, run airflow rotate-fernet-key, and then drop the original key from fernet_key:

Set fernet_key to new_fernet_key,old_fernet_key

Run airflow rotate-fernet-key to re-encrypt existing credentials with the new fernet key

Set fernet_key to new_fernet_key

Secrets Backend
New in version 1.10.10.

In addition to retrieving connections & variables from environment variables or the metastore database, you can also enable alternative secrets backend to retrieve Airflow connections or Airflow variables via Apache Airflow Community provided backends in Secret backends.

Note

The Airflow UI only shows connections and variables stored in the Metadata DB and not via any other method. If you use an alternative secrets backend, check inside your backend to view the values of your variables and connections.

You can also get Airflow configurations with sensitive data from the Secrets Backend. See Setting Configuration Options for more details.

Search path
When looking up a connection/variable, by default Airflow will search environment variables first and metastore database second.

If you enable an alternative secrets backend, it will be searched first, followed by environment variables, then metastore. This search ordering is not configurable. Though, in some alternative secrets backend you might have the option to filter which connection/variable/config is searched in the secret backend. Please look at the documentation of the secret backend you are using to see if such option is available.

Warning

When using environment variables or an alternative secrets backend to store secrets or variables, it is possible to create key collisions. In the event of a duplicated key between backends, all write operations will update the value in the metastore, but all read operations will return the first match for the requested key starting with the custom backend, then the environment variables and finally the metastore.

Configuration
The [secrets] section has the following options:

[secrets]
backend =
backend_kwargs =
Set backend to the fully qualified class name of the backend you want to enable.

You can provide backend_kwargs with json and it will be passed as kwargs to the __init__ method of your secrets backend.

If you want to check which secret backend is currently set, you can use airflow config get-value secrets backend command as in the example below.

$ airflow config get-value secrets backend
airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
Supported core backends
Local Filesystem Secrets Backend
Apache Airflow Community provided secret backends
Apache Airflow Community also releases community developed providers (Provider packages) and some of them also provide handlers that extend secret backends capability of Apache Airflow. You can see all those providers in Secret backends.

Roll your own secrets backend
A secrets backend is a subclass of airflow.secrets.base_secrets.BaseSecretsBackend and must implement either get_connection() or get_conn_value() for retrieving connections, get_variable() for retrieving variables and get_config() for retrieving Airflow configurations.

After writing your backend class, provide the fully qualified class name in the backend key in the [secrets] section of airflow.cfg.

Additional arguments to your SecretsBackend can be configured in airflow.cfg by supplying a JSON string to backend_kwargs, which will be passed to the __init__ of your SecretsBackend. See Configuration for more details, and SSM Parameter Store for an example.

Adapt to non-Airflow compatible secret formats for connections
The default implementation of Secret backend requires use of an Airflow-specific format of storing secrets for connections. Currently most community provided implementations require the connections to be stored as JSON or the Airflow Connection URI format (see Secret backends). However, some organizations may need to store the credentials (passwords/tokens etc) in some other way. For example, if the same credentials store needs to be used for multiple data platforms, or if you are using a service with a built-in mechanism of rotating the credentials that does not work with the Airflow-specific format. In this case you will need to roll your own secret backend as described in the previous chapter, possibly extending an existing secrets backend and adapting it to the scheme used by your organization.

Local Filesystem Secrets Backend
This backend is especially useful in the following use cases:

Development: It ensures data synchronization between all terminal windows (same as databases), and at the same time the values are retained after database restart (same as environment variable)

Kubernetes: It allows you to store secrets in Kubernetes Secrets or you can synchronize values using the sidecar container and a shared volume

To use variable and connection from local file, specify LocalFilesystemBackend as the backend in [secrets] section of airflow.cfg.

Available parameters to backend_kwargs:

variables_file_path: File location with variables data.

connections_file_path: File location with connections data.

Here is a sample configuration:

[secrets]
backend = airflow.secrets.local_filesystem.LocalFilesystemBackend
backend_kwargs = {"variables_file_path": "/files/var.json", "connections_file_path": "/files/conn.json"}
JSON, YAML and .env files are supported. All parameters are optional. If the file path is not passed, the backend returns an empty collection.

Storing and Retrieving Connections
If you have set connections_file_path as /files/my_conn.json, then the backend will read the file /files/my_conn.json when it looks for connections.

The file can be defined in JSON, YAML or env format. Depending on the format, the data should be saved as a URL or as a connection object. Any extra json parameters can be provided using keys like extra_dejson and extra. The key extra_dejson can be used to provide parameters as JSON object where as the key extra can be used in case of a JSON string. The keys extra and extra_dejson are mutually exclusive.

The JSON file must contain an object where the key contains the connection ID and the value contains the definition of one connection. The connection can be defined as a URI (string) or JSON object. For a guide about defining a connection as a URI, see Generating a connection URI. For a description of the connection object parameters see Connection. The following is a sample JSON file.

{
    "CONN_A": "mysql://host_a",
    "CONN_B": {
        "conn_type": "scheme",
        "host": "host",
        "schema": "schema",
        "login": "Login",
        "password": "None",
        "port": "1234"
    }
}
The YAML file structure is similar to that of a JSON. The key-value pair of connection ID and the definitions of one or more connections. In this format, the connection can be defined as a URI (string) or JSON object.

CONN_A: 'mysql://host_a'

CONN_B:
  - 'mysql://host_a'
  - 'mysql://host_b'

CONN_C:
  conn_type: scheme
  host: host
  schema: lschema
  login: Login
  password: None
  port: 1234
  extra_dejson:
    a: b
    nestedblock_dict:
      x: y
You can also define connections using a .env file. Then the key is the connection ID, and the value should describe the connection using the URI. Connection ID should not be repeated, it will raise an exception. The following is a sample file.

mysql_conn_id=mysql://log:password@13.1.21.1:3306/mysqldbrd
google_custom_key=google-cloud-platform://?key_path=%2Fkeys%2Fkey.json
Storing and Retrieving Variables
If you have set variables_file_path as /files/my_var.json, then the backend will read the file /files/my_var.json when it looks for variables.

The file can be defined in JSON, YAML or env format.

The JSON file must contain an object where the key contains the variable key and the value contains the variable value. The following is a sample JSON file.

{
    "VAR_A": "some_value",
    "var_b": "different_value"
}
The YAML file structure is similar to that of JSON, with key containing the variable key and the value containing the variable value. The following is a sample YAML file.

VAR_A: some_value
VAR_B: different_value
You can also define variable using a .env file. Then the key is the variable key, and variable should describe the variable value. The following is a sample file.

VAR_A=some_value
var_B=different_value

Masking sensitive data
Airflow will by default mask Connection passwords and sensitive Variables and keys from a Connection’s extra (JSON) field when they appear in Task logs, in the Variable and in the Rendered fields views of the UI.

It does this by looking for the specific value appearing anywhere in your output. This means that if you have a connection with a password of a, then every instance of the letter a in your logs will be replaced with ***.

To disable masking you can set hide_sensitive_var_conn_fields to false.

The automatic masking is triggered by Connection or Variable access. This means that if you pass a sensitive value via XCom or any other side-channel it will not be masked when printed in the downstream task.

Sensitive field names
When masking is enabled, Airflow will always mask the password field of every Connection that is accessed by a task.

It will also mask the value of a Variable, rendered template dictionaries, XCom dictionaries or the field of a Connection’s extra JSON blob if the name contains any words in (‘access_token’, ‘api_key’, ‘apikey’, ‘authorization’, ‘passphrase’, ‘passwd’, ‘password’, ‘private_key’, ‘secret’, ‘token’). This list can also be extended:

[core]
sensitive_var_conn_names = comma,separated,sensitive,names
Adding your own masks
If you want to mask an additional secret that is not already masked by one of the above methods, you can do it in your DAG file or operator’s execute function using the mask_secret function. For example:

@task
def my_func():
    from airflow.utils.log.secrets_masker import mask_secret

    mask_secret("custom_value")

    ...
or

class MyOperator(BaseOperator):
    def execute(self, context):
        from airflow.utils.log.secrets_masker import mask_secret

        mask_secret("custom_value")

        ...
The mask must be set before any log/output is produced to have any effect.

NOT masking when using environment variables
When you are using some operators - for example airflow.providers.cncf.kubernetes.operators.pod.KubernetesPodOperator, you might be tempted to pass secrets via environment variables. This is very bad practice because the environment variables are visible to anyone who has access to see the environment of the process - such secrets passed by environment variables will NOT be masked by Airflow.

If you need to pass secrets to the KubernetesPodOperator, you should use native Kubernetes secrets or use Airflow Connection or Variables to retrieve the secrets dynamically

Tutorials
Once you have Airflow up and running with the Quick Start, these tutorials are a great way to get a sense for how Airflow works.

Fundamental Concepts
Working with TaskFlow
Building a Running Pipeline
Object Storage

Fundamental Concepts
This tutorial walks you through some of the fundamental Airflow concepts, objects, and their usage while writing your first DAG.

Example Pipeline definition
Here is an example of a basic pipeline definition. Do not worry if this looks complicated, a line by line explanation follows below.

airflow/example_dags/tutorial.py
[source]


import textwrap
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
with DAG(
    "tutorial",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    t1.doc_md = textwrap.dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](https://imgs.xkcd.com/comics/fixing_problems.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = textwrap.dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    t1 >> [t2, t3]
It’s a DAG definition file
One thing to wrap your head around (it may not be very intuitive for everyone at first) is that this Airflow Python script is really just a configuration file specifying the DAG’s structure as code. The actual tasks defined here will run in a different context from the context of this script. Different tasks run on different workers at different points in time, which means that this script cannot be used to cross communicate between tasks. Note that for this purpose we have a more advanced feature called XComs.

People sometimes think of the DAG definition file as a place where they can do some actual data processing - that is not the case at all! The script’s purpose is to define a DAG object. It needs to evaluate quickly (seconds, not minutes) since the scheduler will execute it periodically to reflect the changes if any.

Importing Modules
An Airflow pipeline is just a Python script that happens to define an Airflow DAG object. Let’s start by importing the libraries we will need.

airflow/example_dags/tutorial.py
[source]

import textwrap
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

See Modules Management for details on how Python and Airflow manage modules.

Default Arguments
We’re about to create a DAG and some tasks, and we have the choice to explicitly pass a set of arguments to each task’s constructor (which would become redundant), or (better!) we can define a dictionary of default parameters that we can use when creating tasks.

airflow/example_dags/tutorial.py
[source]

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function, # or list of functions
    # 'on_success_callback': some_other_function, # or list of functions
    # 'on_retry_callback': another_function, # or list of functions
    # 'sla_miss_callback': yet_another_function, # or list of functions
    # 'on_skipped_callback': another_function, #or list of functions
    # 'trigger_rule': 'all_success'
},
For more information about the BaseOperator’s parameters and what they do, refer to the airflow.models.baseoperator.BaseOperator documentation.

Also, note that you could easily define different sets of arguments that would serve different purposes. An example of that would be to have different settings between a production and development environment.

Instantiate a DAG
We’ll need a DAG object to nest our tasks into. Here we pass a string that defines the dag_id, which serves as a unique identifier for your DAG. We also pass the default argument dictionary that we just defined and define a schedule of 1 day for the DAG.

airflow/example_dags/tutorial.py
[source]

with DAG(
    "tutorial",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
Operators
An operator defines a unit of work for Airflow to complete. Using operators is the classic approach to defining work in Airflow. For some use cases, it’s better to use the TaskFlow API to define work in a Pythonic context as described in Working with TaskFlow. For now, using operators helps to visualize task dependencies in our DAG code.

All operators inherit from the BaseOperator, which includes all of the required arguments for running work in Airflow. From here, each operator includes unique arguments for the type of work it’s completing. Some of the most popular operators are the PythonOperator, the BashOperator, and the KubernetesPodOperator.

Airflow completes work based on the arguments you pass to your operators. In this tutorial, we use the BashOperator to run a few bash scripts.

Tasks
To use an operator in a DAG, you have to instantiate it as a task. Tasks determine how to execute your operator’s work within the context of a DAG.

In the following example, we instantiate the BashOperator as two separate tasks in order to run two separate bash scripts. The first argument for each instantiation, task_id, acts as a unique identifier for the task.

airflow/example_dags/tutorial.py
[source]

t1 = BashOperator(
    task_id="print_date",
    bash_command="date",
)

t2 = BashOperator(
    task_id="sleep",
    depends_on_past=False,
    bash_command="sleep 5",
    retries=3,
)
Notice how we pass a mix of operator specific arguments (bash_command) and an argument common to all operators (retries) inherited from BaseOperator to the operator’s constructor. This is simpler than passing every argument for every constructor call. Also, notice that in the second task we override the retries parameter with 3.

The precedence rules for a task are as follows:

Explicitly passed arguments

Values that exist in the default_args dictionary

The operator’s default value, if one exists

Note

A task must include or inherit the arguments task_id and owner, otherwise Airflow will raise an exception. A fresh install of Airflow will have a default value of ‘airflow’ set for owner, so you only really need to worry about ensuring task_id has a value.

Templating with Jinja
Airflow leverages the power of Jinja Templating and provides the pipeline author with a set of built-in parameters and macros. Airflow also provides hooks for the pipeline author to define their own parameters, macros and templates.

This tutorial barely scratches the surface of what you can do with templating in Airflow, but the goal of this section is to let you know this feature exists, get you familiar with double curly brackets, and point to the most common template variable: {{ ds }} (today’s “date stamp”).

airflow/example_dags/tutorial.py
[source]

templated_command = textwrap.dedent(
    """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
{% endfor %}
"""
)

t3 = BashOperator(
    task_id="templated",
    depends_on_past=False,
    bash_command=templated_command,
)
Notice that the templated_command contains code logic in {% %} blocks, references parameters like {{ ds }}, and calls a function as in {{ macros.ds_add(ds, 7)}}.

Files can also be passed to the bash_command argument, like bash_command='templated_command.sh', where the file location is relative to the directory containing the pipeline file (tutorial.py in this case). This may be desirable for many reasons, like separating your script’s logic and pipeline code, allowing for proper code highlighting in files composed in different languages, and general flexibility in structuring pipelines. It is also possible to define your template_searchpath as pointing to any folder locations in the DAG constructor call.

Using that same DAG constructor call, it is possible to define user_defined_macros which allow you to specify your own variables. For example, passing dict(foo='bar') to this argument allows you to use {{ foo }} in your templates. Moreover, specifying user_defined_filters allows you to register your own filters. For example, passing dict(hello=lambda name: 'Hello %s' % name) to this argument allows you to use {{ 'world' | hello }} in your templates. For more information regarding custom filters have a look at the Jinja Documentation.

For more information on the variables and macros that can be referenced in templates, make sure to read through the Templates reference.

Adding DAG and Tasks documentation
We can add documentation for DAG or each single task. DAG documentation only supports markdown so far, while task documentation supports plain text, markdown, reStructuredText, json, and yaml. The DAG documentation can be written as a doc string at the beginning of the DAG file (recommended), or anywhere else in the file. Below you can find some examples on how to implement task and DAG docs, as well as screenshots:

airflow/example_dags/tutorial.py
[source]

t1.doc_md = textwrap.dedent(
    """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](https://imgs.xkcd.com/comics/fixing_problems.png)
**Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
"""
)

dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
dag.doc_md = """
This is a documentation placed anywhere
"""  # otherwise, type it like this
../_images/task_doc.png ../_images/dag_doc.png
Setting up Dependencies
We have tasks t1, t2 and t3 that depend on each other. Here’s a few ways you can define dependencies between them:

t1.set_downstream(t2)

# This means that t2 will depend on t1
# running successfully to run.
# It is equivalent to:
t2.set_upstream(t1)

# The bit shift operator can also be
# used to chain operations:
t1 >> t2

# And the upstream dependency with the
# bit shift operator:
t2 << t1

# Chaining multiple dependencies becomes
# concise with the bit shift operator:
t1 >> t2 >> t3

# A list of tasks can also be set as
# dependencies. These operations
# all have the same effect:
t1.set_downstream([t2, t3])
t1 >> [t2, t3]
[t2, t3] << t1
Note that when executing your script, Airflow will raise exceptions when it finds cycles in your DAG or when a dependency is referenced more than once.

Using time zones
Creating a time zone aware DAG is quite simple. Just make sure to supply a time zone aware dates using pendulum. Don’t try to use standard library timezone as they are known to have limitations and we deliberately disallow using them in DAGs.

Recap
Alright, so we have a pretty basic DAG. At this point your code should look something like this:

airflow/example_dags/tutorial.py
[source]


import textwrap
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
with DAG(
    "tutorial",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    t1.doc_md = textwrap.dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](https://imgs.xkcd.com/comics/fixing_problems.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = textwrap.dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    t1 >> [t2, t3]
Testing
Running the Script
Time to run some tests. First, let’s make sure the pipeline is parsed successfully.

Let’s assume we are saving the code from the previous step in tutorial.py in the DAGs folder referenced in your airflow.cfg. The default location for your DAGs is ~/airflow/dags.

python ~/airflow/dags/tutorial.py
If the script does not raise an exception it means that you have not done anything horribly wrong, and that your Airflow environment is somewhat sound.

Command Line Metadata Validation
Let’s run a few commands to validate this script further.

# initialize the database tables
airflow db migrate

# print the list of active DAGs
airflow dags list

# prints the list of tasks in the "tutorial" DAG
airflow tasks list tutorial

# prints the hierarchy of tasks in the "tutorial" DAG
airflow tasks list tutorial --tree
Testing
Let’s test by running the actual task instances for a specific date. The date specified in this context is called the logical date (also called execution date for historical reasons), which simulates the scheduler running your task or DAG for a specific date and time, even though it physically will run now (or as soon as its dependencies are met).

We said the scheduler runs your task for a specific date and time, not at. This is because each run of a DAG conceptually represents not a specific date and time, but an interval between two times, called a data interval. A DAG run’s logical date is the start of its data interval.

# command layout: command subcommand [dag_id] [task_id] [(optional) date]

# testing print_date
airflow tasks test tutorial print_date 2015-06-01

# testing sleep
airflow tasks test tutorial sleep 2015-06-01
Now remember what we did with templating earlier? See how this template gets rendered and executed by running this command:

# testing templated
airflow tasks test tutorial templated 2015-06-01
This should result in displaying a verbose log of events and ultimately running your bash command and printing the result.

Note that the airflow tasks test command runs task instances locally, outputs their log to stdout (on screen), does not bother with dependencies, and does not communicate state (running, success, failed, …) to the database. It simply allows testing a single task instance.

The same applies to airflow dags test, but on a DAG level. It performs a single DAG run of the given DAG id. While it does take task dependencies into account, no state is registered in the database. It is convenient for locally testing a full run of your DAG, given that e.g. if one of your tasks expects data at some location, it is available.

Backfill
Everything looks like it’s running fine so let’s run a backfill. backfill will respect your dependencies, emit logs into files and talk to the database to record status. If you do have a webserver up, you will be able to track the progress. airflow webserver will start a web server if you are interested in tracking the progress visually as your backfill progresses.

Note that if you use depends_on_past=True, individual task instances will depend on the success of their previous task instance (that is, previous according to the logical date). Task instances with their logical dates equal to start_date will disregard this dependency because there would be no past task instances created for them.

You may also want to consider wait_for_downstream=True when using depends_on_past=True. While depends_on_past=True causes a task instance to depend on the success of its previous task_instance, wait_for_downstream=True will cause a task instance to also wait for all task instances immediately downstream of the previous task instance to succeed.

The date range in this context is a start_date and optionally an end_date, which are used to populate the run schedule with task instances from this DAG.

# optional, start a web server in debug mode in the background
# airflow webserver --debug &

# start your backfill on a date range
airflow dags backfill tutorial \
    --start-date 2015-06-01 \
    --end-date 2015-06-07
What’s Next?
That’s it! You have written, tested and backfilled your very first Airflow pipeline. Merging your code into a repository that has a Scheduler running against it should result in being triggered and run every day.

Here are a few things you might want to do next:

See also

Continue to the next step of the tutorial: Working with TaskFlow

Skip to the Core Concepts section for detailed explanation of Airflow concepts such as DAGs, Tasks, Operators, and more
How-to Guides
Setting up the sandbox in the Quick Start section was easy; building a production-grade environment requires a bit more work!

These how-to guides will step you through common tasks in using and configuring an Airflow environment.

Using the CLI
Set Up Bash/Zsh Completion
Creating a Connection
Exporting DAG structure as an image
Display DAGs structure
Formatting commands output
Purge history from metadata database
Export the purged records from the archive tables
Dropping the archived tables
Upgrading Airflow
Downgrading Airflow
Exporting Connections
Testing for DAG Import Errors
Add tags to DAGs and use it for filtering in the UI
Add Owner Links to DAG
Creating a notifier
Using a notifier
Setting Configuration Options
Configuring local settings
Configuring Flask Application for Airflow Webserver
Set up a Database Backend
Choosing database backend
Database URI
Setting up a SQLite Database
Setting up a PostgreSQL Database
Setting up a MySQL Database
MsSQL Database
Other configuration options
Initialize the database
Database Monitoring and Maintenance in Airflow
What’s next?
Using Operators
BashOperator
BashSensor
BranchDateTimeOperator
FileSensor
PythonOperator
PythonVirtualenvOperator
ExternalPythonOperator
PythonBranchOperator
BranchPythonVirtualenvOperator
BranchExternalPythonOperator
ShortCircuitOperator
PythonSensor
TimeDeltaSensor
TimeDeltaSensorAsync
TimeSensor
TimeSensorAsync
BranchDayOfWeekOperator
DayOfWeekSensor
Cross-DAG Dependencies
Customizing DAG Scheduling with Timetables
Timetable Registration
Define Scheduling Logic
Parameterized Timetables
Timetable Display in UI
Timetable Description Display in UI
Changing generated run_id
Customize view of Apache from Airflow web UI
Custom view Registration
Listener Plugin of Airflow
Listener Registration
Customizing the UI
Customizing state colours
Customizing DAG UI Header and Airflow Page Titles
Add custom alert messages on the dashboard
Creating a custom Operator
Hooks
User interface
Templating
Define an operator extra link
Sensors
Creating Custom @task Decorators
(Optional) Adding IDE auto-completion support
Export dynamic environment variables available for operators to use
Managing Connections
Storing connections in environment variables
Storing connections in a Secrets Backend
Storing connections in the database
Custom connection fields
URI format
Managing Variables
Storing Variables in Environment Variables
Securing Variables
Setup and Teardown
How setup and teardown works
Basic usage
Setup “scope”
Implicit ALL_SUCCESS constraint
Controlling dag run state
Authoring with task groups
Running setups and teardowns in parallel
Trigger rule behavior for teardowns
Running Airflow behind a reverse proxy
Running Airflow with systemd
Define an operator extra link
Add or override Links to Existing Operators
Email Configuration
Send email using SendGrid
Send email using AWS SES
Dynamic DAG Generation
Dynamic DAGs with environment variables
Generating Python code with embedded meta-data
Dynamic DAGs with external configuration from a structured data file
Registering dynamic DAGs
Running Airflow in Docker
Before you begin
Fetching docker-compose.yaml
Initializing Environment
Cleaning-up the environment
Running Airflow
Accessing the environment
Cleaning up
Using custom images
Special case - adding dependencies via requirements.txt file
Special case - Adding a custom config file
Networking
Debug Airflow inside docker container using PyCharm
FAQ: Frequently asked questions
What’s Next?
Environment variables supported by Docker Compose
Upgrading from 1.10 to 2
Step 1: Switch to Python 3
Step 2: Upgrade to 1.10.15
Step 3: Run the Upgrade check scripts
Step 4: Switch to Backport Providers
Step 5: Upgrade Airflow DAGs
Step 6: Upgrade Configuration settings
Step 7: Upgrade to Airflow 2
Appendix

Installing Apache Airflow with Docker
Install Docker Compose:

Install the Docker Compose plugin using the following commands:
bash
Copy
Edit
sudo curl -L "https://github.com/docker/compose/releases/download/v2.9.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
Check the installation:
bash
Copy
Edit
docker-compose --version
Download Docker Compose YAML File for Airflow:

Use this command to download the docker-compose.yaml for Apache Airflow:
bash
Copy
Edit
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'
The file includes several services:
airflow-scheduler: Manages tasks and dependencies.
airflow-webserver: Provides a local web interface (http://localhost:8080).
airflow-worker: Executes tasks as directed by the scheduler.
airflow-init: Initializes accounts and databases.
postgres: Database service.
redis: Facilitates communication between scheduler and worker.
Customize Docker Compose File (Optional):

If you want to customize the Airflow image, update the YAML file:
yaml
Copy
Edit
image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:latest}
Prepare the Environment:

Create necessary directories and environment variables:
bash
Copy
Edit
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
Initialize Airflow:

Run the initialization to set up the database and accounts:
bash
Copy
Edit
docker-compose up airflow-init
Run Airflow:

Start the Airflow container:
bash
Copy
Edit
docker-compose up
Accessing Airflow:

You can use the Airflow system in three ways:
CLI: Interact with Airflow from the command line.
Web Interface: Access the web UI at http://localhost:8080 (default credentials: airflow / airflow).
RestAPI: Use curl or Postman to interact with the Airflow API.
Stop and Remove Containers:

To clean up after testing, you can remove containers and images:
bash
Copy
Edit
docker-compose down --volumes --rmi all
DAGs (Directed Acyclic Graphs)
What is a DAG?:

A DAG defines the sequence of tasks and their dependencies. It ensures that tasks run in the correct order.
DAG Declaration Methods:

Context Manager:
Wrap the code using with DAG().
python
Copy
Edit
with DAG("my_dag", start_date=pendulum.datetime(2021, 1, 1, tz="UTC")) as dag:
    op = EmptyOperator(task_id="task")
Standard Constructor:
Create a DAG instance explicitly:
python
Copy
Edit
my_dag = DAG("my_dag", start_date=pendulum.datetime(2021, 1, 1, tz="UTC"))
op = EmptyOperator(task_id="task", dag=my_dag)
Decorator:
The preferred method, especially in Airflow 2.x:
python
Copy
Edit
@dag(start_date=pendulum.datetime(2021, 1, 1, tz="UTC"))
def generate_dag():
    op = EmptyOperator(task_id="task")
TaskFlow API:

A simpler method of writing tasks and DAGs. It uses the @task decorator for each task, making the code cleaner and more readable.
Example:
python
Copy
Edit
@dag(start_date=pendulum.datetime(2021, 1, 1, tz="UTC"))
def tutorial_etl():
    @task()
    def extract():
        return {"data": 100}
    @task()
    def transform(data):
        return data * 2
    @task()
    def load(data):
        print(data)

    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
