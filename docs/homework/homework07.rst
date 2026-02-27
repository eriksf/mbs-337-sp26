Homework 07
===========

**Due Date: Tuesday, March 3 by 11:00am CST**

Unit 6 Databases and APIs
-------------------------

This homework applies to all of Unit 6 (Databases, Redis, APIs, and the NCBI API).
You will first start up the Redis database server in a container as we did in class
and then you will write a single, well-structured Python script called ``get_ncbi_genbank_records.py``
that uses BioPython and the NCBI API to retrieve records from GenBank and stores them in the Redis database.
The script should also dump the records from the Redis database to a TEXT file. Finally, write a README that
describes how to start up the container and run the script.

Part 1: Redis Database
~~~~~~~~~~~~~~~~~~~~~~

Normally with just a single container, you would use ``docker run`` to start up the container. In this case,
we will use ``docker compose`` to start up the container. This simplifies the process of starting it up
since you won't have to keep writing out the long ``docker run`` command with all the necessary options.

* Create a ``docker-compose.yml`` file in your ``homework07`` directory that defines a single service called
  ``redis-db`` (it should look very similar to the docker compose file that we showed in `class <../unit05/docker_compose.html#write-a-compose-file>`_
  minus the "summarize-data" service).
* Set the ``image`` to the ``redis:8.6.0`` image from Docker Hub.
* Set the ``container_name`` to ``redis``.
* Set the ``ports`` to map port 6379 on the host to port 6379 in the container.
* Create a ``redis-data`` directory in your ``homework07`` directory. Set the ``volumes`` to map that local
  directory to the ``/data`` directory in the container.
* Set the ``user`` to your UID and GID (e.g., ``1000:1000``).
* Set the ``command`` to start the Redis server with ``redis-server --appendonly yes --appendfsync everysec``
  to enable data persistence.
* Start up the container with ``docker compose up -d`` (the ``-d`` flag runs the redis service in the background) and verify that it
  is running with ``docker ps``.
* You can stop the container with ``docker compose down`` when you are done using it.

Part 2: Script
~~~~~~~~~~~~~~

**Create a Python script called** ``get_ncbi_genbank_records.py`` **that does the following:**

1. Using ``Entrez.esearch`` from ``Bio``, search the NCBI protein database for records matching the search
   term "Arabidopsis thaliana AND AT5G10140" and retrieve the list of GI numbers for the matching records (make
   sure to set max return option, ``retmax=30`` to limit the number of results).
2. Using ``Entrez.efetch`` from ``Bio``, retrieve the full GenBank records for the list of GI numbers obtained
   in step 1 (NOTE: the ``id`` parameter can be a single GI number or a comma-separated string of GI numbers).
3. Parse the GenBank records using ``SeqIO.parse`` from ``Bio`` and store the resulting record objects in a list.
4. Connect to the Redis database running in the container using the ``redis`` Python package and store each
   GenBank record in the Redis database with the ``record.id`` as the key and the value being a JSON string
   containing the record's ID (``record.id``), name (``record.name``), description (``record.description``),
   and sequence (``str(record.seq)``).
5. After storing the records in Redis, retrieve all the records from Redis and write them to an output text file
   called ``genbank_records.txt`` that looks like the following:

   .. code-block:: text

     ID: AAV51219.1
     Name: AAV51219
     Description: flowering locus C protein [Arabidopsis thaliana]
     Sequence: MGRKKLEIKRIENKSSRQVTFSKRRNGLIEKARQLSVLCDASVALLVVSASGKLYSFSSGDNLVKILDRYGKQHADDLKALDHQSKALNYGSHYELLELVDSKLVGSNVKNVSIDALVQLEEHLETALSVTRAKKTELMLKLVENLKEKEKMLKEENQVLASQMENNHHVGAEAEMEMSPAGQISDNLPVTLPLLN

     ID: NP_001078563.1
     Name: NP_001078563
     Description: K-box region and MADS-box transcription factor family protein [Arabidopsis thaliana]
     Sequence: MGRKKLEIKRIENKSSRQVTFSKRRNGLIEKARQLSVLCDASVALLVVSASGKLYSFSSGDNLVKILDRYGKQHADDLKALDHQSKALNYGSHYELLELVDSKLVGSNVKNVSIDALVQLEEHLETALSVTRAKKTELMLKLVENLKEKEKMLKEENQVLASQIFLG

     ...
