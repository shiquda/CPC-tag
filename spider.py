import requests
from utils import base64_decode, base64_encode, parse_js
from bs4 import BeautifulSoup
import json
import csv
import time
from tqdm import tqdm

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
LUOGU_BASE_URL = "https://www.luogu.com.cn/problem/"

DEBUG = 0


def scrape_luogu(id):
    url = LUOGU_BASE_URL + id
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    if DEBUG:
        with open("page.html", "w") as f:
            f.write(response.text)
    soup = BeautifulSoup(response.content, "html.parser")

    # 获取题目文本
    markdown_text = soup.find("article").text
    markdown_text_base64 = base64_encode(markdown_text)

    # 获取编码的json信息
    encoded_js_string = soup.find("script").text.split(
        "window._feInjection = JSON.parse(decodeURIComponent(\"")[1].split("\"));window.")[0]
    json_object = parse_js(encoded_js_string)

    if DEBUG:
        print(json_object)
        with open("json_object.json", "w") as f:
            f.write(json.dumps(json_object, ensure_ascii=False, indent=4))

    title = json_object["currentData"]["problem"]["title"]
    tag = json_object["currentData"]["problem"]["tags"]
    return id, title, markdown_text_base64, tag, url


def scrape_luogu_problems():
    try:
        with open("./data/problems.csv", "r") as f:
            reader = csv.reader(f)
            last_id = list(reader)[-1][0]
        st_id = int(last_id.split("P")[1]) + 1
    except:
        st_id = 1000
    for i in tqdm(range(st_id + 1, 10000 + 1)):
        id = "P" + str(i)
        try:
            id, title, markdown_text_base64, tag, url = scrape_luogu(id)
            with open("problems.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([id, title, markdown_text_base64, tag, url])
        except Exception as e:
            print(e)
            with open("failed.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([id])
            continue
    time.sleep(0.2)


if __name__ == "__main__":
    # 检测上次爬取到的csv文件结尾的id
    scrape_luogu_problems()
