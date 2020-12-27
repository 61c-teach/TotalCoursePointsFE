import pickle
import pandas as pd
from grading.utils.fix_cheating_incompletes import fix_cheating_and_incompletes
from files.constants import *

def main():
    with open(CDATA_FILE, "rb") as f:
        c = pickle.load(f)

    # Done now in main_setup.py
    # fix_cheating_and_incompletes(c)

    c.add_ignore_category("EPA")
    c.add_ignore_category("Extra Credit")
    c.add_ignore_category("Visible EPA")
    orig_grade_bins = c.grade_bins.copy()

    print("===Current Class Standing:===")
    c.print_class_statistics(with_hidden=True)

    print("Exporting that roster:")
    c.dump_student_results(REPORT_RAW_NO_EPA_FILE, include_assignment_scores=True, with_hidden=True)
    print("Determining point adjustment:")
    adjustment = c.est_gpa(3.3, start_pts=0, max_pts=100, max_a_plus=4)
    if adjustment is False:
        raise ValueError("Could not find a max number of points which would satisfy your requirements!")
    if isinstance(adjustment, (int, float)):
        adjustment = (adjustment, 0)
    print(f"Adjustments: {adjustment}")
    c.set_raw_additional_pts(adjustment[0])
    c.grade_bins.increment_A_plus(adjustment[1])

    print("===Adjusted Raw no EPA Score:===")
    c.print_class_statistics(with_hidden=True)
    c.dump_student_results(REPORT_NO_EPA_CURVED_FILE, include_assignment_scores=True, with_hidden=True)

    return

    c.remove_ignore_category("EPA")
    c.remove_ignore_category("Extra Credit")
    c.remove_ignore_category("Visible EPA")
    c.grade_bins = orig_grade_bins.copy()
    c.set_raw_additional_pts(0)

    print("===Raw EPA:===")
    c.print_class_statistics(with_hidden=True)
    c.dump_student_results(REPORT_RAW_EPA_FILE, include_assignment_scores=True, with_hidden=True)


    c.set_raw_additional_pts(adjustment[0])
    c.grade_bins.increment_A_plus(adjustment[1])
    c.print_class_statistics(with_hidden=True)

    print("===Curved with EPA:===")
    c.dump_student_results(REPORT_EPA_CURVED_FILE, include_assignment_scores=True, with_hidden=True)

if __name__ == "__main__":
    main()