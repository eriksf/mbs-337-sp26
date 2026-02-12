Unit Testing
============

As our code continues to grow, how can we be sure it is working as expected? If
we make minor changes to the code, what tests can we run to make sure we didn't
break anything? Are our functions written well enough to capture and correctly
handle all of the edge cases we throw at them? In this module, we will use the
Python ``pytest`` library to write **unit tests**: small tests that are designed to
test specific individual components of code. After working through this module,
students should be able to:

* Find the documentation for the Python ``pytest`` library
* Identify parts of code that should be tested
* Identify appropriate assertions and exceptions to test for
* Write and run reasonable unit tests

What is Unit Testing?
---------------------

**Unit testing** is a software testing method where individual components (units) of 
a program are tested in isolation. A "unit" is typically a single function or method. 
The goal is to verify that each unit performs correctly according to its specification.

For example, if we have a function called ``summarize_record()`` that processes a 
single FASTQ read, a unit test would verify that when we give it a specific FASTQ 
record, it returns the expected summary data.

Unit tests help us:

* **Catch bugs early**: Find problems before they affect users or other parts of the code
* **Document behavior**: Tests serve as examples of how functions should be used
* **Enable refactoring**: When you change code, tests verify that behavior hasn't broken
* **Build confidence**: Knowing your code works correctly makes development faster

For this module, we'll be testing the FASTQ summary script we've been working on
throughout Unit 4. Make sure you have your ``fastq_summary.py`` script and ``models.py``
file ready. If you need a reference, see the examples in the 
`Code Organization <organization.html>`_ module.

Devise a Reasonable Test
------------------------

