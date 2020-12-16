Total Course Points Front End
===================

`TotalCoursePointsFE`_ is a Python codebase which utilizes the TotalCoursePoints API to generate a class's grades at UC Berkeley. It has a Gradescope frontend which allows students to have an updated view of how they are doing in the class.

Features:

-  Local Setup to generate the roster by stitching together different rosters from UC Berkeley. It also uploads what is needed for students to Gradescope.
-  A Main Setup which will grab and generate your classes data so that you have a Classroom object.
-  A Main which is callable by Gradescope so that it can generate a report for the students.
-  Multiple helpful grading scripts in the grading folder.
-  Very customizable as you can add custom code to files/settings/ which can change how your classes assignments and other grading policies are.
-  Is able to pull from a Google Sheets to pull grades and extensions.


Installation
------------

.. code:: sh

   git clone https://github.com/61c-teach/TotalCoursePointsFE.git


Requirements: Python 3.7+.

After you have downloaded it, please modify the settings. Please see "Getting Started" for more information".


Getting Started
---------------

Clone the repo to a folder.


API Documentation
---------------------------

.. toctree::
   :maxdepth: 2

   api/index.rst


How to Contribute
-----------------

Please make sure to take a moment and read the `Code of Conduct`_.

Report Issues
~~~~~~~~~~~~~

Please report bugs and suggest features via the `GitHub Issues`_.

Before opening an issue, search the tracker for possible duplicates. If
you find a duplicate, please add a comment saying that you encountered
the problem as well.

Contribute code
~~~~~~~~~~~~~~~

Please make sure to read the `Contributing Guide`_ before making a pull
request.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _TotalCoursePointsFE: https://github.com/61c-teach/TotalCoursePointsFE
.. _Code of Conduct: https://github.com/61c-teach/TotalCoursePointsFE/blob/master/.github/CODE_OF_CONDUCT.md
.. _GitHub Issues: https://github.com/61c-teach/TotalCoursePointsFE/issues
.. _Contributing Guide: https://github.com/61c-teach/TotalCoursePointsFE/blob/master/.github/CONTRIBUTING.md