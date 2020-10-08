from TotalCoursePoints import Assignment, Category, Classroom, Bin, GradeBins, Student, StudentCategoryData
from TotalCoursePoints.utils import GSheetBase, GracePeriod, Time
import TotalCoursePoints.assignment as assignment
import numpy as np

# This is to show that you can mutate the classroom after the fact!
def clobber(c: Classroom):
    init_str = "Applying the clobber..."
    print(init_str)
    exams = c.get_category("Exams")
    midterm = exams.get_assignment("midterm 1")
    final = exams.get_assignment("final")
    midterm_mean, _, midterm_stddev, _, _ = midterm.get_stats()

    tmp = [score for score in final.scores if score and score > 0]
    final_mt_mean = np.mean(tmp)
    final_mt_median = np.median(tmp)
    final_mt_stddev = np.std(tmp)
    final_mt_max = np.max(tmp)
    final_mt_min = np.min(tmp)
    final_mt_stats = [final_mt_mean, final_mt_median, final_mt_stddev, final_mt_max, final_mt_min, len(tmp)]
    final_mt_stats_str = f"Final Clobber Stats:\n" + "mean: {}\nmedian: {}\nstd dev: {}\nmax: {}\nmin: {}\ncount: {}\n".format(*final_mt_stats)
    print(final_mt_stats_str) 

    potrs = lambda main_subscore, main_mean, main_stddev, orig_mean, orig_stddev: (main_subscore - main_mean) / main_stddev * orig_stddev + orig_mean

    clobber_count = 0
    print("Applying clobber to each student...")
    for student in c.students:
        final_score = final.get_student_data(student).score

        if not final_score:
            final_score = 0
        

        fi_mt_prs = potrs(final_score, final_mt_mean, final_mt_stddev, midterm_mean, midterm_stddev)
        
        if final_score <= 0:
            fi_mt_prs = 0

        middata = midterm.get_student_data(student)
        middata.orig_score = middata.score


        # Midterm
        new_score = min(midterm.out_of, max(middata.score, fi_mt_prs))
        middata.append_comment(f"Original Midterm Score: {middata.score}\n")
        middata.append_comment(f"Clobber Score from Final: {fi_mt_prs}")
        if middata.score != new_score:
            if new_score == fi_mt_prs:
                clobber_count += 1
            middata.append_comment(f"Nice job on the clobber!")
            # print(f"Found a clobber! Old Score: {middata.score}, New Score: {new_score}; Student: {student}")
        middata.score = new_score

    print(f"{clobber_count} Received a clobber!")
    
    print(f"{init_str}Done!")