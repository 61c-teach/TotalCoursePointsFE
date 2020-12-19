================
`main_setup.py`
================

This file will generate the classroom data based off how you set up the class. It is default set to pull grades from a Google Sheet though it first checks to see if you have a grade csv in the `files/inputs` directory first.

`stats`
=======

If you add this parameter, it will also print out the bins and other class statistics when it builds the data. It used to always do this though Gradescope was having issues where builds would hang so I changed it to a parameter.