The functions in our FASTQ summary script are relatively simple, but how can we be
sure they are working as intended? Let's begin with the ``summarize_record()``
function. This function takes a single FASTQ record (from BioPython's ``SeqIO``) 
and returns a ``ReadSummary`` object containing the read ID, sequence, total bases, 
and average Phred quality score.

We might choose to test it manually using the Python3 interactive
interpreter. First, we'd need to create a simple FASTQ record to test with:

.. code-block:: python3

    >>> from Bio import SeqIO
    >>> from Bio.Seq import Seq
    >>> from Bio.SeqRecord import SeqRecord
    >>> from fastq_summary import summarize_record
    >>>
    >>> # Create a simple test record
    >>> test_seq = Seq("ATCG")
    >>> test_record = SeqRecord(test_seq, id="test_read_1")
    >>> test_record.letter_annotations['phred_quality'] = [30, 31, 32, 33]
    >>>
    >>> result = summarize_record(test_record)
    >>> print(result.id)
    test_read_1
    >>> print(result.total_bases)
    4
    >>> print(result.average_phred)
    31.5

So simple! We import our code, hand-craft a simple test record, and send it to
our function. We know that the average of [30, 31, 32, 33] is 31.5, and that's 
what we get back.

Instead of writing that out each time we want to test, let's instead put this
into another Python3 script.

.. code-block:: console

   (myenv) [mbs-337]$ touch test_fastq_summary.py

Open up the script with your editor and put in our testing code:

.. code-block:: python3
   :linenos:

    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from fastq_summary import summarize_record

    # Create a simple test record
    test_seq = Seq("ATCG")
    test_record = SeqRecord(test_seq, id="test_read_1")
    test_record.letter_annotations['phred_quality'] = [30, 31, 32, 33]

    result = summarize_record(test_record)
    print(result.id)
    print(result.total_bases)
    print(result.average_phred)

Next we execute the test script on the command line:

.. code-block:: console

    test_read_1
    4
    31.5

Great! We assume the test is working. But we still have to look at the output
and remember back to our hand-crafted data and make sure that is the correct
result. It would be more efficient if we had a way to check that the correct
answer is returned in our test script itself. To do this, we can use the ``assert``
statement.

Assertions
---------------------

An **assertion** is a statement that checks if a condition is true. If the condition
is true, the program continues. If the condition is false, Python raises an
``AssertionError`` and stops execution. Assertions are perfect for testing because
they automatically verify that our code produces the expected results.

.. code-block:: python3
   :linenos:
   :emphasize-lines: 12-14

    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from fastq_summary import summarize_record
    
    # Create a simple test record
    test_seq = Seq("ATCG")
    test_record = SeqRecord(test_seq, id="test_read_1")
    test_record.letter_annotations['phred_quality'] = [30, 31, 32, 33]
    
    result = summarize_record(test_record)
    assert result.id == "test_read_1"
    assert result.total_bases == 4
    assert result.average_phred == 31.5

Now instead of printing the result, we use ``assert`` to make sure it matches
our expected outcome. If all assertions are true, nothing will be printed. If
any assertion is false, we will see an ``AssertionError`` with information about
which assertion failed.

EXERCISE
~~~~~~~~

* Write a few more tests to convince yourself that ``summarize_record()`` correctly
  calculates the average Phred score for different quality score lists.
* Create a test record with a longer sequence (e.g., "ATCGATCGATCG") and verify
  that ``total_bases`` matches the sequence length.
* Modify one of the tests so that it should fail (e.g., change the expected value),
  and execute the tests to confirm that it does fail.
* If you have multiple tests that pass and multiple tests that fail, how would you
  know which ones failed?

Automate Testing with Pytest
----------------------------

We will be using the automated testing framework ``pytest`` to test our code.
**Pytest** is an excellent framework for small unit tests and for large functional
tests.

The Python ``pytest`` unit testing framework supports test automation, set up
and shut down code for tests, and aggregation of tests into collections. It is
not part of the Python Standard Library, so we must install it.

In your project directory, run the following:

.. code-block:: console

    (myenv) [mbs-337]$ pip3 install pytest

Find the `documentation here <https://docs.pytest.org/en/7.0.x/>`_.


Next, we just need to make a minor organizational change to our test code. We
group all of our tests for a given function (e.g. all the tests for 
``summarize_record``) into their own function. By convention, we typically
name that function as "``test_``" plus the name of the function we are testing.
Pytest will automatically look in our working tree for files that start with the
``test_`` prefix, and execute the test functions within.

.. code-block:: python3
   :linenos:
   :emphasize-lines: 11-15

    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from fastq_summary import summarize_record
    
    # Create test records
    test_seq1 = Seq("ATCG")
    test_record1 = SeqRecord(test_seq1, id="test_read_1")
    test_record1.letter_annotations['phred_quality'] = [30, 31, 32, 33]
    
    def test_summarize_record():
        result = summarize_record(test_record1)
        assert result.id == "test_read_1"
        assert result.total_bases == 4
        assert result.average_phred == 31.5

Call the ``pytest`` executable in your top directory with ``pytest``. Pytest will find your test
function in your test script, run that function, and finally print some
informative output:

.. code-block:: console

   (myend) [mbs-337]$ pytest
   =================================== test session starts =====================================
    platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
    rootdir: /home/ubuntu/mbs-337/working-with-bio-data
    collected 1 item                                                                                                        

    test_fastq_summary.py .                                                             [100%]

   ==================================== 2 passed in 0.01s ======================================

The dot (``.``) indicates that one test passed. If a test fails, you'll see an ``F``
instead, along with detailed error information.

What Else Should We Test?
-------------------------

The simple tests we wrote above seem almost trivial, but they are actually great
sanity tests to tell us that our code is working. What other behaviors of our
``summarize_record()`` function should we test? In no particular order, we
could test the following non-exhaustive list:

* **Edge cases**: What if the sequence contains unexpected characters?
* **Data types**: Does the function return a ``ReadSummary`` object?
* **Calculations**: Does the average Phred score calculation work correctly for different
  quality score ranges?
* **Rounding**: Does the function correctly round the average Phred score to 2 decimal places?

For our ``summarize_fastq_file()`` function, we might test:

* **File reading**: Does it correctly read a FASTQ file and process all records?
* **Empty files**: What happens if the FASTQ file is empty?
* **File not found**: What happens if the file path doesn't exist?

For our ``write_summary_to_json()`` function, we might test:

* **File writing**: Does it correctly write JSON to a file?
* **JSON format**: Is the output valid JSON?
* **Data preservation**: Does the written JSON contain all the expected data?

.. tip::

   A list of all of the built-in Python3 exceptions can be found in the
   `Python docs <https://docs.python.org/3/library/exceptions.html>`_.

Testing Exceptions
------------------

Sometimes we want to verify that our code raises an exception when given bad input.
For example, if we try to read a file that doesn't exist, we expect a ``FileNotFoundError``.
Pytest provides a special context manager called ``pytest.raises()`` for testing exceptions.

To test some of these behaviors, let's create some additional assertions and
organize them into their own functions:

.. code-block:: python3
   :linenos:
   :emphasize-lines: 1,12-20

    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from fastq_summary import summarize_record, summarize_fastq_file
    import pytest
    
    # Create test records
    test_seq1 = Seq("ATCG")
    test_record1 = SeqRecord(test_seq1, id="test_read_1")
    test_record1.letter_annotations['phred_quality'] = [30, 31, 32, 33]
    
    def test_summarize_record():
        result = summarize_record(test_record1)
        assert result.id == "test_read_1"
        assert result.total_bases == 4
        assert result.average_phred == 31.5

    def test_summarize_fastq_file_file_not_found():
        with pytest.raises(FileNotFoundError):
            summarize_fastq_file("nonexistent_file.fastq", "fastq-sanger")

The ``with pytest.raises(FileNotFoundError):`` statement tells pytest: "I expect
the code inside this block to raise a ``FileNotFoundError``. If it doesn't raise
that exception, the test fails."

After adding the above tests, run ``pytest`` again:

.. code-block:: console

   (myenv) [mbs-337]$ pytest
   =================================== test session starts =====================================
    platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
    rootdir: /home/ubuntu/mbs-337/working-with-bio-data
    collected 2 items                                                                                                                                                                           

    test_fastq_summary.py ..                                                            [100%]
   
   ==================================== 2 passed in 0.01s ======================================

Success! The tests for our functions are passing. Our test suite essentially
documents our intent for the behavior of our functions. And, if ever we change
the code in those functions, we can see if the behavior we intend still passes
the tests.

EXERCISE
~~~~~~~~

In the same test script, but under new test function definitions:

* Write tests for the ``summarize_fastq_file()`` function using a small test FASTQ file
* Write tests for the ``write_summary_to_json()`` function to verify it writes valid JSON
* Write a test that verifies an exception is raised when ``write_summary_to_json()``
  is given an invalid output path (e.g., a directory that doesn't exist)

Capturing Standard Out
----------------------

If you have a function that prints to standard out (stdout), we can write a 
unit test for that using the ``capsys`` utility. **Standard out** (often abbreviated
as stdout) is the default output stream where programs write their output (like
the terminal screen).

Imagine a function that takes an argument and prints something to screen:

.. code-block:: python3
   :linenos:

    def print_func(num):      
        print(f'hello {num}') 
                            
    def main():               
        print_func(5)         
                            
    if __name__ == '__main__':
        main()    

Executing this code prints ``hello 5`` to screen. To write a unit test for this,
we import the function into our test script, call the function normally, then
capture the response using the ``capsys.readouterr()`` method. Then we assert that
the response matches our expectations. Assume the above Python code is in a script
called ``print_hello.py``.

``capsys`` is a pytest fixture (a special helper function) that captures what
gets printed to stdout and stderr (standard error). We can access it by including
it as a parameter to our test function.

.. code-block:: python3
   :linenos:

    from print_hello import print_func   
                                        
    def test_print_func(capsys):          
        print_func(1)                     
        captured = capsys.readouterr()    
        assert captured.out == 'hello 1\n'

Notice that we put a newline character (``\n``) at the end of the expected output.
This character is automatically added by the ``print`` function. See the additional
resources below for more information on using ``capsys``.

Organizing Your Tests & Test Data
----------------------------------

In the previous example, we put our tests in a ``test_*.py`` file. This is fine if you only have a few tests.
But how should we handle the case in which we are testing many functions, classes, modules, etc?

There are many valid ways to organize your tests and test data.

One common approach is to put all of your tests in a ``tests`` directory at the root of your
project. Quite often, the internal directory structure of ``tests`` will closely mirror the directory 
structure of the project you're building tests for.

For example, if we have a function ``summarize_record`` in ``src/fastq_summary.py`` then we might put the test for that function
in ``tests/test_fastq_summary.py`` or ``tests/fastq_summary/test_summarize_record.py``. Following this pattern will make it easy
to find tests associated with some part of your codebase.

Another possibility is to put your tests adjacent to the code against which those tests are written.

For example, if we have a function ``summarize_record`` in ``fastq_summary.py`` then we might put the test for that function
in ``test_fastq_summary.py`` in the same directory.

Your tests will generally follow the same pattern. In the previous tests that we wrote, the
test data (like ``test_record1``) was initialized in the test itself. But what if we want to reuse those
test objects? We don't want to rewrite the same test data over and over in different tests.

Regardless of whether we are following the first or second organizational pattern, it often makes the most sense to put
your test objects in some centralized location above or adjacent to the tests that will be using that data.

For example, you might create a ``conftest.py`` file (a special pytest configuration file) where you define
test fixtures (reusable test data) that can be shared across multiple test files.

Additional Resources
--------------------
* Materials adapted from `COE 332: Software Engineering & Design
  <https://coe-332-sp26.readthedocs.io/en/latest/unit03/unittest.html>`_
* `Pytest Documentation <https://docs.pytest.org/>`_
* `Exceptions in Python <https://docs.python.org/3/library/exceptions.html>`_
* `Capsys Examples <https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html>`_
* `Pytest Fixtures <https://docs.pytest.org/en/7.1.x/how-to/fixtures.html>`_ — for sharing test data across tests
