============
`roster.csv`
============

This is the roster of your class. The roster has multiple columns which Total Course Points expects.


Name
====

Type: String

This is the name of the student.

SID
===

Type: String

This is the student's ID. It must be unique as this is the primary grouping key.

Email
=====

Type: String

This is the student's email. This should also be unique though is the second grouping key though is not used by everything.

InCanvas
========

Type: Boolean

This parameter tells you if the student is taking the class. This is required as you may have non-students taking the class but not want to include them into your stats.

ForGrade
========

Type: String

This is the grading option which the student is taking the class for. TCP only supports a few grading options such as GRD, CPN, DPN, EPN, ESU.

Incomplete
==========

Type: Boolean

This is another method of designating that a student is taking an incomplete in your class. I recommend that you do not use this and instead use the post processing to set incompletes.