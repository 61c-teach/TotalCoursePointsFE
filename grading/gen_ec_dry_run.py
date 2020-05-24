from grading.utils.merge_gs_canvas import merge_gs_canvas_grades
from files.constants import DATA_PATH, INPUT_PATH
pt_0 = "[DRY RUN] Final Exam Part 0 - TAKE THIS FIRST. (8098815)"
pt_1 = "[DRY RUN] Final Exam Part 1 (8098840)"
def merge(data):
    if data[pt_0] > 0 and data[pt_1] > 0:
        return 1
    return 0
merge_gs_canvas_grades(f"{DATA_PATH}/ec_final_dry_run.csv", f"{INPUT_PATH}/gs_template.csv", f"{INPUT_PATH}/canvas_grades.csv", [pt_0, pt_1], merging_fn=merge)