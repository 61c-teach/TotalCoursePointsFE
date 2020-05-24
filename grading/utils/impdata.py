import pickle
from files.constants import *
with open(CDATA_FILE, "rb") as f:
    c = pickle.load(f)