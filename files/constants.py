from GradescopeBase.Utils import root_dir, submission_dir, results_path

DATA_PATH = "files/data"
INPUT_PATH = "files/input"
CDATA_FILE = "files/data/c.data"
ROSTER_FILE = "files/roster.csv"
PIAZZA_FILE = "files/input/piazza.csv"
RAW_EPA_FILE = "files/input/raw_epa.csv"
FULL_PIAZZA_EPA_FILE = "files/data/full_piazza_epa.csv"
CALCENTRAL_GRADE_ROSTER_FILE = "files/input/calcentral_grade_roster.csv"
CALCENTRAL_GRADE_REPORT_FILE = "files/data/sp20_cs61c_calcentral_report.csv"

STUDENT_INPUT_JSON_FILE = f"{submission_dir()}/input.json"

DISHONESTY_INCOMPLETES_FILE = "files/input/dishonesty_incompletes.csv"
OTHER_INCOMPLETES_FILE = "files/input/other_incompletes.csv"
RESOLVED_CHEATERS_FILE = "files/input/resolved_cheaters.csv"

# These are links to Google Sheets if you choose to use them. You should change the ID to a sheet you would use.
GSHEET_CREDENTIALS_JSON_FILES_LIST = [
    "files/input/credentials.json",
]

# You can check out these google sheets if you want an example
GSHEET_ASSIGNMENTS_ID = "1lurL8QzgXRnDXoAti3hQy3CS7RPwl43wH6IYcg9BycY"
GSHEET_EXTENSIONS_ID = "1ccputUkPoLfP24efpZlhqKKWDr2YJBSCcH4Q5wm_GZs"

REPORT_RAW_NO_EPA_FILE = "files/data/raw_no_epa.csv"
REPORT_NO_EPA_CURVED_FILE = "files/data/no_epa_curved_to_3.3.csv"
REPORT_RAW_EPA_FILE = "files/data/raw_with_epa.csv"
REPORT_EPA_CURVED_FILE = "files/data/epa_curved_like_raw_to_3.3.csv"
REPORT_EPA_CURVED_BIN_ADJ_FILE = "files/data/epa_curved_like_raw_to_3.3_bin_adjust.csv"

COURSE_ID = "123456"
ASSIGNMENT_ID = "123456789"