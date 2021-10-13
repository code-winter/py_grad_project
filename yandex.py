import requests
import json
from datetime import datetime

class Yandex:
    """
    Class for working with Yandex API
    """
    def __init__(self, token):
        self.token = token

    directory = '/API_IMG/'

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }

    def check_photo(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self._get_headers()
        params = {'path': path}
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False

    def upload_to_disk(self, remote_file_path, ext_url):
        """

        :param remote_file_path: path to a remote folder
        :param ext_url: external URL to upload
        :return:
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self._get_headers()
        params = {
            "path": remote_file_path,
            'url': ext_url,
            "overwrite": "true"
        }
        response = requests.post(url=url, headers=headers, params=params)
        print(f'Response code: {response.status_code}')
        return response

    def upload_urls(self, info_dict):
        with open('file_data.json', 'w') as file:
            for items, content in info_dict.items():
                yan_path = str()
                vk_url = str()
                filename = str(content['likes']) + '.jpg'
                yan_path = self.directory + filename
                vk_url = content['photo'][-1]
                is_exist = self.check_photo(yan_path)
                if is_exist is False:
                    response = self.upload_to_disk(yan_path, vk_url)
                    if response.status_code == 202:
                        print(f'Файл {filename} загружен на Яндекс.Диск\n')
                elif is_exist is True:
                    date = str(datetime.now())
                    date = date.replace(':', '_')
                    filename = f'{content["likes"]}__{date}.jpg'
                    yan_path = self.directory + filename
                    response = self.upload_to_disk(yan_path, vk_url)
                    if response.status_code == 202:
                        print(f'Файл {filename} загружен на Яндекс.Диск\n')
                data = {'filename': filename, 'size': content['photo'][0]}
                json.dump(data, file, indent=4)

