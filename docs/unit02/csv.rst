CSV Reference
================

This reference guide is designed to introduce you to CSV format. CSV (Comma
Separated Value) is probably the most intuitive and most human-readable data
format we will encounter. Many spreadsheet tools (like Excel) can read and write
CSV, and many biological data sets are stored in CSV format. However, there
is no data typing, no support for complex data structures, and it lacks in
versatility compared to formats like JSON.

CSV Basics
----------

CSV is usually used for simple, tabular data and generally cannot be used to
represent some of the more complex data structures we will be exposed to in this
class. However, CSV is a very common data format, and you will often encounter
tabular CSV data that you want to transform into **a list of dictionaries**.

For example, consider the following valid CSV file with one header line followed
by three record lines containing gene information:

.. code-block:: text

   gene_symbol,organism,chromosome,is_disease_associated
   BRCA1,Homo sapiens,17,true
   TP53,Homo sapiens,17,true
   EGFR,Homo sapiens,7,true

The same CSV file could be represented by a **list of dictionaries** where the
headers are used as the keys, and the records are used as the values:

.. code-block:: json

   [
     {
       "gene_symbol": "BRCA1",
       "organism": "Homo sapiens",
       "chromosome": 17,
       "is_disease_associated": true
     },
     {
       "gene_symbol": "TP53",
       "organism": "Homo sapiens",
       "chromosome": 17,
       "is_disease_associated": true
     },
     {
       "gene_symbol": "EGFR",
       "organism": "Homo sapiens",
       "chromosome": 7,
       "is_disease_associated": true
     }
   ]

As a slight modification of the above, you will often see that list of
dictionaries stored as a **value** and assigned to a **key** with a descriptive
name. This is the same structure we saw in the JSON module:

.. code-block:: json

   {
     "genes": [
       {
         "gene_symbol": "BRCA1",
         "organism": "Homo sapiens",
         "chromosome": 17,
         "is_disease_associated": true
       },
       {
         "gene_symbol": "TP53",
         "organism": "Homo sapiens",
         "chromosome": 17,
         "is_disease_associated": true
       },
       {
         "gene_symbol": "EGFR",
         "organism": "Homo sapiens",
         "chromosome": 7,
         "is_disease_associated": true
       }
     ]
   }

The latest specification for CSV provides the following guidelines that "seem to
be followed by most implementations" of CSV:

1. Each record is located on a separate line with a line break
2. The last record in the file may or may not have a line break
3. There may be an optional header line appearing as the first line of the file
   with the same format as normal record lines
4. Within the header and each record, there may be one or more fields, separated
   by commas.  Each line should contain the same number of fields throughout the
   file
5. Each field may or may not be enclosed in double quotes
6. Fields containing line breaks, double quotes, and commas should be enclosed
   in double-quotes
7. If double-quotes are used to enclose fields, then a double-quote appearing
   inside a field must be escaped by preceding it with another double quote

Source: https://datatracker.ietf.org/doc/html/rfc4180

Keep an eye out for similar formats, too. For example ``.tsv`` files generally
are the exact same thing as ``.csv`` files except tab-delimited rather than
comma-delimited.

.. note::

   Check out the list of uniprot proteins we worked with in the JSON section, but
   now in CSV format `here <https://raw.githubusercontent.com/kbeavers/mbs-337-sp26/refs/heads/main/docs/unit02/sample-data/uniprot_proteins_simple.csv>`_.


Read CSV from File
------------------

Imagine you have a CSV file with headers containing protein data, e.g.:

.. code-block:: text

   proteinName,organism,className,mass,length
   Myoglobin,Homo sapiens,oxygen carrier,17184,154
   Hemoglobin subunit beta,Homo sapiens,oxygen carrier,15998,147
   Insulin,Canis lupus familiaris,hormone,12190,110
   ... etc

To read it into a dictionary object, use the ``csv`` module that is part of the
Python3 standard library:

