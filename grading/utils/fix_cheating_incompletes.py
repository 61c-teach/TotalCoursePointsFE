from TotalCoursePoints import Classroom
import pandas as pd
import os
from files.constants import *

dishonesty_incompletes_file = DISHONESTY_INCOMPLETES_FILE
other_incompletes_file = OTHER_INCOMPLETES_FILE
resolved_cheaters_file = RESOLVED_CHEATERS_FILE

def fix_cheating_and_incompletes(c: Classroom):
    print("Fixing cheating and incompletes...")
    if os.path.exists(dishonesty_incompletes_file):
        incompletes = list(pd.read_csv(dishonesty_incompletes_file)["SID"])
        for sid in incompletes:
            s = c.get_student(sid)
            s.append_comment("You have been given an incomplete due to suspected academic dishonesty.")
            s.incomplete = True

    if os.path.exists(other_incompletes_file):
        incompletes = list(pd.read_csv(other_incompletes_file)["SID"])
        for sid in incompletes:
            s = c.get_student(sid)
            s.incomplete = True

    if os.path.exists(resolved_cheaters_file):
        dfrc = pd.read_csv(resolved_cheaters_file)
        """
        The resolved cheaters file must have the following columns:
        SID - The sid of the cheater
        assignments - The list of assignments separated ONLY by a ';' in the form category/assignment.
        For example, if someone cheated on project 1 (Projects/proj1) and the midterm (Exams/midterm), you would input:
        'Projects/proj1;Exams/midterm'
        """
        resolved_cheaters = list(zip(dfrc["Name"], dfrc["Email"], dfrc["SID"], dfrc["assignments"]))
        from TotalCoursePoints.utils import Time
        for name, email, cheater, assignments in resolved_cheaters:
            cheater_str = f"{name} ({email}) [{cheater}]"
            s = c.get_student(cheater)
            if s is None:
                print(f"{cheater_str} is not in the class's roster!")
                continue
            epa = s.categoryData.get("EPA")
            if epa:
                epa.override_score = 0
            else:
                print(f"Could not remove epa as it was not found for {cheater_str}")
            if isinstance(assignments, float):
                raise ValueError(f"Detected a float for {cheater_str}. The CSV must be malformed!")
                # import ipdb; ipdb.set_trace()
            split_assignments = assignments.split(";")
            for atxt in split_assignments:
                cat, assign = atxt.split("/")
                if cat not in s.categoryData:
                    print(f"Unknown category: {cat} for {cheater_str}")
                    continue
                ct = s.categoryData[cat]
                for a in ct.assignments_data:
                    if a.assignment.id == assign:
                        a.append_comment("You have been caught cheating on this assignment!")
                        a.score = -a.assignment.out_of
                        a.time = Time()
                        break
                else:
                    print(f"Unknown assignment: '{atxt}' ({assignments}) for {cheater_str}")