import requests
import json
import time
from tqdm import tqdm


def write_json(data):
    with open('photos.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_largest(size):
    if size['width'] >= size['height']:
        return size['width']
    else:
        return size['height']


def get_photo():
    upload_info = {}
    url = "https://api.vk.com/method/photos.get"
    r = requests.get(url=url, params={'owner_id': id_vk,
                                      'access_token': token_vk,
                                      'album_id': 'profile',
                                      'count': count,
                                      'extended': True,
                                      'photo_sizes': True,
                                      'v': 5.131})
    write_json(r.json())
    photos = json.load(open('photos.json'))['response']['items']
    for photo in photos:
        max_size_url = max(photo['sizes'], key=get_largest)['url']
        max_size = max(photo['sizes'], key=get_largest)['type']

        if photo['likes']['count'] not in upload_info:
            upload_info[photo['likes']['count']] = (max_size_url, max_size)
        else:
            upload_info[photo['date']] = (max_size_url, max_size)
    return upload_info


def get_headers():
    return {'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(token_ya)}


def create_folder():
    headers = get_headers()
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': path}
    res = requests.put(url=url, headers=headers, params=params)
    return res


def upload():
    photo = get_photo()

    for key, value in tqdm(photo.items()):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = get_headers()
        params = {'path': f'{path}/{key}', 'overwrite': 'true', 'url': value[0]}
        requests.post(url=url, headers=headers, params=params)
        time.sleep(1)


def write_ya_json():
    photo = get_photo()

    with open('photos.json', 'w') as f:
        f.write('[')
        for key in photo:
            f.write('\n')
            f.write('{')
            f.writelines("'file name':" + "'" + str(key) + "'")
            f.write('\n')
            f.writelines("'size' :" + "'" + str(photo[key][1]) + "'")
            f.write('}')
        f.write(']')


if __name__ == "__main__":
    id_vk =         # Необходимо ввести id пользователся vk
    count =         # Необходимо ввести количество скачиваемых фото
    token_vk = ''   # Необходимо ввести токен vk
    token_ya = ''   # Необходимо ввести токен яндекс.диска
    path = id_vk
    create_folder()
    upload()
    write_ya_json()
