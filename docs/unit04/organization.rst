Code Organization
=================

Following standard Python3 code organization practices will make our code easier
to read by other developers, and by our future selves who are looking back to see
what we did. After going through this module, students should be able to:

* Organize code into ``main()`` functions
* Import functions into other scripts without executing the ``main()`` block
* Write functions in a generalizable way so they are reusable
* Use a shebang in their Python3 scripts to make them executable

Main Function 
--------------

In many Python programs, you will find the developer has organized their code into 
a ``main()`` function. Then, you will see a conditional statement that looks like 
the example below:

.. code-block:: python3 

    def main():
        # application code goes here 
        print("Hello World!")

    if __name__ == '__main__':
        main()

In this code, there is a function called ``main()`` that prints the phrase ``Hello World!``. 
There is also a conditional ``if`` statement that checks the value of ``__name__`` and sees if 
it matches the string ``__main__``. When the ``if`` statement evaluates to ``True``, Python
will execute ``main()``. 

This code pattern is quite common in Python files that you want to be **executed as a script** 
and **imported in another module**. To understand how this works, let's explore how the Python 
interpreter sets ``__name__`` depending on how the code is being executed. 

Execution Modes in Python
~~~~~~~~~~~~~~~~~~~~~~~~~

There are two primary ways that you can instruct the Python interpreter to execute or use code:

1. You can execute the Python file **directly as a script** using the command line (what we have been doing thus far):

.. code-block:: console 

    $[mbs-337] python3 my_script.py 

2. You can **import** the code from one Python file into another file or into the interactive interpreter:

.. code-block:: python3 

    import my_script

Python needs a way to understand which of these is happening. To do this, it will automatically 
create a special variable called ``__name__``. 

**What's in a** ``__name__`` **?**

``__name__`` is a special string variable that Python sets for you, and its value answers 
the following question: *"How is this file being used right now?"*

Python then follows a simple rule:

* If the file is run **directly**, then:

.. code-block:: text 

    __name__ == "__main__"

* If the file is **imported**, then:

.. code-block:: text 

    __name__ == "<module_name>"

To demonstrate this, copy/paste the contents below into a file called ``test.py``:

.. code-block:: python3 

    print("This is my file to test Python's execution methods.")
    print("The variable __name__ tells me which context this file is running in.")
    print("The value of __name__ is:", __name__)

When we run this directly, we get the following output: 

.. code-block:: text
    :emphasize-lines: 3

    This is my file to test Python's execution methods.
    The variable __name__ tells me which context this file is running in.
    The value of __name__ is: __main__

Now, let's create a second file called ``use_test.py``:

.. code-block:: python3

    import test

When we run this, we get this output:

.. code-block:: text
    :emphasize-lines: 3

    This is my file to test Python's execution methods.
    The variable __name__ tells me which context this file is running in.
    The value of __name__ is: test

When a Python file is imported, ``__name__`` becomes the name of the **module**!

.. admonition:: Important! 

    Did you notice that Python executed all of the code within ``test.py`` when 
    we imported the ``test`` module? 
    This is important behavior that we need to be aware of. 
    More on this later...

.. tip:: 

    You'll see the words **file**, **module**, and **script** used throughout this 
    doc. Sometimes they are used interchangeably, but today we should highlight 
    the differences between them:

    * **File**: Any Python file that contains code; ends in the ``.py`` extension. 
    * **Script**: A Python file that you intend to *execute from the command line*.
    * **Module**: A Python file that you intend to *import into a script*. 

Best Practices for Python Main Functions 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These four best practices will ensure that your code can always be run as a script *and* 
as a module:

1. Put most of your code into a function or class
2. Use ``__name__`` to control execution of your code
3. Create a function called ``main()`` to contain the code you want to run
4. Call other functions from ``main()``

Put Most Code Into a Function or Class
++++++++++++++++++++++++++++++++++++++

Let's consider the code we wrote in the last unit to print the number of residues 
per chain in a mmCIF file:

.. code-block:: python3 

    from Bio.PDB.MMCIFParser import MMCIFParser

    parser = MMCIFParser()
    with open('1MBN.cif', 'r') as f:
        structure = parser.get_structure('myoglobin', f)

    for model in structure:
        for chain in model:
            chain_id = chain.get_id()
            num_residues = 0
            for residue in chain:
                num_residues += 1
            print(f"Chain {chain_id}: {num_residues} residues")

Our goal is to rewrite this so that it can be run as a script *and* imported 
into another script as a module. 

