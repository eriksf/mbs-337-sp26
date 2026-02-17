Docker Compose
==============

Up to this point, we have been looking at single-container applications - small
units of code that are containerized, executed *ad hoc* to generate or read a
JSON file, then exit on completion. But what if we want to do something more
complex? For example, what if our goal is to orchestrate a multi-container
application consisting of, e.g., a Flask app, a database, a message queue, an
authentication service, and more.

**Docker compose** is a tool for managing multi-container applications. A YAML
file is used to define all of the application service, and a few simple commands
can be used to spin up or tear down all of the services.

In this module, we will get a first look at Docker compose. After going
through this module, students should be able to:

* Translate Docker run commands into YAML files for Docker compose
* Run commands inside *ad hoc* containers using Docker compose
* Manage small software systems composed of more than one script, and more than
  one container
* Copy data into and out of containers as needed


Another Tool, Another Container
-------------------------------

We have been working a lot with a script for reading in and summarizing a
FASTQ file and outputting a summary JSON file. The input to that file has been a small
sample FASTQ file. Instead, let's create a container that actually downloads FASTQ files from the
`NCBI Sequence Read Archive (SRA) <https://www.ncbi.nlm.nih.gov/sra/>`_. Fortunately for us,
there is a set of command line tools created by NCBI called
`sra-tools <https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit>`_ that can be used
to download FASTQ files from the SRA and they have already created a container that is published on
`Docker Hub <https://hub.docker.com/r/ncbi/sra-tools>`_! 

.. figure:: images/docker_hub_sra_tools.png
   :width: 600
   :align: center

   NCBI sra-tools container at Docker hub.

So, let's pull that container and use it to download a FASTQ file.

.. code-block:: console

   [mbs337-vm]$ docker pull ncbi/sra-tools:3.3.0
   3.3.0: Pulling from ncbi/sra-tools
   2d35ebdb57d9: Pull complete
   9c0db82dbf54: Pull complete
   a0e62295a7bb: Pull complete
   192a2de187a1: Pull complete
   Digest: sha256:2bcbd43672de26d93b11eef713241a61bd60fd74bb9775a2511972f0467677f2
   Status: Downloaded newer image for ncbi/sra-tools:3.3.0
   docker.io/ncbi/sra-tools:3.3.0
   [mbs337-vm]$ docker images
   REPOSITORY                                                      TAG       IMAGE ID       CREATED         SIZE
   eriksf/fastq_summary                                            1.0       9ccdd4b5eaf2   3 hours ago     1.24GB
   python                                                          3.12      ac67f52b7509   13 days ago     1.11GB
   python                                                          latest    9a7c5808942d   13 days ago     1.12GB
   ncbi/sra-tools                                                  3.3.0     2e0e3109402b   2 months ago    174MB
   registry.gitlab.com/exosphere/exosphere/guacamole/guacd         latest    b87c151e82aa   12 months ago   241MB
   registry.gitlab.com/exosphere/exosphere/guacamole/guacamole     latest    37a59d9ff144   12 months ago   511MB
   registry.gitlab.com/exosphere/exosphere/containrrr/watchtower   latest    e7dd50d07b86   2 years ago     14.7MB

The standard way to use sra-tools to download and convert data from SRA is to first use the ``prefetch``
command to download the SRA file into NCBI's native format, ``.sra``, and then use the ``fasterq-dump`` or
``fastq-dump`` command to convert the SRA file into FASTQ format. So, let's make sure that those tools are
available in the container.

.. code-block:: console

   [mbs337-vm]$ docker run --rm ncbi/sra-tools:3.3.0 which prefetch
   /usr/local/bin/prefetch
   [mbs337-vm]$ docker run --rm ncbi/sra-tools:3.3.0 which fasterq-dump
   /usr/local/bin/fasterq-dump
   [mbs337-vm]$ docker run --rm ncbi/sra-tools:3.3.0 which fastq-dump
   /usr/local/bin/fastq-dump

We'll use SRA accession number `SRR1553607 <https://www.ncbi.nlm.nih.gov/sra/?term=SRR1553607>`_ which is a run
from a genome sequencing experiment on Zaire ebolavirus from a 2014 outbreak in Sierra Leone on the
Illumina HiSeq 2500 and will generate a small FASTQ file that we can use for testing.

.. figure:: images/SRR1553607_from_SRA.png
   :width: 600
   :align: center

   Run SRR1553607 from the SRA.

Now let's do a test download of this data using the sra-tools container. Instead of using the ``prefetch``
and ``fasterq-dump`` commands separately, we're going to use just the ``fastq-dump`` command with the
``--split-files`` flag to separate the paired-end reads into separate FASTQ files and the ``-X`` flag
to limit the number of reads. For example:

.. code-block:: console

   [mbs337-vm]$ docker run --rm -v $PWD:/data -u $(id -u):$(id -g) ncbi/sra-tools:3.3.0 fastq-dump --split-files -X 1000 -O /data SRR1553607
   Read 1000 spots for SRR1553607
   Written 1000 spots for SRR1553607
   [mbs337-vm]$ ls -l
   total 568
   -rw-rw-r-- 1 ubuntu ubuntu    155 Feb 17 18:11 Dockerfile
   -rw-r--r-- 1 ubuntu ubuntu 265572 Feb 17 22:13 SRR1553607_1.fastq
   -rw-r--r-- 1 ubuntu ubuntu 265572 Feb 17 22:13 SRR1553607_2.fastq
   drwxr-xr-x 2 root   root     4096 Feb 17 18:00 __pycache__
   -rw-r--r-- 1 ubuntu ubuntu  10801 Feb 17 21:15 fastq_summary.json
   -rwxrwxr-x 1 ubuntu ubuntu   4241 Feb 17 17:50 fastq_summary.py
   -rw-rw-r-- 1 ubuntu ubuntu    199 Feb 17 17:50 models.py
   -rw-rw-r-- 1 ubuntu ubuntu  14443 Feb 17 17:50 raw_reads.fastq

