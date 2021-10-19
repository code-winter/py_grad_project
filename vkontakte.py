import requests
from urllib import request
import os


def _strip_excess(dict_to_sort, count):
    """
    This strips excess info from response (leaves URI of photo, likes and size)

    :param dict_to_sort:
    :return: dict with likes and photo's URI
    """
    result = dict()
    for pos, values in enumerate(dict_to_sort):
        temp_dict = dict()
        temp_dict['date'] = values['date']
        temp_dict['photo'] = values['sizes'][-1]['type'], values['sizes'][-1]['url']
        temp_dict['likes'] = values['likes']['count']
        result[pos] = temp_dict
        if pos >= (count - 1):
            break
    return result


class VK:
    """
    Class for working with Vkontakte API
    """
    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    main_url = 'https://api.vk.com/method/'

    def get_photos(self, vk_id, album_id):
        """
        Gets all photos from public profile

        :param album_id: Album ID of VK profile (profile or wall)
        :param vk_id: VK user ID
        :return: dict with likes and photo URLs
        """
        url = self.main_url + 'photos.get/'
        album_name = str()
        params = {
            'owner_id': vk_id,
            'album_id': album_id,
            'extended': '1',
            'photo_sizes': '1',
            'access_token': self.token,
            'v': '5.131'

        }
        if album_id == 'profile':
            album_name = 'профиль'
        elif album_id == 'wall':
            album_name = 'стена'

        response = requests.get(url=url, params=params).json()
        amount = response['response']['count']
        print(f'\nПолучено {amount} фотографий ({album_name}) пользователя ВКонтакте\n')
        while True:
            cmd_param = int(input(f'Сколько фотографий нужно загрузить? (1-{amount}) '))
            if cmd_param <= 0 or cmd_param > amount:
                print('Некорректное количество, введите снова')
            else:
                break
        dict_res = _strip_excess(response['response']['items'], cmd_param)
        print(f'Получено: {cmd_param} фото Вконтакте\n')
        return dict_res
