import requests

# TBOAH:
# bot_token = '6341783038:AAE3WWKJgzRqbJ-rywlJ7-b_pVmHY1d9Etw'
# The birth of a hero
bot_token = '6175733522:AAHTUgNp54bv6TFxGVIJKY4jrAkDkMSK0oo'
MAIN_URL = f'https://api.telegram.org/bot{bot_token}'

r = requests.get(f'{MAIN_URL}/getMe').json()
# print(r)

bot_name = r['result']['first_name']
chat_id = r['result']['id']
