import requests
from pprint import pprint

class Instagram:
    TOKEN = f'IGQVJXYjBIcktQeG9nWDNqb1Bubm02Q1VnWC1ieTBWTjAxMVFoeW5rcjN1R1VzdEdqNGd5cjkwTXhwczNiNlQtYTFDQUpJOEFJMU' \
            f'9NMnMzQkVrc0w4eWVzOW9MSWxueVF6eUZAhc1VkN1pUV1otNUE0QgZDZD'
    media_url = 'https://graph.instagram.com/v12.0/'

    def write_data(self, photo_data, photo_count):
        res_dict = dict()
        count = 0
        for photo in photo_data:
            buffer = dict()
            date = photo['timestamp']
            date = date.replace(':', '_')
            buffer['date'] = date
            buffer['photo'] = 'inst', photo['media_url']
            res_dict[count] = buffer
            count += 1
            if count >= photo_count:
                break
        return res_dict

    def get_photos(self, user_id):
        res_dict = dict()
        count = 0
        token = self.TOKEN
        URI = f'{self.media_url}{user_id}/media'
        params = {
            'access_token': token,
            'fields': 'media_url, timestamp'
        }
        response = requests.get(url=URI, params=params).json()
        temp_dict = response['data']
        amount = len(temp_dict)
        print(f'\nПолучено {amount} фотографий пользователя Instagram.')
        while True:
            cmd = int(input(f'Сколько фотографий необходимо получить? (1-{amount})\n'))
            if cmd <= 0 or cmd > amount:
                print('Некорректное количество, введите снова')
            else:
                break
        photo_data = self.write_data(temp_dict, cmd)
        print(f'Получено: {cmd} фото Instagram')
        return photo_data

