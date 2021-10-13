from yandex import Yandex
from vkontakte import VK
from ok import OK
from datetime import datetime

def main():
    token_yandex = ''
    vkont = VK()
    likes_and_url = vkont.get_photos_profile('552934290')
    yand = Yandex(token_yandex)
    yand.upload_urls(likes_and_url)






if __name__ == '__main__':
    main()