If we were to import this code as-is as a module into a new script, Python would 
execute the full code. Instead, we want the user to be able to control the 
execution of this code. The best way to do this is to put as much of the code 
into a **function** or **class**. When Python encounters a ``def`` or ``class`` keyword,
it stores those definitions for later use and only executes them when you tell it to.

Let's start by putting the "summarize chains" logic in a function:

.. code-block:: python3

    from Bio.PDB.MMCIFParser import MMCIFParser

    def summarize_chains(structure):
        # Print residue count for each chain in each model.

        for model in structure:
            for chain in model:
                chain_id = chain.get_id()
                num_residues = 0
                for residue in chain:
                    num_residues += 1
                print(f"Chain {chain_id}: {num_residues} residues")

Now we have reusable logic in ``summarize_chains()``, but we still need a way to 
control when the file actually runs the full workflow (parsing the file and 
calling ``summarize_chains``).

Create a  ``main()`` Function 
+++++++++++++++++++++++++++++

Now we need to put the step-by-step workflow (create parser, open file, get structure)
in a single function called ``main()``. This will give us one clear **entry point** to 
run our code.

Define **constants** at the top of the file (with other global configuration) so that
they are easy to find and change, and so that ``main()`` only contains the workflow steps:

.. code-block:: python3

    from Bio.PDB.MMCIFParser import MMCIFParser

    CIF_FILE = "1MBN.cif"
    STRUCTURE_ID = "myoglobin"

    def summarize_chains(structure):
        # Print residue count for each chain in each model.

        for model in structure:
            for chain in model:
                chain_id = chain.get_id()
                num_residues = 0
                for residue in chain:
                    num_residues += 1
                print(f"Chain {chain_id}: {num_residues} residues")

    def main():
        # Create parser, open file, create structure object, call summarize_chains()

        parser = MMCIFParser()
        with open(CIF_FILE, 'r') as f:
            structure = parser.get_structure(STRUCTURE_ID, f)
        summarize_chains(structure)


Use ``__name__`` to Control Execution 
++++++++++++++++++++++++++++++++++++++

Then, at the bottom of the file, we'll write a conditional statement that will 
only call ``main()`` when ``__name__ == "__main__"`` so that running the 
file as a script runs the workflow, but importing the file does not:

.. code-block:: python3

    from Bio.PDB.MMCIFParser import MMCIFParser

    CIF_FILE = "1MBN.cif"
    STRUCTURE_ID = "myoglobin"

    def summarize_chains(structure):
        # Print residue count for each chain in each model.

        for model in structure:
            for chain in model:
                chain_id = chain.get_id()
                num_residues = 0
                for residue in chain:
                    num_residues += 1
                print(f"Chain {chain_id}: {num_residues} residues")

    def main():
        # Create parser, open file, create structure object, call summarize_chains()
        
        parser = MMCIFParser()
        with open(CIF_FILE, 'r') as f:
            structure = parser.get_structure(STRUCTURE_ID, f)
        summarize_chains(structure)

    if __name__ == "__main__":
        main()


Call Other Functions From ``main()``
++++++++++++++++++++++++++++++++++++++

Your ``main()`` function should orchestrate the workflow by calling your other 
functions.

* Keep the actual steps inside helper functions (``summarize_chains()``)
* Use ``main()`` to run them in order.

Doing this makes the file both a standalone script as well as a module that can be loaded 
into other scripts. 

Let's put this code in a module called ``mmcif_analysis.py``.

If this code is imported into another Python3 script, that other script will have access to the 
``summarize_chains()`` function and the ``main()`` function, but it will not automatically 
execute either. 

Let's create another file called ``use_mmcif_analysis.py`` containing the following code:

.. code-block:: python3

    import mmcif_analysis

When we run this script, no output is printed to the terminal. Why is that?

.. toggle::

    When you import the script, ``__name__`` is now == the module name (``mmcif_analysis``).
    So the ``if __name__ == '__main__'`` block is now False. ``main()`` is not called, 
    and the code within ``mmcif_analysis.py`` is not run automatically on import anymore. 

If you *do* want the same workflow to run from the importing script, call ``main()`` 
explicitly after the import:

.. code-block:: python3

    # within use_mmcif_analysis.py
    import mmcif_analysis

    mmcif_analysis.main()   # run the same workflow (parse 1MBN.cif and print chain summary)

You now also have access to any other functions defined in the ``mmcif_analysis`` module.
For example, you can parse your own mmCIF file and pass the resulting structure to
``summarize_chains()``:

.. code-block:: python3

    import mmcif_analysis
    from Bio.PDB.MMCIFParser import MMCIFParser

    parser = MMCIFParser()
    with open("other.cif", "r") as f:
        structure = parser.get_structure("other", f)
    mmcif_analysis.summarize_chains(structure)

