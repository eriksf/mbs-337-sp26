Error Handling
==============

Error handling is an important part of data science. Even syntactically correct code can 
fail at runtime due to missing files, malformed data, or invalid user input. Being able 
to understand error messages, anticipate where errors might happen, and program defensively 
against errors will make your code more robust. After working through this 
module, students should be able to:

* Anticipate where and what types of errors might occur in their code
* Read traceback statements and identify exceptions
* Write code blocks to catch and handle exceptions

Why Do We Need Error Handling?
------------------------------

#. Prevents program from crashing if an error occurs
    * If an error occurs in a program, we don't want the program to unexpectedly
      crash on the user. Instead, error handling can be used to notify the user of
      why the error occurred and gracefully exit the process that caused the error.

#. Saves time debugging errors
    * Following reason #1, having the program display an error instead of immediately
      crashing will save a lot of time when debugging errors.
    * The logic inside the error handler can be updated to display useful information
      for the developer, such as the code traceback, type of error, etc.

#. Helps define requirements for the program
    * If the program crashes due to bad input, the error handler could notify the user
      of why the error occurred and define the requirements and constraints of the program.


`Source <https://betterprogramming.pub/handling-errors-in-python-9f1b32952423>`_


Errors in Data
--------------

Consider our FASTQ summary script and the functions we use to read FASTQ files,
summarize reads, and write JSON (e.g. ``summarize_fastq_file``, ``summarize_record``,
``write_summary_to_json``). We have seen that they work when we use valid data and
a valid file path. But what happens when we introduce invalid or unexpected data?

For example:

* The input FASTQ file might not exist where we think it does, and the code is unable to read it in.
* A record in the file might be malformed — for example, missing quality scores.
* The output JSON path might be invalid or we might not have write permission.

We are given no guarantees about the integrity of our input data or the
environment. In the wild you will sometimes encounter files that are empty,
missing expected fields, or have values that do not conform to the expected type.

At this point we need to make a choice. If we have input that could be 10s or
100s of thousands of reads (or more), do we want to manually inspect every file
for problems? It would be better to update our code to anticipate these possible
errors and handle them so that our program does not crash and we still get a
result that makes sense.


Understanding Exceptions
------------------------

When errors do occur, Python3 prints a **traceback** message to help you pinpoint
where the specific **exception** occurred. With traceback messages, you generally
want to read the bottom line first, which identifies the specific exception, and
then start reading up to find out where in the code (i.e. in what function) the
exception occurred. For most errors, you can probably get away with only looking
at the last three or so lines of the traceback message.

At first glance, exceptions and traceback messages may seem to be undecipherable, 
but understanding that there are a finite number of built in exceptions and each
named exception actually is a pretty useful hint to where the error occurred. 
Consider some of the following exceptions:

