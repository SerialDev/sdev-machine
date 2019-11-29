import requests
from bs4 import BeautifulSoup
import subprocess
from urllib import parse

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

def get_root(folder=os.getcwd()):
    return folder


url = 'https://github.com/'
username = 'SerialDev'
projects_url = f'{username}?tab=stars'
url = url + projects_url
root = get_root()
work_folder_name = '{username}_stars'


ensure_dir(f'{root + os.sep + work_folder_name}')


soup  = make_soup(url)

user_star_list = soup.find_all("div", {"class":"col-12 d-block width-full py-4 border-bottom"})



def next_page(soup):
    next = soup.find("div", {"class": "paginate-container"}).find_all('a')
    if len(next) == 1:
        next = next[0].get('href')
    else:
        next = next[1].get('href')
    query = parse.urlparse(next).query.split('=')[0]
    if query == 'after':
        return next
    else:
        print('no more pages')
        return 0


def next_page_repos(repos_list, soup):
    next = next_page(soup)
    if next == 0:
        return repos_list
    else:
        soup_next = make_soup(next)
        for i in soup_next.find_all("div", {"class":"col-12 d-block width-full py-4 border-bottom"}):
            repos_list.append(i.find('a').get('href'))
        next_page_repos(repos_list, soup_next)
        return repos_list


repos = []
for i in user_star_list:
    repos.append(i.find('a').get('href'))

repos = next_page_repos(repos, soup)


for current_repo in repos:
    if os.path.exists(rf'{root + os.sep +  work_folder_name + os.sep + current_repo.split("/")[-1] }'):
        b = execute(rf"cd {root +os.sep + work_folder_name}{os.sep+current_repo.split('/')[-1]} && git pull origin master")
    else:
        a = execute(rf"cd {root + os.sep + work_folder_name} && git clone https://github.com{current_repo}.git")
    break
