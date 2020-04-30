from dotenv import load_dotenv
import os
import requests
import validators
import argparse
import json


def get_account_info(bitly_token):
    api_url = 'https://api-ssl.bitly.com/v4/user'
    headers = {
        'Authorization': f'Bearer {bitly_token}'
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    with open('account_info.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=4)


def create_bitlinks(url, bitly_token):
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    if validators.url(url):
        data = {
            'long_url': url
        }
        headers = {
            'Authorization': f'Bearer {bitly_token}'
        }

        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        with open('short_link.txt', 'w', encoding='utf-8') as f:
            f.write('Базовая ссылка: {} | Сокращённая ссылка: {}'.format(response.json()['long_url'], response.json()['link']))
    else:
        print('Был введён некорректный урл, попробуйте ещё раз')


def count_clicks(bitlink, bitly_token):
    headers = {
        'Authorization': f'Bearer {bitly_token}'
    }
    params = {
        'units': -1
    }
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()
    with open('count_clicks.txt', 'w', encoding='utf-8') as f:
        f.write('Сокращённая ссылка: {} | Количество кликов: {}'.format(bitlink, response.json()['total_clicks']))


def main():
    parser = argparse.ArgumentParser(description='Сокращение ссылок через bit.ly, а также подсчет кликов по ссылке')
    parser.add_argument('-short', type=str, help='Ссылка которую нужно сократить. Передается урл сайта.')
    parser.add_argument('-count', type=str, help='Ссылка по которой нужно узнать ко-во кликов. '
                                                 'Передается сокращённая ссылка bit.ly.')
    parser.add_argument('-info', type=str, help='Получить информацию по аккаунту. Передается токен.')
    args = parser.parse_args()
    try:
        if args.short:
            create_bitlinks(args.short, os.getenv('BITLY_TOKEN'))
        if args.count:
            short_url = args.count.replace('https://', '')
            if short_url.startswith('bit.'):
                count_clicks(short_url, os.getenv('BITLY_TOKEN'))
            else:
                print('Был введён некорректный урл, попробуйте ещё раз')
        if args.info:
            get_account_info(args.info)
    except requests.exceptions.HTTPError:
        print('Возникла ошибка при запросе. Попробуйте ещё раз.')


if __name__ == '__main__':
    load_dotenv()
    main()
