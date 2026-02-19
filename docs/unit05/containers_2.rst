Advanced Containers
===================

In the first part, we pulled and ran existing container images from Docker Hub.
In this section, we will build an image from scratch for running some of our own
Python3 code. Then, we will push that image back up to Docker Hub so others may
find and use it. After going through this module, students should be able to:

* Install and test code in a container interactively
* Write a Dockerfile from scratch
* Build a Docker image from a Dockerfile
* Push a Docker image to Docker Hub
* Volume mount external data inside a Docker container
* **Design Principles:** Containers contribute to the portability of software projects


Getting Set Up
--------------

*Scenario:* You are a researcher who has written some code for reading and
summarizing FASTQ files and outputting the data in JSON format. You now want to distribute that
code for others to use in what you know to be a stable production environment
(including OS and dependency versions). End users may want to use this application
on their local workstations, in the cloud, or on an HPC cluster.


The first step in a typical container development workflow entails installing
and testing an application interactively within a running Docker container.

.. note::

   We recommend doing this on your VMs. But, one of the most
   important features of Docker is that it is platform agnostic. These steps
   could be done anywhere Docker is installed.


To begin, make a new folder for this work and prepare to gather some important
files.


.. code-block:: console

   [mbs337-vm]$ mkdir -p mbs-337/docker-exercise/
   [mbs337-vm]$ cd mbs-337/docker-exercise/
   [mbs337-vm]$ pwd
   /home/ubuntu/mbs-337/docker-exercise

Specifically, you need your ``fastq_summary.py`` and ``models.py`` scripts and the input data
file called ``raw_reads.fastq``. You can make copies of your own, or
download sample copies from the links below. You also need a ``Dockerfile``, and
we can just make an empty one with no contents for now.

.. code-block:: console

   [mbs337-vm]$ pwd
   /home/ubuntu/mbs-337/docker-exercise
   [mbs337-vm]$ touch Dockerfile
   [mbs337-vm]$ wget https://raw.githubusercontent.com/tacc/mbs-337-sp26/main/docs/unit03/sample-data/raw_reads.fastq
   [mbs337-vm]$ wget https://raw.githubusercontent.com/tacc/mbs-337-sp26/main/docs/unit05/scripts/fastq_summary.py
   [mbs337-vm]$ wget https://raw.githubusercontent.com/tacc/mbs-337-sp26/main/docs/unit05/scripts/models.py
   [mbs337-vm]$ ls
   Dockerfile  fastq_summary.py  models.py  raw_reads.fastq

.. warning::

   It is important to carefully consider what files and folders are in the same
   ``PATH`` as a Dockerfile (known as the 'build context'). The ``docker build``
   process will index and send all files and folders in the same directory as
   the Dockerfile to the Docker daemon, so take care not to ``docker build`` at
   a root level.


Containerize Code Interactively
-------------------------------

There are several questions you must ask yourself when preparing to containerize
code for the first time:

1. What is an appropriate base image?
2. What dependencies are required for my program?
3. What is the installation process for my program?
4. What environment variables may be important?

We can work through these questions by performing an **interactive installation**
of our Python script. Our development environment (e.g. the Jetstream VM)
is a Linux server running Ubuntu 24.04 and Python 3.12. We know our code works there,
so that is how we will containerize it. Use ``docker run`` to interactively attach to a fresh
`Python 3.12 container <https://hub.docker.com/_/python/tags?name=3.12>`_.

.. code-block:: console

   [mbs337-vm]$ docker run --rm -it -v $PWD:/code python:3.12 /bin/bash
   root@8f029d530d0e:/#

Here is an explanation of the options:

.. code-block:: text

   docker run       # run a container
   --rm             # remove the container on exit
   -it              # interactively attach terminal to inside of container
   -v $PWD:/code    # mount the current directory to /code
   python:3.12      # image and tag from Docker Hub
   /bin/bash        # shell to start inside container


