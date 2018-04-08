import argparse
import urllib2
from bs4 import BeautifulSoup

def scrape_reddit_gif_page(url):
  next_page_url = ''

  hdr = { 'user-agent' : 'gif bot' }
  req = urllib2.Request(url, headers=hdr)
  page = urllib2.urlopen(req).read()
  soup = BeautifulSoup(page, 'html.parser')

  gif_soup_links = soup.find_all('a')
  for soup_link in gif_soup_links :
    link_href = soup_link.get('href')

    if not link_href:
      continue
  
    if is_gif_url(link_href) and link_href not in gif_links_set:
      print "  " + link_href
      gif_links_set.add(link_href)
      print >> file, link_href
      continue

    # find link to next page
    if next_page_url:
      continue

    link_text = soup_link.string
    if not link_text:
      continue

    if 'next ' in link_text and 'r/gifs/?count' in link_href:
      next_page_url = link_href
    
  return next_page_url

def is_gif_url(url):
  for ext in [ '.gif', '.gifv', '.ogg', '.mp4', '.webm' ]:
    if url.endswith(ext):
      return True

  return False

def parse_command_line_args():
  global start_url
  global num_pages
  global out_file_name

  parser = argparse.ArgumentParser()
  parser.add_argument("--url", help="start page url")
  parser.add_argument("--pages", type=int, help="number of pages to scrape")
  parser.add_argument("--output", help="output file name")

  args = parser.parse_args()
  if args.url:
    start_url = args.url
  if args.pages:
    num_pages = args.pages
  if args.output:
    out_file_name = args.output

# =====

start_url = 'https://www.reddit.com/r/gifs'
num_pages = 50
out_file_name="reddit_gifs.txt"

gif_links_set = set()

parse_command_line_args()
print "start URL: " + start_url
print "pages: " + str(num_pages)
print "output: " + out_file_name

file = open(out_file_name, "a")

url=start_url
for i in range(0, num_pages):
    print url
    url = scrape_reddit_gif_page(url)

file.close()
