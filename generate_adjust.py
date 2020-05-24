import pickle
import pandas as pd
with open("c.data", "rb") as f:
    c = pickle.load(f)

incompletes = list(pd.read_csv("dishonesty_incompletes.csv")["SID"])
incompletes += list(pd.read_csv("other_incompletes.csv")["SID"])
for sid in incompletes:
    s = c.get_student(sid)
    s.incomplete = True

dfrc = pd.read_csv("resolved_cheaters.csv")
resolved_cheaters = list(zip(dfrc["SID"], dfrc["assignments"]))
class dummy:
    def give_zero(self, with_hidden=False):
        return 0
from TotalCoursePoints.utils import Time
for cheater, assignments in resolved_cheaters:
    s = c.get_student(cheater)
    s.categoryData["EPA"].get_total_score = dummy().give_zero
    exams = s.categoryData["Exams"]
    q = exams.assignments_data[0]
    m = exams.assignments_data[1]
    q.score = q.orig_score
    m.score = m.orig_score
    split_assignments = assignments.split(";")
    for a in split_assignments:
        cat, assign = a.split("/")
        ct = s.categoryData[cat]
        for a in ct.assignments_data:
            if a.assignment.id == assign:
                a.score = -a.assignment.out_of
                a.time = Time()
                break
        else:
            print(f"Unknown assignment: {assignments} for {cheater}")

c.add_ignore_category("EPA")
orig_grade_bins = c.grade_bins.copy()
print("===Current Class Standing:===")
c.print_class_statistics(with_hidden=True)
print("Exporting that roster:")
c.dump_student_results("raw_no_epa.csv", include_assignment_scores=True, with_hidden=True)
print("Determining point adjustment:")
adjustment = c.est_gpa(3.3, start_pts=0, max_pts=100, max_a_plus=50)
if not adjustment:
    raise ValueError("Could not find a max number of points which would satisfy your requirements!")
if isinstance(adjustment, (int, float)):
    adjustment = (adjustment, 0)
print(f"Adjustments: {adjustment}")
c.set_raw_additional_pts(adjustment[0])
c.grade_bins.increment_A_plus(adjustment[1])
print("===Adjusted Raw no EPA Score:===")
c.print_class_statistics(with_hidden=True)
c.dump_student_results("no_epa_curved_to_3.3.csv", include_assignment_scores=True, with_hidden=True)
c.remove_ignore_category("EPA")
c.grade_bins = orig_grade_bins.copy()
c.set_raw_additional_pts(0)
print("===Raw EPA:===")
c.print_class_statistics(with_hidden=True)
c.dump_student_results("raw_with_epa.csv", include_assignment_scores=True, with_hidden=True)
c.set_raw_additional_pts(adjustment[0])
c.grade_bins.increment_A_plus(adjustment[1])
c.print_class_statistics(with_hidden=True)
print("===Curved with EPA:===")
c.dump_student_results("epa_curved_like_raw_to_3.3.csv", include_assignment_scores=True, with_hidden=True)

