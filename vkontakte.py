import requests


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
        dict_res = self._strip_excess(requests.get(url, params=params).json()['response']['items'])
        print('Got VK profile photos\n')
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
        dict_res = self._strip_excess(requests.get(url, params=params).json()['response']['items'])
        print('Got VK wall photos\n')
        return dict_res

    def _strip_excess(self, dict_to_sort):
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
        return result
