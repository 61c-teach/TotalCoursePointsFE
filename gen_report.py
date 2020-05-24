from TotalCoursePoints.grade_bins import Bin, GradeBins
import pandas as pd
import pickle
with open("c.data", "rb") as f:
    c = pickle.load(f)

grade_bins = GradeBins(bins = 
    [
        Bin("A+", 4.0, 290,  None), 
        Bin("A",  4.0, 270,  290),
        Bin("A-", 3.7, 260,  270),
        Bin("B+", 3.3, 250,  260),
        Bin("B",  3.0, 230,  250),
        Bin("B-", 2.7, 220,  230),
        Bin("C+", 2.3, 210,  220),
        Bin("C",  2.0, 190,  210),
        Bin("C-", 1.7, 180,  190),
        Bin("D",  1.0, 140,  180),
        Bin("F",  0.0, None, 140)
    ],
    pass_threshold = 180,
    normal_max_points = 300
)
c.grade_bins = grade_bins

general_increase = 0
a_plus_increase = 0
c.set_raw_additional_pts(general_increase)
c.grade_bins.increment_A_plus(a_plus_increase)

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


c.print_class_statistics(with_hidden=True)



c.dump_student_results("epa_curved_like_raw_to_3.3_bin_adjust.csv", include_assignment_scores=True, with_hidden=True)

comment_sid = {}
epa_scores = []
quest_scores = []
midterm_scores = []
final_scores = []
for student in c.students:
    if not student.active_student:
        continue
    sid = student.sid
    EPA_Score = student.categoryData["EPA"].get_total_score(with_hidden=True)
    exams = student.categoryData["Exams"]
    quest = exams.assignments_data[0].score
    midterm = exams.assignments_data[1].score
    final = exams.assignments_data[2].score
    epa_scores.append((sid, EPA_Score))
    quest_scores.append((sid, quest))
    midterm_scores.append((sid, midterm))
    final_scores.append((sid, final))
def get_top_n(l, n):
    l = sorted(l, reverse=True, key=lambda x: x[1])
    res = []
    prev = l[0][1]
    ctr = 1
    for i in l:
        cur = i[1]
        if len(res) >= n and cur != prev:
            return res
        if prev != cur:
            ctr += 1
        res.append((i[0], ctr))
        prev = cur
    return res
epa_scores = get_top_n(epa_scores, 10)
quest_scores = get_top_n(quest_scores, 10)
midterm_scores = get_top_n(midterm_scores, 10)
final_scores = get_top_n(final_scores, 10)
for name, data in [("EPA", epa_scores), ("Quest", quest_scores), ("Midterm", midterm_scores), ("Final", final_scores)]:
    for sid, rank in data:
        if sid in comment_sid:
            comment_sid[sid] += f" and Num {rank} {name}"
        else:
            comment_sid[sid] = f" and Num {rank} {name}"
def comment_fn(sid):
    if sid in comment_sid.keys():
        return comment_sid[sid]
    return ""
c.gen_calcentral_report("fa19_cs61c_calcentral.csv", "2019-FALL_COMPSCI-61C-001-27519_20191231-1330.csv", comment_fn=comment_fn)