The command prompt will change, signaling you are now 'inside' the container.
And, new to this example, we are using the ``-v`` flag which mounts the contents
of our current directory (``$PWD``) inside the container in a folder in the root
directory called (``/code``).


Check for and Install Necessary Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first thing we will typically do is check if our dependenices are available
in the container. If they are not available, we will use a package manager to
install them. To run our FASTQ summarizing code, we just need Python3 and
a few simple Python libraries.

.. code-block:: console

   root@8f029d530d0e:/# which python3
   /usr/local/bin/python3
   root@8f029d530d0e:/# python3 --version
   Python 3.12.12

Python3 is available in this container (as expected). But what about the ``biopython`` and ``pydantic``
libraries? Run ``pip3 list`` in your terminal and you will see output like the following:

.. code-block:: console

   root@8f029d530d0e:/# pip3 list
   Package Version
   ------- -------
   pip     25.0.1

We can see that the libraries are not installed in this (or any) python base image by default. Let's
install them in our container just as we did at the beginning of the course.

.. code-block:: console

   root@8f029d530d0e:/# pip3 install biopython pydantic
   root@8f029d530d0e:/# pip3 list
   Package           Version
   ----------------- -------
   annotated-types   0.7.0
   biopython         1.86
   numpy             2.4.2
   pip               25.0.1
   pydantic          2.12.5
   pydantic_core     2.41.5
   typing_extensions 4.15.0
   typing-inspection 0.4.2

Now that we have set up the container with the same packages as our VM, Let's run
our fastq_summary.py script and see if it works:

.. code-block:: console

   root@8f029d530d0e:/# cd /code
   root@8f029d530d0e:/code# python3 fastq_summary.py --help
   usage: fastq_summary.py [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] -f FASTQFILE [-e {fastq-sanger,fastq-solexa,fastq-illumina}]
                           [-o OUTPUT]

   Summarize FASTQ file and output JSON summary

   options:
     -h, --help            show this help message and exit
     -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                           Set the logging level (default: WARNING)
     -f FASTQFILE, --fastqfile FASTQFILE
                           The path to the input FASTQ file
     -e {fastq-sanger,fastq-solexa,fastq-illumina}, --encoding {fastq-sanger,fastq-solexa,fastq-illumina}
                           The FASTQ encoding format (default: fastq-sanger)
     -o OUTPUT, --output OUTPUT
                           The path to the output JSON file (default: fastq_summary.json)
   root@8f029d530d0e:/code# python3 fastq_summary.py -l INFO f raw_reads.fastq
   [2026-02-15 21:18:25,637 3081fb2d9615] fastq_summary.main:117 - INFO - Starting FASTQ summary workflow
   [2026-02-15 21:18:25,637 3081fb2d9615] fastq_summary.summarize_fastq_file:90 - INFO - Reading FASTQ file 'raw_reads.fastq'
   [2026-02-15 21:18:25,639 3081fb2d9615] fastq_summary.summarize_fastq_file:97 - INFO - Finished reading 40 reads
   [2026-02-15 21:18:25,639 3081fb2d9615] fastq_summary.write_summary_to_json:111 - INFO - Writing summary to 'fastq_summary.json'
   [2026-02-15 21:18:25,640 3081fb2d9615] fastq_summary.write_summary_to_json:114 - INFO - Finished writing 'fastq_summary.json'
   [2026-02-15 21:18:25,640 3081fb2d9615] fastq_summary.main:126 - INFO - FASTQ summary workflow complete
   root@8f029d530d0e:/code# ls
   Dockerfile  __pycache__  fastq_summary.json  fastq_summary.py  models.py  raw_reads.fastq

It works!

.. warning::

   An important question to ask is: Does the versions of Python and other
   dependencies match the versions you are developing with in your local
   environment? If not, make sure to install the correct version of Python.


We now have functional versions of our script 'installed' in this container.
Now would be a good time to execute the `history` command to see a record of the
build process. When you are ready, type `exit` to exit the container and we can
start writing these build steps into a Dockerfile.


