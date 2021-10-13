import requests
from datetime import datetime

class VK:
    """
    Class for working with Vkontakte API
    """
    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    main_url = 'https://api.vk.com/method/'

    def get_photos_profile(self, vk_id):
        """
        Gets all photos from public profile

        :param vk_id: VK user ID
        :return: dict with likes and photo URLs
        """
        url = self.main_url + 'photos.get/'
        params = {
            'owner_id': vk_id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'access_token': self.token,
            'v': '5.131'

        }
        response = requests.get(url=url, params=params).json()
        amount = response['response']['count']
        print(f'Получено {amount} фотографий (профиль) пользователя ВКонтакте\n')
        while True:
            cmd_param = int(input('Сколько фотографий нужно загрузить? '))
            if cmd_param <= 0 or cmd_param > amount:
                print('Некорректное количество, введите снова')
            else:
                break
        dict_res = self._strip_excess(response['response']['items'], cmd_param)
        return dict_res

    def get_photos_wall(self, vk_id):
        """
                Gets all photos from user's wall

                :param vk_id: VK user ID
                :return: dict with likes and photo URLs
                """
        url = self.main_url + 'photos.get/'
        params = {
            'owner_id': vk_id,
            'album_id': 'wall',
            'extended': '1',
            'photo_sizes': '1',
            'access_token': self.token,
            'v': '5.131'

        }
        response = requests.get(url=url, params=params).json()
        amount = response['response']['count']
        print(f'Получено {amount} фотографий (стена) пользователя ВКонтакте\n')
        while True:
            cmd_param = int(input('Сколько фотографий нужно загрузить? '))
            if cmd_param <= 0 or cmd_param > amount:
                print('Некорректное количество, введите снова')
            else:
                break
        dict_res = self._strip_excess(response['response']['items'], cmd_param)
        return dict_res

    def _strip_excess(self, dict_to_sort, count):
        """
        This strips excess info from response

        :param dict_to_sort:
        :return: dict with likes and photo's URL
        """
        result = dict()
        for pos, values in enumerate(dict_to_sort):
            temp_dict = dict()
            temp_dict['photo'] = values['sizes'][-1]['type'], values['sizes'][-1]['url']
            temp_dict['likes'] = values['likes']['count']
            result[pos] = temp_dict
            if pos >= (count - 1):
                break
        return result
