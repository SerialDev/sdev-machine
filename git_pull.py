import requests
from bs4 import BeautifulSoup
import subprocess

def ensure_dir(directory):
    """
    Ensure a directory exists

    Parameters
    ----------

    directory : str
       Name of the directory to check

    Returns
    -------

    None
       nil
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


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


def execute(cmd, working_directory=os.getcwd()):
    """
        Purpose  : To execute a command and return exit status
        Argument : cmd - command to execute
        Return   : exit_code
    """
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=working_directory,
    )
    (result, error) = process.communicate()

    rc = process.wait()

    if rc != 0:
        print("Error: failed to execute command:", cmd)
        print(error)
    return result, error

ensure_dir('work_den')

url = 'https://github.com/'
username = 'SerialDev'
projects_url = f'{username}?tab=repositories'
url = url + projects_url

soup  = make_soup(url)

ol = soup.find("div", {"id": "user-repositories-list"}).find('ul')

repos = []
for i in ol.find_all('li'):
    repos.append(i.find('h3').find('a').get('href'))

for current_repo in repos:
    if os.path.exists(rf'{os.getcwd() + os.sep + "work_den" + os.sep + current_repo.split("/")[-1] }'):
        b = execute(rf"cd {os.getcwd()+os.sep}work_den{os.sep+current_repo.split('/')[-1]} && git pull origin master")
    else:
        a = execute(rf"cd {os.getcwd()+os.sep}work_den && git clone https://github.com{current_repo}.git")
    break
