import requests
from bs4 import BeautifulSoup
import json

base_url = "https://myanimelist.net/anime/season"
all_animes = []

def url_crawler(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    tv_list = soup.find('div', class_="seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix")
    container = tv_list.find_all('div', class_="seasonal-anime js-seasonal-anime")
    #print(container)
    for container in container:
      genres = []
      title = container.find_all('div')[0].find('div', class_="title").find('h2', class_="h2_anime_title").find('a', class_="link-title").get_text(strip=True)
      url = container.find_all('div')[0].find('div', class_="title").find('h2', class_="h2_anime_title").find('a', class_="link-title").get('href')
      episodes = container.find_all('div')[0].find('div', class_="prodsrc").find('div', class_="eps").find('a').find('span').text.strip()
      genres_list = container.find_all('div')[0].find('div', class_="genres").find_all('div', class_="genres-inner")
      image_jpg = container.find('div', class_="image").find('a').find('img').get('src')
      image_wbp = container.find('div', class_="image").find('a').find('img').get('data-src')
      for genres_list in genres_list:
        genre_list = genres_list.find_all('span')
        for d in genre_list:
          genres.append(d.find('a').text.strip())
      
      if(image_jpg):
        image = image_jpg
      elif(image_wbp):
        image = image_wbp
      
      
      if(episodes == '? eps'):
        episodes = 'No episode estimates'
      
      


      anime_dict = {}
      anime_dict['title'] = title
      anime_dict['url'] = url
      anime_dict['episodes'] = episodes
      anime_dict['genres'] = genres
      anime_dict['image'] = image

      all_animes.append(anime_dict)
    f = open('output.json', 'w')
    f.write(json.dumps(all_animes))
    f.close()
    return all_animes
       
      

all_animes = url_crawler(base_url)