.. code-block:: python3

   >>> 10 * (1/0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ZeroDivisionError: division by zero

   >>> 4 + spam*3
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   NameError: name 'spam' is not defined

   >>> '2' + 2
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: can only concatenate str (not "int") to str

ZeroDivisionError, NameError, and TypeError are somewhat self explanatory when
you see when they are raised. Knowing what circumstances can cause a built-in
exception to occur (e.g. NameErrors are raised when a name is not found) is the
first step toward identifying the cause and the solution. Some common situations
that generate exceptions are:

* Trying to open a file that does not exist raises a ``FileNotFoundError``.
* Trying to divide by zero raises a ``ZeroDivisionError``.
* Trying to access a list at an index beyond its length raises an ``IndexError``.
* Trying to use an object of the wrong type in a function raises a ``TypeError``.
* Trying to use an object with the wrong kind of value in a function raises a ``ValueError``
  (for example, calling ``int('abc')``).
* Trying to access a non-existent attribute on an object raises an ``AttributeError`` (a special
  case is accessing a null/uninitialized object, resulting in the dreaded
  ``AttributeError: 'NoneType' object has no attribute 'foo'`` error).

A list of all built-in exceptions that could occur can be found 
`here <https://docs.python.org/3/library/exceptions.html>`_.

.. note:: 

    Note that syntax errors stand apart as exceptions that can't be handled at runtime:

.. code-block:: python3

   >>> print 'Hello, world!'
    File "<stdin>", line 1
        print 'Hello, world!'
        ^^^^^^^^^^^^^^^^^^^^^
    SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?


Handling Exceptions
-------------------

We can use a strategy called **exception handling** to prevent our program from
crashing if it encounters an exception during runtime. The specific statements
we use for this in Python3 are ``try`` and ``except``. In general, it follows 
the format:

.. code-block:: python

    try:
        # potentially risky code
        f(x, y, z)
    except SomeException1 as e:
        # do something if the exception was of type SomeException1...
    except SomeException2 as e:
        # do something if the exception was of type SomeException2...

    # . . . additional except blocks . . .

    finally:
        # do something regardless of whether an exception was raised or not.

A few notes:

* If a statement(s) within the ``try`` block does *not* raise an exception, the
  ``except`` blocks are skipped.
* If a statement within the ``try`` block *does* raise an exception, Python looks
  at the ``except`` blocks for the first one matching the type of the exception
  raised and executes that block of code.
* The ``finally`` block is optional but it executes regardless of whether an
  exception was raised by a statement or not.
* The ``as e`` clause puts the exception object into a variable (``e``) that we
  can use.
* The use of ``e`` was arbitrary; we could choose to use any other valid variable
  identifier.
* We can also leave off the ``as e`` part altogether if we don't need to reference
  the exception object in our code.

Here's some simple examples that demonstrate how this works:

.. code-block:: python3 

    try:
        number = int("42.5")
        print("Success:", number)
    except ValueError as e:
        print("Error:", e)


.. code-block:: python3 

    try:
        f = open("data.txt")
        data = f.read()
    except FileNotFoundError as e:
        print("Error:", e)
    finally:
        print("Closing file.")

Let's take another look at our ``fastq_summary.py`` script. Right now, we have no graceful 
way to gracefully exit the process and notify the user if the main function is unable to 
find our input FASTQ file. We should add exception handling for a FileNotFoundError:


.. code-block:: python3 
    :linenos:
    :emphasize-lines: 9, 12,13

    import sys # access system specific functions

    def main():
        logging.info("Starting FASTQ summary workflow")

        try:
            summary = summarize_fastq_file(FASTQ_FILE, ENCODING)
            write_summary_to_json(summary, OUTPUT_JSON)
            logging.info("FASTQ summary workflow complete")

        except FileNotFoundError:
            logging.error(f"Input FASTQ file {FASTQ_FILE} not found. Exiting.")
            sys.exit(1) # Stop the execution of the script with an error 

What if we accidentally wiped our input FASTQ file and how our input is empty? 
Create a new empty file called ``empty_reads.fastq`` and set this as your ``FASTQ_FILE`` constant. 
What happens when you run the script now?

Somtimes the best solution is to just add a **guard statement** instead of exception handling. 

.. code-block:: python3 
    :linenos:
    :emphasize-lines: 9-11

    def summarize_fastq_file(fastq_file: str, encoding: str) -> FastqSummary:
        logging.info(f"Reading FASTQ file {fastq_file}")

        reads_list = []
        with open(fastq_file, 'r') as f:
            for record in SeqIO.parse(f, encoding):
                reads_list.append(summarize_record(record))

        if len(reads_list) == 0:
            logging.error(f"Input FASTQ file {fastq_file} is empty. Exiting.")
            sys.exit(1)

        logging.info(f"Finished reading {len(reads_list)} reads")
        return FastqSummary(reads=reads_list)


Exception Hierarchy
-------------------

Exceptions form a class hierarchy with the base ``Exception`` class being at the root. So,
for example:

* ``FileNotFoundError`` is a type of ``OSError`` as is ``PermissionError``, which is raised in case
  the attempted file access is not permitted by the OS due to lack of permissions.
* ``ZeroDivisionError`` and ``OverflowError`` are instances of ``ArithmeticError``, the latter
  being raised whenever the result of a calculation exceeds the limits of what can be represented
  (try running ``2.**5000`` in a Python shell).
* Every built-in Python exception is of type ``Exception``.

Therefore, we could use any of the following to deal with a ``FileNotFoundError``:

* ``except FileNotFoundError``
* ``except OSError``
* ``except Exception``

For example, we could have technically done this instead: 

.. code-block:: python3 

    def main():
    logging.info("Starting FASTQ summary workflow")

    try:
        summary = summarize_fastq_file(FASTQ_FILE, ENCODING)
        write_summary_to_json(summary, OUTPUT_JSON)
        logging.info("FASTQ summary workflow complete")

    except Exception as e:
        logging.error(e)
        sys.exit(1)

Here are some best practices to keep in mind for handling exceptions:

* Put a minimum number of statements within a ``try`` block so that you can detect which
  statement caused the error.
* Similarly, put the most specific exception type in the ``except`` block that is appropriate
  so that you can detect exactly what went wrong. Using ``except Exception...`` should
  be seen as a last resort
  because an ``Exception`` could be any kind of error.


See the resources below for tips on building more complicated try-except statements.

Additional Resources
--------------------
* Materials adapted from `COE 332: Software Engineering & Design
  <https://coe-332-sp26.readthedocs.io/en/latest/unit03/errorhandling.html>`_
* `Python 3 Error Handling <https://docs.python.org/3/tutorial/errors.html>`_
* `Python 3 Exception Class <https://docs.python.org/3/library/exceptions.html>`_