6. In addition to the ``loglevel`` command-line argument for setting the logging level, add a command-line argument
   for specifying the output file name (default should be ``genbank_records.txt``). **BONUS**: add a command-line
   argument for specifying the search term (default should be "Arabidopsis thaliana AND AT5G10140").

Requirements checklist
``````````````````````

* Script name: ``get_ncbi_genbank_records.py``
* Use the shebang line ``#!/usr/bin/env python3`` at the top of the script
* At least **2 functions** plus ``main()``
* Properly formatted ``if __name__ == "__main__"`` statement
* **Type hints** on all functions (parameters and return types)
* **Docstrings** with description, Args, and Returns for every function
* **Logging** at at least **1 levels**
* **argparse** for log level
* **socket** used in logging
* At least **one try/except** for error handling
* Output TEXT file matches the required format

.. admonition:: .gitignore

   In this assignment, you have created a directory called ``redis-data`` that is persisting
   data for the Redis database. We don't actually need (or want) to store that in our GitHub
   repository, so if you haven't already, create a file called ``.gitignore`` in your root GitHub
   repository. This files tells Git which files and directories to ignore when you commit and push
   your work. Add ``redis-data`` to your ``.gitignore`` file to ignore that directory. For Python projects,
   you might want it to look like:

   .. code-block:: text

      env
      venv
      .venv
      redis-data

What to Turn In
---------------

1. Create a ``homework07`` directory in your Git repository (on your VM).
2. Add ``docker-compose.yml`` and ``get_ncbi_genbank_records.py`` to this directory.
3. Add your  output file (e.g., ``genbank_records.txt``) in an ``output_files`` directory.
4. Add a ``README.md`` in ``homework07`` that:

   * Describes how to start up the Redis container with ``docker compose``
   * Describes what the script does and how to run it (including example commands)
   * Includes a section on AI usage (if applicable — see note below)

5. Commit and push your work to GitHub.

**Expected directory layout:**

.. code-block:: text

   my-mbs337-repo/
   ├── homework07
       ├── docker-compose.yml
       ├── get_ncbi_genbank_records.py
       ├── output_files
       │   └── genbank_records.txt

Note on Using AI
----------------

The use of AI to complete this assignment is not recommended, but it is permitted
with the following restrictions:

The use of LLMs (like ChatGPT, Copilot, etc) or any other AI must be rigorously
cited. Any code blocks or text that are generated by an AI model should be
clearly marked as such with in-code comments describing what was generated, how
it was generated, and why you chose to use AI in that instance. The homework
README must also contain a section that summarizes where AI was used in the assignment.

Additional Resources
--------------------

* `Unit 6: Introduction to Databases and Persistence <../unit06/intro_to_redis.html>`_
* `Unit 6: Introduction to APIs <../unit06/intro_to_apis.html>`_
* `Unit 6: iNaturalist, RCSB PDB, and NCBI APIs <../unit06/bio_apis.html>`_
* `Docker Compose Docs <https://docs.docker.com/compose/>`_
* `Docker Hub <https://hub.docker.com/>`_
* `Redis Docs <https://redis.io/documentation>`_
* `Redis Python Library <https://redis-py.readthedocs.io/en/stable/>`_
* `NCBI APIs documentation <https://www.ncbi.nlm.nih.gov/home/develop/api/>`_
* `BioPython documentation <https://biopython.org/docs/1.76/api/index.html>`_
* `BioPython Tutorial and Cookbook <https://biopython.org/docs/latest/Tutorial>`_
* Please find us in the class Slack channel if you have any questions!
