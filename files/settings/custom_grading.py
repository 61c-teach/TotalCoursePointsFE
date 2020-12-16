from TotalCoursePoints import Classroom, Student, Category, Assignment, StudentAssignmentData
from files.constants import CDATA_FILE, DISHONESTY_INCOMPLETES_FILE, OTHER_INCOMPLETES_FILE, RESOLVED_CHEATERS_FILE
import pickle
import pandas as pd

from TotalCoursePoints.utils import Time

def custom_grading(c: Classroom):
    """
    This function is useful if you want to modify add custom grading to your class data.
    """
    pass