from TotalCoursePoints import Assignment, Category, Classroom, Bin, GradeBins, Student, StudentCategoryData

# Example Grade Bins From CS61C
Ap = Bin("A+", 4.0, 290,  None)
A  = Bin("A",  4.0, 270,  290)
Am = Bin("A-", 3.7, 260,  270)
Bp = Bin("B+", 3.3, 250,  260)
B  = Bin("B",  3.0, 230,  250)
Bm = Bin("B-", 2.7, 220,  230)
Cp = Bin("C+", 2.3, 210,  220)
C  = Bin("C",  2.0, 190,  210)
Cm = Bin("C-", 1.7, 180,  190)
D  = Bin("D",  1.0, 140,  180)
F  = Bin("F",  0.0, None, 140)
grade_bins = GradeBins(bins = 
    [Ap, A, Am, Bp, B, Bm, Cp, C, Cm, D, F],
    pass_threshold = Cm.min,
    pass_threshold_map = {
        "EPN": Cm.min,
        "ESU": Bm.min,
        "DPN": Cm.min,
        "CPN": Cm.min,
    },
    normal_max_points = 300,
)