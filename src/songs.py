# -*- coding: utf-8 -*-

import sys
import json
import urllib2
import re

from bs4 import BeautifulSoup

def searchSong(artist, query, arg='data'):

	data = []
	lyrics = []
	annotations = []

	artist = '-'.join(artist.split())

	query = '-'.join(query.split())
	query = query.replace("'", '')
	query = artist +'-' + query + '-lyrics'

	opener = urllib2.build_opener()
	url = "http://rapgenius.com/%s" % query
	page = opener.open(url)
	soup = BeautifulSoup(page, from_encoding="utf-8")
	text = soup.find_all(class_="lyrics")
	l = len(text)

	for i in range(0, l):
		words = str(text[i])
		words = words.replace("<div", "{<div").replace('">', '">}')
		words = re.sub(r'\{.*?\}', '', words)
		words = words.replace('">}', '">')
		words = words.replace("<i>", '').replace("</i>", '')
		words = words.replace('<br/>', '')
		words = words.replace("<p>", '').replace("</p>", '')
		words = words.split("</a>")
		m = len(words)

		for j in range(0, m-1):
			a = re.search(r'\<.*?\>', words[j])
			lyric = re.sub(r'\<.*?\>', '', words[j])
			lyric = lyric.strip()
			#lyric = ' '.join(lyric.split())
			annotation = a.group(0)
			lyrics.append(lyric)

			search1 = annotation.find('"no_annotation"')
			search2 = annotation.find('data-editorial-state')

			if search1 != -1:
				annotations.append("Not annotated")
			elif search2 != -1:
				annotations.append("YES")


	return annotations
