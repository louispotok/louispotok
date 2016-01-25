"""
Recursively search a web directory for a given string.

Possible improvements:
	* Make more generic (I'm sure a lot of this is quite fragile and tied to the specific website I was searching).
		* Maybe most important, I use the line_is_parent_directory function to avoid getting stuck in loops, but this won't cover all cases.
	* Broaden the match criteria (not just strict substring)
	* There's some messiness around the initial call and the recursion base case that could be cleaned up.
	* Similarly, could probably refactor this to avoid splitting by line and split by <a> tags instead.
		* This would make it easier to search only within actual text (currently it matches anything in the HTML)
	* Would be nice to cache results to speed up repeated searches on the same url
	* Visual indication of progress would be pretty cool.
"""

import requests
import argparse
from bs4 import BeautifulSoup

DEFAULT_SEARCH_URL = 'http://www.golosa.org/private/'
FOLDER_ICON_STRING = '/icons/folder.gif'
PARENT_DIRECTORY_STRING = 'Parent Directory'

def get_text(url):
    return requests.get(url).text

def get_text_lines(url):
	return get_text(url).split('\n')

def line_is_folder(line):
	image = BeautifulSoup(line).find('img')
	if image:
		has_folder_string = FOLDER_ICON_STRING in BeautifulSoup(line).find('img').get('src')
		is_parent_line = line_is_parent_directory(line)
		return has_folder_string and not is_parent_line
	else:
		return False

def line_is_parent_directory(line):
	return 'PARENT_DIRECTORY_STRING' in line

def get_line_link(line):
	return BeautifulSoup(line).find('a').get('href')

def page_search(current_url='', lines_to_search = [], search_term='', links_found=[]):
	if len(lines_to_search) == 2:
		return links_found + line_search(current_url, lines_to_search[0], search_term,links_found) + line_search(current_url, lines_to_search[1], search_term,links_found)
	else:
		return line_search(current_url, lines_to_search[0],search_term,links_found) + page_search(current_url, lines_to_search[1:], search_term,links_found)

def line_search(url, line, search_term,links_found):

	if line_is_folder(line):
		line_url = url + get_line_link(line)
		return page_search(line_url,get_text_lines(line_url),search_term,links_found)
	elif search_term in line:
		line_url = url + get_line_link(line)
		return [line_url]
	else:
		return []

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("search_term")
	parser.add_argument("--search_url", default='')
	args = parser.parse_args()
	if not args.search_url:
		args.search_url = DEFAULT_SEARCH_URL
	print "searching for {0} on {1}".format(args.search_term,args.search_url)
	base_text_lines = get_text_lines(args.search_url)
	result = page_search(args.search_url, base_text_lines, args.search_term)
	print '\nRESULTS:\n'
	for r in result:
		print r

if __name__=='__main__':
	main()

