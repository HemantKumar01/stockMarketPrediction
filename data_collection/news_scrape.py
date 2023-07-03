class console_colors:  # for printing color texts to console
    HIGHLIGHT = "\x1b[6;30;42m"
    HIGHLIGHT_END = "\x1b[0m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


import sys
import json
import signal
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus as url_encode
from datetime import datetime, timedelta

# * Inputs
# ----------------------------
query = "Tata Motors"
starting_date = "9/25/2018"  # ? MM/DD/YYYY without leading zero
ending_date = "6/28/2023"  # ? MM/DD/YYYY without leading zero
max_req_limit = (
    50  #! your IP can get banned if you give to much requests (maybe 2500 req/ day)
)
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"
}

# ----------------------------
starting_datetime = datetime.strptime(starting_date, "%m/%d/%Y")
ending_datetime = datetime.strptime(ending_date, "%m/%d/%Y")
current_datetime = starting_datetime
one_day = timedelta(days=1)

num_req = 0

news = (
    []
)  # ? list of object {"title":'...', "link":'...', "upload_time":'...'} (upload_time is like '26 min ago")
URL_safe_query = url_encode(query)

# google presents search in many pages (with maybe 10 queries in each page
num_page = 1

# following error message can be changed in future
error_message = "did not match any news results."

# If you are not from india, you need to change the URL, using following steps
# - Go To Google and search anything
# - Go To News Tab
# - select tools->select date->custom range and select any range
# - Scroll to bottom of page and select 2 , ie the second page of google result
# - fill q={URL_safe_query},  cd_min={starting_date} and cd_max={ending_date}


def save_news_JSON(file_name):
    print(
        f"{console_colors.OKCYAN}Saving Data in /news_data/{file_name}.{console_colors.ENDC}"
    )
    with open("news_data/" + file_name, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=4)


def signal_handler(sig, frame):
    save_news_JSON("fallback.json")
    print(f"{console_colors.FAIL}You pressed Ctrl+C!{console_colors.ENDC}")
    print("Data until now is saved as fallback.json")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def get_news():
    global num_req, num_page, current_datetime, URL_safe_query, news

    num_page = 1
    news = []

    while True:
        if num_req >= max_req_limit:
            print(
                f"{console_colors.FAIL}Reached Max Request Limit: {console_colors.ENDC}",
                max_req_limit,
            )
            sys.exit()
            break

        url = f"https://www.google.com/search?q={URL_safe_query}&tbs=cdr:1,cd_min:{current_datetime.strftime('%m/%d/%Y')},cd_max:{(current_datetime).strftime('%m/%d/%Y')}&tbm=nws&start={((num_page -1) * 10)}"

        page = requests.get(url, headers=headers)
        num_req += 1

        soup = BeautifulSoup(page.content, "html.parser")
        if error_message in soup.body.text:
            print(f"{console_colors.OKGREEN}All News Scraped.{console_colors.ENDC}")
            break

        print(f"  - getting page number {num_page} of google search:")
        print(f"    URL: {url}")

        titles = soup.select(
            "div.n0jPhd.ynAwRc.MBeuO.nDgy9d"
        )  # ? selector can change in future.It it does not work, Use developer tools of your browser to inspect and find a working selecto
        links = soup.select(
            "a.WlydOe"
        )  # ? selector can change in future.It it does not work, Use developer tools of your browser to inspect and find a working selector
        upload_time = soup.select(".OSrXXb.rbYSKb.LfVVr")

        assert len(titles) == len(
            links
        ), "The CSS Selectors are Outdated as number of links , titles and upload times are not equal. Edit the selectors or change a code near this assert statement to save this data"

        for i in range(len(titles)):
            news.append(
                {
                    "title": titles[i].text,
                    "link": links[i]["href"],
                    "upload_time": upload_time[i].text,
                }
            )

        num_page += 1
    # ----------LOOP ENDED-------------------------------------
    save_news_JSON(f"news_data_{current_datetime.strftime('%d-%m-%Y')}.json")


while True:
    if current_datetime > ending_datetime:
        print(f"{console_colors.OKGREEN}All Data Scraped.{console_colors.ENDC}")
        break
    print(
        f"{console_colors.HIGHLIGHT}getting news on given query on date : {console_colors.HIGHLIGHT_END}",
        current_datetime,
    )
    get_news()
    print("--------------------------------------------------------------")
    current_datetime = current_datetime + one_day
