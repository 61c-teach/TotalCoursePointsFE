from fullGSapi.api.client import GradescopeClient
from fullGSapi.api.login_tokens import LoginTokens
import os
import pickle
import getpass
import hashlib

from files.constants import COURSE_ID, ASSIGNMENT_ID

GS_CLIENT_FILE = "~/.gradescope"
GDA_ZIP_FILE = "GDA/TotalCoursePointsFE-GDA.zip"

# Just wanna make this global for debugging.
gc: GradescopeClient = None

def check_GDA_change(file="GDA/settings.sh"):
    m = hashlib.sha512()
    with open(file, "rb") as f:
        m.update(f.read())
    return m.digest() != b"Y\xca\xa0\xd1\x88\xc3\x08&\xca\x04\xa8\xaa\xcd\xd2\xcf\xaa\xa1.\xdf\t\xa3.\xe0.WcO\x87*F\x86 !\x98\xb6\xb1U{dn\x97\xe20\xd8\xea\xcc\x94C\xd7\xf2d\xe5\x93\xd8P\x81\xf4q\x97\xf5S\xcb\xff'"

def main():
    if not check_GDA_change():
        print("You did not modify the GDA settings.sh to point to your repo! Please do that then run the `compress_GDA.sh` script.")
        return
    if not os.path.exists(GDA_ZIP_FILE):
        print(f"Could not find the GDA zip file at '{GDA_ZIP_FILE}'!\nMake sure to modify the settings.sh file then run comress_GDA.sh to create the zip file.")
        return
    token = LoginTokens.load(GS_CLIENT_FILE)
    if not token:
        token = LoginTokens(path=GS_CLIENT_FILE)
        token.prompt_login()
    
    global gc
    gc = token.gsFullapi

    print("Fetching autograder class...")
    ag = gc.get_autograder(COURSE_ID, ASSIGNMENT_ID)
    print("Uploading GDA build file and rebuilding...")
    if ag.rebuild_and_print_output(GDA_ZIP_FILE):
        print("Regrading all...")
        ag.regrade_all()
    else:
        print("[ERROR]: Build failed!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error has occurred!")
        import traceback
        traceback.print_exc()
        import IPython
        IPython.embed()