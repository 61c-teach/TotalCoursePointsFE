"""
This file will contain the stuff necessary for creating the roster and uploading the submissions.
"""
from fullGSapi.api.login_tokens import LoginTokens
import getpass
import os
import csv
from tqdm import tqdm

gs_roster_loc = "files/input/gs_roster.csv"
canvas_roster_loc = "files/input/canvas_roster.csv" # Currently does not work though will be smart enough later.
calcentral_roster_loc = "files/input/calcentral_roster.csv"
grade_status_roster = "files/input/calcentral_grade_roster.csv"
dest_roster_loc = "files/roster.csv"

# FIXME Go to the files/constants.py file to enter your course ID and assignment ID.
from files.constants import COURSE_ID, ASSIGNMENT_ID

def main():
    import sys
    argv = sys.argv
    upload_to_gs = True
    only_sync = False
    if len(argv) > 1:
        if argv[1] == "regen":
            print("Only regenerating the roster.")
            upload_to_gs = False
        elif argv[1] == "sync":
            print("Only syncing students without submissions.")
            only_sync = True
    
    print("Generating the roster...")
    roster = generate_roster()
    print("Generating the roster...Done!")
    if upload_to_gs:
        # Login to Gradescopes real api.
        token: LoginTokens = LoginTokens().prompt_login(until_success=True)

        input("Press enter to start uploading students...")

        # Filter roster to only upload new students without submissions
        if only_sync:
            print("Mutating roster to only sync students without submissions...")
            roster = only_sync_new_students(token.gsFullapi, roster, COURSE_ID, ASSIGNMENT_ID)
            print("Mutating roster to only sync students without submissions...Done!")
        print("Uploading the students...")
        upload_sids_to_gs(roster, token.gsAPI, COURSE_ID, ASSIGNMENT_ID)
        print("Uploading the students...Done!")
    
    

def generate_roster(gs_roster=gs_roster_loc, canvas_roster=calcentral_roster_loc, dest=dest_roster_loc):
    print("Loading the Canvas roster...")
    dup_c_sids = set()
    canvas_roster_data = {}
    with open(canvas_roster) as csvfile:
            croster = csv.DictReader(csvfile)
            for row in croster:
                name = row.get("Name")
                if name:
                    try:
                        name = " ".join(name.split(", ")[::-1])
                    except Exception as e:
                        print(f"Failed to flip the name {name}! Ignoring...")
                sid = row.get("Student ID")
                email = row.get("Email Address")
                if not sid:
                    print(f"The student {name} does not have an SID!")
                    continue
                sid = str(sid)
                data = {
                    "name": name,
                    "email": email
                }
                grade = row.get("Grading Basis")
                if grade is not None:
                    g = None
                    if grade == "P/NP":
                        g = "EPN"
                    elif grade == "S/U":
                        g = "ESU"
                    elif grade == "DPN":
                        g = "DPN"
                    elif grade == "CPN":
                        g = "CPN"
                    data["ForGrade"] = g
                if sid in canvas_roster_data:
                    print(f"A student with sid {sid} already exists! (Attempted to add student {data} but failed!)")
                    dup_c_sids.add(sid)
                    continue
                canvas_roster_data[sid] = data
    for sid in dup_c_sids:
        del canvas_roster_data[sid]
    print("Loading the Canvas roster...Done!\nLoading the Gradescope roster...")
    dup_g_sids = set()
    gs_roster_data = {}
    with open(gs_roster) as csvfile:
        gsroster = csv.DictReader(csvfile)
        for row in gsroster:
            # name = row.get("Name")
            fname = row.get("First Name")
            lname = row.get("Last Name")
            name = fname + " " + lname
            sid = row.get("SID")
            email = row.get("Email")
            if not sid:
                print(f"Could not find the sid of {name} (email: {email})! Checking the Canvas roster...")
                def partial_match(email, name):
                    matched_names = []
                    for sid, data in canvas_roster_data.items():
                        if data["email"] == email:
                            return sid
                        if data["name"] == name:
                            matched_names.append(sid)
                    if len(matched_names) == 1:
                        return matched_names[0]
                    return False
                pos_sid = partial_match(email, name)
                if pos_sid:
                    print("Found a matching entry in the Canvas roster!")
                    sid = pos_sid
                else:
                    print("Could not find a matching entry in the Canvas roster!")
                    continue
            sid = str(sid)
            data = {
                "name": name,
                "email": email
            }
            if sid in gs_roster_data:
                print(f"A student with sid {sid} already exists! (Attempted to add student {data} but failed!)")
                # dup_g_sids.add(sid)
                # continue
            gs_roster_data[sid] = data
    for sid in dup_g_sids:
        del gs_roster_data[sid]
    print("Loading the Gradescope roster...Done!\nChecking missing SID's in the Gradescope roster...")
    for sid, data in canvas_roster_data.items():
        if sid not in gs_roster_data:
            print(f"Could not find the sid {sid} ({data['name']}, {data['email']}) in the Gradescope roster!")
        else:
            gs_roster_data[sid]["ForGrade"] = data.get("ForGrade")
    print("Added P/NP data")
    if os.path.exists(grade_status_roster):
        with open(grade_status_roster, "r+") as csvfile:
            croster = csv.DictReader(csvfile)
            for row in croster:
                sid = row.get("SID")
                name = row.get("Name")
                grade_status = row.get("Grading Basis")
                if sid not in gs_roster_data:
                    if sid not in canvas_roster_data:
                        print(f"The student {name} ({sid}) [{grade_status}] is not in the canvas or gradescope roster!")
                    else:
                        print(f"The student {name} ({sid}) [{grade_status}] is not in the gradescope roster!")
                else:
                    if grade_status not in ["GRD", "EPN", "ESU", "DPN", "CPN"]:
                        print(f"The student {name} ({sid}) has an unsupported grade status [{grade_status}]")
                    gs_roster_data[sid]["ForGrade"] = grade_status
    else:
        print("Could not find the calcentral grade roster!")

    print("Writing roster...")
    with open(dest_roster_loc, "w+") as fd:
        writer = csv.writer(fd)
        writer.writerow(["Name", "SID", "Email", "InCanvas", "ForGrade", "Incomplete"])
        for sid, data in gs_roster_data.items():
            graded = data.get("ForGrade")
            if graded is None:
                graded = "GRD"
            writer.writerow([data["name"], sid, data["email"], str(sid in canvas_roster_data), graded, False])
    print("Writing roster...Done!")
    return gs_roster_data

def only_sync_new_students(gc, roster, course_id, assignment_id):
    raw_scores_csv = gc.download_scores(course_id, assignment_id)

    import csv
    from io import StringIO

    new_roster = {}

    for row in csv.DictReader(StringIO(raw_scores_csv.decode())):
        if row["Status"] == "Missing":
            sid = row["SID"]
            if sid and sid in roster:
                new_roster[sid] = roster[sid]
            else:
                print(f"{row} is missing and does not have an SID in the roster!")
                

    return new_roster


def upload_sids_to_gs(roster, client, course_id, assignment_id):
    for sid, data in tqdm(roster.items(), dynamic_ncols=True, unit="Student", desc="Uploading Students"):
        email = data["email"]
        # Files is a dictionary mapping a filename to the contents of that file. You can add as many files as you want.
        files = {
            "input.json": f"{{\"sid\":\"{sid}\"}}"
        }
        client.upload_programming_submission(course_id, assignment_id, email, files_dict=files)
    print("Finished uploading students!")

if __name__ == "__main__":
    main()