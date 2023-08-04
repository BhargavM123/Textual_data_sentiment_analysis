#all the functions required

from bs4 import BeautifulSoup
import urllib.request, json
import requests

def scrapper(url_id, url):
  title = []
  text = []

  response = requests.get(url)
  htmlcontent = response.content
  soup = BeautifulSoup(htmlcontent, "html.parser")

  s = soup.title.string
  if '?' in s:
            s = s[:s.index("?")]
  if '|' in s:
            s = s[:s.index("|")-1]

  title.append(s)

  div_text=soup.find("div",{"class":"td-post-content"})

  try:
    for tag in div_text.select('pre.wp-block-preformatted'):
      tag.decompose()
  except:
    pass



  text.append(div_text.get_text())

  file = open(f'E:/Machine_learning_projects/Data_extraction_NLP/files_text/{url_id}.txt', 'x', encoding="utf-8")
  file.write(div_text.get_text())

  # return title, text


