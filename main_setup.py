"""
This file uses the other files to parse student grades.
"""

from TotalCoursePoints import Assignment, Category, Classroom, Bin, GradeBins, Student, StudentCategoryData
import TotalCoursePoints.assignment as assignment
import json
import numpy as np
from TotalCoursePoints.utils import GSheetBase, GracePeriod, Time
import pickle
import re
from grading.utils.fix_cheating_incompletes import fix_cheating_and_incompletes
from files.constants import *

GSheetBase.default_credentials = GSHEET_CREDENTIALS_JSON_FILE

print("=" * 5 + "Building the class data" + "=" * 5)

# We need to import the gradebins from the settings...
from files.settings.grade_bins import *

# Due to limitations in how long a gradescope ag can run and the api limits of google sheets, it is better to keep the grades in the ag locally.
# This has been resolved by precomputing grades on the AG build!
Assignment.default_gsheet_id = GSHEET_ASSIGNMENTS_ID
Assignment.default_gsheet_base = GSheetBase(Assignment.default_gsheet_id)
Assignment.use_gsheet_grades = True

# Next lets create our classroom
c = Classroom("Machine Structures", "CS61C", grade_bins)
c.append_comment("[NOTICE]: The point values of assignments may change!\n\n")
# Next lets grab our assignments
from files.settings.assignments import add_assignments
add_assignments(c)

StudentCategoryData.apply_slip_time = StudentCategoryData.apply_optimal_slip_time

c.load_students_from_roster(ROSTER_FILE)

c.process(with_gsheet_extensions=GSHEET_EXTENSIONS_ID)
# c.process()

# We do not have a clobber this semester!
from files.settings.clobber import clobber
clobber(c)

fix_cheating_and_incompletes(c)

c.print_class_statistics()

c.set_time_now()
print("=" * 5 + f"Class data finished building at {c.get_localized_time()}" + "=" * 5)
import os
os.system(f"mkdir -p {DATA_PATH}")
pickle.dump(c, open(CDATA_FILE, "wb"))
print("=" * 5 + "Finished data setup!" + "=" * 5)