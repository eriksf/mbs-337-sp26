Python Refresher
================

To be successful in this class, students should be able to:

* Write and execute Python code on the class server
* Use variables, lists, and dictionaries in Python
* Write conditionals using a variety of comparison operators
* Write useful while and for loops
* Arrange code into clean, well organized functions
* Read input from and write output to a file
* Import and use standard and non-standard Python libraries

Topics covered in this module include:

* Data types and variables (ints, floats, bools, strings, type(), print())
* Arithmetic operations (+, -, \*, /, \*\*, %, //)
* Lists and dictionaries (creating, interpreting, appending)
* Conditionals and control loops (comparison operators, if/elif/else, while, for, break, continue, pass)
* Functions (defining, passing arguments, returning values)
* File handling (open, with, read(), readline(), strip(), write())
* Importing libraries (import, random, names, pip)


Log in to the Class Server
--------------------------

All computing for this course will take place on Linux virtual machines (VMs). To reach them, you will connect in two steps:

1. First, we'll connect to ``student-login.tacc.utexas.edu``. This is a persistent Linux VM at TACC that acts as a login gateway (jump host). 
2. Second, from ``student-login``, you'll connect to your own personal course VM. This VM is named ``mbs-337`` and is hosted on JetStream2. 

To connect from your own computer, you will use the **Secure Shell (SSH)** protocol through a CLI or an SSH client. The exact steps depend slightly on your computer's operating system. 

.. note::

   Replace ``username`` with your TACC username.

---- 

**Mac / Linux**

From the terminal, connect to the TACC login VM:

.. code-block:: console

   ssh username@student-login.tacc.utexas.edu
   (enter password)
   (enter MFA token)

Once connected to ``student-login``, connect to your course VM:

.. code-block:: console

   ssh mbs-337

----

**Windows**

To connect:

.. code-block:: console

   Open the application 'PuTTY'
   Enter Host Name: student-login.tacc.utexas.edu
   (Click 'Open')
   (Enter username)
   (Enter password)
   (Enter MFA token)

Once connected to ``student-login``, connect to your course VM:

.. code-block:: console

   ssh mbs-337

----

**Chromebook**

1. Open **Settings**
2. Go to **Advanced -> Developers**
3. Enable **Linux development environment**

Once enabled, you can open the Terminal app from your launcher and connect using SSH:

.. code-block:: console

   ssh username@student-login.tacc.utexas.edu
   (enter password)
   (enter MFA token)

----

Once connected to ``student-login``, connect to your course VM:

.. code-block:: console

   ssh mbs-337

If you can't access the class server yet, a local or web-based Python 3
environment will work for this guide. However, you will need to access the class
server for future lectures.

Try this `Python 3 environment in a browser <https://www.katacoda.com/scenario-examples/courses/environment-usages/python>`_.


.. note::

   For the first few sections below, we will be using the Python interpreter
   in *interactive mode* to try out different things. Later on when we get to
   more complex code, we will be saving the code in files (scripts) and invoking
   the interpreter non-interactively.


Data Types and Variables
------------------------

Start up the interactive Python interpreter:

.. code-block:: console

   [mbs-337]$ python3
   Python 3.x.x (main, Nov  6 2025, 13:44:16) [GCC 13.3.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

.. tip::

   To exit the interpreter, type ``quit()``.

The most common data types in Python are similar to other programming languages.
For this class, we probably only need to worry about **integers**, **floats**,
**booleans**, and **strings**.

Assign some values to variables by doing the following:

.. code-block:: python3

   >>> gene_count = 42
   >>> protein_mass = 55.5
   >>> is_expressed = True      # or False, notice capital letters
   >>> gene_name = 'BRCA1'

In Python, you don't have to declare type. Python figures out the type
automatically. Check using the ``type()`` function:

.. code-block:: python3

   >>> type(gene_count)
   <class 'int'>
   >>> type(protein_mass)
   <class 'float'>
   >>> type(is_expressed)
   <class 'bool'>
   >>> type(gene_name)
   <class 'str'>

Print the values of each variable using the ``print()`` function:

.. code-block:: python3

   >>> print(gene_count)
   42
   >>> print('gene_count')
   gene_count

(Try printing the others as well). And, notice what happens when we print with
and without single quotes? What is the difference between ``gene_count`` and
``'gene_count'``?

You can convert between types using a few different functions. For example, when
you read in data from a file, numbers are often read as strings. Thus, you may
want to convert the string to integer or float as appropriate:

.. code-block:: python3

   >>> str(gene_count)      # convert int to string
   >>> str(protein_mass)    # convert float to string
   >>> type(gene_count)
   >>> type(protein_mass)

What do you notice about the above ``type()`` commands? Is the output what you expected?

Using ``str()`` prints a string of the original variable to the console, but it does not actually change the original variable itslef —
``gene_count`` and ``protein_mass`` are still whatever you assigned earlier (an integer and a float, respectively).

If you want ``gene_count`` and ``protein_mass`` to become strings, you must reassign the variable:

.. code-block:: python3

   >>> gene_count = str(gene_count)
   >>> protein_mass = str(protein_mass)
   >>> type(gene_count)
   >>> type(protein_mass)

Alternatively, you can assign new variables as a different type of the original variable:

.. code-block:: python3

   >>> gene_count_new = int(gene_count)
   >>> type(gene_count)
   >>> type(gene_count_new)
   >>>
   >>> protein_mass_new = float(protein_mass)
   >>> type(protein_mass)
   >>> type(protein_mass_new)

Arithmetic Operations
---------------------

Next, we will look at some basic arithmetic. You may be familiar with the
standard operations from other languages:

.. code-block:: text
   :emphasize-lines: 1

   Operator   Function          Example   Result
   +          Addition          1+1       2
   -          Subtraction       9-5       4
   *          Multiplication    2*2       4
   /          Division          8/4       2
   **         Exponentiation    3**2      9
   %          Modulus           5%2       1
   //         Floor division    5//2      2


Try a few things to see how they work:

.. code-block:: python3

   >>> print(2+2)
   >>> print(355/113)
   >>> print(10%9)
   >>> print(3+5*2)
   >>> print('ATGC' + 'CGTA')
   >>> print('gene' + str(1))
   >>> print('A' * 5)

Also, carefully consider how arithmetic options may affect type:

.. code-block:: python3

   >>> concentration1 = 5/2
   # What output do we expect from the following commands?

   >>> type(concentration1)
   >>> print(concentration1)

   >>> concentration2 = 6/2
   >>> type(concentration2)
   >>> print(concentration2)

.. admonition:: Check Your Understanding

   Which operator can we use if we want ``concentration2`` to to be an integer instead of a float?

Lists and Dictionaries
----------------------

**Lists** are a data structure in Python that can contain multiple elements.
They are ordered, they can contain duplicate values, and they can be modified.
Declare a list with square brackets as follows:

.. code-block:: python3

   >>> gene_list = ['BRCA1', 'TP53', 'EGFR', 'MYC']
   >>> type(gene_list)
   <class 'list'>
   >>> print(gene_list)
   ['BRCA1', 'TP53', 'EGFR', 'MYC']

Access individual list elements:

.. code-block:: python3

   >>> print(gene_list[0])
   BRCA1
   >>> type(gene_list[0])
   <class 'str'>
   >>> print(gene_list[2])
   EGFR

Create an empty list and add things to it:

.. code-block:: python3

   >>> expression_levels = []
   >>> expression_levels.append(5.2)     # 'append()' is a method of the list class
   >>> expression_levels.append(3.8)
   >>> expression_levels.append(12.1)
   >>> expression_levels.append(2**2)
   >>> print(expression_levels)
   [5.2, 3.8, 12.1, 4]
   >>> type(expression_levels)
   <class 'list'>
   >>> type(expression_levels[1])
   <class 'float'>

Lists are not restricted to containing one data type. Combine the lists together
to demonstrate:

.. code-block:: python3

   >>> mixed_data = gene_list + expression_levels
   >>> print(mixed_data)
   ['BRCA1', 'TP53', 'EGFR', 'MYC', 5.2, 3.8, 12.1, 4]

Another way to access the contents of lists is by slicing. Slicing supports a
start index, stop index, and step taking the form: ``mylist[start:stop:step]``.
Only the first colon is required. If you omit the start, stop, or :step, it is
assumed you mean the beginning, end, and a step of 1, respectively. Here are
some examples of slicing:

.. code-block:: python3

   >>> dna_sequence = ['A', 'T', 'G', 'C', 'A', 'A', 'A']
   >>> print(dna_sequence[0:2])     # returns the first two bases
   ['A', 'T']
   >>> print(dna_sequence[:2])      # if you omit the start index, it assumes the beginning
   ['A', 'T']
   >>> print(dna_sequence[-2:])     # returns the last two bases (omit the stop index and it assumes the end)
   ['A', 'A']
   >>> print(dna_sequence[:])       # returns the entire sequence
   ['A', 'T', 'G', 'C', 'A', 'A', 'A']
   >>> print(dna_sequence[::2])     # return every other base (step = 2)
   ['A', 'G', 'A', 'A']

.. note::

   If you slice from a list, it returns an object of type list. If you access a
   list element by its index, it returns an object of whatever type that element
   is. The choice of whether to slice from a list, or iterate over a list by
   index, will depend on what you want to do with the data.


**Dictionaries** are another data structure in Python that contain key:value
pairs. They maintain the order in which items were inserted (as of Python 3.7), they cannot contain duplicate keys, and they
can be modified. Create a new dictionary using curly brackets:

.. code-block:: python3

   >>> gene_info = {
   ...   'name': 'BRCA1',
   ...   'chromosome': 17,
   ...   'function': 'DNA repair',
   ...   'disease': 'breast cancer'
   ... }
   >>> type(gene_info)
   <class 'dict'>
   >>> print(gene_info)
   {'name': 'BRCA1', 'chromosome': 17, 'function': 'DNA repair', 'disease': 'breast cancer'}
   >>> print(gene_info['name'])
   BRCA1

As your data changes over time, so too can values stored in dictionaries.
Add new key:value pairs to the dictionary as follows:

.. code-block:: python3

   >>> gene_info['protein_length'] = 1863
   >>> print(gene_info['protein_length'])
   1863


Many other methods exist to access, manipulate, interpolate, copy, etc., lists
and dictionaries. We will learn more about them out as we encounter them later
in this course.

Conditionals and Control Loops
------------------------------

Python **comparison operators** allow you to add conditions into your code in
the form of ``if`` / ``elif`` / ``else`` statements. Valid comparison operators
include:

.. code-block:: text
   :emphasize-lines: 1

   Operator   Comparison                 Example   Result
   ==         Equal                      1==2       False
   !=         Not equal                  1!=2       True
   >          Greater than               1>2        False
   <          Less than                  1<2        True
   >=         Greater than or equal to   1>=2       False
   <=         Less Than or equal to      1<=2       True

A valid conditional statement might look like:

.. code-block:: python3

   >>> expression1 = 10.5
   >>> expression2 = 20.3
   >>>
   >>> if (expression1 > expression2):           # notice the colon
   ...     print('expression1 is higher')        # notice the indent
   ... elif (expression2 > expression1):
   ...     print('expression2 is higher')
   ... else:
   ...     print('expression levels are equal')


In addition, conditional statements can be combined with **logical operators**.
Valid logical operators include:

.. code-block:: text
   :emphasize-lines: 1

   Operator   Description                           Example
   and        Returns True if both are True         a < b and c < d
   or         Returns True if at least one is True  a < b or c < d
   not        Negate the result                     not( a < b )

For example, consider the following code:

.. code-block:: python3

   >>> expression1 = 10.5
   >>> expression2 = 20.3
   >>>
   >>> if (expression1 < 100 and expression2 < 100):
   ...     print('both expression levels are below threshold')
   ... else:
   ...     print('at least one expression level exceeds threshold')

The ``not`` operator negates a boolean value. For example:

.. code-block:: python3

   >>> expression1 = 10.5
   >>> expression2 = 20.3
   >>>
   >>> if not (expression1 > expression2):
   ...     print('expression1 is not higher than expression2')
   >>> else:
   ...   print('expression1 is higher than expression2')

.. admonition:: Check Your Understanding

   What output do you expect from the following command?

   .. code-block:: python3

      >>> expression1 = 10.0
      >>> expression2 = 20.0
      >>> threshold = 15.0
      >>>
      >>> if expression1 < threshold and expression2 > threshold:
      ...     if expression2 > expression1 * 2:
      ...         print('High gene activation')
      ...     else:
      ...         print('Moderate gene activation')
      >>> elif expression1 >= threshold or expression2 < threshold:
      ...     print('Threshold check failed')
      >>> else:
      ...     print('Error: No match')

----

**While loops** also execute according to conditionals.
They will continue to execute as long as a condition is True. 

For example:

.. code-block:: python3

   >>> base_count = 0                     
   >>>
   >>> while (base_count < 10):           
   ...     print(base_count)              
   ...     base_count = base_count + 1    

Let's trace through what happens step-by-step:

* **Initial state**: ``base_count = 0``
* **Iteration 1**: Check ``0 < 10`` → True, so print ``0``, then set ``base_count = 1``
* **Iteration 2**: Check ``1 < 10`` → True, so print ``1``, then set ``base_count = 2``
* **Iteration 3**: Check ``2 < 10`` → True, so print ``2``, then set ``base_count = 3``
* ... (continues for iterations 4-9) ...
* **Iteration 10**: Check ``10 < 10`` → False, so exit the loop

.. tip::

   **Important**: Notice that we increment ``base_count`` inside the loop. If we forgot to do this, 
   ``base_count`` would always be 0, the condition ``0 < 10`` would always be True, and the loop 
   would run forever (an infinite loop)! Always make sure your while loop has a way to eventually 
   make the condition False.

   If you get stuck, you can terminate a process in Linux with ``control`` + ``C``.

The ``break`` statement can also be used to escape loops:

.. code-block:: python3

   >>> base_count = 0
   >>>
   >>> while (base_count < 10):
   ...     print(base_count)
   ...     base_count = base_count + 1
   ...     if (base_count==10):
   ...         break
   ...     else:
   ...         continue

----

**For loops** in Python are useful when you need to execute the same set of
instructions over and over again. They are especially great for iterating over
lists:

.. code-block:: python3

   >>> gene_list = ['BRCA1', 'TP53', 'EGFR', 'MYC']
   >>>
   >>> for gene in gene_list:
   ...     print(gene)
   >>>
   >>> for gene in gene_list:
   ...     if (gene == 'TP53'):
   ...         pass                    # do nothing
   ...     else:
   ...         print(gene)

You can also use the ``range()`` function to iterate over a range of numbers.
This function can take one, two, or three arguments:

* ``range(stop)`` -- starts at 0, goes up to (but not including) stop, increments by 1
* ``range(start, stop)`` -- starts at start, goes up to (but not including) stop, increments by 1
* ``range(start, stop, step)`` -- starts at start, goes up to (but not including) stop, increments by step

Here are some examples:

.. code-block:: python3

   >>> for i in range(10):
   ...     print(i)
   # Prints: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
   >>>
   >>> for position in range(10, 100, 5):
   ...     print(position)
   # Prints: 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95

**Nested loops** are loops inside other loops. The inner loop completes all its iterations for each
iteration of the outer loop. This is useful when you need to iterate over multiple dimenensions of data.

For example, if you have three replicates of three samples under three conditions, you can print all combinations of
replicates, samples, and conditions like so:

.. code-block:: python3

   >>> for replicate in range(1,4):
   ...     for sample in range(1,4):
   ...         for condition in range(1,4):
   ...             print( f'Replicate {replicate}, Sample {sample}, Condition {condition}' )

In the code above, the ``f''`` prefix before a string creates an **f-string** (formatted string literal),
which allows you to embed Python expressions directly inside the string. Any expression inside curly braces 
``{}`` will be evaluated and inserted into the string. 

.. note::

   The code is getting a little bit more complicated now. It will be better to
   stop running in the interpreter's interactive mode, and start writing our
   code in Python scripts.


Functions
---------

**Functions** are blocks of codes that are run only when we call them. We can
pass data into functions, and have functions return data to us. Functions are
absolutely essential to keeping our code clean and organized.

On the command line, use a text editor to start writing a Python script:

.. code-block:: console

   [mbs-337]$ vim function_test.py


Enter the following text into the script:

.. code-block:: python3
   :linenos:

   def print_gene_name():
       print('BRCA1')

   print_gene_name()

After saving and quitting the file, execute the script with the ``python3`` executable:

.. code-block:: console

   [mbs-337]$ python3 function_test.py
   BRCA1

.. note::

   Future examples from this point on will assume familiarity with using the
   text editor and executing the script. We will just be showing the contents of
   the script and console output.

More advanced functions can take parameters and return results. Before we look at an example,
let's understand **dot notation** and **methods**. 

**Dot Notation and Methods**

In Python, many data types have built-in **methods** -- functions that are attached to the data
itself. You call a method using **dot notation**: ``variable.method()``

For example, strings have a ``.count()`` method that counts how many times a character or substring appears:

.. code-block:: python3

   >>> dna_seq = 'ATGCGATCGATCG'
   >>> len(dna_seq)           # len() function counts characters in a string
   13
   >>> dna_seq.count('G')     # .count() method counts how many 'G' characters are in the string
   4
   >>> dna_seq.count('AT')    # you can also count substrings
   3

.. admonition:: Terminology

   **Methods vs Functions**: Methods are called with dot notation (``string.count()``), while functions
   are called directly (``len(string)``). Both ``len()`` and ``.count()`` can give you information
   about a string, but they're used differently. 

   Functions like ``len()``, ``print()``, and ``type()`` are **built-in functions** -- they come with
   Python and are always available. Functions you create yourself using ``def`` are **user-defined functions**.
   Both work the same way (they're blocks of code that execute when called), but built-in functions are 
   already written for you, while user-defined ones are ones you write to solve your specific problems. 

Let's write a function to calculate the GC content of our DNA sequence:

.. code-block:: python3
   :linenos:

   def calculate_gc_content(sequence):
       gc_count = sequence.count('G') + sequence.count('C')
       total_bases = len(sequence)
       return (gc_count / total_bases) * 100

   dna_seq = 'ATGCGATCGATCG'
   gc_percent = calculate_gc_content(dna_seq)
   print(f'GC content: {gc_percent:.2f}%')

The function above does the following:

1. The function definition takes on parameter called ``sequence`` (a DNA sequence string)
2. It then counts how many 'G' and 'C' bases are in the string, and adds them together to get the total GC count
3. Then, it calculates the total number of bases in the sequence
4. Finally, it calculates the percentage by dividing GC count by total bases and multiplying by 100. The ``return`` statement sends this value back to whoever called the function.

The ``.2f`` in the f-string formats the number to 2 decimal places.

.. code-block:: console

   GC content: 53.85%

Pass multiple parameters to a function:

.. code-block:: python3
   :linenos:

   def calculate_fold_change(control, treatment):
       return (treatment / control)

   fold_change = calculate_fold_change(10.5, 21.0)
   print(f'Fold change: {fold_change}')

.. code-block:: console

   Fold change: 2.0

It is a good idea to put your list operations into a function in case you plan
to iterate over multiple lists:

.. code-block:: python3
   :linenos:

   def find_genes_starting_with(mylist, prefix):
       for gene in mylist:
           if (gene.startswith(prefix)):      # check if string starts with prefix
               print(gene)

   gene_list1 = ['BRCA1', 'BRCA2', 'TP53', 'EGFR']
   gene_list2 = ['MYC', 'MYCN', 'TP53', 'RB1']

   find_genes_starting_with(gene_list1, 'BRC')
   find_genes_starting_with(gene_list2, 'MYC')

.. code-block:: console

   BRCA1
   BRCA2
   MYC
   MYCN

There are many more ways to call functions, including handing an arbitrary
number of arguments, passing keyword / unordered arguments, assigning default
values to arguments, and more.

File Handling
-------------

The ``open()`` function does all of the file handling in Python. It takes two
arguments - the *filename* and the *mode*. The possible modes are read (``r``),
write (``w``), append (``a``), or create (``x``).

For example, to read a file do the following:


.. code-block:: python3
   :linenos:

   with open('/usr/share/dict/words', 'r') as f:
       for x in range(5):
           print(f.readline())

.. code-block:: text

   1080

   10-point

   10th

   11-point

   12-point

.. tip::

   By opening the file with the ``with`` statement above, you get built in
   exception handling, and it automatically will close the file handle for you.
   It is generally recommended as the best practice for file handling.


You may have noticed in the above that there seems to be an extra space between
each word. What is actually happening is that the file being read has newline
characters on the end of each line (``\n``). When read into the Python script,
the original new line is being printed, followed by another newline added by the
``print()`` function. Stripping the newline character from the original string
is the easiest way to solve this problem:

.. code-block:: python3
   :linenos:

   with open('/usr/share/dict/words', 'r') as f:
       for x in range(5):
           print(f.readline().strip('\n'))

.. code-block:: text

   1080
   10-point
   10th
   11-point
   12-point


Read the whole file and store it as a list:

.. code-block:: python3
   :linenos:

   gene_names = []

   with open('/usr/share/dict/words', 'r') as f:
       gene_names = f.read().splitlines()                # careful of memory usage

   for x in range(5):
       print(gene_names[x])

.. code-block:: text

   1080
   10-point
   10th
   11-point
   12-point


Write output to a new file on the file system; make sure you are attempting to
write somewhere where you have permissions to write:

.. code-block:: python3
   :linenos:

   gene_list = ['BRCA1', 'TP53', 'EGFR', 'MYC']

   with open('gene_list.txt', 'w') as f:
       for gene in gene_list:
           f.write(gene)

.. code-block:: console

   (in gene_list.txt)
   BRCA1TP53EGFRMYC


You may notice the output file is lacking in newlines this time. Try adding
newline characters to your output:

.. code-block:: python3
   :linenos:

   gene_list = ['BRCA1', 'TP53', 'EGFR', 'MYC']

   with open('gene_list.txt', 'w') as f:
       for gene in gene_list:
           f.write( f'{gene}\n' )

.. code-block:: console

   (in gene_list.txt)
   BRCA1
   TP53
   EGFR
   MYC


Now notice that the original line in the output file is gone - it has been
overwritten. Be careful if you are using write (``w``) vs. append (``a``).

Importing Libraries
-------------------

The Python built-in functions, some of which we have seen above, are useful but
limited. Part of what makes Python so powerful is the huge number and variety
of libraries that can be *imported*. For example, if you want to work with
random numbers, you have to import the 'random' library into your code, which
has a method for generating random numbers called 'random'.

.. code-block:: python3
   :linenos:

   import random

   for i in range(5):
       print(random.random())

.. code-block:: bash

   0.47115888799541383
   0.5202615354150987
   0.8892412583071456
   0.7467080997595558
   0.025668541754695906

More information about using the ``random`` library can be found in the
`Python docs <https://docs.python.org/3/library/random.html>`_

Some libraries that you might want to use are not included in the official
Python distribution - called the *Python Standard Library*. Libraries written
by the user community can often be found on `PyPI.org <https://pypi.org/>`_ and
downloaded to your local environment using a tool called ``pip3``.

For example, if you wanted to download the
`BioPython <https://pypi.org/project/biopython/>`_ library (a popular library for
biological data analysis) and use it in your Python
code, you would do the following:

.. code-block:: bash

   [mbs-337]$ pip3 install --user biopython
   Collecting biopython
     Downloading ...
   Installing collected packages: biopython
   Successfully installed biopython-x.x.x

Notice the library is installed above with the ``--user`` flag. The class server
is a shared system and non-privileged users can not download or install packages
in root locations. The ``--user`` flag instructs ``pip3`` to install the library
in your own home directory.

.. code-block:: python3
   :linenos:

   from Bio.Seq import Seq

   dna_sequence = Seq("ATGCGATCGATCG")
   print(f"DNA sequence: {dna_sequence}")
   print(f"Reverse complement: {dna_sequence.reverse_complement()}")


.. code-block:: bash

   DNA sequence: ATGCGATCGATCG
   Reverse complement: CGATCGATCGCAT


Exercises
---------

Test your understanding of the materials above by attempting the following
exercises.

* Create a list of ~10 different gene names. Write a function (using modulus and
  conditionals) to determine if each gene name has an even or odd number of characters. Print to screen
  each gene name followed by the word 'even' or 'odd' as appropriate.
* Using nested for loops and if statements, write a program that iterates over
  every integer from 3 to 100 (inclusive) and prints out the number only if it
  is a prime number. (This could represent finding positions in a sequence that
  are prime-numbered.)
* Create three lists containing 10 expression values each. The first list should contain
  all the integers sequentially from 1 to 10 (inclusive). The second list
  should contain the squares of each element in the first list (representing
  squared fold changes). The third list
  should contain the cubes of each element in the first list. Print all three
  lists side-by-side in three columns. E.g. the first row should contain 1, 1, 1
  and the second row should contain 2, 4, 8.
* Write a script to read in /usr/share/dict/words and print just the last 10
  lines of the file. Write another script to only print words beginning with the
  letters "gen" (hint: this might find some biology-related terms).


Additional Resources
--------------------

* `The Python Standard Library <https://docs.python.org/3/library/>`_
* `PEP 8 Python Style Guide <https://www.python.org/dev/peps/pep-0008/>`_
* `Python3 environment in a browser <https://www.katacoda.com/scenario-examples/courses/environment-usages/python>`_
* `Jupyter Notebooks in a browser <https://jupyter.org/try>`_
* `BioPython Documentation <https://biopython.org/>`_