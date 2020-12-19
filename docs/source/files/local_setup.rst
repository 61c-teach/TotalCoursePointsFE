================
`local_setup.py`
================

This file will generate the roster. It will build the roster based off of the `files/input/calcentral_roster.csv`, `files/input/calcentral_grade_roster.csv`, and `gs_roster.csv` to generate the roster. It will place the roster at `files/roster.csv`. It will then upload the 'submissions' to the Total Course Points Gradescope assignment for each student so they can view how they are doing in your course.

This file has some parameters which it takes in: `regen` and `sync`:

`regen`
=======

This will only regenerate the `files/roster.csv` file. It will not attempt to upload anything to Gradescope.

`sync`
======

This option will only upload submissions to students who are in the roster but do not have any submission. This is very useful for if you need to give some students submissions but you do not want other students to have a record of previous runs of TCP.