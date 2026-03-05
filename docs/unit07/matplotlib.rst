Plotting with Matplotlib
========================

Matplotlib a graphing library for Python. It has a nice collection of tools that you can use to
create anything from simple graphs, to scatter plots, to 3D graphs. It is used heavily in
the scientific Python community for data visualization.


Using Matplotlib
----------------

.. tip::

   An easy place to test the examples below is by starting up a notebook on your Linux VM
   or in a browser-based `Jupyter notebook <https://jupyter.org/>`_.


First install matplotlib with pip. Installing matplotlib will install some other
dependencies as well, including numpy which is a library with support for arrays
and high-level mathematical functions.

.. note::

  If you went through the previous section, you should have already installed matplotlib as
  part of the requirements for that section.

.. code-block:: console

   [mbs337-vm]$ cd $HOME/mbs-337
   [mbs337-vm]$ source .venv/bin/activate
   (.venv) [mbs337-vm]$ pip3 install matplotlib
   (.venv) [mbs337-vm]$ curl ip.me
   129.114.38.51
   (.venv) [mbs337-vm]$ jupyter lab  # or "jupyter notebook"
   [I 2026-03-01 17:40:03.353 ServerApp] jupyter_lsp | extension was successfully linked.
   [I 2026-03-01 17:40:03.357 ServerApp] jupyter_server_terminals | extension was successfully linked.
   [I 2026-03-01 17:40:03.361 ServerApp] jupyterlab | extension was successfully linked.
   [I 2026-03-01 17:40:03.365 ServerApp] notebook | extension was successfully linked.
   [I 2026-03-01 17:40:03.609 ServerApp] notebook_shim | extension was successfully linked.
   [I 2026-03-01 17:40:03.623 ServerApp] notebook_shim | extension was successfully loaded.
   [I 2026-03-01 17:40:03.625 ServerApp] jupyter_lsp | extension was successfully loaded.
   [I 2026-03-01 17:40:03.626 ServerApp] jupyter_server_terminals | extension was successfully loaded.
   [I 2026-03-01 17:40:03.628 LabApp] JupyterLab extension loaded from /home/ubuntu/mbs-337/.venv/lib/python3.12/site-packages/jupyterlab
   [I 2026-03-01 17:40:03.628 LabApp] JupyterLab application directory is /home/ubuntu/mbs-337/.venv/share/jupyter/lab
   [I 2026-03-01 17:40:03.628 LabApp] Extension Manager is 'pypi'.
   [I 2026-03-01 17:40:03.670 ServerApp] jupyterlab | extension was successfully loaded.
   [I 2026-03-01 17:40:03.673 ServerApp] notebook | extension was successfully loaded.
   [I 2026-03-01 17:40:03.673 ServerApp] Serving notebooks from local directory: /home/ubuntu/mbs-337
   [I 2026-03-01 17:40:03.673 ServerApp] Jupyter Server 2.17.0 is running at:
   [I 2026-03-01 17:40:03.673 ServerApp] http://mbs-337-15:8888/lab
   [I 2026-03-01 17:40:03.673 ServerApp]     http://127.0.0.1:8888/lab
   [I 2026-03-01 17:40:03.674 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).

Go to a browser and enter the following URL to access the Jupyter Notebook/Lab interface using the public IP
address of your Linux VM (that you got from the ``curl ip.me`` command above):

.. code-block:: text

   http://<your-vm-public-ip>:8888/lab  # or "http://<your-vm-public-ip>:8888/tree" for the classic notebook interface


Simple Plots
------------

Plot a simple sin wave:

.. code-block:: python3

   import matplotlib.pyplot as plt
   import numpy as np

   x = np.linspace(0, 2*np.pi, 50)
   plt.plot(x, np.sin(x))


Continuing from the same file, plot two graphs on the same axis:

.. code-block:: python3

   plt.plot(x, np.sin(x), x, np.sin(2*x))

Change the colors and add markers:

.. code-block:: python3

   plt.plot(x, np.sin(x), 'r-o', x, np.sin(2*x), 'g--')