Assemble a Dockerfile
---------------------

After going through the build process interactively, we can translate our build
steps into a Dockerfile using the directives described below. Open up your copy
of ``Dockerfile`` with a text editor and enter the following:


The FROM Instruction
~~~~~~~~~~~~~~~~~~~~

We can use the FROM instruction to start our new image from a known base image.
This should be the first line of our Dockerfile. In our scenario, we want to
match our development environment with Python3.12. We know our code works in
that environment, so that is how we will containerize it for others to use:

.. code-block:: dockerfile

   FROM python:3.12

Base images typically take the form `os:version`. Avoid using the '`latest`'
version; it is hard to track where it came from and the identity of '`latest`'
can change.

.. tip::

   Browse `Docker Hub <https://hub.docker.com/>`_ to discover other potentially
   useful base images. Keep an eye out for the 'Official Image' badge.


The RUN Instruction
~~~~~~~~~~~~~~~~~~~

We can install updates, install new software, or download code to our image by
running commands with the RUN instruction. In our case, our dependencies
were Python3 (built into our base image), ``pydantic``, and ``biopython``. So, we will use a RUN instruction to
install anything that is missing.

.. code-block:: dockerfile

   RUN pip3 install biopython pydantic


Each RUN instruction creates an intermediate image (called a 'layer'). Too many
layers makes the Docker image less performant, and makes building less
efficient. We can minimize the number of layers by combining RUN instructions.
Dependencies that are more likely to change over time (e.g. Python3 libraries)
still might be better off in in their own RUN instruction in order to save time
building later on.



The COPY Instruction
~~~~~~~~~~~~~~~~~~~~

There are a couple different ways to get your source code inside the image. One
way is to use a RUN instruction with ``wget`` to pull your code from the web.
When you are developing, however, it is usually more practical to copy code in
from the Docker build context using the COPY instruction. For example, we can
copy our script to the root-level ``/code`` directory with the following
instructions:

.. code-block:: dockerfile

   COPY fastq_summary.py /code/fastq_summary.py

   COPY models.py /code/models.py

The ENV Instruction
~~~~~~~~~~~~~~~~~~~

Another useful instruction is the ENV instruction. This allows the image
developer to set environment variables inside the container runtime. In our
interactive build, we added the ``/code`` folder to the ``PATH``. We can do this
with ENV instructions as follows:

.. code-block:: dockerfile

   ENV PATH="/code:$PATH"



Putting It All Together
~~~~~~~~~~~~~~~~~~~~~~~

The contents of the final Dockerfile should look like:

.. code-block:: dockerfile
   :linenos:

   FROM python:3.12

   RUN pip3 install biopython pydantic

   COPY fastq_summary.py /code/fastq_summary.py

   COPY models.py /code/models.py

   ENV PATH="/code:$PATH"


Build the Image
---------------

Once the Dockerfile is written and we are satisfied that we have minimized the
number of layers, the next step is to build an image. Building a Docker image
generally takes the form:

.. code-block:: console

   [mbs337-vm]$ docker build -t <dockerhubusername>/<code>:<version> ./

