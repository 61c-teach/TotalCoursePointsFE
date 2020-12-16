data_url = "https://example.com/c.data"
key = b'A SPECIAL KEY'

from files.constants import CDATA_FILE
from cryptography.fernet import Fernet

def fetch_data():
    import requests
    data = requests.get(data_url).content
    f = Fernet(key)
    return f.decrypt(data)

def generate_data(dest):
    import main_setup
    with open(CDATA_FILE, "rb") as f:
        raw_data = f.read()
    
    f = Fernet(key)

    enc_data = f.encrypt(raw_data)

    with open(dest, "wb") as f:
        f.write(enc_data)