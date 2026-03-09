Building Real Dashboards with Plotly Dash
=========================================

Now that we have a good understanding of how Dash works and how to create visualizations with Plotly,
we can start building real dashboards using Plotly Dash. In this section, we will go through the process
of building a dashboard that interfaces with RCS PDB to grab pdb files and display information from it including
a 3D molecular viewer, header information, and a visualization showing the amino acid distribution. We will
go through this process step by step, from setting up the environment to deploying the dashboard. By the end
of this section, you should be able to:

- Create a Dash application that interfaces with an external API (`RCS PDB <https://www.rcsb.org/>`_).
- Display a 3D molecular viewer using a dash-bio component, **Molecule3dViewer**.
- Extract and display header information from PDB files using Biopython's **Bio.PDB** module.
- Visualize amino acid distribution using a histogram with Plotly.
- Deploy the dashboard in production (with `gunicorn <https://gunicorn.org/>`_) in a Docker container using Docker Compose.


Setting up the Environment
--------------------------

Before we start building our dashboard, we need to set up our environment. To get started, we will create
a new directory called ``pdb_dashboard`` in our mbs-337 directory on the Linux VM.

.. code-block:: console

    [mbs337-vm]$ mkdir pdb_dashboard
    [mbs337-vm]$ cd pdb_dashboard

Instead of using our ever-growing virtual environment, we will create a new one specifically for this project.
This will help us keep our dependencies organized and avoid conflicts with other projects.

.. code-block:: console

    [mbs337-vm]$ python3 -m venv .venv
    [mbs337-vm]$ source .venv/bin/activate
    [mbs337-vm]$ ls -la
    total 12
    drwxrwxr-x  3 ubuntu ubuntu 4096 Mar  9 18:05 .
    drwxrwxr-x 12 ubuntu ubuntu 4096 Mar  9 18:05 ..
    drwxrwxr-x  5 ubuntu ubuntu 4096 Mar  9 18:05 .venv

Next, we will install the necessary dependencies for our dashboard. To start, we will need Dash, Plotly,
Biopython, dash-bootstrap-components, and dash-bio. Instead of installing these packages one by one,
we will create a ``requirements.txt`` file that lists all of our dependencies. This way, we can easily install
them all at once and keep track of our dependencies.

.. code-block:: console

    (.venv) [mbs337-vm]$ touch requirements.txt
    (.venv) [mbs337-vm]$ echo "dash" >> requirements.txt
    (.venv) [mbs337-vm]$ echo "biopython" >> requirements.txt
    (.venv) [mbs337-vm]$ echo "dash-bootstrap-components" >> requirements.txt
    (.venv) [mbs337-vm]$ echo "dash-bio" >> requirements.txt
    (.venv) [mbs337-vm]$ cat requirements.txt
    dash
    biopython
    dash-bootstrap-components
    dash-bio

Now that we have our ``requirements.txt`` file, we can install all of our dependencies at once using pip.

.. code-block:: console
    :emphasize-lines: 6, 12-14, 33

    (.venv) [mbs337-vm]$ pip install -r requirements.txt
    (.venv) [mbs337-vm]$ pip list
    Package                   Version
    ------------------------- -----------
    attrs                     25.4.0
    biopython                 1.86
    blinker                   1.9.0
    certifi                   2026.2.25
    charset-normalizer        3.4.5
    click                     8.3.1
    colour                    0.1.5
    dash                      4.0.0
    dash_bio                  1.0.2
    dash-bootstrap-components 2.0.4
    Flask                     3.1.3
    GEOparse                  2.0.4
    idna                      3.11
    importlib_metadata        8.7.1
    itsdangerous              2.2.0
    Jinja2                    3.1.6
    joblib                    1.5.3
    jsonschema                4.26.0
    jsonschema-specifications 2025.9.1
    MarkupSafe                3.0.3
    narwhals                  2.17.0
    nest-asyncio              1.6.0
    numpy                     2.4.3
    packaging                 26.0
    pandas                    3.0.1
    ParmEd                    4.3.1
    periodictable             2.1.0
    pip                       24.0
    plotly                    6.6.0
    pyparsing                 3.3.2
    python-dateutil           2.9.0.post0
    referencing               0.37.0
    requests                  2.32.5
    retrying                  1.4.2
    rpds-py                   0.30.0
    scikit-learn              1.8.0
    scipy                     1.17.1
    setuptools                82.0.1
    six                       1.17.0
    threadpoolctl             3.6.0
    tqdm                      4.67.3
    typing_extensions         4.15.0
    urllib3                   2.6.3
    Werkzeug                  3.1.6
    zipp                      3.23.0


Building the Basic Dashboard
----------------------------
