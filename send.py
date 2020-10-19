import os
import pickle
import pprint

import requests

if not os.path.exists("send.pickle"):
    token = input("token:\n")
    chatid = input("chatid:\n")
    with open("send.pickle", 'wb') as p:
        pickle.dump(token, p)
        pickle.dump(chatid, p)
else:
    with open("send.pickle", 'rb') as p:
        token = pickle.load(p)
        chatid = pickle.load(p)

if not os.path.exists("grade.pickle"):
    print("No grade result QQ!!")
    exit(1)
else:
    with open("grade.pickle", 'rb') as p:
        grade = pickle.load(p)

requests.get(
    f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatid}&text={pprint.pformat(grade)}")
