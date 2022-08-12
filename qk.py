import requests
import json
import time
url = ""
cookies = {
    "JSESSIONID":""
}
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "X-Requested-With":"XMLHttpRequest"
}
data = {
}
d = "".split("&")
for i in d:
    data[i.split("=")[0]] = i.split("=")[1]
# print(data)
count = 1
while True:
    try:
        rep = requests.post(url=url,data=data,cookies=cookies,headers=headers,timeout=1).text
        res = json.loads(rep)
        flag = res["flag"]
        print(res)
        time.sleep(0.35)
        if flag == "-1":
            print(f"[+]第{count}次尝试抢课...")
            count += 1
        elif flag == "1":
            print(f"[-]抢课成功 共用{count}次")
            break
    except:
        pass