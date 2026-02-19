Homework 06
===========

**Due Date: Tuesday, February 24 by 11:00am CST**

Unit 5 Containerization
-----------------------

This homework applies to the first two parts of Unit 5 (Introduction to Containers and
Advanced Containers). You will containerize (a single container) the scripts
from the first three exercises from Homework 4 and the script from Homework 5, run
the container multiple times to generate output from each script, push the container to Docker Hub, and
finally write a README that describes how to build and use the container.

Part 1A: Input files
^^^^^^^^^^^^^^^^^^^^

* **FASTA:** A multi-sequence FASTA file named ``immune_proteins.fasta``. Download with:

.. code-block:: console

   wget https://github.com/TACC/mbs-337-sp26/raw/refs/heads/main/docs/unit03/sample-data/immune_proteins.fasta.gz
   gunzip immune_proteins.fasta.gz

* **FASTQ:** A FASTQ file named ``sample1_rawReads.fastq``.

.. code-block:: console

   wget https://github.com/TACC/mbs-337-sp26/raw/refs/heads/main/docs/unit03/sample-data/sample1_rawReads.fastq.gz
   gunzip sample1_rawReads.fastq.gz

* **mmCIF:** The hemoglobin structure **4HHB**. Download with:

.. code-block:: console

   wget https://files.rcsb.org/download/4HHB.cif.gz
   gunzip 4HHB.cif.gz

Part 1B: Scripts to containerize
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Script 1: Count residues in FASTA file (from `Homework 4 - Exercise 1 <homework04.html#exercise-1-count-residues-in-fasta-file>`_)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Rename the Python script ``exercise1.py`` to ``fasta_stats.py`` and have it read ``immune_proteins.fasta``
and write to a text file called ``immune_proteins_stats.txt`` instead of printing to the console. To make it
more flexible for container use, the script should take the input FASTA file and output text file as command-line
arguments in addition to the log level (see general requirements below) using ``argparse``. The output text file
should contain the exact same information as before described in Homework 4 - Exercise 1.

Script 2: Write a new FASTA file (from `Homework 4 - Exercise 2 <homework04.html#exercise-2-write-new-fasta-file>`_)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Rename the Python script ``exercise2.py`` to ``fasta_filter.py`` and have it read ``immune_proteins.fasta``
and write out a new FASTA file called ``long_only.fasta`` containing only the sequences longer than or equal to
1000 residues (or a specified length). Each output record must be a valid FASTA with the original headers format
preserved. To make it more flexible for container use, the script should take the input FASTA file,
output FASTA file, and minimum sequence length as command-line arguments in addition to the log level
(see general requirements below) using ``argparse``.

Script 3: FASTQ quality filter and write (from `Homework 4 - Exercise 3 <homework04.html#exercise-3-fastq-quality-filter-and-write>`_)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Rename the Python script ``exercise3.py`` to ``fastq_filter.py`` and have it read ``sample1_rawReads.fastq``
and write out a new FASTQ file called ``sample1_cleanReads.fastq`` containing only the reads where the average
Phred score is greater than or equal to 30 (or a specified threshold). To make it more flexible for container use,
the script should take the input FASTQ file, output FASTQ file, encoding, and Phred score threshold as command-line
arguments in addition to the log level (see general requirements below) using ``argparse``. Instead of printing the
total number of reads and the number of reads that passed quality control to the console, write this information
to the log.

Script 4: mmCIF Summary Script (from `Homework 5 <homework05.html#unit-4-best-practices-mmcif-summary-script>`_)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Just copy the Python script you created for Homework 5 (``mmcif_summary.py``). This script should only need minor
modifications to take the input CIF file and output JSON file as command-line arguments to make it more flexible
for container use. It's output should still be the same JSON format as described in Homework 5.

General Requirements checklist for all scripts
""""""""""""""""""""""""""""""""""""""""""""""

* Use the shebang line ``#!/usr/bin/env python3`` at the top of each script
* At least **1 function** plus ``main()``
* Properly formatted ``if __name__ == "__main__"`` statement
* **Type hints** on all functions (parameters and return types)
* **Docstrings** with description, Args, and Returns for every function
* **Logging** at at least **1 level**
* **argparse** for log level and other parameters as described above
* **socket** used in logging
* At least **one try/except** for error handling

Part 2: Build the container
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Write a Dockerfile to containerize all of the script described above.

Requirements
""""""""""""

* Use an official Python base image (e.g., ``python:3.12``)
* Install all necessary dependencies
* Copy all scripts into the container at ``/code``
* Make sure all the scripts are executable (hint: ``chmod ugo+x <file>``)
* Add ``/code`` to the PATH so the scripts can be run from anywhere in the container

Part 3: Run each script
^^^^^^^^^^^^^^^^^^^^^^^

Run each script in the container to generate the expected output files. You can use the same input files as before
described above (``immune_proteins.fasta``, ``sample1_rawReads.fastq``, and ``4HHB.cif``).

Requirements
""""""""""""

* Run each script with ``docker run`` from outside the container (not interactively) with the proper command-line
  arguments to specify the input and output files (and other parameters as needed by each script).
* Make sure to mount $PWD (directory containing the input files and where output files will be written)
  to a directory in the container (``/data``) using the ``-v`` flag of ``docker run``.
* Make sure to use the ``-u`` flag of ``docker run`` to run the container with the ubuntu user ID so that
  output files are owned by you and not root.

Part 4: Push to Docker Hub
^^^^^^^^^^^^^^^^^^^^^^^^^^

When you have successfully built and run your container, push it to Docker Hub so that others can use it.

Requirements
""""""""""""

* Create a Docker Hub account if you don't have one already.
* Tag your container with your Docker Hub username and a repository name and version of your choosing
  (e.g., ``username/my_bio_tools:1.0``).

Part 5: README
^^^^^^^^^^^^^^

The README should describe how a user who has just cloned your repository can run your tools in a container
from start to finish. Take special care to describe how to:

* Build the image from a Dockerfile
* Get the input data from the web (data should be cited)
* Mount the data inside the container at run time
* Run the containerized code as a specific user to avoid permission issues
* Describe the available parameters for each script and how to specify them at run time
* Describe the expected output files and where to find them after running the container
* Includes a section on AI usage (if applicable — see note below)

What to Turn In
---------------

1. Create a ``homework06`` directory in your Git repository (on your VM).
2. Add ``fasta_stats.py``, ``fasta_filter.py``, ``fastq_filter.py``, and ``mmcif_summary.py`` to this directory.
3. Add your 4 output files (e.g., ``immune_proteins_stats.txt``, ``long_only.fasta``, ``sample1_cleanReads.fastq``,
   and ``4HHB_summary.json``) in an ``output_files`` directory.
4. Add a ``README.md`` in ``homework06``.
5. Commit and push your work to GitHub.

**Expected directory layout:**

.. code-block:: text

   my-mbs337-repo/
    └── homework06/
        ├── Dockerfile
        ├── README.md
        ├── fasta_filter.py
        ├── fasta_stats.py
        ├── fastq_filter.py
        ├── mmcif_summary.py
        ├── output_files
        │   ├── 4HHB_summary.json
        │   ├── immune_proteins_stats.txt
        │   ├── long_only.fasta
        │   └── sample1_cleanReads.fastq

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

* `Unit 5: Introduction to Containers <../unit05/containers_1.html>`_
* `Unit 5: Advanced Containers <../unit05/containers_2.html>`_
* `Docker Docs <https://docs.docker.com/>`_
* `Best practices for writing Dockerfiles <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`_
* `Docker Hub <https://hub.docker.com/>`_
* Please find us in the class Slack channel if you have any questions!
