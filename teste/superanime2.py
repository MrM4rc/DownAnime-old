import requests

r = requests.post("https://www.superanimes.org/download.php?file=ZTk1YzkxMWU5NDcwYjNmNA==&token=xmcOoIMTU3MDI0MTc4NQ==&n=YmxhY2stY2xvdmVyLWVwaXNvZGlvLTEwMQ==")

print(r.history)

