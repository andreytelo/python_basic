import requests
import datetime
import json
import time
from tqdm import tqdm
from pprint import pprint


def get_id_vk(id_vk):
    if id_vk is int:
        id_vk = id_vk
    else:
        url = "https://api.vk.com/method/users.get"
        r = requests.get(url=url, params={'access_token': token_vk, 'v': 5.131}).json()
    return r['response'][0]['id']


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
    r = requests.get(url=url, params={'owner_id': get_id_vk(id_vk),
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
            m = (datetime.datetime.fromtimestamp(int(photo['date'])).strftime('%Y-%m-%d'))
            upload_info[m] = (max_size_url, max_size)
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


def write_log_json():
    photos = get_photo()
    json_list = []
    for photo in photos.items():
        new_dict = {}
        new_dict["filename"] = f'{photo[0]}.jpg'
        new_dict["size"] = photo[1][1]
        json_list.append(new_dict)
    with open('photos.json', 'w') as f:
        json.dump(json_list, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    id_vk =   # Необходимо ввести id или username пользователся vk
    count =   # Необходимо ввести количество скачиваемых фото
    token_vk = ''  # Необходимо ввести токен vk
    token_ya = ''  # Необходимо ввести токен яндекс.диска
    path = id_vk
    create_folder()
    upload()
    write_log_json()
