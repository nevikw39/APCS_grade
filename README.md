# APCS_grade
## 手刀查詢ＡＰＣＳ成績ㄉ爬蟲 o'_'o

## 注意！！注意！！注意！！
# 請保持低調！！保持低調！！低調！！

> 我是沒差喇，高三生倒數學測中，以後也不會考惹ＸＤ
>
> 好好把握ＡＰＣＳ還沒有 *reCAPTCHA* 的時代ＱＱ

每一次ＡＰＣＳ考完都要 15 天才可以查成績，到底是為什麼喇欸。這 15 天說長不長說短不短，卻總是令人煎熬難耐。每次查成績那天的早上十點，你是否也是懷抱著既期待又害怕的心情立刻打開手機狂刷？？這樣實在太麻煩惹，對吧？？

## Requirements

- Python 3
- requests
- BeautifulSoup 4

註冊ＡＰＣＳ的 `email` 必須是 *gmail* 或者 *GSuite*（例如學校提供的帳號）。

另外，必須打開 [__「低安全性應用程式存取權」__](https://myaccount.google.com/lesssecureapps) 方能使爬蟲得以藉由 *IMAP* 讀取驗證信。

## Usage

```bash
python3 main.py
```

第一次使用時需輸入 `ID` 身分證字號、`Email` 註冊ＡＰＣＳ的 *Email*、`Password` 該 *Email* 的密碼。

您的所有個資將以 `pickle`（*Python* 版 `json`??）儲存在本機。

執行完畢後將結果輸出在 console 並儲存至 `grade.pickle`，俾後續操作。

## Exception

### APCS log-in failed

可能是你 *gmail* 帳號或身分證有誤。

### IMAP log-in failed

可能是你 *gmail* 帳號或密碼有誤，或者尚未開啟[__「低安全性應用程式存取權」__](https://myaccount.google.com/lesssecureapps)。

## Features

你懂的，像是先跑過一次記住帳號密碼後，用 `crontab` 讓他準時十點執行。

未來再搭個 *Telegram* bot 之類ㄉ＞＜