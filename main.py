import email
import getpass
import imaplib
import os
import pickle
import pprint
import sys
import time

import requests
from bs4 import BeautifulSoup as bs


def wk(x: str, y: bs) -> str:
    """
    Get the value of the hidden form element.
    """
    return y.select_one(f'input[name="wk_{x}"]').attrs["value"]


def get_subject() -> str:
    """
    Get the subject of the latest email in inbox.
    """
    global imap, x
    x += 1
    print(f".", end='', file=sys.stderr)
    _, idx = imap.select("INBOX")
    _, msg = imap.fetch(idx[0].decode(), "(RFC822)")
    return email.header.decode_header(email.message_from_bytes(msg[0][1])["Subject"])[0][0].decode()


if os.path.exists("config.pickle"):
    with open("config.pickle", 'rb') as p:
        ID = pickle.load(p)
        EMAIL = pickle.load(p)
        PASSW = pickle.load(p)
else:
    ID = input("ID      >>>")
    EMAIL = input("\nEmail   >>>")
    PASSW = getpass.getpass("\nPassword>>>")
    with open("config.pickle", 'wb') as p:
        pickle.dump(ID, p)
        pickle.dump(EMAIL, p)
        pickle.dump(PASSW, p)

# First, post our ID and email, and wait the check number mail to our box.
s = requests.session()
r = s.get("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do")
h = bs(r.text, 'html.parser')
r = s.post("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do",{"wk_action": "a_getchecknum", "wk_token": wk("token", h), "wk_authnumber": ID, "wk_email": EMAIL}).json()['res']
if r['error']:
    print("APCS log-in failed.\n\tPlease check your ID and email.\n\tFor more detail, visit https://github.com/nevikw39/APCS_grade", file=sys.stderr)
    if os.path.exists("config.pickle"):
        os.remove("config.pickle")
    exit(1)

# Second, log in to our gmail and wait for the check number.
imap = imaplib.IMAP4_SSL("imap.gmail.com")
try:
    imap.login(EMAIL, PASSW)
except imaplib.IMAP4.error:
    # Only if you turn on "Less secure app access" can we read your emails via IMAP.
    print("IMAP log-in failed.\n\tPlease check if both your email and password is correct, and whether \"Less secure app access\" is on for your account.\n\tFor more detail, visit https://github.com/nevikw39/APCS_grade", file=sys.stderr)
    if os.path.exists("config.pickle"):
        os.remove("config.pickle")
    exit(1)
x = 0  # Count for the waiting time
subject = ""
while "【大學程式設計先修檢測】驗證碼:" not in subject:
    subject = get_subject()
    time.sleep(1)  # ``Patient you must have'' by Yoda
num = subject[-5:]
_, idx = imap.select("INBOX")
imap.store(idx[0].decode(), '+FLAGS', '\\Deleted') # Delete the verifying email.
imap.expunge()
imap.close()
imap.logout()
print(f"\n\tx={x}", file=sys.stderr)

# Finally, we have the check number and we can go back to the form
r = s.get("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do")
h = bs(r.text, 'html.parser')
r = s.post("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do", {"wk_action": "a_validateCheckNum", "wk_token": wk("token", h), "wk_authnumber": ID, "wk_email": EMAIL, "wk_testList": wk("testList", h), "wk_checknum": num}).json()['res']
if r['error']:
    print("APCS verification failed.\n\tPlease assure there's no other APCS verification email on the top of your inbox.\n\tFor more detail, visit https://github.com/nevikw39/APCS_grade", file=sys.stderr)
    exit(1)
grade = r['info']
key = ','.join([i["t_key_"] for i in grade])
for i in grade:
    del i['email_']
    del i['level1_str_']
    del i['level2_str_']
    del i['score1_str_']
    del i['score2_str_']
    del i['t_key_']
    del i['name_']
pprint.pprint(grade)
with open("grade.pickle", 'wb') as p:
    pickle.dump(grade, p)
    pickle.dump(x, p)

# Apply for PDF
r = s.get("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do")
h = bs(r.text, 'html.parser')
r = s.post("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do", {"wk_action": "a_applygrade_pdf", "wk_token": wk("token", h), "wk_authnumber": ID, "wk_email": EMAIL, "wk_checkbox_applygrade": '', "wk_office": '', "wk_office_mail": '', "wk_key_str": key}).json()['res']
if r['error']:
    print("APCS failed.\n\tPlease.\n\tFor more detail, visit https://github.com/nevikw39/APCS_grade", file=sys.stderr)
    exit(1)
