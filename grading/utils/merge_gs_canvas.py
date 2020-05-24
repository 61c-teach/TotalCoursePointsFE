import csv

GS_SCORE_COL = "Total Score"
GS_SID_COL = "SID"
GS_STATUS_COL = "Status"
GS_LATENESS_COL = "Lateness (H:M:S)"

GS_GRADED_STATUS = "Graded"
GS_NO_LATENESS = "0:00:00"

CANVAS_SID_COL = "SIS User ID"

def merge_gs_canvas_grades(output_csv_file: str, gs_assignment_csv_file: str, canvas_grades_csv_file: str, canvas_assignment_titles: [str], merging_fn=lambda x: sum(x.values())):
    gs_assignment_data = {}
    # Open and create Gradescope Assignment Data
    print("Loading Gradescope format file...")
    with open(gs_assignment_csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sid = row[GS_SID_COL]
            if sid in gs_assignment_data:
                print(f"[ERROR]: Duplicate SID in GS assignment ({row[GS_SID_COL]})! Ignorring add of {row}.")
            else:
                row[GS_SCORE_COL] = 0
                gs_assignment_data[sid] = row

    print("Loading canvas data and determining score...")
    # Load and merge canvas grades
    with open(canvas_grades_csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sid = row[CANVAS_SID_COL]
            if not sid:
                print(f"[WARNING]: Skipping row with null sid: {row}")
                continue
            assignments = {}
            for a in canvas_assignment_titles:
                score = row[a]
                assignments[a] = float(score) if score else 0.0
            score = merging_fn(assignments)
            if sid not in gs_assignment_data:
                print(f"[ERROR]: Could not find student with sid {sid}! They would have received a {score}")
                continue
            std = gs_assignment_data[sid]
            std[GS_SCORE_COL] = score
            std[GS_STATUS_COL] = GS_GRADED_STATUS
            std[GS_LATENESS_COL] = GS_NO_LATENESS

        
    print("Dumping GS assignment data...")
    # Dump Gradescope Assignment Data
    with open(output_csv_file, "w") as csvfile:
        fieldnames = list(gs_assignment_data.values())[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in gs_assignment_data.values():
            writer.writerow(row)

    print("Done!")