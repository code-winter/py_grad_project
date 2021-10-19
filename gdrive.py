from __future__ import print_function
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from urllib import request
from googleapiclient.http import MediaFileUpload


def delete_files(file_dict):
    """
    Deletes local files after the upload to G.Drive

    :param file_dict: dict with file names
    :return:
    """
    directory = os.getcwd()
    for photo, data in file_dict.items():
        filename = data['filename']
        path = os.path.join(directory, filename)
        os.remove(path)


def save_files(file_dict):
    """
    Saves photos from URIs into local folder for further upload to G.Drive

    :param file_dict: dict with URIs and sizes
    :return: changed dict with file names
    """
    result = dict()
    pos = 0
    for photo, data in file_dict.items():
        temp = dict()
        filename = str(data['likes']) + '.jpg'
        url = data['photo'][-1]
        if not os.path.isfile(filename):
            with open(filename, 'wb') as img:
                image = request.urlopen(url).read()
                img.write(image)
                temp['filename'] = filename
                temp['size'] = data['photo'][0]
                result[pos] = temp
                pos += 1
        else:
            filename = f'{str(data["likes"])}_{data["date"]}.jpg'
            with open(filename, 'wb') as img:
                image = request.urlopen(url).read()
                img.write(image)
                temp['filename'] = filename
                temp['size'] = data['photo'][0]
                result[pos] = temp
                pos += 1
    return result


def save_files_inst(file_dict):
    """
    Saves photos from URIs into local folder for further upload to G.Drive

    :param file_dict: dict with URIs and sizes
    :return: changed dict with file names
    """
    result = dict()
    pos = 0
    for photo, data in file_dict.items():
        temp = dict()
        filename = str(data['date']) + '.jpg'
        url = data['photo'][-1]
        with open(filename, 'wb') as img:
            image = request.urlopen(url).read()
            img.write(image)
            temp['filename'] = filename
            temp['size'] = data['photo'][0]
            result[pos] = temp
            pos += 1

    return result


class GDrive:
    """
    Class for working with Google Drive API
    """
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    url = "https://www.googleapis.com/upload/drive/v3/files"

    def auth_gdrive(self):
        """
        This authenticates user for Drive API

        :return: credentials object
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def _upload_to_gdrive_vk(self, jpg_dict):
        """
        Performs a upload to Google Drive into a folder named "API_folder"

        :param jpg_dict: dict with URIs for the upload
        :return: dict with local file names
        """
        data = dict()
        counter = 0
        creds = self.auth_gdrive()
        service_fld = build('drive', 'v3', credentials=creds)
        folder_metadata = {
            "name": "API_folder",
            "mimeType": "application/vnd.google-apps.folder"
        }
        file = service_fld.files().create(body=folder_metadata, fields="id").execute()
        folder_id = file.get('id')
        service = build('drive', 'v3', credentials=creds)
        info_dict = save_files(jpg_dict)
        with open('filedata_google.json', 'w') as json_file:
            for photo, content in info_dict.items():
                metadata = {
                    'name': content['filename'],
                    'parents': [folder_id]
                }
                media = MediaFileUpload(content['filename'], mimetype='image/jpeg')
                upload = service.files().create(body=metadata, media_body=media, fields='id').execute()
                print(f'Файл {content["filename"]} загружен на Google Диск в папку {folder_metadata["name"]}')
                data[counter] = {'filename': content['filename'], 'size': content['size']}
                counter += 1
            json.dump(data, json_file, indent=4)
        return info_dict

    def _upload_to_gdrive_inst(self, jpg_dict):
        """
        Performs a upload to Google Drive into a folder named "API_folder"

        :param jpg_dict: dict with URIs for the upload
        :return: dict with local file names
        """
        data = dict()
        counter = 0
        creds = self.auth_gdrive()
        service_fld = build('drive', 'v3', credentials=creds)
        folder_metadata = {
            "name": "API_folder",
            "mimeType": "application/vnd.google-apps.folder"
        }
        file = service_fld.files().create(body=folder_metadata, fields="id").execute()
        folder_id = file.get('id')
        service = build('drive', 'v3', credentials=creds)
        info_dict = save_files_inst(jpg_dict)
        with open('filedata_google.json', 'w') as json_file:
            for photo, content in info_dict.items():
                metadata = {
                    'name': content['filename'],
                    'parents': [folder_id]
                }
                media = MediaFileUpload(content['filename'], mimetype='image/jpeg')
                upload = service.files().create(body=metadata, media_body=media, fields='id').execute()
                print(f'Файл {content["filename"]} загружен на Google Диск в папку {folder_metadata["name"]}')
                data[counter] = {'filename': content['filename'], 'size': content['size']}
                counter += 1
            json.dump(data, json_file, indent=4)
        return info_dict

    def upload_files_vk(self, info_dict):
        print('Начинаю загрузку на Google Диск...')
        res = self._upload_to_gdrive_vk(info_dict)
        delete_files(res)
        print('Загрузка на Google Диск завершена.')

    def upload_files_inst(self, info_dict):
        print('Начинаю загрузку на Google Диск...')
        res = self._upload_to_gdrive_inst(info_dict)
        delete_files(res)
        print('Загрузка на Google Диск завершена.')

