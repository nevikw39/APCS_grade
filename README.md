# APCS_grade
## 手刀查詢ＡＰＣＳ成績ㄉ爬蟲 o'_'o

## 注意！！注意！！注意！！
# 請保持低調！！保持低調！！低調！！

> 我是沒差喇，高三生倒數學測中，以後也不會考惹ＸＤ
>
> 好好把握ＡＰＣＳ還沒有 *reCAPTCHA* 的時代ＱＱ

每一次ＡＰＣＳ考完都要 15 天才可以查成績，到底是為什麼喇欸。這 15 天說長不長說短不短，卻總是令人煎熬難耐。每次查成績那天的早上十點，你是否也是懷抱著既期待又害怕的心情立刻打開手機狂刷？？這樣實在太麻煩惹，對吧？？

此爬蟲幫助您一鍵取得ＡＰＣＳ成績並申請寄送ＰＤＦ至信箱，同時提供 _Telegram_ bot 通知的解決方案。

## Requirements

- Python 3
- requests
- BeautifulSoup 4

註冊ＡＰＣＳ的 `email` 必須是 *gmail* 或者 *GSuite*（例如學校提供的帳號）。

另外，必須打開 [__「低安全性應用程式存取權」__](https://myaccount.google.com/lesssecureapps) 方能使爬蟲得以藉由 *IMAP* 讀取驗證信。

假如您很在乎資安且已開啟 __二步驟驗證__ ，則可以使用[__「應用程式密碼」__](https://support.google.com/accounts/answer/185833)。

## Usage

### main.py

送出表單、讀取驗證碼、得到成績，輸出並保存。

```bash
# Default, print grade and save as pickle, and you can use it by other Python scripts.
python3 main.py
# Save grade as both pickle and json so that you could use it for other purpose.
python3 main.py > grade.json
```

第一次使用時需輸入 `ID` 身分證字號、`Email` 註冊ＡＰＣＳ的 *Email*、`Password` 該 *Email* 的密碼。

您的所有個資將以 __pickle__（*Python* 版 __json__??）儲存在本機。

執行完畢後將結果以 __JSON__ 格式輸出在 stdin 並儲存至 `grade.pickle`，俾後續操作。

### send.py

將成績傳送至 _Telegram_ 帳號。

```bash
python3 send.py
```

建立一個 _Telegram_ bot，取得其 `token` 及自己的 `chat_id`。第一次執行時輸入之。

## Exception

### APCS log-in failed

可能是你 *gmail* 帳號或身分證有誤。

### IMAP log-in failed

可能是你 *gmail* 帳號或密碼有誤，或者尚未開啟[__「低安全性應用程式存取權」__](https://myaccount.google.com/lesssecureapps)。

### APCS verification failed

可能是你 *gmail* 信箱最上方的信恰好是上次手動查詢的驗證信，請確保已經刪除最上方的驗證信。

## Examples

你懂的，像是先跑過一次記住帳號密碼後，用 `at` 讓他準時十點執行。

```bash
at -t 11020000 <<< "./apcs_grade.sh" # UTC time
```