import datetime

import bs4
import requests
from flask_restful import Resource

from src import db
from src.services.film_service import FilmService


def convert_time(time: str) -> float:
    hour, minute = time.split('h')
    minutes = (60 * int(hour)) + int(minute.strip('min'))
    return minutes


class PopulateDB(Resource):
    url = 'http://www.imdb.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def post(self):
        t0 = datetime.datetime.now()
        films_urls = self.get_films_urls()
        print(f"Fetched film URLs: {films_urls}", flush=True)
        films = self.parse_films(films_urls)
        created_films = self.populate_db_with_films(films)
        dt = datetime.datetime.now() - t0
        print(f'Done in {dt.total_seconds():.2f} sec.')
        return {"message": f'Database were populated with {created_films} films'}, 201

    def get_films_urls(self):
        print('Getting film urls', flush=True)
        url = 'https://www.imdb.com/chart/top/'
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all('td', class_='posterColumn')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:10]
        return movie_links

    def parse_films(self, film_urls):
        film_to_create = []
        for url in film_urls:
            print(f"Fetching film page: {url}", flush=True)
            url = self.url + url
            print(f'Getting a detailed info about the film - {url}')
            film_content = requests.get(url, headers=self.headers)
            print(f"Fetching film page: {url}", flush=True)
            film_content.raise_for_status()
            html = film_content.text
            soup = bs4.BeautifulSoup(html, features='html.parser')

            title = soup.find('div', class_='sc-dae4a1bc-0').text.split(':')[1].strip()
            rating_content = soup.find('div', class_='sc-7ab21ed2-2')
            rating = float(rating_content.find('span', {'class': 'sc-7ab21ed2-1'}).get_text())
            description_content = soup.find('p', class_='sc-16ede01-6')
            description = description_content.find('span', class_='sc-16ede01-0').text.strip()
            release_date = '01 January 1900'
            release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
            length_content = soup.find('div', class_='sc-94726ce4-3')
            length_content = length_content.find_all('li', class_='ipc-inline-list__item')[-1]
            length = convert_time(length_content.text.strip())

            print(f"Parsed film: {film_to_create[-1]}", flush=True)

            film_to_create.append(
                {
                    'title': title,
                    'rating': rating,
                    'description': description,
                    'release_date': release_date,
                    'length': length,
                    'distributed_by': 'Warner Bros. Pictures'
                }
            )
            print(f"Films to be created: {film_to_create}", flush=True)

        return film_to_create

    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)
















