import email
import imaplib
import pickle
import time
import os

import requests
from bs4 import BeautifulSoup as bs


def wk(x: str, y):
    return bs(y, 'html.parser').select_one(f'input[name="wk_{x}"]').attrs["value"]


def get_subject():
    _, idx = imap.select("INBOX")
    _, msg = imap.fetch(idx[0].decode(), "(RFC822)")
    return email.header.decode_header(email.message_from_bytes(msg[0][1])["Subject"])[0][0].decode()


try:
    with open("config.pickle", 'rb') as p:
        ID = pickle.load(p)
        EMAIL = pickle.load(p)
        PASSW = pickle.load(p)
except FileNotFoundError:
    ID = input("ID:\n")
    EMAIL = input("\nEmail:\n")
    PASSW = input("\nPassword:\n")
    with open("config.pickle", 'wb') as p:
        pickle.dump(ID, p)
        pickle.dump(EMAIL, p)
        pickle.dump(PASSW, p)

s = requests.session()
r = s.get("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do")
r = s.post("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do",
           {"wk_action": "a_getchecknum", "wk_token": wk("token", r.text), "wk_authnumber": ID, "wk_email": EMAIL})

imap = imaplib.IMAP4_SSL("imap.gmail.com")
try:
    imap.login(EMAIL, PASSW)
except imaplib.IMAP4.error:
    print("IMAP log-in failed.\n\tPlease check if both your email and password is correct, and whether \"Less secure app access\" is on for your account.\n\tFor more detail, visit https://github.com/nevikw39/APCS_grade")
    if os.path.exists("config.pickle"):
        os.remove("config.pickle")
    exit(1)
subject = ""
while "大學程式設計先修檢測】驗證碼:" not in subject:
    subject = get_subject()
    time.sleep(1)
num = subject[-5:]
_, idx = imap.select("INBOX")
imap.store(idx[0].decode(), '+FLAGS', '\\Deleted')
imap.expunge()
imap.close()
imap.logout()

r = s.get("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do")
r = s.post("https://webapi.apcs.csie.ntnu.edu.tw/APCS/Applygrade.do", {"wk_action": "a_validateCheckNum", "wk_token": wk(
    "token", r.text), "wk_authnumber": ID, "wk_email": EMAIL, "wk_testList": wk("testList", r.text), "wk_checknum": num})
print(r.json()['res']['info'])

with open("grade.pickle", 'wb') as p:
    pickle.dump(r.json()['res']['info'], p)
