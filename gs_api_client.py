#!/usr/bin/env python3
import requests
import getpass

BASE_URL = 'https://www.gradescope.com'

class GradescopeAPIClient:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.cookie = None

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def log_in(self, email, password):
        url = "{base}/api/v1/user_session".format(base=BASE_URL)

        form_data = {
            "email": email,
            "password": password
        }
        r = self.post(url, data=form_data)
        try:
            self.cookie = r.json()
            self.token = self.cookie['token']
            return True
        except Exception as e:
            print("Login failed!")
            print(r.text)
            return False
        
    def prompt_login(self):
        while not self.token:
            email = input("Please provide the email address on your Gradescope account: ")
            password = getpass.getpass('Password: ')
            if not self.log_in(email, password):
                print("An error occured when attempting to log you in, try again...")

    def upload_pdf_submission(self, course_id, assignment_id, student_email, filename="", file_data=None):
        if not self.token:
            print("You must login before you can upload a submission!")
            return False
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        if file_data is not None:
            files = {'pdf_attachment': file_data}
        else:
            files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def replace_pdf_submission(self, course_id, assignment_id, student_email, filename="", file_data=None):
        if not self.token:
            print("You must login before you can upload a submission!")
            return False
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions/replace_pdf".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        if file_data is not None:
            files = {'pdf_attachment': file_data}
        else:
            files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def upload_programming_submission(self, course_id, assignment_id, student_email, filenames=[], files_dict = {}):
        if not self.token:
            print("You must login before you can upload a submission!")
            return False
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        if files_dict:
            files = [('files[]', (filename, filedata)) for filename, filedata in files_dict.items()]
        else:
            files = [('files[]', (filename, open(filename, 'rb'))) for filename in filenames]

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def regrade(self, course_id, assignment_id, sub_id):
        if not self.token:
            print("You must login before you can upload a submission!")
            return False
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions/{2}/regrade".format(
            course_id, assignment_id, sub_id, base=BASE_URL
        )

        request_headers = {'access-token': self.token}
        r = self.post(url, headers=request_headers)
        return r

    def download(self, course_id, assignment_id, cookies: dict):
        url = "https://www.gradescope.com/courses/{}/assignments/{}/scores.csv".format(
            course_id, assignment_id, base=BASE_URL
        )
        print(url)
        r = self.post(url, cookies=cookies)
        print(r)
        return r
    # def download(self, course_id, assignment_id):
    #     if not self.token:
    #         print("You must login before you can upload a submission!")
    #         return False
    #     url = "{base}/courses/{}/assignments/{}/scores.csv".format(
    #         course_id, assignment_id, base=BASE_URL
    #     )

    #     request_headers = {'access-token': self.token}
    #     r = self.post(url, headers=request_headers)
    #     return r

if __name__ == '__main__':
    client = GradescopeAPIClient()
    client.prompt_login()
    # Use the APIClient to upload submissions after logging in, e.g:
    # client.upload_pdf_submission(1234, 5678, 'student@example.edu', 'submission.pdf')
    # client.upload_programming_submission(1234, 5678, 'student@example.edu', ['README.md', 'src/calculator.py'])
    # You can get course and assignment IDs from the URL, e.g.
    # https://www.gradescope.com/courses/1234/assignments/5678
    # course_id = 1234, assignment_id = 5678

