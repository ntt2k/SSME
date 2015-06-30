# Trung Nguyen

import urllib.request
import urllib.error


def download_and_decode_data(url: str) -> list:
    """ Try to download 'with' urllib.request and except when fail """

    try:

        with urllib.request.urlopen(url) as response:

            content_string = response.read().decode(encoding='utf-8')
            content_lines = content_string.splitlines()

            return content_lines

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
        print()

    except:
        print('Something else went wrong! ... Program exits.')