Refactoring
------------

**Refactoring** is when you reorganize your code while preserving its original behavior.
Refactoring code is analogous to factoring in mathematics. For example:

``f(x) = x^2 + x`` can be written as ``f(x) = x(x+1)``

or in the opposite direction:

``f(x) = x(x+1)`` → ``f(x) = x^2 + x``

The expression changes, but the result does not. 

In software engineering, we refactor our code so that it is better organized, more 
readable, and easier to reason out. 

EXERCISE 
~~~~~~~~

Now let's consider another script that we wrote to write FASTQ quality metrics to a JSON:

.. code-block:: python3
    :linenos:

    import json
    from Bio import SeqIO
    from pydantic import BaseModel

    # Define ReadSummary model
    class ReadSummary(BaseModel):
        id: str
        sequence: str
        total_bases: int
        average_phred: float

    # Define FastqSummary model
    class FastqSummary(BaseModel):
        reads: list[ReadSummary]

    # Create list of ReadSummary instances
    reads_list = []
    with open('raw_reads.fastq', 'r') as f:
        for record in SeqIO.parse(f, 'fastq-sanger'):
            reads_list.append(ReadSummary(
                id=record.id,
                sequence=str(record.seq),
                total_bases=len(record.seq),
                average_phred=sum(record.letter_annotations['phred_quality']) / len(record.letter_annotations['phred_quality'])
            ))

    data = FastqSummary(reads=reads_list)
    with open('fastq_summary.json', 'w') as outfile:
        json.dump(data.model_dump(), outfile, indent=2)

When looking at our code, we should always ask ourselves the following:

1. Can I succinctly describe what this code is doing?
2. Can I reorganize my code in some way that improves its readability and the ability of others to reason what it does?
    
.. note::

    Let the following software development principle guide your thinking:

    **Single Responsibility Principle (SRP):** A function, class, or module should have a single, 
    well-defined job or responsibility.

The first thing we can do is put our Pydantic models into a separate module called ``models.py``.
Models such as this should always live in their own module so that this module has a single 
responsibility: describe the data. 

.. code-block:: python3
    :linenos:
    :caption: models.py

    from pydantic import BaseModel

    class ReadSummary(BaseModel):
        id: str
        sequence: str
        total_bases: int
        average_phred: float

    class FastqSummary(BaseModel):
        reads: list[ReadSummary]

The next thing we should do is refactor our analysis logic into small functions with 
single jobs:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 3, 25
    :caption: fastq_summary.py 

    import json
    from Bio import SeqIO
    from models import ReadSummary, FastqSummary

    def summarize_record(record) -> ReadSummary:
        # Convert one FASTQ record into a ReadSummary instance

        phred_scores = record.letter_annotations['phred_quality']
        average_phred = sum(phred_scores) / len(phred_scores)

        return ReadSummary(
            id=record.id,
            sequence=str(record.seq),
            total_bases=len(record.seq),
            average_phred=round(average_phred, 2)
        )

    def summarize_fastq_file(fastq_file: str, encoding: str) -> FastqSummary:
        # Read a FASTQ file and return a FastqSummary instance 

        reads_list = []

        with open(fastq_file, 'r') as f:
            for record in SeqIO.parse(f, encoding):
                reads_list.append(summarize_record(record))

        return FastqSummary(reads=reads_list)

    def write_summary_to_json(summary: FastqSummary, output_file: str) -> None:
        # Write FastqSummary to a JSON file

        with open(output_file, 'w') as outfile:
            json.dump(summary.model_dump(), outfile, indent=2)

Now we've decomposed the analysis into smaller, more focused functions. Now we just need to 
define a ``main()`` function that will handle the configuration and execution of these functions:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 2,3

    def main():
        summary = summarize_fastq_file(FASTQ_FILE, ENCODING)
        write_summary_to_json(summary, OUTPUT_JSON)

    if __name__ == '__main__':
        main()

Putting this all together, we end up with a file that can be run as a standalone script or imported as 
a module:

