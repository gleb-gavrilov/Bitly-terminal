from dotenv import load_dotenv
import os
import requests
import validators

load_dotenv()


def get_account_info():
    api_url = 'https://api-ssl.bitly.com/v4/user'
    headers = {
        'Authorization': 'Bearer {}'.format(os.getenv('BITLY_TOKEN'))
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print(f'Не смог соедениться с {api_url}, статус ошибки: {response.status_code}')
    return False


def create_bitlinks():
    bitlinks = []
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    print('Введите урл, который хотите сократить:')
    while True:
        url = input()
        if validators.url(url):
            data = {
                'long_url': url
            }
            headers = {
                'Authorization': 'Bearer {}'.format(os.getenv('BITLY_TOKEN'))
            }
            try:
                response = requests.post(api_url, headers=headers, json=data)
                response.raise_for_status()
                bitlinks.append({
                    'short_url': response.json()['link'],
                    'long_url': response.json()['long_url']
                })
                print('Сделано, нужно сократить ещё один урл? Введите соответствующую цифру:')
                print('1 — Да')
                print('2 — Нет')
                try:
                    one_more_bitlink = int(input())
                except ValueError:
                    one_more_bitlink = 2

                if one_more_bitlink == 2:
                    break
                elif one_more_bitlink == 1:
                    print('Введите урл, который хотите сократить:')
                else:
                    print('Введите урл, который хотите сократить:')
            except requests.exceptions.HTTPError:
                print(f'Ошибка соединения с {api_url}, статус ошибки: {response.status_code}')
                print('Попробуйте ввести урл ещё раз:')
        else:
            print('Введите нормальный url адрес!')
    return bitlinks


def count_clicks(bitlink):
    bitlink = bitlink.replace('https://', '')
    is_correct_bitlink = bitlink.startswith('bit.')
    if not is_correct_bitlink:
        return False
    bitlink_click_count = []
    headers = {
        'Authorization': 'Bearer {}'.format(os.getenv('BITLY_TOKEN'))
    }
    params = {
        'units': -1
    }
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        bitlink_click_count.append({
            'link': bitlink,
            'total_clicks': response.json()['total_clicks']
        })
    except requests.exceptions.HTTPError:
        print(f'Ошибка соединения с {api_url}, статус ошибки: {response.status_code}')

    return bitlink_click_count


def main():
    while True:
        print('Главное меню. Для выбора введите соответствующую цифру:')
        print('1 — Сократить ссылки')
        print('2 — Узнать кол-во кликов по ссылке')
        print('3 — Выход')
        try:
            user_answer = int(input())
            if user_answer == 1:
                bitlinks = create_bitlinks()
                for bitlink in bitlinks:
                    print('Long url {} | Short url {}'.format(bitlink['long_url'], bitlink['short_url']))
                    print('-' * 20)
            elif user_answer == 2:
                print('Напишите по какой ссылке считать кол-во кликов:')
                user_link = input()
                bitlink_click_count = count_clicks(user_link)
                if not bitlink_click_count:
                    print('Введена некоррекная ссылка bit.ly')
                else:
                    print('Кол-во кликов по ссылке {} {} шт.'.format(bitlink_click_count[0]['link'], bitlink_click_count[0]['total_clicks']))
            elif user_answer == 3:
                break

        except ValueError:
            print('Введён некорректный ответ. Попробуйте ещё раз')







if __name__ == '__main__':
    main()
