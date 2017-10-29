import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': USER_AGENT,
    }
)


def do_request(url, params):
    response = requests.get(url=url, params=params, headers=headers)
    return response.text
