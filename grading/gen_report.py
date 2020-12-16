from TotalCoursePoints.grade_bins import Bin, GradeBins
import pandas as pd
import pickle
from grading.utils.fix_cheating_incompletes import fix_cheating_and_incompletes
from files.constants import *

default_bins = False

def main():
    with open(CDATA_FILE, "rb") as f:
        c = pickle.load(f)

    if default_bins:
        from files.settings.grade_bins import grade_bins
    else:
        Ap = Bin("A+", 4.0, 320,  None)
        A  = Bin("A",  4.0, 265,  320)
        Am = Bin("A-", 3.7, 258,  265)
        Bp = Bin("B+", 3.3, 250,  258)
        B  = Bin("B",  3.0, 235,  250)
        Bm = Bin("B-", 2.7, 225,  235)
        Cp = Bin("C+", 2.3, 205,  225)
        C  = Bin("C",  2.0, 190,  205)
        Cm = Bin("C-", 1.7, 180,  190)
        D  = Bin("D",  1.0, 150,  180)
        F  = Bin("F",  0.0, None, 150)
        grade_bins = GradeBins(bins = 
            [Ap, A, Am, Bp, B, Bm, Cp, C, Cm, D, F],
            pass_threshold = Cm.min,
            pass_threshold_map = {
                "EPN": Cm.min,
                "ESU": Bm.min,
                "DPN": Cm.min,
            },
            normal_max_points = 300,
        )
    c.grade_bins = grade_bins

    general_increase = 42
    a_plus_increase = 0

    c.set_raw_additional_pts(general_increase)
    c.grade_bins.increment_A_plus(a_plus_increase)


    # Fixed in class data generation.
    # fix_cheating_and_incompletes(c)


    c.print_class_statistics(with_hidden=True, include_pnp=False)


    c.dump_student_results(REPORT_EPA_CURVED_BIN_ADJ_FILE, include_assignment_scores=True, with_hidden=True)

    # return

    comment_sid = {}
    epa_scores = []
    midterm1_scores = []
    midterm2_scores = []
    final_scores = []
    for student in c.students:
        if not student.active_student:
            continue
        sid = student.sid
        EPA_Score = student.categoryData["EPA"].get_total_score(with_hidden=True)
        exams = student.categoryData["Exams"]
        midterm1 = exams.assignments_data[0].score
        midterm2 = exams.assignments_data[1].score
        final = exams.assignments_data[2].score
        epa_scores.append((sid, EPA_Score))
        midterm1_scores.append((sid, midterm1))
        midterm2_scores.append((sid, midterm2))
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
    midterm1_scores = get_top_n(midterm1_scores, 10)
    midterm2_scores = get_top_n(midterm2_scores, 10)
    final_scores = get_top_n(final_scores, 10)
    for name, data in [("Midterm 1", midterm1_scores), ("Midterm 2", midterm2_scores), ("Final", final_scores)]:
        for sid, rank in data:
            if sid in comment_sid:
                comment_sid[sid] += f" and Num {rank} {name}"
            else:
                comment_sid[sid] = f" and Num {rank} {name}"
    def comment_fn(sid):
        if sid in comment_sid.keys():
            return comment_sid[sid]
        return ""
    c.gen_calcentral_report(CALCENTRAL_GRADE_REPORT_FILE, CALCENTRAL_GRADE_ROSTER_FILE, comment_fn=comment_fn)

if __name__ == "__main__":
    main()