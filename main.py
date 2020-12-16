"""
This file uses the other files to parse student grades.
"""

from TotalCoursePoints import Assignment, Category, Classroom, Bin, GradeBins, Student
from GradescopeBase.Utils import root_dir, submission_dir, results_path
import json
import numpy as np
from TotalCoursePoints.utils import GSheetBase
import pickle
from files.constants import *
from grading.utils.remote_processes import fetch_data

def dump_results(data: dict) -> None:
        jsondata = json.dumps(data, ensure_ascii=False)
        with open(results_path(), "w") as f:
            f.write(jsondata)

def load_class_data(fetch=True):
    if fetch:
        try:
            return pickle.load(fetch_data())
        except Exception as e:
            print("Failed to fetch the remote data!")
            print(e)
            import traceback
            traceback.print_exc
    try:
        with open(CDATA_FILE, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(e)
        print("Failed to load the data!")
        dump_results({"score": 0, "output":"Failed to load the computed classroom data!"})
        exit()


def main(sid=None):
    if sid is None:
        try:
            with open(STUDENT_INPUT_JSON_FILE) as f:
                std = json.load(f)
            sid = std["sid"]
        except Exception as e:
            print(e)
            msg = "Please enter a valid input file!"
            print(msg)
            dump_results({"score": 0, "output":msg})
            return
    
    print(f"Generating report for {sid}")

    c = load_class_data(fetch=False)

    s = c.get_student(sid)

    if s is None:
        msg = "Could not find an entry for the given SID!"
        print(msg)
        dump_results({"score": 0, "output": msg})
        return
    
    print(f"Found student: {s}")

    def check_possible_final_scores(s):
        f = s.categoryData["Exams"].get_assignment_data("final")
        current_points = s.total_points()
        f.append_comment("Here is the relative percentage you need on the final to get the corresponding grade:")
        res = []
        total_possible = f.get_total_possible()
        if total_possible == 0:
            f.append_comment("Could not calculate percentages since you have 0 points!")
            return
        for b in c.grade_bins.get_bins():
            if b.min is not None:
                m = b.min
                percent_needed = ((b.min - current_points) / total_possible) * 100
                if percent_needed > 0:
                    res.append((b.id, percent_needed))
        longest = max([len('%.3f'%(a[1])) for a in res])
        for b, score in res:
            score = '%.3f' % (score)
            score = " " * (longest - len(score)) + score
            f.append_comment(f"{b}{'' if len(b) == 2 else ' '}: {score}%")
    if not c.get_category("Exams").get_assignment("final").is_inputted():
        check_possible_final_scores(s)

    if s is None:
        msg = "Could not find your student information."
        print(msg)
        dump_results({"score": 0, "output":msg})
        return

    s.dump_result(c, class_dist=False, class_stats=True, results_file=results_path())
    print("Report dumpped!")
    
if __name__ == "__main__":
    import sys
    sid = None
    if len(sys.argv) > 1:
        sid = sys.argv[1]
    main(sid)
