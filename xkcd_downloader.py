from bs4 import BeautifulSoup
from shutil import copyfileobj
from pathlib import Path
import requests
import time
from os import path

Path('xkcd').mkdir(parents=True, exist_ok=True)
if not path.exists("xkcd/history.txt"):
	fh = open("xkcd/history.txt", 'w')
	fh.write('')
	fh.close()

url = "https://xkcd.com/archive"
url_base = "https://xkcd.com"
html = requests.get(url).text
soup = BeautifulSoup(html, features="html.parser")
links = soup.find(id = "middleContainer")
comic_list = []
for link in links.find_all("a"):
	temp_dict = {
	"url": url_base + link["href"],
	"date": link["title"],
	"title": link.string
	}
	comic_list.append(temp_dict)

def get_picture_link(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html, features="html.parser")
	if soup.find(id="comic").find("img") != None:
		img_link = "https:" + soup.find(id="comic").find("img")["src"].replace(".png", "_2x.png")
		return img_link
	else:
		return "no_link"

def get_picture(link, path):
	r = requests.get(link, stream=True)
	fh = open(path + link.split('/')[-1], 'wb')
	r.raw.decode_content = True
	copyfileobj(r.raw, fh)
	del r
	fh.close()

fh = open('xkcd\\history.txt', 'r')
skip_text = fh.read()
fh.close()
if skip_text != '':
	skip_list = skip_text.split(';')
else:
	skip_list = []

for comic in comic_list:
	link = comic["url"]
	title = comic["title"]
	if link not in skip_list:
		print('Downloading ' + title)
		date = comic["date"]
		year = date.split('-')[0]
		month = date.split('-')[1]
		day = date.split('-')[2]
		dir_path = 'xkcd/' + year + '/' + month + '/' + day + '/'
		Path(dir_path).mkdir(parents=True, exist_ok=True)
		comic_url = get_picture_link(link)
		if comic_url != "no_link":
			if 'imgs.xkcd' in comic_url:
				get_picture(comic_url, dir_path)
		file_name = comic_url.split('/')[-1].split('_2x.')[0]
		number = link.split('/')[-2]
		lines = [
		"title: " + title,
		"number: " + number,
		"date: " + date,
		"link: " + link
		]
		s = '\n'
		info = s.join(lines)
		fh = open(dir_path + file_name + '.txt', 'w')
		fh.write(info)
		fh.close()
		fh = open('xkcd\\history.txt', 'a')
		fh.write(link + ';')
		fh.close
		time.sleep(5)
	else:
		print('Already Downloaded ' + title)