Matplotlib supports some built-in colors, and others can be accessed using
HTML hex strings (e.g. ``'#eeefff'``):

+---------+------+
| Color   | Code |
+=========+======+
| Blue    | 'b'  |
+---------+------+
| Green   | 'g'  |
+---------+------+
| Red     | 'r'  |
+---------+------+
| Cyan    | 'c'  |
+---------+------+
| Magenta | 'm'  |
+---------+------+
| Yellow  | 'y'  |
+---------+------+
| Black   | 'k'  |
+---------+------+
| White   | 'w'  |
+---------+------+

Built-in line codes:

+----------+--------+
| Line     | Code   |
+==========+========+
| Solid    | '-'    |
+----------+--------+
| Dashed   | '--'   |
+----------+--------+
| Dash-dot | '-.'   |
+----------+--------+
| Dotted   | ':'    |
+----------+--------+
| No line  | 'None' |
+----------+--------+

And marker codes:

+-----------------+--------+
| Marker          | Code   |
+=================+========+
| Point           | '.'    |
+-----------------+--------+
| Pixel           | ','    |
+-----------------+--------+
| Circle          | 'o'    |
+-----------------+--------+
| Triangle down   | 'v'    |
+-----------------+--------+
| Triangle up     | '^'    |
+-----------------+--------+
| Square          | 's'    |
+-----------------+--------+
| Pentagon        | 'p'    |
+-----------------+--------+
| Star            | '*'    |
+-----------------+--------+
| Diamond         | 'D'    |
+-----------------+--------+
| X marker        | 'x'    |
+-----------------+--------+
| Plus marker     | '+'    |
+-----------------+--------+
| Horizontal line | '_'    |
+-----------------+--------+
| No marker       | 'None' |
+-----------------+--------+


Subplots
--------

Using the subplot() function, we can plot two graphs at the same time within the same "canvas".
Think of the subplots as "tables", each subplot is set with the number of rows, the number of columns,
and the active area, the active areas are numbered left to right, then up to down.

.. code-block:: python3

   plt.subplot(2, 1, 1) # (row, column, active area)
   plt.plot(x, np.sin(x))
   plt.subplot(2, 1, 2) # switch the active area
   plt.plot(x, np.sin(2*x))

Scatter plots
-------------

A simple scatter plot based on the sine function:

.. code-block:: python3

   y = np.sin(x)
   plt.scatter(x,y)

Use random numbers and add a colormap to a scatter plot:

.. code-block:: python3

   x = np.random.rand(1000)
   y = np.random.rand(1000)
   size = np.random.rand(1000) * 50
   color = np.random.rand(1000)
   plt.scatter(x, y, size, color)
   plt.colorbar()

We brought in two new parameters, size and color, which will vary the diameter and the
color of our points. Then adding the colorbar() gives us a nice color legend to the side.


Histograms
----------

A histogram is one of the simplest types of graphs to plot in Matplotlib. All you need to do is pass the hist()
function an array of data. The second argument specifies the amount of bins to use. Bins are intervals of values
that our data will fall into. The more bins, the more bars.

.. code-block:: python3

   plt.hist(x, 50)

Adding Labels and Legends
-------------------------

Plots look much more finished and professional with appropriate labels and
legends added. This is highly recommended for the final project.

.. code-block:: python3

   x = np.linspace(0, 2 * np.pi, 50)
   plt.plot(x, np.sin(x), 'r-x', label='Sin(x)')
   plt.plot(x, np.cos(x), 'g-^', label='Cos(x)')
   plt.legend() # Display the legend.
   plt.xlabel('Rads') # Add a label to the x-axis.
   plt.ylabel('Amplitude') # Add a label to the y-axis.
   plt.title('Sin and Cos Waves') # Add a graph title.


Additional Resources
--------------------

* `Try Jupyter in a Browser <https://jupyter.org/>`_
* `Matplotlib reference documentation <https://matplotlib.org/stable/users/index>`_
