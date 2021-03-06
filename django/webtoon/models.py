from django.db import models

import os
import re
import requests
from bs4 import BeautifulSoup, NavigableString


# Create your models here.
class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_episode_list(self, webtoon_id, refresh_html=True):
        '''
         """웹에서 크롤링 한 결과로 이 Webtoon에 속하는 Episode들을 생성해준다"""
        :return:
        '''
        # webtoon_id = '703835' #1인용기분
        page = 1

        url = "https://comic.naver.com/webtoon/list.nhn"
        parameter = {
            'titleId': webtoon_id,
            'page': page
        }
        response = requests.get(url, parameter)
        soup = BeautifulSoup(response.text, 'lxml')

        banner = soup.find('tr', class_='band_banner')
        if banner:
            banner.extract()

        viewlist = soup.select('div#content table.viewList > tr')
        result = list()
        for tr in viewlist:
            title = tr.find('td', class_="title").find('a').text
            episode_id_meta = tr.find('a').get('href')
            episode_id = re.search(r"=.*?=(.*?)&", episode_id_meta, re.DOTALL).group(1)
            url_thumbnail = tr.find('a').find('img').get('src')
            rating = tr.find('div', class_='rating_type').find('strong').text
            created_date = tr.find('td', class_='num').text

            # Episode.objects.create(webtoon=self, title=title, episode_id=episode_id,
            #                                  rating=rating, created_date=created_date)

            # if Episode.objects.filter(episode_id=episode_id, webtoon=self).exist() == False:
            # 데이터가 있다면 pass , 없다면 create -> 중복 제거
            Episode.objects.get_or_create(webtoon=self, title=title, episode_id=episode_id,
                                          rating=rating, created_date=created_date)


class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    created_date = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.episode_id} {self.webtoon} | {self.title}'
