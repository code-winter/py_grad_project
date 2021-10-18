from gdrive import GDrive
from yandex import Yandex
from vkontakte import VK



def main():
    # token_yandex = 'AQAAAAAOgRTpAADLW9eaCRyTskHLg71bc-vNziw'
    vkont = VK()
    drive = GDrive()
    likes_and_url = vkont.get_photos('552934290', 'profile')
    drive.upload_files(likes_and_url)
    # yand = Yandex(token_yandex)
    # yand.upload_urls(likes_and_url)


if __name__ == '__main__':
    main()
