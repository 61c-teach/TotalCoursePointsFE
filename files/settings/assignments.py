from TotalCoursePoints import Assignment, Category, Classroom, Bin, GradeBins, Student, StudentCategoryData
from TotalCoursePoints.utils import GSheetBase, GracePeriod, Time

def add_assignments(c: Classroom):
    epa = Category(
        "EPA", 
        comment="We will not be releasing details of how we distribute EPA! Also it does not show up in your total points calculation but it IS calculated into the estimated grade.",
        hidden=True)
    epa.add_assignments([
        Assignment("Effort", epa, course_points=3),
        Assignment("Participation", epa, course_points=3),
        Assignment("Altruism", epa, course_points=3),
    ])
    c.add_category(epa)

    exams = Category("Exams")
    exams.add_assignments([
        Assignment("midterm 1", exams, out_of=68, course_points=30),
        Assignment("midterm 2", exams, out_of=60, course_points=30),
        Assignment("final", exams, out_of=121, course_points=75)
    ])
    c.add_category(exams)

    gshomeworks = Category("Gradescope Homeworks", course_points=30, grace_period=GracePeriod(time=Time(minutes=30)))
    gshomeworks.add_assignments([
        Assignment("hw1", gshomeworks, name="HW1 - Number Representations", out_of=57, percentage=True),
        Assignment("hw2", gshomeworks, name="HW2 - C Concepts", out_of=48, percentage=True),
        Assignment("hw3", gshomeworks, name="HW3 - Floating Point", out_of=18, percentage=True),
        Assignment("hw4", gshomeworks, name="HW4 - RISC-V", out_of=33, percentage=True),
        Assignment("hw5", gshomeworks, name="HW5 - Logic, Timing", out_of=33, percentage=True),
        Assignment("hw6", gshomeworks, name="HW6 - RISC-V Datapath", out_of=15, percentage=True),
        Assignment("hw7", gshomeworks, name="HW7 - Caches", out_of=105, percentage=True),
        Assignment("hw8", gshomeworks, name="HW8 - Virtual Memory", out_of=32, percentage=True),
        Assignment("hw9", gshomeworks, name="HW9 - Performance Programming", out_of=44, percentage=True),
        Assignment("hw10", gshomeworks, name="HW10 - Parity, and ECC", out_of=26, percentage=True)
    ])
    c.add_category(gshomeworks)

    labs = Category("Labs", course_points=15, out_of=2, late_interval=Time(days=7), late_penalty=1/2, grace_period=GracePeriod(time=Time(minutes=30)), drop_lowest_n_assignments=1)
    labs.add_assignments([
        Assignment("lab00", labs, name="Lab 0: Intro and Setup", percentage=True),
        Assignment("lab01", labs, name="Lab 1: Number Representation, C, CGDB", percentage=True),
        Assignment("lab02", labs, name="Lab 2: Advanced C", percentage=True),
        Assignment("lab03", labs, name="Lab 3: None - President's Day", course_points=0),
        Assignment("lab04", labs, name="Lab 4: RISC-V Assembly", percentage=True),
        Assignment("lab05", labs, name="Lab 5: RISC-V Functions, Pointers", percentage=True),
        Assignment("lab06", labs, name="Lab 6: Logisim", percentage=True),
        Assignment("lab07", labs, name="Lab 7: Pipelining and CPU", percentage=True),
        Assignment("lab08", labs, name="Lab 8: None - Spring Break", course_points=0),
        Assignment("lab09", labs, name="Lab 9: Caches", percentage=True),
        Assignment("lab10", labs, name="Lab 10: None", course_points=0),
        Assignment("lab11", labs, name="Lab 11: Virtual Memory", percentage=True),
        Assignment("lab12", labs, name="Lab 12: SIMD Instructions", percentage=True),
        Assignment("lab13", labs, name="Lab 13: Thread-Level Parallelism", percentage=True),
    ])
    c.add_category(labs)

    projects = Category("Projects", late_penalty=1/3, max_slip_count=6, grace_period=GracePeriod(time=Time(minutes=30)))
    projects.add_assignments([
        Assignment("proj1", projects, course_points=30, out_of=100, allowed_slip_count=3),

        Assignment("proj2A", projects, course_points=30 * 0.5, out_of=100, allowed_slip_count=3),
        Assignment("proj2B", projects, course_points=30 * 0.5, out_of=100, allowed_slip_count=3),

        Assignment("proj3A", projects, course_points=30 * 0.2, out_of=20, allowed_slip_count=3),
        Assignment("proj3B", projects, course_points=30 * 0.8, out_of=80, allowed_slip_count=3),

        Assignment("proj4", projects, course_points=30, out_of=100, allowed_slip_count=6),
    ])
    c.add_category(projects)

    extra_credit = Category("Extra Credit", extra_credit=True)
    extra_credit.add_assignments([
        Assignment("Course Evals", extra_credit, name="80% on Course Evals", comment="Only reached 64.17%. :'(", out_of=1),
        Assignment("Final Dry Run", extra_credit, name="Final Dry Run", out_of=1),
    ])
    c.add_category(extra_credit)

    vepa = Category(
        "Visible EPA",
        comment="This is the EPA tokens we see you have.\nPlease note that the points ARE NOT a 1 to 1 mapping to real course points. We are keeping that private.\n\n",
        extra_credit=True,
        course_points=3,
        late_penalty=0,
    )
    vepa.add_assignments([
        Assignment("EPA Week 1", vepa, out_of=1),
        Assignment("EPA Week 2", vepa, out_of=1),
        Assignment("EPA Week 3", vepa, out_of=1),
        Assignment("EPA Week 4", vepa, out_of=1),
        Assignment("EPA Week 5", vepa, out_of=1),
        Assignment("EPA Week 6", vepa, out_of=1),
        Assignment("EPA Week 7", vepa, out_of=1),
        Assignment("EPA Week 8", vepa, out_of=1),
        Assignment("EPA Week 9", vepa, out_of=1),
        Assignment("EPA Week 10", vepa, out_of=1),
        Assignment("EPA Week 11", vepa, out_of=1),
        Assignment("EPA Week 12", vepa, out_of=1),
        Assignment("EPA Week 13", vepa, out_of=1),
        Assignment("EPA Week 14", vepa, out_of=1),
        Assignment("EPA Week 15", vepa, out_of=1),
    ])
    c.add_category(vepa)