.. code-block:: python3
   :linenos:

   import csv

   data = {}
   data['protein_entries'] = []

   with open('Protein_List.csv', 'r') as f:
       reader = csv.DictReader(f)
       for row in reader:
           data['protein_entries'].append(row))

Let's break this down:

* **Line 1**: Import Python's built-in ``csv`` module
* **Line 3**: Create an empty dictionary
* **Line 4**: Add a key called ``'protein_entries'`` to the dictionary, whose value is an empty list
  
  At this point, ``data`` looks like this:

  .. code-block:: python

   {
      'protein_entries' = []
   }

* **Line 6**: Open the ``Protein_List.csv`` file in read mode, setting ``f`` as the file object
* **Line 7**: Create a ``DictReader`` object. This special reader will automatically:
  
  * Use the first row (header) as dictionary keys
  * Convert each subsequent row into a dictionary

* **Lines 8-9**: Loop through each row in the CSV file:
  
  * Each ``row`` is already a dictionary (thanks to ``DictReader``)
  * We add each ``row`` dictionary to our ``data['protein_entries']`` list using ``.append()``

In the above case, each row of the CSV file is iterated one by one. The keys from
the header line are assigned values from the subsequent lines, then they are appended
to a list of dictionaries in the ``data`` data structure.

**Important Note:** All values read from CSV are strings by default. If you need
numbers (integers or floats), you'll need to convert them. For example:

.. code-block:: python3

   # Convert mass and length to integers
   row['mass'] = int(row['mass'])
   row['length'] = int(row['length'])


Write CSV to File
-----------------

Given the same data structure as in the previous example (a list of dictionaries
where each dictionary has identical keys), to write that object to a CSV file,
use the following:

.. code-block:: python3
   :linenos:

   import csv
   import json

   data = {}

   with open('Protein_List.json', 'r') as f:
       data = json.load(f)

   with open('Protein_List.csv', 'w') as o:
       csv_dict_writer = csv.DictWriter(o, data['protein_entries'][0].keys())
       csv_dict_writer.writeheader()
       csv_dict_writer.writerows(data['protein_entries'])

This code:

1. Reads protein data from a JSON file
2. Creates a CSV writer that uses the keys from the first dictionary as column headers
3. Writes the header row to the CSV file
4. Writes all the protein entries as rows in the CSV file

**Handling Nested Fields:**

If your data contains nested dictionaries or lists (e.g., ``organism`` is a dictionary with
``scientificName``, ``commonName``, etc.), you'll need to flatten the structure or select
specific nested fields. In this case, manually create the header row using ``.writerow()``:

.. code-block:: python3
   :linenos:

   with open('Protein_List.csv', 'w') as o:
       csv_writer = csv.writer(o)
       
       # Manually write header row with flattened field names
       header = ['proteinName',
                 'organism_scientificName',
                 'organism_commonName'
                 ]
       csv_writer.writerow(header)
       
       # Write data rows, extracting nested values
       for protein in data['protein_entries']:
           row = [
               protein['proteinName'],
               protein['organism']['scientificName'],
               protein['organism']['commonName']
               ]
           csv_writer.writerow(row)

This code:

1. Creates a regular CSV writer (not DictWriter)
2. Manually writes the header row with flattened field names (using underscores to indicate nesting)
3. Iterates through entries and extracts nested values to create each row
4. Writes each flattened row to the CSV file



Additional Resources
--------------------
* Many of the materials in this module were adapted from `COE 332: Software Engineering & Design <https://coe-332-sp26.readthedocs.io/en/latest/unit02/json.html>`_
* `CSV Basics <https://en.wikipedia.org/wiki/Comma-separated_values>`_
* `CSV Module in the Python Standard Library <https://docs.python.org/3/library/csv.html>`_
* Many biological databases export data in CSV format — check out NCBI, UniProt, or GBIF for examples
