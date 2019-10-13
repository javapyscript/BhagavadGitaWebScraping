# -*- coding: utf-8 -*-0
import nltk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import lxml.html as le

columns = ['Chapter', 'Verse', 'Translation', 'Purport']
data = []
url = 'https://asitis.com/1/1.html'
next_url_present = True

while next_url_present != False:
    split_list = url.split('/')
    chapter = split_list[-2]
    verse = split_list[-1].split('.html')[0]
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    root = le.fromstring(str(soup))
    translation = root.xpath('//div[@class="Translation"]')
    if len(translation) > 0:
        translation = translation[0].text_content()
    else:
        translation = ''
    purport = root.xpath('//div[@class="Purport"]')
    if len(purport) > 0:
        purport = purport[0].text_content()
    else:
        purport = ''
    data.append({'Chapter': chapter, 'Verse': verse, 'Translation': translation, 'Purport': purport})
    print("Completed chap " + str(chapter) + " verse " + str(verse))
    url = root.xpath('//a[@class="fa fa-arrow-circle-right fa-2x"]')[0].attrib['href']
    if url == 'https://asitis.com/18/books.html':
        next_url_present = False

Gita = pd.DataFrame(data=data, columns=columns)
Gita.to_csv('Gita.csv', sep=',', index=False)