.. code-block:: python3
    :linenos:

    import json
    from Bio import SeqIO
    from models import ReadSummary, FastqSummary

    # -------------------------
    # Constants (configuration)
    # -------------------------
    FASTQ_FILE = 'raw_reads.fastq'
    OUTPUT_JSON = 'fastq_summary.json'
    ENCODING = 'fastq-sanger'

    # -------------------------
    # Functions 
    # -------------------------
    def summarize_record(record) -> ReadSummary:
        # Convert one FASTQ record into a ReadSummary instance

        phred_scores = record.letter_annotations['phred_quality']
        average_phred = sum(phred_scores) / len(phred_scores)

        return ReadSummary(
            id=record.id,
            sequence=str(record.seq),
            total_bases=len(record.seq),
            average_phred=round(average_phred, 2)
        )

    def summarize_fastq_file(fastq_file: str, encoding: str) -> FastqSummary:
        # Read a FASTQ file and return a FastqSummary instance 

        reads_list = []

        with open(fastq_file, 'r') as f:
            for record in SeqIO.parse(f, encoding):
                reads_list.append(summarize_record(record))

        return FastqSummary(reads=reads_list)

    def write_summary_to_json(summary: FastqSummary, output_file: str) -> None:
        # Write FastqSummary to a JSON file

        with open(output_file, 'w') as outfile:
            json.dump(summary.model_dump(), outfile, indent=2)

    def main():
        summary = summarize_fastq_file(FASTQ_FILE, ENCODING)
        write_summary_to_json(summary, OUTPUT_JSON)

    if __name__ == '__main__':
        main()

We now have a cleaner, easier to read application that is simple to reason about. We could use this as a module if we 
wanted:

.. code-block:: python3
    :linenos:
    :caption: new_fastq_analysis.py 

    from fastq_summary import summarize_fastq_file, write_summary_to_json

    summary = summarize_fastq_file('new_reads.fastq', 'fastq-sanger')
    write_summary_to_json(summary, 'new_output.json')

Shebang 
-------

So far, we have been running Python programs like this:

.. code-block:: console 

    [mbs-337]$ python3 fastq_summary.py 

The above code explicitly tells the operating system to use the Python3 interpreter to run the file. 

A **shebang** is a special instruction that we put at the top of a script that tells the 
operating system which interpreter should be used to run the script. You will often see these 
used in Python, Perl, Bash, C shell, and a number of other scripting languages. In our case, 
we want to use the following shebang, which should appear on the first line of our Python3 scripts:

.. code-block:: python3 

    #!/usr/bin/env python3 

* ``#!``: This tells the operating system that this file is a script and it needs some interpreter to run it 
* ``/usr/bin/env``: This is the path to ``env``, which is a utility on Unix-like systems that finds interpreters on your system. So instead of hard-coding the exact location of Python3, we ask ``env`` to find it for us 
* ``python3``: This is the interpreter that we want to use to run the script. 

Conceptually, this shebang is saying: "*Find Python 3 on this system and use it to run this file.*"

We also need to make the script executable using the Linux command ``chmod``:

.. code-block:: console 

    [mbs-337]$ chmod u+x fastq_summary.py 

This enables you to call the Python3 code within as a standalone executable without invoking the 
interpreter on the command line:

.. code-block:: console 

    [mbs-337]$ ./fastq_summary.py 

This is helpful to lock in a Python version (e.g. Python3) for a script that may be executed on 
multiple different machines or in various environments. 

Essentially, a shebang lets you tell the computer which program should run your script, so the 
script can be executed directly instead of calling Python explicitly.

Other Tips 
----------

As our Python3 scripts become longer and more complex, we should put more thought into how different 
contents of the script are ordered. As a rule of thumb, try to organize the different sections of your 
Python3 code into this order:

.. code-block:: python3

   # Shebang

   # Imports

   # Global variables / constants

   # Class definitions

   # Function definitions

   # Main function definition

   # Call to main function

Other general tips for writing code that is easy to read can be found in the 
`PEP 8 Style Guide <https://www.python.org/dev/peps/pep-0008/>`_, including:

* Use four spaces per indentation level (no tabs)
* Limit lines to 80 characters, wrap and indent where needed 
* Avoid extraneous whitespace unless it improves readability 
* Be consistent with naming variables and functions
    * Classes are usually ``CapitalWords``
    * Constants are usually ``ALL_CAPS``
    * Functions and variables are usually ``lowercase_with_underscores``
    * Consistency is key 
* Use functions to improve organization and reduce redundancy
* Document and comment your code 

.. note::

    Beyond individual Python3 scripts, there is a lot more to learn about organizing 
    *projects* which may consist of many files. We will get into that later in the 
    semester.  

Additional Resources 
--------------------

* Many of the materials in this module were adapted from `COE 332: Software Engineering & Design <https://coe-332-sp26.readthedocs.io/en/latest/unit03/organization.html#>`_
* `PEP 8 Style Guide <https://www.python.org/dev/peps/pep-0008/>`_
* `Defining Main Functions in Python <https://realpython.com/python-main-function/>`_