.. note::

   To reiterate, because we mounted our current location as a folder called "/data"
   (``-v $PWD:/data``), and we made sure to write the output file to that location in
   the container (``fastq-dump -O /data``), then we get to keep the file
   after the container exits, and it shows up in our current location (``$PWD``). Also,
   because we used the ``-u`` flag to specify our user and group ID namespace, the new
   files are owned by us instead of root.

EXERCISE
~~~~~~~~

Spend a few minutes testing both containers. Be sure you can generate data with
one container, then read in and analyze the same data with the other. Data needs
to persist outside the containers in order to do this.



Write a Compose File
--------------------

Docker compose works by interpreting rules declared in a YAML file (typically
called ``docker-compose.yml``). The rules we will write will replace the
``docker run`` commands we have been using, and which have been growing quite
complex. For example, the commands we used to run our JSON parsing scripts in a
container looked like the following:

.. code-block:: console

   [coe332-vm]$ docker run --rm -v $PWD:/data -u $(id -u):$(id -g) username/gen_ml_data:1.0 gen_ml_data.py /data/ml.json
   [coe332-vm]$ docker run --rm -v $PWD/ml.json:/data/ml.json username/ml_data_analysis:1.0 ml_data_analysis.py /data/ml.json

The above ``docker run`` commands can be loosely translated into a YAML file.
Navigate to the folder that contains your Python scripts and Dockerfiles, then
create a new empty file called ``docker-compose.yml``:

.. code-block:: console

   [coe332-vm]$ pwd
   /home/ubuntu/coe-332/docker-exercise
   [coe332-vm]$ touch docker-compose.yml
   [coe332-vm]$ ls
   docker-compose.yml  Dockerfile-analysis  Dockerfile-gen  gen_ml_data.py  ml_data_analysis.py  data/


Next, open up ``docker-compose.yml`` with your favorite text editor and type /
paste in the following text:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 9,12,18

   ---
   services:
       gen-data:
           build:
               context: ./
               dockerfile: ./Dockerfile-gen
           image: username/gen_ml_data:1.0
           volumes:
               - ./data:/data
           user: "1000:1000"
           command: gen_ml_data.py /data/ml.json
       analyze-data:
           build:
               context: ./
               dockerfile: ./Dockerfile-analysis
           depends_on:
               - gen-data
           image: username/ml_data_analysis:1.0
           volumes:
               - ./data:/data
           command: ml_data_analysis.py /data/ml.json

.. warning::

   The highlighted lines above may need to be edited with your username / userid /
   groupid in order for this to work. See instructions below.

The ``services`` section defines the configuration of individual container
instances that we want to orchestrate. In our case, we define two called
``gen-data`` for the gen_ml_data functionality, and ``analyze-data`` for
the ml_data_analysis functionality.

Each of those services is configured with its own Docker image,
a mounted volume (equivalent to the ``-v`` option for ``docker run``), a user
namespace (equivalent to the ``-u`` option for ``docker run``), and a default
command to run.

Please note that the image name above should be changed to use your image. Also,
the user ID / group ID are specific to ``ubuntu`` - to find your user and group
ID, execute the Linux commands ``id -u`` and ``id -g``.

.. note::

   The top-level ``services`` keyword shown above is just one important part of
   Docker compose. Later in this course we will look at named volumes and
   networks which can be configured and created with Docker compose.


Running Docker Compose
----------------------

The Docker compose command line tool follows the same syntax as other Docker
commands:

.. code-block:: console

   docker compose <verb> <parameters>

Just like Docker, you can pass the ``--help`` flag to ``docker compose`` or to
any of the verbs to get additional usage information. To get started on the
command line tools, try issuing the following two commands:

.. code-block:: console

   [coe332-vm]$ docker compose version
   [coe332-vm]$ docker compose config

The first command prints the version of Docker compose installed, and the second
searches your current directory for ``docker-compose.yml`` and checks that it
contains only valid syntax.

To run one of these services, use the ``docker compose run`` verb, and pass the
name of the service as defined in your YAML file:

.. code-block:: console

   [coe332-vm]$ ls test/     # currently empty
   [coe332-vm]$ docker compose run gen-data
   Data written to /data/ml.json!
   [coe332-vm]$ ls test/
   ml.json               # new file!
   [coe332-vm]$ docker compose run analyze-data
   6004.5
   Southern & Eastern
   ... etc.


Now we have an easy way to run our *ad hoc* services consistently and
reproducibly. Not only does ``docker-compose.yml`` make it easier to run our
services, it also represents a record of how we intend to interact with this
container.



Essential Docker Compose Command Summary
----------------------------------------

+------------------------+------------------------------------------------+
| Command                | Usage                                          |
+========================+================================================+
| docker compose version | Print version information                      |
+------------------------+------------------------------------------------+
| docker compose config  | Validate docker-compose.yml syntax             |
+------------------------+------------------------------------------------+
| docker compose up      | Spin up all services                           |
+------------------------+------------------------------------------------+
| docker compose down    | Tear down all services                         |
+------------------------+------------------------------------------------+
| docker compose build   | Build the images listed in the YAML file       |
+------------------------+------------------------------------------------+
| docker compose run     | Run a container as defined in the YAML file    |
+------------------------+------------------------------------------------+


Additional Resources
--------------------

* `Docker Compose Docs <https://docs.docker.com/compose/>`_
