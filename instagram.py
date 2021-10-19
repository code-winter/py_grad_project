import requests


class Instagram:
    """
    Class for working with Instagram API
    """
    TOKEN = ' '
    media_url = 'https://graph.instagram.com/v12.0/'

    def write_data(self, photo_data, photo_count):
        """
        Writes needed metadata for further upload from response

        :param photo_data: dict with media response from server
        :param photo_count: amount of photos to upload
        :return: dict with filled metadata
        """
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
        """
        This gets a list of photos from open Instagram account

        :param user_id: Instagram user ID
        :return: dict with URL and file metadata
        """
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
        print(f'Получено: {cmd} фото Instagram\n')
        return photo_data

