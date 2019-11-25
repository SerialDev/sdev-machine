import requests
from bs4 import BeautifulSoup

def make_soup(url, parser="html.parser"):
    """
    * type-def ::String :: PyObj -> BeautifulSoup
    * ---------------{Function}---------------
    * Take in a url and return beautifulsoup object . . .
    * ----------------{Params}----------------
    * : url    | String with the url to parse
    * : parser | beautifulsoup parser
    * ----------------{Returns}---------------
    * BeautifulSoup . . .
    """
    r = requests.get(url)
    contents = r.content
    soup = BeautifulSoup(contents, parser)
    return soup


url = 'https://github.com/'
username = 'SerialDev'
projects_url = f'{username}?tab=repositories'
url = url + projects_url

soup  = make_soup(url)

ol = soup.find("div", {"id": "user-repositories-list"})
