from gdrive import GDrive
from yandex import Yandex
from vkontakte import VK
from instagram import Instagram



def main():
    token_yandex = ' '
    vkont = VK()
    vk_photo = dict()
    inst_photo = dict()
    vk_id = ' '
    drive = GDrive()
    yand = Yandex(token_yandex)
    inst = Instagram()
    inst_id = ' '
    while True:
        command = int(input('Откуда необходимо получить фотографии? 1 - ВКонтакте, 2 - Instagram\n'))
        if command < 1 or command > 2:
            print('Неверно введена команда\n')
        elif command == 1:
            cmd_vk = int(input('Откуда получить фотографии ВКонтакте? 1 - профиль, 2 - стена\n'))
            if cmd_vk < 1 or cmd_vk > 2:
                print('Неверно введена команда\n')
            elif cmd_vk == 1:
                vk_photo = vkont.get_photos(vk_id, 'profile')
            elif cmd_vk == 2:
                vk_photo = vkont.get_photos(vk_id, 'wall')
            upload_cmd = int(input('Куда загрузить фотографии ВКонтакте? 1 - Яндекс.Диск, 2 - Google Диск\n'))
            if upload_cmd < 1 or upload_cmd > 2:
                print('Неверно введена команда\n')
            elif upload_cmd == 1:
                yand.upload_urls_vk(vk_photo)
                break
            elif upload_cmd == 2:
                drive.upload_files_vk(vk_photo)
                break
        elif command == 2:
            inst_photo = inst.get_photos(inst_id)
            upload_inst = int(input('Куда загрузить фото Instagram? 1 - Яндекс.Диск, 2 - Google Диск\n'))
            if upload_inst < 1 or upload_inst > 2:
                print('Неверно введена команда\n')
            elif upload_inst == 1:
                yand.upload_urls_inst(inst_photo)
                break
            elif upload_inst == 2:
                drive.upload_files_inst(inst_photo)
                break


if __name__ == '__main__':
    main()