The ``-t`` flag is used to name or 'tag' the image with a descriptive name and
version. Optionally, you can preface the tag with your **Docker Hub username**.
Adding that namespace allows you to push your image to a public registry and
share it with others. The trailing dot '``.``' in the line above simply
indicates the location of the Dockerfile (a single '``.``' means 'the current
directory').

To build the image, use:

.. code-block:: console

   [mbs337-vm]$ docker build -t username/fastq_summary:1.0 ./

.. note::

   Don't forget to replace 'username' with your Docker Hub username.


Use ``docker images`` to ensure you see a copy of your image has been built. You can
also use `docker inspect` to find out more information about the image.

.. code-block:: console

   [mbs337-vm]$ docker images
   REPOSITORY                                                      TAG       IMAGE ID       CREATED              SIZE
   eriksf/fastq_summary                                            1.0       6743d1e0807f   About a minute ago   1.24GB
   ...

.. code-block:: console

   [mbs337-vm]$ docker inspect username/fastq_summary:1.0


If you need to rename your image, you can either re-tag it with ``docker tag``, or
you can remove it with ``docker rmi`` and build it again. Issue each of the
commands on an empty command line to find out usage information.



Test the Image
--------------

We can test a newly-built image two ways: interactively and non-interactively.
In interactive testing, we will use ``docker run`` to start a shell inside the
image, just like we did when we were building it interactively. The difference
this time is that we are NOT mounting the code inside with the ``-v`` flag,
because the code is already in the container:

.. code-block:: console

   [mbs337-vm]$ docker run --rm -it username/fastq_summary:1.0 /bin/bash

   root@d8a3afd0fc61:/# fastq_summary.py -l INFO -f raw_reads.fastq
   [2026-02-15 21:52:20,816 d8a3afd0fc61] fastq_summary.main:117 - INFO - Starting FASTQ summary workflow
   [2026-02-15 21:52:20,816 d8a3afd0fc61] fastq_summary.summarize_fastq_file:90 - INFO - Reading FASTQ file 'raw_reads.fastq'
   [2026-02-15 21:52:20,817 d8a3afd0fc61] fastq_summary.main:123 - ERROR - Input FASTQ file 'raw_reads.fastq' not found. Exiting.


Here is an explanation of the options:

.. code-block:: text

   docker run      # run a container
   --rm            # remove the container when we exit
   -it             # interactively attach terminal to inside of container
   username/...    # image and tag on local machine
   /bin/bash       # shell to start inside container


Uh oh! We forgot about ``raw_reads.fastq``! We get an error message that we caught
when checking for the FASTQ file. This is because we did not (1) copy the FASTQ file into the container
at build time, nor did we (2) copy the FASTQ file into the container at run
time.

We should pause at this moment to think about how we want to distribute this
application. Should the data be encapsulated within? Or should we expect potential
users to be bring their own data for analysis?

Let's try again, but this time mount the data inside the container so we can
access it. If we mount the current folder as, e.g., ``/data``, then everything
in the current folder will be available. In addition, if we write any new files
inside the container to ``/data``, those will be preserved and persist outside
the container once it stops.

.. code-block:: console

   [mbs337-vm]$ docker run --rm -it -v $PWD:/data username/fastq_summary:1.0 /bin/bash
   ...
   root@dc0d6bf1875c:/# pwd
   /
   root@dc0d6bf1875c:/# ls /data
   Dockerfile  fastq_summary.py  models.py  raw_reads.fastq
   root@dc0d6bf1875c:/# ls /code
   fastq_summary.py  models.py
   root@dc0d6bf1875c:/# fastq_summary.py -l INFO -f /data/raw_reads.fastq -o /data/fastq_summary.json
   [2026-02-15 22:14:59,674 3ac578d80356] fastq_summary.main:123 - INFO - Starting FASTQ summary workflow
   [2026-02-15 22:14:59,674 3ac578d80356] fastq_summary.summarize_fastq_file:96 - INFO - Reading FASTQ file '/data/raw_reads.fastq'
   [2026-02-15 22:14:59,675 3ac578d80356] fastq_summary.summarize_fastq_file:103 - INFO - Finished reading 40 reads
   [2026-02-15 22:14:59,675 3ac578d80356] fastq_summary.write_summary_to_json:117 - INFO - Writing summary to '/data/fastq_summary.json'
   [2026-02-15 22:14:59,676 3ac578d80356] fastq_summary.write_summary_to_json:120 - INFO - Finished writing '/data/fastq_summary.json'
   [2026-02-15 22:14:59,676 3ac578d80356] fastq_summary.main:132 - INFO - FASTQ summary workflow complete
   root@dc0d6bf1875c:/# ls -l /data
   total 48
   -rw-rw-r-- 1 1000 1000   155 Feb 17 18:11 Dockerfile
   drwxr-xr-x 2 root root  4096 Feb 17 18:00 __pycache__
   -rw-r--r-- 1 root root 10801 Feb 17 20:54 fastq_summary.json
   -rwxrwxr-x 1 1000 1000  4241 Feb 17 17:50 fastq_summary.py
   -rw-rw-r-- 1 1000 1000   199 Feb 17 17:50 models.py
   -rw-rw-r-- 1 1000 1000 14443 Feb 17 17:50 raw_reads.fastq

Alas, there is one more issue to address. The new file is owned by root, simply
because it is root who created the file inside the container. This is one minor
Docker annoyance that we run in to from time to time. The simplest fix is to use
one more ``docker run`` flag (``-u``) to specify the user and group ID namespace
that should be used inside the container.

.. code-block:: console

   root@dc0d6bf1875c:/# rm /data/fastq_summary.json
   root@dc0d6bf1875c:/# exit
   [mbs337-vm]$ docker run --rm -it -v $PWD:/data -u $(id -u):$(id -g) username/fastq_summary:1.0 /bin/bash
   I have no name!@75ee647ed283:/$ fastq_summary.py -l INFO -f /data/raw_reads.fastq -o /data/fastq_summary.json
   [2026-02-17 21:08:51,675 75ee647ed283] fastq_summary.main:122 - INFO - Starting FASTQ summary workflow
   [2026-02-17 21:08:51,675 75ee647ed283] fastq_summary.summarize_fastq_file:95 - INFO - Reading FASTQ file '/data/raw_reads.fastq'
   [2026-02-17 21:08:51,676 75ee647ed283] fastq_summary.summarize_fastq_file:102 - INFO - Finished reading 40 reads
   [2026-02-17 21:08:51,676 75ee647ed283] fastq_summary.write_summary_to_json:116 - INFO - Writing summary to '/data/fastq_summary.json'
   [2026-02-17 21:08:51,677 75ee647ed283] fastq_summary.write_summary_to_json:119 - INFO - Finished writing '/data/fastq_summary.json'
   [2026-02-17 21:08:51,677 75ee647ed283] fastq_summary.main:131 - INFO - FASTQ summary workflow complete
   I have no name!@75ee647ed283:/$ ls -l /data/
   total 48
   -rw-rw-r-- 1 1000 1000   155 Feb 17 18:11 Dockerfile
   drwxr-xr-x 2 root root  4096 Feb 17 18:00 __pycache__
   -rw-r--r-- 1 1000 1000 10801 Feb 17 21:08 fastq_summary.json
   -rwxrwxr-x 1 1000 1000  4241 Feb 17 17:50 fastq_summary.py
   -rw-rw-r-- 1 1000 1000   199 Feb 17 17:50 models.py
   -rw-rw-r-- 1 1000 1000 14443 Feb 17 17:50 raw_reads.fastq
   I have no name!@75ee647ed283:/$ exit
   [mbs337-vm]$ pwd
   /home/ubuntu/mbs-337/docker-exercise
   [mbs337-vm]$ ls -l
   total 48
   -rw-rw-r-- 1 ubuntu ubuntu   155 Feb 17 18:11 Dockerfile
   drwxr-xr-x 2 root   root    4096 Feb 17 18:00 __pycache__
   -rw-r--r-- 1 ubuntu ubuntu 10801 Feb 17 21:08 fastq_summary.json
   -rwxrwxr-x 1 ubuntu ubuntu  4241 Feb 17 17:50 fastq_summary.py
   -rw-rw-r-- 1 ubuntu ubuntu   199 Feb 17 17:50 models.py
   -rw-rw-r-- 1 ubuntu ubuntu 14443 Feb 17 17:50 raw_reads.fastq

Everything looks like it works now! Next, exit the container and test the code
non-interactively. Notice we are calling the container again with ``docker run``,
but instead of specifying an interactive (``-it``) run, we just issue the command
as we want to call it on the command line. Also, notice the return of the ``-v``
flag, because we need to create a volume mount so that our data
(``raw_reads.fastq``) is available inside the container and our JSON output is preserved.

.. code-block:: console

   [mbs337-vm]$ docker run --rm \
                         -v $PWD:/data \
                         -u $(id -u):$(id -g) \
                         username/fastq_summary:1.0 \
                         fastq_summary.py -l INFO -f /data/raw_reads.fastq -o /data/fastq_summary.json
   [2026-02-17 21:15:18,109 01eb956402d6] fastq_summary.main:122 - INFO - Starting FASTQ summary workflow
   [2026-02-17 21:15:18,109 01eb956402d6] fastq_summary.summarize_fastq_file:95 - INFO - Reading FASTQ file '/data/raw_reads.fastq'
   [2026-02-17 21:15:18,110 01eb956402d6] fastq_summary.summarize_fastq_file:102 - INFO - Finished reading 40 reads
   [2026-02-17 21:15:18,110 01eb956402d6] fastq_summary.write_summary_to_json:116 - INFO - Writing summary to '/data/fastq_summary.json'
   [2026-02-17 21:15:18,111 01eb956402d6] fastq_summary.write_summary_to_json:119 - INFO - Finished writing '/data/fastq_summary.json'
   [2026-02-17 21:15:18,111 01eb956402d6] fastq_summary.main:131 - INFO - FASTQ summary workflow complete
   [mbs337-vm]$ pwd
   /home/ubuntu/mbs-337/docker-exercise
   [mbs337-vm]$ ls -l
   total 48
   -rw-rw-r-- 1 ubuntu ubuntu   155 Feb 17 18:11 Dockerfile
   drwxr-xr-x 2 root   root    4096 Feb 17 18:00 __pycache__
   -rw-r--r-- 1 ubuntu ubuntu 10801 Feb 17 21:15 fastq_summary.json
   -rwxrwxr-x 1 ubuntu ubuntu  4241 Feb 17 17:50 fastq_summary.py
   -rw-rw-r-- 1 ubuntu ubuntu   199 Feb 17 17:50 models.py
   -rw-rw-r-- 1 ubuntu ubuntu 14443 Feb 17 17:50 raw_reads.fastq

Much simpler and cleaner! Our only local dependencies are the Docker runtime and
some input data that we provide. Then we pull and run the image, mounting our
data inside the container and executing the embedded Python3 script. Anyone with
their own data could follow our same steps to replicate our work in their own
environments.



Share Your Docker Image
-----------------------

Now that you have containerized, tested, and tagged your code in a Docker image,
the next step is to disseminate it so others can use it.

Docker Hub is the *de facto* place to share an image you built. Remember, the
image must be name-spaced with either your Docker Hub username or a Docker Hub
organization where you have write privileges in order to push it:

.. code-block:: console

   [mbs337-vm]$ docker login
   ...
   [mbs337-vm]$ docker push username/fastq_summary:1.0


You and others will now be able to pull a copy of your container with:

.. code-block:: console

   [mbs337-vm]$ docker pull username/fastq_summary:1.0


As a matter of best practice, it is highly recommended that you store your
Dockerfiles somewhere safe. A great place to do this is alongside the code
in, e.g., GitHub. GitHub also has integrations to automatically update your
image in the public container registry every time you commit new code. (More on
this later in the semester).

For example, see: `Publishing Docker Images <https://docs.github.com/en/actions/publishing-packages/publishing-docker-images/>`_




Additional Resources
--------------------

* Many of the materials in this module were adapted from `COE 332: Software Engineering & Design <https://coe-332-sp26.readthedocs.io/en/latest/unit05/containers_2.html>`_
* `Docker for Beginners <https://training.play-with-docker.com/beginner-linux/>`_
* `Play with Docker <https://labs.play-with-docker.com/>`_
