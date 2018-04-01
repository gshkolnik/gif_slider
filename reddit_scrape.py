import urllib2
from bs4 import BeautifulSoup

gif_links_set = set()


def scrape_reddit_gif_page(url):
  next_page_url = ''

  hdr = { 'User-Agent' : 'gif bot' }
  req = urllib2.Request(url, headers=hdr)
  page = urllib2.urlopen(req).read()
  soup = BeautifulSoup(page, 'html.parser')

  gif_soup_links = soup.find_all('a')
  for soup_link in gif_soup_links :
    link_href = soup_link.get('href')

    if not link_href:
      continue
  
    for ext in [ '.gif', '.gifv', '.ogg', '.mp4', '.webm' ]:
      if ext in link_href:
        gif_links_set.add(link_href)
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

url = 'https://www.reddit.com/r/gifs'
num_next_pages = 10
for i in range(0, num_next_pages):
    print url
    url = scrape_reddit_gif_page(url)

file = open("reddit_gifs.txt", "w")
for gif_link in gif_links_set:
  print >> file, gif_link
file.close()
