import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import csv
import re

USER_AGENT_CHOICES = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
]

def clean_title(title):
    title = title.replace('&', 'and')
    cleaned_title = re.sub(r'[^\w\s-]', '', title)
    cleaned_title = cleaned_title.replace(" ", "_").lower()
    return cleaned_title

def fetch_where_to_watch(title, year, genre, rating):
    clean_title = title.replace(" ", "+")
    main_url = f'https://www.filmaffinity.com/us/advsearch.php?stext={clean_title}&stype%5B%5D=title&country=&genre=&fromyear=&toyear={year}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(main_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie = soup.find('div', class_='fa-shadow adv-search-item')
        
        if movie:
            link = movie.a.get('href')
            time.sleep(random.uniform(2, 5))
            html_text = requests.get(link)
            
            if html_text.status_code == 200:
                soup = BeautifulSoup(html_text.text, 'html.parser')
                w2w_elements = soup.find_all('div', class_='prov-offers-wrapper')
                platform2watch = {}

                for w2w in w2w_elements:
                    where2watch = w2w.find_all('a')
                    for w in where2watch:
                        platform = w.img
                        if platform and platform.get('title'):
                            platform_title = platform.get('title')
                            platform_href = w.get('href') 
                            platform2watch[platform_title] = platform_href

                with open('movie_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for platform_title, platform_href in platform2watch.items():
                        writer.writerow([title, year, genre, rating, platform_title, platform_href])
                
                print(f"{title} ({year}): {platform2watch}")
    else:
        print(f"Error for {title} ({year}): {response.status_code}")




def get_rottentomatoes(title, year=None):
    clean_title_str = clean_title(title)
    main_url = f'https://www.rottentomatoes.com/m/{clean_title_str}'


    user_agent = random.choice(USER_AGENT_CHOICES)
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(main_url, headers=headers)
        
    if year:    
        main_url_new = f'https://www.rottentomatoes.com/m/{clean_title_str}_{year}'
        rotten_tomatoes_results = requests.get(main_url_new)

        if rotten_tomatoes_results.status_code == 200:
            rotten_tomatoes_html = rotten_tomatoes_results.content
            rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes_html, 'html.parser')
            rotten_tomatoes_div = rotten_tomatoes_soup.find('div', class_='media-scorecard')

            if rotten_tomatoes_div:
                rotten_tomatoes_element = rotten_tomatoes_div.find('rt-text')
                if rotten_tomatoes_element:
                    rotten_tomatoes_rating = rotten_tomatoes_element.text.strip()
                    return f'{rotten_tomatoes_rating}', main_url_new

    if response.status_code == 200:
        rotten_tomatoes_html = response.content
        rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes_html, 'html.parser')
        rotten_tomatoes_div = rotten_tomatoes_soup.find('div', class_='media-scorecard')

        if rotten_tomatoes_div:
            rotten_tomatoes_element = rotten_tomatoes_div.find('rt-text')
            if rotten_tomatoes_element:
                rotten_tomatoes_rating = rotten_tomatoes_element.text.strip()
                return f'{rotten_tomatoes_rating}', main_url
        
    
print(get_rottentomatoes("Crescent City", 2024))
