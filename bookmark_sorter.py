
import time
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from selenium import webdriver
from PIL import Image
import io
from pandas import set_option
from urllib.parse import urlparse
import argparse
import ast
import pandas as pd


def concat_pd_list(data, axis=0):
    for i, section in enumerate(data):
        if i == 0:
            sections = section
        else:
            sections = pd.concat((sections, section), axis=axis)
    return sections


def pd_row_header(df, idx=0):
    df.columns = df.iloc[idx]
    return df.reindex(df.index.drop(idx))


def tuples_to_pd(tup):
    """
    Convert a list of tuples to a pandas dataframe
    Parameters
    ----------
    tup : list
       List of tuples
    Returns
    -------
    pd.DataFrame
        A pandas dataframe with tuples[0] as header
    """
    temp = pd.DataFrame(tup).T

    return pd_row_header(temp)


def try_catch(funcall):
    try:
        ast.literal_eval(funcall)
    except Exception as e:
        print("{} : failed to execute".format(funcall))
    return 1


def get_netloc(href):
    return urlparse(href).netloc


def screenshot_as_b64(href):

    try:

        driver = webdriver.PhantomJS()
        # driver.add_argument('headless') # When usin chrome driver
        driver.get(href)
        screenshot = driver.get_screenshot_as_base64()
        # screenshot = driver.get_screenshot_as_png()
        driver.quit()
    except Exception as e:
        print(e)
        return ""

    return screenshot


def bookmark_header():
    bookmark_header = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="1527767863" LAST_MODIFIED="1533829947" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks bar</H3>"""
    return bookmark_header


def tree_begin():
    tree_begin = "<DL><p>"
    return tree_begin


def tree_end():
    tree_end = "</DL><p>"
    return tree_end


def str_now():
    return str(int(time.time()))


def bookmark_folder(name):

    bookmark_folder = f'<DT><H3 ADD_DATE="{str_now()}" LAST_MODIFIED="{str_now()}">{name}</H3>'
    return bookmark_folder


def bookmark_link(href, icon, description):
    bookmark_link = f'<DT><A HREF="{href}" ADD_DATE="{str_now()}" ICON="{icon}">{description}</A>'
    return bookmark_link


def test_bookmark():
    return "\n".join([bookmark_header(), tree_begin(), bookmark_folder("test"), tree_end(), tree_end()])


def wrap_header(data):
    return "\n".join([bookmark_header(), tree_begin(), *data, tree_end()])


def wrap_bookmark_folder(folder_name, data):
    return "\n".join([bookmark_folder(folder_name), tree_begin(), data, tree_end()])


def wrap_bookmark_link(hrefs, icons, descriptions):
    temp = []
    for i in range(len(hrefs)):
        temp.append(bookmark_link(hrefs[i], icons[i], descriptions[i]))
    return "            \n".join(temp)
    # return "/n".join(temp)


parser = argparse.ArgumentParser(description='Sort Bookmarks')
parser.add_argument('--bookmark_name', nargs='*', help='path to bookmark')
parser.add_argument('--output_name', nargs='*', help='file to output without filetype')

args = parser.parse_args()
bookmark_name = args.bookmark_name[0]
output_name = args.output_name[0]
output_name = output_name + ".html"

with open(bookmark_name, "r") as f:
    soup = BeautifulSoup(f, "html5lib")

links = iter(soup.find_all('a'))

pd_list = []
for link in links:

    folder = link.parent.parent.parent.find_all('h3')[0]

    href = link.get("href")

    link_metadata = [("add_date", link.get("add_date")),
                     ("href", href),
                     ("description", link.text),
                     ("icon", link.get("icon")),
                     ("folder_add_date", folder.get("add_date")),
                     ("folder_last_modified", folder.get("last_modified")),
                     ("folder_name", folder.text), ]

    pd_list.append(tuples_to_pd(link_metadata))

set_option('display.max_columns', 100)
set_option('display.width', 1000)

bookmark_df = concat_pd_list(pd_list)
bookmark_df.sort_values(["add_date", "folder_last_modified"], inplace=True)

bookmark_df['netloc'] = bookmark_df['href'].apply(get_netloc)

domains = bookmark_df.netloc.unique()

temp = []
for i in domains:
    temp_df = bookmark_df[bookmark_df['netloc'] == i]
    hrefs = list(temp_df['href'])
    icons = list(temp_df['icon'])
    descriptions = list(temp_df['description'])
    temp.append(wrap_bookmark_folder(i, wrap_bookmark_link(hrefs, icons, descriptions)))


final_bookmark = wrap_header(temp)

with open(output_name, "w") as f:
    f.write(final_bookmark)


# bookmark_df['screenshots'] = bookmark_df['href'].apply(screenshot_as_b64)

# bookmark_df['screenshots'] = swiftapply(bookmark_df['href'], screenshot_as_b64)
